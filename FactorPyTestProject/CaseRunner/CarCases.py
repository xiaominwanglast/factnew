#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ProductApi.CarDecisionApi import CarDecisionApi
env='T1'
test=CarDecisionApi(env=env,productId='CDW',sceneId='pre_approval')
serial_no_list=[]
serial_no_list.append(test.makeDecision(certId='321321199109012916',phone='18301924915',userName=u'王孝敏'))
# serial_no_list.append(test.makeDecision(certId='452702198501041568',phone='13907786977',userName=u'侯佛晓'))
print (serial_no_list)
