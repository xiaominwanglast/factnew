#coding:utf-8
from ProductApi.VIPDecisionAPi import  VIPDecisionApi
env='T1'
test=VIPDecisionApi(env=env,productId='ql_loan',sceneId='credit')
serial_no_list=[]

# serial_no_list.append(test.makeDecision(userId='13612215127',customerId='216684819158107474'))
# serial_no_list.append(test.makeDecision(userId='13612215287',customerId='216684819158107762'))
# serial_no_list.append(test.makeDecision(userId='13612215312',customerId='216684819158107806'))
# serial_no_list.append(test.makeDecision(userId='13612215440',customerId='216684819158108015'))

serial_no_list.append(test.makeDecision(userId='100000474',customerId='100000000000000947'))
# serial_no_list.append(test.makeDecision(userId='184928794',customerId='100000001743099133'))
print (serial_no_list)