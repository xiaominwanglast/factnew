#coding:utf-8
import pytest
import requests
# import redis
from utils.Setting import SETTING
from utils.generatorTool import *
from FactorScoreCase.env_config import env_config
from FactorScoreCase.test_api_use_method import *
from utils.InfoGenerate import *

class TestApi(object):
    """风控输出接口测试"""
    key="abc123"
    merchant_code="88881"
    support_treasure="creditScore"
    port = "10108"
    http_url="skynet-embrace/risk/creditScore"
    



    @classmethod
    def setup_class(cls):
        pass

    def teardown_method(self, method):
        print('\n测试用例执行完毕')

    #准备数据
    @pytest.fixture(scope="module", autouse=True)
    def init_data(self,request):
        envopt=request.config.getoption("--envopt")
        print ("env:"+envopt)
        if not envopt:
            envopt="T1"
        # conn = redis.Redis(host=SETTING[envopt]['redis']['host'], port=SETTING[envopt]['redis']['port'], password=SETTING[envopt]['redis']['password'], db=SETTING[envopt]['redis']['db'])
        # if conn.keys(pattern='*com*'):
        #     conn.delete(*conn.keys(pattern='*com*'))
        host=env_config[envopt]
        # gateway
        mysqlUtil = MysqlPyUntil(envopt,"tob_api_gateway")
        sql = "select * from  cfg_signature where merchant_code='%s' and publickey='%s' and privatekey='%s'" % (
        self.merchant_code, self.key,self.key)
        res = mysqlUtil.queryNewOne(sql)
        if not res:
            print("insert into cfg_signature")
            sql = "insert into cfg_signature VALUES(null,'%s','%s','%s',1,'2019-08-21 12:00:00','2019-08-21  12:00:00',0)" % (
            self.merchant_code, self.key,self.key)  # 添加商户key对应关系
            mysqlUtil.insertIntoData(sql)

        # 先查询有没有key
        mysqlUtil = MysqlPyUntil(envopt, "skynet_merchant")
        sql="select * from  risk_out_merchant_auth where merchant_code='%s' and secret_key='%s'"  % (self.merchant_code,self.key)
        res=mysqlUtil.queryNewOne(sql)
        if not res:
            print("insert into risk_out_merchant_auth")
            sql = "insert into risk_out_merchant_auth VALUES(null,'%s','%s','user',0,0,'2019-08-21 12:00:00','2019-08-21  12:00:00')" % (self.merchant_code,self.key)#添加商户key对应关系
            mysqlUtil.insertIntoData(sql)

        sql = "select * from  risk_out_merchant_treasure where merchant_code='%s' and support_treasure='%s'" % (
        self.merchant_code, self.support_treasure)
        res = mysqlUtil.queryNewOne(sql)
        if not res:
            print ("insert into risk_out_merchant_treasure")
            sql= "insert into risk_out_merchant_treasure VALUES(null,'%s','%s',0,'2019-08-21 12:00:00','2019-08-21  12:00:00')"% (self.merchant_code,self.support_treasure)#添加鉴权信息
            mysqlUtil.insertIntoData(sql)
        print ("end")
        return {"host":host,"env":envopt}


    def test_1(self,init_data):
        """用例1：正常情况 --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "12345678",
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId":create_certid(),
            }
        }
        print ("insertsql")
        insertScore(init_data.get("env"),data['data'].get('certId'),data['data'].get('name'),data['data'].get('mobile'),'620')
        data['data']['merchantCode']=self.merchant_code
        data['data']['applyNo']=gen_random_str_num()
        data.pop("sign")
        sign =Des().get_sign(data['data'],secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"),self.port,self.http_url)
        print(url)
        print(data)
        print("begin invoke interface")
        r = requests.post(url=url, json=data)
        print("end invoke interface")
        print (r.json())
        res_sign = Des().get_sign(r.json().get('result'), secret_key=self.key)

        checkReponseOk(r.json(), data['data'].get("applyNo"), '000000', "成功",res_sign)
        #mongo检查
        assert checkMongoLog(init_data.get("env"),data['data'].get("applyNo"))==True
        #time.sleep(1)
        assert checkMongoStatics(init_data.get("env"),data['data'].get("applyNo"))==True


    def test_2(self,init_data):
        """用例2：手机号存在，身份证不存在且不为空 --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "12345678",
                "applyNo": "20080808200000001",
                "name": "李四",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }
        insertScore(init_data.get("env"),"1234567",data['data'].get('name'),data['data'].get('mobile'),'630') #故意将身份证写错
        data['data']['merchantCode']=self.merchant_code
        data['data']['applyNo'] = gen_random_str_num()
        data.pop("sign")
        sign =Des().get_sign(data['data'],secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"),self.port,self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print (r.json())

        checkReponseNotOk(r.json(),data['data'].get("applyNo"),'001003',"未命中")
        #mongo检查
        assert checkMongoLog(init_data.get("env"),data['data'].get("applyNo"))==True
        assert checkMongoStatics(init_data.get("env"),data['data'].get("applyNo"))==False


    def test_3(self,init_data):
        """用例3：验签失败 --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "12345678",
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }
        insertScore(init_data.get("env"), "1234567", data['data'].get('name'), data['data'].get('mobile'), '630')  # 故意将身份证写错
        data['data']['merchantCode'] = self.merchant_code
        data['data']['applyNo'] = gen_random_str_num()
        data.pop("sign")
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = "sign"  #随便给个sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port,self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print(r.json())

        checkReponseNotOk(r.json(), data['data'].get("applyNo"), '990006', "签名验证失败")
        # mongo检查
        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo"))==False
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo"))==False

    def test_4(self, init_data):
        """用例4：鉴权失败，都没有key --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "12345678",
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }
        data['data']['merchantCode']=gen_random_str_num()
        data['data']['applyNo'] = gen_random_str_num()
        insertScore(init_data.get("env"), data['data'].get('certId'), data['data'].get('name'), data['data'].get('mobile'), '630')
        data.pop("sign")
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port,self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print(r.json())

        checkReponseNotOk(r.json(), data['data'].get("applyNo"), '020005', "不存在的商户号")
        # mongo检查
        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo")) == False
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo")) == False

    def test_5(self, init_data):
        """用例5：鉴权失败,gateway，有key，风控没key --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "33333", #因为gateway缘故，写死
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }
        # data['merchantCode'] = gen_random_str_num()
        # mysqlUtil = MysqlPyUntil(init_data.get('env'), "tob_api_gateway")
        # sql = "insert into cfg_signature VALUES(null,'%s','%s','%s',1,'2019-08-21 12:00:00','2019-08-21  12:00:00',0)" % (
        #     data['merchantCode'], self.key, self.key)  # 添加商户key对应关系
        # mysqlUtil.insertIntoData(sql)
        insertScore(init_data.get("env"), data['data'].get('certId'), data['data'].get('name'), data['data'].get('mobile'), '630')
        data['data']['applyNo'] = gen_random_str_num()
        print ("lllllll"+data['data']['applyNo'])
        data.pop("sign")
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port, self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print(r.json())
        checkReponseNotOk(r.json(), data['data'].get("applyNo"), '020005', "不存在的商户号")
        # mongo检查
        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo")) == False
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo")) == False

    def test_6(self, init_data):
        """用例6：鉴权失败，没有权限 --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "44444",#因为gateway缘故，写死
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }

        #data['merchantCode'] = self.merchant_code
        genKeyAndTreasure(init_data.get('env'), data['data']['merchantCode'],self.key,"")
        data['data']['applyNo'] = gen_random_str_num()
        # insertScore(init_data.get("env"), data['data'].get('certId'), data['data'].get('name'), data['data'].get('mobile'), '630')
        data.pop("sign")
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port, self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print(r.json())
        checkReponseNotOk(r.json(), data['data'].get("applyNo"), '020001', "商户访问权限不足")
        # mongo检查
        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo")) == False
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo")) == False

    def test_7(self, init_data):
        """用例7：未命中 --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "12345678",
                "applyNo": "20080808200000001",
                "name": "张三",
                 "mobile": create_phone(),
                "certId": create_certid(),
            }
        }
        data['data']['merchantCode']=self.merchant_code
        data['data']['applyNo'] = gen_random_str_num()
       # insertScore(init_data.get("env"), data['data'].get('certId'), data['data'].get('name'), data['data'].get('mobile'), '630')
        data.pop("sign")
        print (data)
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port, self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print(r.json())
        checkReponseNotOk(r.json(), data['data'].get("applyNo"), '001003', "未命中")
        # mongo检查
        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo")) == True
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo")) == False


#delteflag测试
    def test_8(self, init_data):
        """用例8：delteflag测试 gatewaykey budui --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "555555",#因为gateway缘故，写死
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }
        # data['merchantCode'] = self.merchant_code
        genKeyAndTreasure(init_data.get('env'), data['data']['merchantCode'], self.key, "creditScore",gate_delete_flag=1,)
        data['data']['applyNo'] = gen_random_str_num()
        # insertScore(init_data.get("env"), data['data'].get('certId'), data['data'].get('name'), data['data'].get('mobile'), '630')
        data.pop("sign")
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port, self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print(r.json())
        checkReponseNotOk(r.json(), data['data'].get("applyNo"), '020005', "不存在的商户号")
        # mongo检查
        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo")) == False
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo")) == False

    def test_9(self, init_data):
        """用例9：商户访问权限不足 fengkong key budui --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "666666",#因为gateway缘故，写死
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }

        # data['merchantCode'] = self.merchant_code
        genKeyAndTreasure(init_data.get('env'),  data['data']['merchantCode'], self.key, "creditScore",auth_delete_flag=1)
        data['data']['applyNo'] = gen_random_str_num()
        # insertScore(init_data.get("env"), data['data'].get('certId'), data['data'].get('name'), data['data'].get('mobile'), '630')
        data.pop("sign")
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port, self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print(r.json())
        checkReponseNotOk(r.json(), data['data'].get("applyNo"), '020005', "不存在的商户号")
        # mongo检查
        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo")) == False
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo")) == False

#新加逻辑，只有certid为空的情况下才能读到分数
    def test_10(self, init_data):
        """用例10：不存在的商户号--类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "777777",#因为gateway缘故，写死
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }

        # data['merchantCode'] = self.merchant_code
        genKeyAndTreasure(init_data.get('env'),  data['data']['merchantCode'], self.key, "creditScore",treasure_delete_flag=1)
        data['data']['applyNo'] = gen_random_str_num()
        # insertScore(init_data.get("env"), data['data'].get('certId'), data['data'].get('name'), data['data'].get('mobile'), '630')
        data.pop("sign")
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port, self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print(r.json())
        checkReponseNotOk(r.json(), data['data'].get("applyNo"), '020001', "商户访问权限不足")
        # mongo检查

        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo")) == False
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo")) == False

    def test_11(self, init_data):
        """用例11：手机号存在，身份证为空 --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "12345678",
                "applyNo": "20080808200000001",
                "name": "李四",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }
        insertScore(init_data.get("env"), "", data['data'].get('name'), data['data'].get('mobile'),
                    '640')  # 故意将身份证写错
        data['data']['merchantCode'] = self.merchant_code
        data['data']['applyNo'] = gen_random_str_num()
        data.pop("sign")
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port, self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print(r.json())
        checkReponseNotOk(r.json(), data['data'].get("applyNo"), '001003', "未命中")
        # mongo检查
        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo")) == True
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo")) == False

    def test_12(self, init_data):
        """用例12：手机号存在，身份证不存在 --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "12345678",
                "applyNo": "20080808200000001",
                "name": "李四",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }
        insertScoreNotEn(init_data.get("env"), "", data['data'].get('name'), data['data'].get('mobile'),
                    '650')  # 故意将身份证写错
        data['data']['merchantCode'] = self.merchant_code
        data['data']['applyNo'] = gen_random_str_num()
        data.pop("sign")
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port, self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print(r.json())
        res_sign = Des().get_sign(r.json().get('result'), secret_key=self.key)
        checkReponseOk(r.json(), data['data'].get("applyNo"), '000000', "成功",res_sign)
        # mongo检查
        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo")) == True
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo")) == True

#begin rsa test
    # def test_13(self, init_data):
    #     """用例12：交易核心正常case --类型:评分"""
    #     data = {
    #         "sign": "2a41558e04a3c8570cc9e232d51fcb49",
    #         "signType": "RSA",
    #         "encKey":"",
    #         "data": {
    #             "requestTime": "1218196800000",
    #             "merchantCode": "rsa123",
    #             "reqOrderNo": "20080808200000005",
    #             "name": "李四",
    #             "reservePhone": "13402099999",
    #             "idCardNo": "310225198701182638",
    #
    #         }
    #     }
    #
    #
    #     print(json.dumps(data['data'],ensure_ascii=False))
    #     deskey="cf410f84904a44cc8a7f48fc4134e8f7"
    #     sign=Des().rsa_sign(open("../keys/privatekey-pkcs8.pem").read(),content=json.dumps(data['data'],ensure_ascii=False).encode('utf-8'))## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
    #     data_no_encrypt=json.dumps(data['data'],ensure_ascii=False)
    #     data1=encrypt_by_key(key=deskey,content=data_no_encrypt)
    #     encKey=Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(),deskey)
    #     data['sign']=sign
    #     data['encKey']=encKey
    #     data['data'] = data1
    #     print (data)
    #     target_url="http://%s:10108/mock/5d7a1efe9b0d930018d64a56/cc/posttrans" % init_data.get("host")
    #     #target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
    #     print (target_url)
    #     r = requests.post(url=target_url, json=data)
    #     resp=r.json()
    #
    #     #check
    #     print("res:  "+str(resp))
    #     assert resp['encKey']==encKey
    #     data_res = decrypt_by_key(key=deskey, content=resp.get('data'))
    #     print ("res:"+data_res)
    #
    #     result=Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(),data_res.encode('utf-8'),resp.get('sign').strip())
    #     assert True==result
    #     assert json.loads(data_res).get('message')=='请求成功'
    #     #result=Des().rsa_signverify(open("../keys/publickey.pem").read(),data_no_encrypt.encode('utf-8'),sign)
    #
    # def test_14(self, init_data):
    #     """用例12：交易核心merchantCode不存在 --类型:评分"""
    #     data = {
    #         "sign": "2a41558e04a3c8570cc9e232d51fcb49",
    #         "signType": "RSA",
    #         "encKey":"",
    #         "data": {
    #             "requestTime": "1218196800000",
    #             "merchantCode": "rsa124",
    #             "reqOrderNo": "20080808200000005",
    #             "name": "李四",
    #             "reservePhone": "13402099999",
    #             "idCardNo": "310225198701182638",
    #
    #         }
    #     }
    #
    #
    #     print(json.dumps(data['data'],ensure_ascii=False))
    #     deskey="cf410f84904a44cc8a7f48fc4134e8f7"
    #     sign=Des().rsa_sign(open("../keys/privatekey-pkcs8.pem").read(),content=json.dumps(data['data'],ensure_ascii=False).encode('utf-8'))## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
    #     data_no_encrypt=json.dumps(data['data'],ensure_ascii=False)
    #     data1=encrypt_by_key(key=deskey,content=data_no_encrypt)
    #     encKey=Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(),deskey)
    #     data['sign']=sign
    #     data['encKey']=encKey
    #     data['data'] = data1
    #     print (data)
    #     target_url="http://%s:10108/mock/5d7a1efe9b0d930018d64a56/cc/posttrans" % init_data.get("host")
    #     #target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
    #     print (target_url)
    #     r = requests.post(url=target_url, json=data)
    #     resp=r.json()
    #
    #     #check
    #     print("res:  "+str(resp))
    #     assert resp['encKey']==encKey
    #     data_res = decrypt_by_key(key=deskey, content=resp.get('data'))
    #     print ("res:"+data_res)
    #
    #     result=Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(),data_res.encode('utf-8'),resp.get('sign').strip())
    #     assert True==result
    #     assert json.loads(data_res).get('message') == '不存在的商户号'
    #     #result=Des().rsa_signverify(open("../keys/publickey.pem").read(),data_no_encrypt.encode('utf-8'),sign)
    #
    #
    # def test_15(self, init_data):
    #     """用例12：验签不过 --类型:评分"""
    #     data = {
    #         "sign": "2a41558e04a3c8570cc9e232d51fcb49",
    #         "signType": "RSA",
    #         "encKey":"",
    #         "data": {
    #             "requestTime": "1218196800000",
    #             "merchantCode": "rsa123",
    #             "reqOrderNo": "20080808200000005",
    #             "name": "李四",
    #             "reservePhone": "13402099999",
    #             "idCardNo": "310225198701182638",
    #
    #         }
    #     }
    #
    #
    #     print(json.dumps(data['data'],ensure_ascii=False))
    #     deskey="cf410f84904a44cc8a7f48fc4134e8f7"
    #     sign="sign"## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
    #     data_no_encrypt=json.dumps(data['data'],ensure_ascii=False)
    #     data1=encrypt_by_key(key=deskey,content=data_no_encrypt)
    #     encKey=Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(),deskey)
    #     data['sign']=sign
    #     data['encKey']=encKey
    #     data['data'] = data1
    #     print (data)
    #     target_url="http://%s:10108/mock/5d7a1efe9b0d930018d64a56/cc/posttrans" % init_data.get("host")
    #     #target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
    #     print (target_url)
    #     r = requests.post(url=target_url, json=data)
    #     resp=r.json()
    #
    #     #check
    #     print("res:  "+str(resp))
    #     assert resp['encKey']==encKey
    #     data_res = decrypt_by_key(key=deskey, content=resp.get('data'))
    #     print ("res:"+data_res)
    #
    #     result=Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(),data_res.encode('utf-8'),resp.get('sign').strip())
    #     assert True==result
    #     assert json.loads(data_res).get('message') == '签名验证失败'
    #     #result=Des().rsa_signverify(open("../keys/publickey.pem").read(),data_no_encrypt.encode('utf-8'),sign)




    # def test_16(self, init_data):
    #     """用例12：白名单不存在--类型:评分"""
    #     data = {
    #         "sign": "2a41558e04a3c8570cc9e232d51fcb49",
    #         "signType": "RSA",
    #         "encKey": "",
    #         "data": {
    #             "requestTime": "1218196800000",
    #             "merchantCode": "rsa123",
    #             "reqOrderNo": "20080808200000005",
    #             "name": "李四",
    #             "reservePhone": "13402099999",
    #             "idCardNo": "310225198701182638",
    #
    #         }
    #     }
    #
    #     print(json.dumps(data['data'], ensure_ascii=False))
    #     deskey = "cf410f84904a44cc8a7f48fc4134e8f7"
    #     sign = Des().rsa_sign(open("../keys/privatekey-pkcs8.pem").read(),
    #                           content=json.dumps(data['data'], ensure_ascii=False).encode(
    #                               'utf-8'))  ## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
    #     data_no_encrypt = json.dumps(data['data'], ensure_ascii=False)
    #     data1 = encrypt_by_key(key=deskey, content=data_no_encrypt)
    #     encKey = Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(), deskey)
    #     data['sign'] = sign
    #     data['encKey'] = encKey
    #     data['data'] = data1
    #     print(data)
    #     target_url = "http://%s:10108/mock/5d7a1efe9b0d930018d64a56/cc/posttrans" % init_data.get("host")
    #     # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
    #     print(target_url)
    #     r = requests.post(url=target_url, json=data)
    #     resp = r.json()
    #
    #     # check
    #     print("res:  " + str(resp))
    #     assert resp['encKey'] == encKey
    #     data_res = decrypt_by_key(key=deskey, content=resp.get('data'))
    #     print("res:" + data_res)
    #
    #     result = Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(), data_res.encode('utf-8'),
    #                                   resp.get('sign').strip())
    #     assert True == result
    #     assert json.loads(data_res).get('message') == '无权访问'
