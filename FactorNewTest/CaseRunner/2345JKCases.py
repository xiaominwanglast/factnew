#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ProductApi.JKDecisionAPI import  JKDecisionAPI
env='T1'
test=JKDecisionAPI(env=env,productId='jk_loan',sceneId='credit')
field_serialNo_list=[]
serial_no_list=[]
# serial_no_list.append(test.makeDecision(userId='13612220810',customerId='216684819158104231'))
# serial_no_list.append(test.makeDecision(userId='100001009',customerId='178906606329659418'))
# serial_no_list.append(test.makeDecision(userId='999877418', customerId='214338958027393294'))

# serial_no_list.append(test.makeDecision(userId='2143523079',customerId='216684819156208595'))
# serial_no_list.append(test.makeDecision(userId='999946476',customerId='214338958027393458'))
# serial_no_list.append(test.makeDecision(userId='2143522779',customerId='216684819156208169'))
# serial_no_list.append(test.makeDecision(userId='3258596243',customerId='214338958027399551'))

# serial_no_list.append(test.makeDecision(userId='300',customerId='300'))
# serial_no_list.append(test.makeDecision(userId='3258595075',customerId='214338958027397846'))
# serial_no_list.append( test.makeDecision(userId='999944103271', customerId='241143793082960827'))

#TODO T1
serial_no_list.append(test.makeDecision(userId='300',customerId='300',orcChangeFlag='0'))
# serial_no_list.append(test.makeDecision(userId='10001593933',customerId='216684819156209613'))
print serial_no_list