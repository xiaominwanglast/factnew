#coding:utf-8
from ProductApi.CarDecisionApiAuto import CarDecisionApiAuto
test = CarDecisionApiAuto(env='T1', productId='CDW', sceneId='transaction_approval')
print (test.makeDecisionTransaction(vehicleIdNumber='fwaf1111111111111', certId='371312198808046937',phone='13355495678', userName='王立吉'))