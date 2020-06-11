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

reqNo = create_random_id()
global old_req_number  # 赋值给下一个用例
old_req_number = reqNo  # 赋值给下一个用例

deskey = "cf410f84904a44cc8a7f48fc4134e8f7"
merchant_code = "merchantTest"
port = "80"
verificationCode = "123456"
bankCode = "ABC"

# user info
bankCardNo = create_bank_card()
cert_id = create_certid()
phone = create_phone()
name = create_name()

host="kmopenapi.2345.com"
def invoke():
    #host="kmopenapi.2345.com"

    data = {
        "sign": "2a41558e04a3c8570cc9e232d51fcb49",
        "signType": "RSA",
        "encKey": "",
        "data": {
            "bankCardNo": bankCardNo,
            "bankCardType": "DEBIT",
            "bankCode": bankCode,
            "idCardName": name,
            "idCardNo": cert_id,
            "merchantCode": merchant_code,
            "reqOrderNo": reqNo,
            "reservePhone": phone,
            "validTime": "30"

        }
    }
    logger.info("req:" + json.dumps(data['data'], ensure_ascii=False))

    sign = Des().rsa_sign(open("../keys/privatekey-pkcs8.pem").read(),  ###他们的私钥
                          content=json.dumps(data['data'], ensure_ascii=False).encode(
                              'utf-8'))  ## json.dumps(data['data'],ensure_ascii=False).encode('utf-8')
    data_no_encrypt = json.dumps(data['data'], ensure_ascii=False)
    data1 = encrypt_by_key(key=deskey, content=data_no_encrypt)

    encKey = Des().RSAencript(open("../keys/rsa_public_key_2048.pem").read(), deskey)  ###我们的公钥
    data['sign'] = sign
    data['encKey'] = encKey
    data['data'] = data1

    target_url = "https://%s/hexin-trader/outpay/1001" % (host)
    # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
    logger.info("url:" + target_url)
    r = requests.post(url=target_url, json=data)
    resp = r.json()
    LogUtil.printlog(data, resp)
    # check
    assert resp['encKey'] == encKey
    data_res = decrypt_by_key(key=deskey, content=resp.get('data'))
    logger.info("res:" + data_res)

    result = Des().rsa_signverify(open("../keys/rsa_public_key_2048.pem").read(), data_res.encode('utf-8'),  ##我们的公钥
                                  resp.get('sign').strip())
    assert True == result
    assert json.loads(data_res).get('msg') == '成功'


def test_callback():
    """用例1：正常情况，交易回调--类型:交易"""
    # print (create_random_id())

    trans_reqNo1="12121313"


    data = {
            "callback": "http://172.17.0.121:7300/mock/5da169279b0d930018d64a65/cc_copy/tran",
            "merchantCode": merchant_code,
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
    target_url = "https://%s/api-gateway/callback/trader" % (host)
    # target_url = "http://172.17.0.121:7300/mock/5d7a1efe9b0d930018d64a56/cc/test2"
    print(target_url)
    r = requests.post(url=target_url, json=data)
    resp = r.json()
    LogUtil.printlog(data, resp)
    assert resp.get('result')== 'success'

if __name__=='__main__':
    test_callback()



