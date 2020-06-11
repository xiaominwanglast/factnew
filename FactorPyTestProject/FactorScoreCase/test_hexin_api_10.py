# coding:utf-8
import datetime
import pytest
import requests
# import redis
from utils.Setting import SETTING
from utils.generatorTool import *
from FactorScoreCase.env_config import env_config
from FactorScoreCase.test_api_use_method import *
from utils.InfoGenerate import *
import logging
from utils import logger_config  # 导入自定义的logging配置

import json
from utils.log_utils import *
logger = logging.getLogger(__file__)  # 生成logger实例

old_req_number="" ## 原订单号
signNo=""  ##鉴权确认给予signNo
trans_reqNo="" ##交易流水号

class TestApi(object):
    """风控输出接口测试"""


    deskey = "cf410f84904a44cc8a7f48fc4134e8f7"
    merchant_code = "ZHUJTest"
    port = "10108"
    verificationCode="123456"
    bankCode="ABC"

    #user info
    bankCardNo=create_bank_card()
    cert_id=create_certid()
    phone=create_phone()
    name=create_name()

    #merchant_code = "rsa1231"
    #chuandi canyu



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

        host = env_config[envopt]
        print("end")
        return {"host": host, "env": envopt}

    def test_auth_apply(self, init_data):
        """用例1：正常情况，交易鉴权申请 --类型:交易"""
        reqNo=create_random_id()
        global old_req_number #赋值给下一个用例
        old_req_number=reqNo #赋值给下一个用例
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "RSA",
            "encKey": "",
            "data": {
                "bankCardNo":self.bankCardNo,
                "bankCardType":"DEBIT",
                "bankCode":self.bankCode,
                "idCardName":self.name,
                "idCardNo":self.cert_id,
                "merchantCode":self.merchant_code,
                "reqOrderNo":reqNo,
                "reservePhone":self.phone,
                "validTime":"30"

            }
        }
        logger.info("req:"+json.dumps(data['data'], ensure_ascii=False))

        sign = Des().rsa_sign(open("../keys/privatekey-pkcs8.pem").read(),  ###他们的私钥
                              content=json.dumps(data['data'], ensure_ascii=False).encode(
                                  'utf-8'))  ## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
        data_no_encrypt = json.dumps(data['data'], ensure_ascii=False)
        data1 = encrypt_by_key(key=self.deskey, content=data_no_encrypt)


        encKey = Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(), self.deskey)  ###我们的公钥
        data['sign'] = sign
        data['encKey'] = encKey
        data['data'] = data1

        target_url = "http://%s:%s/hexin-trader/outpay/1001" % (init_data.get("host"),self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        logger.info("url:"+target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data,resp)
        # check
        assert resp['encKey'] == encKey
        data_res = decrypt_by_key(key=self.deskey, content=resp.get('data'))
        logger.info("res:" + data_res)

        result = Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(), data_res.encode('utf-8'), ##我们的公钥
                                      resp.get('sign').strip())
        assert True == result
        assert json.loads(data_res).get('msg') == '成功'

    def test_auth_check(self, init_data):
        """用例1：正常情况，交易鉴权确认 --类型:交易"""
        # print (create_random_id())
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "RSA",
            "encKey": "",
            "data": {
                "merchantCode": self.merchant_code,
                "oriReqOrderNo": old_req_number,
                "reqOrderNo": create_random_id(),
                "verificationCode": self.verificationCode,

            }
        }
        print(json.dumps(data['data'], ensure_ascii=False))

        sign = Des().rsa_sign(open("../keys/privatekey-pkcs8.pem").read(),  ###我们的私钥
                              content=json.dumps(data['data'], ensure_ascii=False).encode(
                                  'utf-8'))  ## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
        data_no_encrypt = json.dumps(data['data'], ensure_ascii=False)
        data1 = encrypt_by_key(key=self.deskey, content=data_no_encrypt)

        encKey = Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(), self.deskey)  ###他们的公钥
        data['sign'] = sign
        data['encKey'] = encKey
        data['data'] = data1

        target_url = "http://%s:%s/hexin-trader/outpay/1002" % (init_data.get("host"), self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        print(target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data, resp)
        # check
        assert resp['encKey'] == encKey
        data_res = decrypt_by_key(key=self.deskey, content=resp.get('data'))
        logger.info("res:" + data_res)
        global signNo
        #signNo=(json.loads(data_res))['result']['singNo']
        signNo=(json.loads(data_res)['result']['signNo'])
        result = Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(), data_res.encode('utf-8'),
                                      resp.get('sign').strip())
        assert True == result
        assert json.loads(data_res).get('msg') == '成功'

    # result=Des().rsa_signverify(open("../keys/publickey.pem").read(),data_no_encrypt.encode('utf-8'),sign)

    def test_repay_invoke(self, init_data):
        """用例1：正常情况，交易劈扣调用--类型:交易"""
        # print (create_random_id())
        global trans_reqNo
        trans_reqNo=str(create_random_id())
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "RSA",
            "encKey": "",
            "data": {
                "bankCode": self.bankCode,
                "idCardName": self.name,
                "merchantCode": self.merchant_code,
                "bankCardNo": self.bankCardNo,
                "idCardNo": self.cert_id,
                "signNo": signNo,
                "reqOrderNo":trans_reqNo,
                "totalAmount": "123500",
                "reservePhone": self.phone,
                "signType": "1",
                "tradeSummary": "10",
                "callbackUrl": "http://172.17.0.121:7300/mock/5da169279b0d930018d64a65/cc_copy/tran",
                "payChannel": "ZJ",
                "applyDate": str(datetime.datetime.now())[0:19]

            }
        }
        print(json.dumps(data['data'], ensure_ascii=False))

        sign = Des().rsa_sign(open("../keys/privatekey-pkcs8.pem").read(),  ###我们的私钥
                              content=json.dumps(data['data'], ensure_ascii=False).encode(
                                  'utf-8'))  ## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
        data_no_encrypt = json.dumps(data['data'], ensure_ascii=False)
        data1 = encrypt_by_key(key=self.deskey, content=data_no_encrypt)

        encKey = Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(), self.deskey)  ###他们的公钥
        data['sign'] = sign
        data['encKey'] = encKey
        data['data'] = data1

        target_url = "http://%s:%s/hexin-trader/outpay/1410" % (init_data.get("host"), self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        print(target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data, resp)
        # check
        assert resp['encKey'] == encKey
        data_res = decrypt_by_key(key=self.deskey, content=resp.get('data'))
        logger.info("res:" + data_res)

        result = Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(), data_res.encode('utf-8'),
                                      resp.get('sign').strip())
        assert True == result
        assert json.loads(data_res).get('msg') == '成功'

    def test_repay_query(self, init_data):
        """用例1：正常情况，交易劈扣查询--类型:交易"""
        # print (create_random_id())
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "RSA",
            "encKey": "",
            "data": {
                "merchantCode":self.merchant_code,
                "applyDate":str(datetime.datetime.now())[0:19],
                "reqOrderNo":trans_reqNo

            }
        }
        print(json.dumps(data['data'], ensure_ascii=False))

        sign = Des().rsa_sign(open("../keys/privatekey-pkcs8.pem").read(),  ###他们的私钥
                              content=json.dumps(data['data'], ensure_ascii=False).encode(
                                  'utf-8'))  ## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
        data_no_encrypt = json.dumps(data['data'], ensure_ascii=False)
        data1 = encrypt_by_key(key=self.deskey, content=data_no_encrypt)

        encKey = Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(), self.deskey)  ###我们的公钥
        data['sign'] = sign
        data['encKey'] = encKey
        data['data'] = data1

        target_url = "http://%s:%s/hexin-trader/outpay/1403" % (init_data.get("host"), self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        print(target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data, resp)
        # check
        assert resp['encKey'] == encKey
        data_res = decrypt_by_key(key=self.deskey, content=resp.get('data'))
        logger.info("res:" + data_res)

        result = Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(), data_res.encode('utf-8'),
                                      resp.get('sign').strip())
        assert True == result
        assert json.loads(data_res).get('msg') == '成功'

    def test_callback(self, init_data):
        """用例1：正常情况，交易回调--类型:交易"""
        # print (create_random_id())
        if trans_reqNo=="":
            trans_reqNo1="12121313"
        else:
            trans_reqNo1=trans_reqNo

        data = {
                "callback": "http://172.17.0.121:7300/mock/5da169279b0d930018d64a65/cc_copy/tran",
                "merchantCode": self.merchant_code,
               # "applyDate": str(datetime.datetime.now())[0:19],
                "reqOrderNo": trans_reqNo1

        }



        # print(json.dumps(data['data'], ensure_ascii=False))
        #

        # data_no_encrypt = json.dumps(data['data'], ensure_ascii=False)
        # data1 = encrypt_by_key(key=self.deskey, content=data_no_encrypt)
        #
        # encKey = Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(), self.deskey)  ###他们的公钥
        # data['sign'] = sign
        # data['encKey'] = encKey
        # data['data'] = data1
        logger.info("req:"+str(data))
        target_url = "http://%s:%s/api-gateway/callback/trader" % (init_data.get("host"), self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        print(target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data, resp)
        assert resp.get('result')== 'success'
        # check
        # assert resp['encKey'] == encKey
        # data_res = decrypt_by_key(key=self.deskey, content=resp.get('data'))
        # logger.info("res:" + data_res)
        #
        # result = Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(), data_res.encode('utf-8'),
        #                               resp.get('sign').strip())
        # assert True == result
        # assert json.loads(data_res).get('msg') == '成功'
        #checkshifou

        dic1={"signType":"RSA","sign":"gWDFBctqwTalny7zbWojNXfW3XHPX/dSqhjexDUwC3ZsZfwTjndNHm5jfQy6O46Hg2nfRSu9eEM0TPmgTmW9ql/IrRUNZKB3DS5GAq1+F7/nDJHQQctWATDviaFXofrdCXe7M7ZYf97HnCkfnUfRJNzx6HROPbkUjON+frvIpWmTpJPlDjtfugkirFLvdMztS69M+UaA2PpaS5Yh/L6YlnEA0DqcUiMC0jv9/FuDkebXiZCKQzBVRUE+i93unSnf2YWDual2R4K5XqFahSQx05PvivXKVF5FrRJNQlCrX2TeWNaA7E/KF4f0nYcTkiTzRT3893JRMB7marNj0idNhw==","encKey":"gvqTjn+7N81p23k/6UuxUnJSpk5ViWVVbkZgjNq7nKM3l1vsc30z2cBPM4UvVOUTX5atOpkXhznF\r\n7JMDsa+y+fAB1d6V8jIf/DG8e+LHkPxqitfrs599Eoqk4hmGyJPXB+2ezbl78ZWuhPLDFy9F2AaJ\r\n29j1xw0Cyhdf7d+VW4ZmCikz0RMVOC4ICZRjVmr5HszyAAmEbXTyBxrNIUPgZOqaXnW3Dzl29Xv2\r\nejXRqplOmBS38wYDi9lrwumCGr9FNZB/gItVoARUbKj4sn9xQ89IoMAcmBu0lfOCgfLLz4JETAYW\r\nqhPcptisWRyuYdCgRCoC3Q3mwk8xM0fxMZGx+A==\r\n","data":"ixo7aQMAeftKU8tLxZe2EBdYVkhlPd9p4giZ/ZSHmQ/YXHegG9QBpFoTi6DT8jZVUpohTfddTY7d\r\nVWU6cYjUtf6W+8jkVa7umO7O3SR6YoMMRgEi3HpAV+1mVVclaTX3TA3FpJRWMh/gkzgAsj7K4Ns7\r\nZi2doX8McyS2zWp4XL09lLBXdrsKiZagRjhwm6QlyJayhbXoAbdjXHs3bSEVG/rfgUGDYh6Kkyk4\r\nqfsEK7s=\r\n"}
        enc_key = Des().RSAdecript(open("../keys/privatekey-pkcs8.pem").read(),dic1['encKey'] )
        enc_key=str(enc_key, encoding="utf-8")
        logger.info("enc_key:" + str(enc_key))
        encrypt_data = decrypt_by_key(key=enc_key, content=dic1['data'])
        logger.info("encrypt_data:" + encrypt_data)
        res=Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(),  ###他们公钥
                                 encrypt_data.encode(
                                  'utf-8'),dic1['sign'])  ## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
        logger.info("signres:"+str(res))


    def test_callback_no_callback(self, init_data):
        """用例1：没给callback--类型:交易"""
        # print (create_random_id())
        if trans_reqNo=="":
            trans_reqNo1="12121313"
        else:
            trans_reqNo1=trans_reqNo

        data = {
                #"callback": "http://172.17.0.121:7300/mock/5da169279b0d930018d64a65/cc_copy/tran",
                "merchantCode": self.merchant_code,
               # "applyDate": str(datetime.datetime.now())[0:19],
                "reqOrderNo": trans_reqNo1

        }
        logger.info("req:"+str(data))
        target_url = "http://%s:%s/api-gateway/callback/trader" % (init_data.get("host"), self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        print(target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data, resp)

    def test_callback_gateway_error(self, init_data):
        """用例1：网关内部异常--类型:交易"""
        # print (create_random_id())
        if trans_reqNo=="":
            trans_reqNo1="12121313"
        else:
            trans_reqNo1=trans_reqNo

        data = {
                "callback": "http://172.17.0.121:7300/mock/5da169279b0d930018d64a65/cc_copy/tran",
                "merchantCode": 32424,
               # "applyDate": str(datetime.datetime.now())[0:19],
                "reqOrderNo": trans_reqNo1

        }
        logger.info("req:"+str(data))
        target_url = "http://%s:%s/api-gateway/callback/trader" % (init_data.get("host"), self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        print(target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data, resp)
        assert resp.get('error').get('message') == '网关内部异常'

    def test_callback_connect_fail(self, init_data):
        """用例1：商户链接异常--类型:交易"""
        # print (create_random_id())
        if trans_reqNo == "":
            trans_reqNo1 = "12121313"
        else:
            trans_reqNo1 = trans_reqNo

        data = {
            "callback": "http://172.17.0.121:7400/mock/5da169279b0d930018d64a65/cc_copy/tran",
            "merchantCode": self.merchant_code,
            # "applyDate": str(datetime.datetime.now())[0:19],
            "reqOrderNo": trans_reqNo1

        }
        logger.info("req:" + str(data))
        target_url = "http://%s:%s/api-gateway/callback/trader" % (init_data.get("host"), self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        print(target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data, resp)
        assert resp.get('error').get('message') == '商户连接异常'

    def test_callback_connecttimeout(self, init_data):
        """用例1：商户链接超时--类型:交易"""
        # print (create_random_id())
        if trans_reqNo == "":
            trans_reqNo1 = "12121313"
        else:
            trans_reqNo1 = trans_reqNo

        data = {
            "callback": "http://172.17.16.50:8075/cc",
            "merchantCode": self.merchant_code,
            # "applyDate": str(datetime.datetime.now())[0:19],
            "reqOrderNo": trans_reqNo1

        }
        logger.info("req:" + str(data))
        target_url = "http://%s:%s/api-gateway/callback/trader" % (init_data.get("host"), self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        print(target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data, resp)
        assert resp.get('error').get('message')=='请求超时'


    def test_callback_need_resend(self, init_data):
        """用例1：商户请求重试--类型:交易"""
        # print (create_random_id())
        if trans_reqNo == "":
            trans_reqNo1 = "12121313"
        else:
            trans_reqNo1 = trans_reqNo

        data = {
            "callback": "http://172.17.0.121:7300/mock/5da169279b0d930018d64a65/cc_copy/tran_error",
            "merchantCode": self.merchant_code,
            # "applyDate": str(datetime.datetime.now())[0:19],
            "reqOrderNo": trans_reqNo1

        }
        logger.info("req:" + str(data))
        target_url = "http://%s:%s/api-gateway/callback/trader" % (init_data.get("host"), self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        print(target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data, resp)
        assert resp.get('error').get('message') == '商户请求重试'

    def test_auth_apply_auth_error(self, init_data):
        """用例1：网关鉴权错误 --类型:交易"""
        reqNo = create_random_id()
        global old_req_number  # 赋值给下一个用例
        old_req_number = reqNo  # 赋值给下一个用例
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "RSA",
            "encKey": "",
            "data": {
                "bankCardNo": self.bankCardNo,
                "bankCardType": "DEBIT",
                "bankCode": self.bankCode,
                "idCardName": self.name,
                "idCardNo": self.cert_id,
                "merchantCode": "1111",
                "reqOrderNo": reqNo,
                "reservePhone": self.phone,
                "validTime": "30"

            }
        }
        logger.info("req:" + json.dumps(data['data'], ensure_ascii=False))

        sign = Des().rsa_sign(open("../keys/privatekey-pkcs8.pem").read(),  ###他们的私钥
                              content=json.dumps(data['data'], ensure_ascii=False).encode(
                                  'utf-8'))  ## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
        data_no_encrypt = json.dumps(data['data'], ensure_ascii=False)
        data1 = encrypt_by_key(key=self.deskey, content=data_no_encrypt)

        encKey = Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(), self.deskey)  ###我们的公钥
        data['sign'] = sign
        data['encKey'] = encKey
        data['data'] = data1

        target_url = "http://%s:%s/hexin-trader/outpay/1001" % (init_data.get("host"), self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        logger.info("url:" + target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data, resp)
        # check
        assert resp['encKey'] == encKey
        data_res = decrypt_by_key(key=self.deskey, content=resp.get('data'))
        logger.info("res:" + data_res)

        result = Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(), data_res.encode('utf-8'),  ##我们的公钥
                                      resp.get('sign').strip())
        assert True == result
        assert json.loads(data_res).get('msg') == '不存在的商户号'
        assert json.loads(data_res)['result'] == None

    def test_auth_apply_sign_error(self, init_data):
        """用例1：延签失败 --类型:交易"""
        reqNo = create_random_id()
        global old_req_number  # 赋值给下一个用例
        old_req_number = reqNo  # 赋值给下一个用例
        data = {
            "sign": "2a41558e04a3c8570cc9e232d51fcb49",
            "signType": "RSA",
            "encKey": "",
            "data": {
                "bankCardNo": self.bankCardNo,
                "bankCardType": "DEBIT",
                "bankCode": self.bankCode,
                "idCardName": self.name,
                "idCardNo": self.cert_id,
                "merchantCode": self.merchant_code,
                "reqOrderNo": reqNo,
                "reservePhone": self.phone,
                "validTime": "30"

            }
        }
        logger.info("req:" + json.dumps(data['data'], ensure_ascii=False))

        sign = Des().rsa_sign(open("../keys/privatekey-pkcs8.pem").read(),  ###他们的私钥
                              content=json.dumps(data['data'], ensure_ascii=False).encode(
                                  'utf-8'))  ## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
        data_no_encrypt = json.dumps(data['data'], ensure_ascii=False)
        data1 = encrypt_by_key(key=self.deskey, content=data_no_encrypt)

        encKey = Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(), self.deskey)  ###我们的公钥
        data['sign'] = "sign"
        data['encKey'] = encKey
        data['data'] = data1

        target_url = "http://%s:%s/hexin-trader/outpay/1001" % (init_data.get("host"), self.port)
        # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
        logger.info("url:" + target_url)
        r = requests.post(url=target_url, json=data)
        resp = r.json()
        LogUtil.printlog(data, resp)
        # check
        assert resp['encKey'] == encKey
        data_res = decrypt_by_key(key=self.deskey, content=resp.get('data'))
        logger.info("res:" + data_res)

        result = Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(), data_res.encode('utf-8'),  ##我们的公钥
                                      resp.get('sign').strip())
        assert True == result
        assert json.loads(data_res).get('msg') == '签名验证失败'
        assert json.loads(data_res)['result'] == None

    # def test_auth_apply_whiteip_error(self, init_data):
    #     """用例1：白名单失败 --类型:交易"""
    #     reqNo = create_random_id()
    #     global old_req_number  # 赋值给下一个用例
    #     old_req_number = reqNo  # 赋值给下一个用例
    #     data = {
    #         "sign": "2a41558e04a3c8570cc9e232d51fcb49",
    #         "signType": "RSA",
    #         "encKey": "",
    #         "data": {
    #             "bankCardNo": self.bankCardNo,
    #             "bankCardType": "DEBIT",
    #             "bankCode": self.bankCode,
    #             "idCardName": self.name,
    #             "idCardNo": self.cert_id,
    #             "merchantCode": self.merchant_code,
    #             "reqOrderNo": reqNo,
    #             "reservePhone": self.phone,
    #             "validTime": "30"
    #
    #         }
    #     }
    #     logger.info("req:" + json.dumps(data['data'], ensure_ascii=False))
    #
    #     sign = Des().rsa_sign(open("../keys/privatekey-pkcs8.pem").read(),  ###他们的私钥
    #                           content=json.dumps(data['data'], ensure_ascii=False).encode(
    #                               'utf-8'))  ## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
    #     data_no_encrypt = json.dumps(data['data'], ensure_ascii=False)
    #     data1 = encrypt_by_key(key=self.deskey, content=data_no_encrypt)
    #
    #     encKey = Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(), self.deskey)  ###我们的公钥
    #     data['sign'] = sign
    #     data['encKey'] = encKey
    #     data['data'] = data1
    #
    #     target_url = "http://%s:%s/hexin-trader/outpay/1001" % (init_data.get("host"), self.port)
    #     # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
    #     logger.info("url:" + target_url)
    #     r = requests.post(url=target_url, json=data)
    #     resp = r.json()
    #     LogUtil.printlog(data, resp)
    #     # check
    #     assert resp['encKey'] == encKey
    #     data_res = decrypt_by_key(key=self.deskey, content=resp.get('data'))
    #     logger.info("res:" + data_res)
    #
    #     result = Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(), data_res.encode('utf-8'),  ##我们的公钥
    #                                   resp.get('sign').strip())
    #     assert True == result
    #     assert json.loads(data_res).get('msg') == '无权访问'
    #     assert json.loads(data_res)['result'] == None