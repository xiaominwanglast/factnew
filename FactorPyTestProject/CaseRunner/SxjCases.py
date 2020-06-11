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

