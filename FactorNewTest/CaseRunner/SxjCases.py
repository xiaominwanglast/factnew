#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ProductApi.VIPDecisionAPi import  VIPDecisionApi
env='T2'
test=VIPDecisionApi(env=env,productId='sxj_loan',sceneId='pre_borrow')
field_serialNo_list=[]
serial_no_list=[]
serial_no_list.append(test.makeDecision(userId='223250051',customerId='622440064',borrowCount=1))
# serial_no_list.append(test.makeDecision(userId='100001009',customerId='178906606329659418'))
# serial_no_list.append(test.makeDecision(userId='999877418', customerId='214338958027393294'))

# serial_no_list.append(test.makeDecision(userId='2143523079',customerId='216684819156208595'))
# serial_no_list.append(test.makeDecision(userId='999946476',customerId='214338958027393458'))
# serial_no_list.append(test.makeDecision(userId='2143522779',customerId='216684819156208169'))
# serial_no_list.append(test.makeDecision(userId='3258596243',customerId='214338958027399551'))
#
# serial_no_list.append(test.makeDecision(userId='2143522922',customerId='216684819156208374'))
# serial_no_list.append(test.makeDecision(userId='3258595075',customerId='214338958027397846'))
# serial_no_list.append( test.makeDecision(userId='999944103271', customerId='241143793082960827'))

#TODO T3
# serial_no_list.append(test.makeDecision(userId='101842908',customerId='433919141863241122'))
# serial_no_list.append(test.makeDecision(userId='10001593933',customerId='216684819156209613'))
print serial_no_list