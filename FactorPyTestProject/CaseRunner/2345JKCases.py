#coding:utf-8
from ProductApi.JKDecisionAPI import JKDecisionAPI
env='T1'
serial_no_list=[]
test=JKDecisionAPI(env=env,productId='jk_loan',sceneId='transaction_antifraud')
# test=VIPDecisionApi(env=env,productId='vip_loan',sceneId='extra_credit')
serial_no_list.append(test.makeDecision(userId='1261',customerId='100000001743099277',orcChangeFlag=1))
print (serial_no_list)