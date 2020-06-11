#coding:utf-8
from ProductApi.GdDecisionAPI import GdDecisonAPI
env='T1'
test=GdDecisonAPI(env=env,productId='gd_loan',sceneId='credit')
serial_no_list=[]
# serial_no_list.append(test.makeDecision(userId='13612215127',customerId='216684819158107474'))
# serial_no_list.append(test.makeDecision(userId='13612215287',customerId='216684819158107762'))
# serial_no_list.append(test.makeDecision(userId='13612215312',customerId='216684819158107806'))
# serial_no_list.append(test.makeDecision(userId='13612215440',customerId='216684819158108015'))

# serial_no_list.append(test.makeDecision(userId='2149',customerId='2552'))

serial_no_list.append(test.makeDecision(userId='100000480',customerId='100000000000000960'))
print (serial_no_list)