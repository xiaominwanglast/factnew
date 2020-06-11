#coding:utf-8
from ProductApi.VIPDecisionAPi import VIPDecisionApi
env='T1'
serial_no_list=[]
test=VIPDecisionApi(env=env,productId='vip_loan',sceneId='credit')
# test=VIPDecisionApi(env=env,productId='vip_loan',sceneId='extra_credit')
# serial_no_list.append(test.makeDecision(userId='13612217304',customerId='216684819158110111'))
#TODO T1
# serial_no_list.append(test.makeDecision(userId='13612215287',customerId='216684819158105036'))
# serial_no_list.append(test.makeDecision(userId='13612220819',customerId='216684819158104242'))
serial_no_list.append(test.makeDecision(userId='100025963',customerId='100000000000051919'))