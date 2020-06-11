#coding:utf-8
from ProductApi.GdDecisionAPI import GdDecisonAPI
env='T2'
test=GdDecisonAPI(env=env,productId='jyj_loan',sceneId='credit')
serial_no_list=[]
# serial_no_list.append(test.makeDecision(userId='13612215127',customerId='216684819158107474'))
serial_no_list.append(test.makeDecision(userId='13612215287',customerId='216684819158107762'))
# serial_no_list.append(test.makeDecision(userId='20000005850',customerId='220000000000008030'))
# serial_no_list.append(test.makeDecision(userId='20000004737',customerId='220000000000006599'))
# serial_no_list.append(test.makeDecision(userId='13612219796',customerId='220000000000000186'))
print serial_no_list