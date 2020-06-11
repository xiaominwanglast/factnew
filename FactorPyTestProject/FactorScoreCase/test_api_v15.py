# coding:utf-8
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
    key = "abc123"
    merchant_code = "88881"
    support_treasure = "creditScore"
    port = "10108"
    http_url = "skynet-embrace/risk/1.5/creditScore"

    @classmethod
    def setup_class(cls):
        pass

    def teardown_method(self, method):
        print('\n测试用例执行完毕')

    # 准备数据
    @pytest.fixture(scope="module", autouse=True)
    def init_data(self, request):
        envopt = request.config.getoption("--envopt")
        print("env:" + envopt)
        if not envopt:
            envopt = "T1"
        # conn = redis.Redis(host=SETTING[envopt]['redis']['host'], port=SETTING[envopt]['redis']['port'],
        #                    password=SETTING[envopt]['redis']['password'], db=SETTING[envopt]['redis']['db'])
        # if conn.keys(pattern='*com*'):
        #     conn.delete(*conn.keys(pattern='*com*'))
        host = env_config[envopt]
        # gateway
        mysqlUtil = MysqlPyUntil(envopt, "tob_api_gateway")
        sql = "select * from  cfg_signature where merchant_code='%s' and publickey='%s' and privatekey='%s'" % (
            self.merchant_code, self.key, self.key)
        res = mysqlUtil.queryNewOne(sql)
        if not res:
            print("insert into cfg_signature")
            sql = "insert into cfg_signature VALUES(null,'%s','%s','%s',1,'2019-08-21 12:00:00','2019-08-21  12:00:00',0)" % (
                self.merchant_code, self.key, self.key)  # 添加商户key对应关系
            mysqlUtil.insertIntoData(sql)

        # 先查询有没有key
        mysqlUtil = MysqlPyUntil(envopt, "skynet_merchant")
        sql = "select * from  risk_out_merchant_auth where merchant_code='%s' and secret_key='%s'" % (
        self.merchant_code, self.key)
        res = mysqlUtil.queryNewOne(sql)
        if not res:
            print("insert into risk_out_merchant_auth")
            sql = "insert into risk_out_merchant_auth VALUES(null,'%s','%s','user',0,0,'2019-08-21 12:00:00','2019-08-21  12:00:00')" % (
            self.merchant_code, self.key)  # 添加商户key对应关系
            mysqlUtil.insertIntoData(sql)

        sql = "select * from  risk_out_merchant_treasure where merchant_code='%s' and support_treasure='%s'" % (
            self.merchant_code, self.support_treasure)
        res = mysqlUtil.queryNewOne(sql)
        if not res:
            print("insert into risk_out_merchant_treasure")
            sql = "insert into risk_out_merchant_treasure VALUES(null,'%s','%s',0,'2019-08-21 12:00:00','2019-08-21  12:00:00')" % (
            self.merchant_code, self.support_treasure)  # 添加鉴权信息
            mysqlUtil.insertIntoData(sql)
        print("end")
        return {"host": host, "env": envopt}

    def test_v15_1(self, init_data):
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
                "certId": create_certid(),
            }
        }
        print("insertsql")
        insertScore(init_data.get("env"), data['data'].get('certId'), data['data'].get('name'),
                    data['data'].get('mobile'), '720',version='_v150')
        data['data']['merchantCode'] = self.merchant_code
        data['data']['applyNo'] = gen_random_str_num()
        data.pop("sign")
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port, self.http_url)
        print(url)
        print(data)
        print("begin invoke interface")
        r = requests.post(url=url, json=data)
        print("end invoke interface")
        print(r.json())
        res_sign = Des().get_sign(r.json().get('result'), secret_key=self.key)
        checkReponseOk(r.json(), data['data'].get("applyNo"), '000000', "成功",res_sign)
        # mongo检查
        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo")) == True
        # time.sleep(1)
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo")) == True

    def test_v15_2(self, init_data):
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
        insertScore(init_data.get("env"), "1234567", data['data'].get('name'), data['data'].get('mobile'),
                    '730',version='_v150')  # 故意将身份证写错
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

    def test_v15_3(self, init_data):
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
        insertScore(init_data.get("env"), "1234567", data['data'].get('name'), data['data'].get('mobile'),
                    '730',version='_v150')  # 故意将身份证写错
        data['data']['merchantCode'] = self.merchant_code
        data['data']['applyNo'] = gen_random_str_num()
        data.pop("sign")
        sign = Des().get_sign(data['data'], secret_key=self.key)
        data['sign'] = "sign"  # 随便给个sign
        url = "http://%s:%s/%s" % (init_data.get("host"), self.port, self.http_url)
        print(data)
        r = requests.post(url=url, json=data)
        print(r.json())
        checkReponseNotOk(r.json(), data['data'].get("applyNo"), '990006', "签名验证失败")
        # mongo检查
        assert checkMongoLog(init_data.get("env"), data['data'].get("applyNo")) == False
        assert checkMongoStatics(init_data.get("env"), data['data'].get("applyNo")) == False

    def test_v15_4(self, init_data):
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
        data['data']['merchantCode'] = gen_random_str_num()
        data['data']['applyNo'] = gen_random_str_num()
        insertScore(init_data.get("env"), data['data'].get('certId'), data['data'].get('name'),
                    data['data'].get('mobile'), '730',version='_v150')
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

    def test_v15_5(self, init_data):
        """用例5：鉴权失败,gateway，有key，风控没key --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "33333",  # 因为gateway缘故，写死
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
        insertScore(init_data.get("env"), data['data'].get('certId'), data['data'].get('name'),
                    data['data'].get('mobile'), '730',version='_v150')
        data['data']['applyNo'] = gen_random_str_num()
        print("lllllll" + data['data']['applyNo'])
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

    def test_v15_6(self, init_data):
        """用例6：鉴权失败，没有权限 --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "44444",  # 因为gateway缘故，写死
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }

        # data['merchantCode'] = self.merchant_code
        genKeyAndTreasure(init_data.get('env'), data['data']['merchantCode'], self.key, "")
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

    def test_v15_7(self, init_data):
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
        data['data']['merchantCode'] = self.merchant_code
        data['data']['applyNo'] = gen_random_str_num()
        # insertScore(init_data.get("env"), data['data'].get('certId'), data['data'].get('name'), data['data'].get('mobile'), '630')
        data.pop("sign")
        print(data)
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

    # delteflag测试
    def test_v15_8(self, init_data):
        """用例8：delteflag测试 gatewaykey budui --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "555555",  # 因为gateway缘故，写死
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }
        # data['merchantCode'] = self.merchant_code
        genKeyAndTreasure(init_data.get('env'), data['data']['merchantCode'], self.key, "creditScore",
                          gate_delete_flag=1, )
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

    def test_v15_9(self, init_data):
        """用例9：商户访问权限不足 fengkong key budui --类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "666666",  # 因为gateway缘故，写死
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }

        # data['merchantCode'] = self.merchant_code
        genKeyAndTreasure(init_data.get('env'), data['data']['merchantCode'], self.key, "creditScore",
                          auth_delete_flag=1)
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

    # 新加逻辑，只有certid为空的情况下才能读到分数
    def test_v15_10(self, init_data):
        """用例10：不存在的商户号--类型:评分"""
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "MD5",
            "data": {
                "requestTime": "1218196800000",
                "merchantCode": "777777",  # 因为gateway缘故，写死
                "applyNo": "20080808200000001",
                "name": "张三",
                "mobile": create_phone(),
                "certId": create_certid(),
            }
        }

        # data['merchantCode'] = self.merchant_code
        genKeyAndTreasure(init_data.get('env'), data['data']['merchantCode'], self.key, "creditScore",
                          treasure_delete_flag=1)
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

    def test_v15_11(self, init_data):
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
                    '740',version='_v150')  # 故意将身份证写错
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

    def test_v15_12(self, init_data):
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
                         '750',version='_v150')  # 故意将身份证写错
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


