from utils.DES import Des
from utils.MongoUtil import MongoPyUtil
from utils.MysqlUtil import MysqlPyUntil
from utils.threeDES import *
from utils.DES import *

def insertScore(env,cert_id, name, phone, score,version=''):
    #td = triple_des()
    des = Des()

    #print ("ssss"+cert_id)
    if cert_id!=None:
        cert_id_en = factor_encrypt_identity(str(cert_id))
    name_en = factor_encrypt_identity(name)
    phone_en = factor_encrypt_identity(phone)
    if cert_id!=None:
        cert_id_md5 = des.get_md5(cert_id)
    name_md5 = des.get_md5(name)
    phone_md5 = des.get_md5(phone)
    mysqlUtil = MysqlPyUntil(env, 'skynet_embrace')
    table_name="risk_out_score"+version
    if cert_id!=None:
        sql = "insert into {7} VALUES(null,'{0}','{1}','{2}','{3}','{4}','{5}','{6}',0,'2019-08-21','2019-08-21')".format(
        cert_id_en, name_en, phone_en, cert_id_md5, name_md5, phone_md5, score,table_name)
    else:
        sql = "insert into {5} VALUES(null,null,'{0}','{1}',null,'{2}','{3}','{4}',0,'2019-08-21','2019-08-21')".format(
             name_en, phone_en, name_md5, phone_md5, score,table_name)
    print (sql)
    res=mysqlUtil.insertIntoData(sql)
    print ("name insert:"+str(res))
    if res:
        return True
    else:
        return False

def insertScoreNotEn(env,cert_id, name, phone, score,version=""):
    #td = triple_des()
    des = Des()

    #print ("ssss"+cert_id)
    cert_id_en = (str(cert_id))
    name_en = factor_encrypt_identity(name)
    phone_en = factor_encrypt_identity(phone)
    cert_id_md5 = (cert_id)
    name_md5 = des.get_md5(name)
    phone_md5 = des.get_md5(phone)
    mysqlUtil = MysqlPyUntil(env, 'skynet_embrace')
    table_name = "risk_out_score" + version
    sql = "insert into {7} VALUES(null,'{0}','{1}','{2}','{3}','{4}','{5}','{6}',0,'2019-08-21','2019-08-21')".format(
        cert_id_en, name_en, phone_en, cert_id_md5, name_md5, phone_md5, score,table_name)
    print (sql)
    res=mysqlUtil.insertIntoData(sql)
    print ("name insert:"+str(res))
    if res:
        return True
    else:
        return False



def checkMongoLog(env,apply_no):
    mongoClient=MongoPyUtil(env,"skynet-embrace");
    res=mongoClient.queryNewOne("risk_out_request_log",{"apply_no":apply_no})
    print(res)
    if res:
        return True
    else:
        #raise Exception("checkMongoLog error")
        return False

def checkMongoStatics(env,apply_no,code="000000"):
    flag=False
    mongoClient=MongoPyUtil(env,"skynet-embrace");
    res=mongoClient.queryNewOne("risk_out_interface_statistics",{"apply_no":apply_no})
    print(res)
    try:
        if res[0].get('code')==code and res:
            flag=True
    except Exception as e:
        flag=False
    return flag

def checkReponseOk(response,applyNo,code,message,res_sign):
    assert response.get('applyNo')==applyNo
    assert response.get('message')==message
    assert response.get('code')==code
    assert response.get('sign')==res_sign
    try:
        score=int(response.get('result').get('score'))
        print("score:"+str(score))
    except Exception as e:
        print("exception:"+str(e))
        assert "score is not float"==""



def checkReponseNotOk(response,applyNo,code,message):
    assert applyNo==response.get('applyNo')
    assert message==response.get('message')
    assert code==response.get('code')


def genKeyAndTreasure(envopt,merchant_code,key,support_treasure,gate_delete_flag=0,auth_delete_flag=0,treasure_delete_flag=0):
    mysqlUtil = MysqlPyUntil(envopt, "tob_api_gateway")
    sql = "select * from  cfg_signature where merchant_code='%s' and publickey='%s' and privatekey='%s'" % (
        merchant_code, key, key)
    res = mysqlUtil.queryNewOne(sql)
    if not res:
        print("insert into cfg_signature")
        sql = "insert into cfg_signature VALUES(null,'%s','%s','%s',1,'2019-08-21 12:00:00','2019-08-21  12:00:00',%s)" % (
            merchant_code, key, key,gate_delete_flag)  # 添加商户key对应关系
        mysqlUtil.insertIntoData(sql)

    # 先查询有没有key
    mysqlUtil = MysqlPyUntil(envopt, "skynet_merchant")
    sql = "select * from  risk_out_merchant_auth where merchant_code='%s' and secret_key='%s'" % (
    merchant_code, key)
    res = mysqlUtil.queryNewOne(sql)
    if not res:
        print("insert into risk_out_merchant_auth")
        sql = "insert into risk_out_merchant_auth VALUES(null,'%s','%s','user',0,%s,'2019-08-21 12:00:00','2019-08-21  12:00:00')" % (
        merchant_code, key,auth_delete_flag)  # 添加商户key对应关系
        mysqlUtil.insertIntoData(sql)

    sql = "select * from  risk_out_merchant_treasure where merchant_code='%s' and support_treasure='%s'" % (
        merchant_code, support_treasure)
    res = mysqlUtil.queryNewOne(sql)
    if not res:
        print("insert into risk_out_merchant_treasure")
        sql = "insert into risk_out_merchant_treasure VALUES(null,'%s','%s','%s','2019-08-21 12:00:00','2019-08-21  12:00:00')" % (
        merchant_code, support_treasure,treasure_delete_flag)  # 添加鉴权信息
        mysqlUtil.insertIntoData(sql)

# def getRSAsign(key,dic):
#     list = []
#     for i in dic.keys():
#         list.append(i)
#         new = sorted(list, key=lambda i: i[0])
#     sign_str = ""
#     for i in new:
#         sign_str = sign_str + i + "=" + dic.get(i) + "&"
#     sign_str = sign_str[0:-1] + "&secretKey=" + key
#     print(sign_str)
#     return Des().rsa_sign(key,sign_str)




