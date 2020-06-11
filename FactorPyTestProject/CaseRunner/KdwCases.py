#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
from ProductApi.VIPDecisionAPi import  VIPDecisionApi

env='T3'
test=VIPDecisionApi(env=env,productId='kdw_loan',sceneId='credit')
field_serialNo_list=[]
serial_no_list=[]
# serial_no_list.append(test.makeDecision(userId='3258596405',customerId='214338958027399861'))
# serial_no_list.append(test.makeDecision(userId='2143522920',customerId='2166848191562083712'))
#
# serial_no_list.append(test.makeDecision(userId='3258597315',customerId='214338958027401550'))
# serial_no_list.append(test.makeDecision(userId='100005988',customerId='168757185663208323'))
# serial_no_list.append(test.makeDecision(userId='3258595618',customerId='214338958027399693'))
# serial_no_list.append(test.makeDecision(userId='999877418', customerId='214338958027393294'))
# serial_no_list.append(test.makeDecision(userId='3258596023',customerId='214338958027399140'))
# serial_no_list.append(test.makeDecision(userId='3258595994',customerId='214338958027399081'))
# serial_no_list.append(test.makeDecision(userId='3258595599',customerId='214338958027398611'))

#todo T3
serial_no_list.append(test.makeDecision(userId='1800250019',customerId='433919141863241167'))


print serial_no_list