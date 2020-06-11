# -*- coding: utf-8 -*-
import requests
import hashlib
import json
from ProductApi.Property.DecisionApi import DecisionApi
from ProductApi.Property.CarDecisionProperty import CarDecisionProperty

class CarDecisionApiAuto(DecisionApi,CarDecisionProperty):
    def __init__(self, env, productId, sceneId):
        DecisionApi.__init__(self,env, productId, sceneId)
        CarDecisionProperty.__init__(self)
        if self.env=='Online':
            self.salt="q>5Nw8pd"
        else:
            self.salt="cpo8%osM"

    def makeDecision(self, certId='', phone='', userName='', bankcardNo='', registerLocation='', agentName=''):
        """
        :param certId: 身份证号  (必传字段)
        :param phone: 手机号  (必传字段)
        :param userName: 用户名  (必传字段)
        :param bankcardNo: 银行卡号
        :param registerLocation: 注册地址
        :param agentName: 注册商
        :return:
        """
        IfIsInstance = lambda Info: Info if not isinstance(Info, unicode) else Info.encode('utf-8')
        userName=IfIsInstance(userName)
        czcbGeneralRiskResult=IfIsInstance(self.czcbGeneralRiskResult)
        czcbDebtRiskResult=IfIsInstance(self.czcbDebtRiskResult)
        czcbOverdueRiskResult=IfIsInstance(self.czcbOverdueRiskResult)

        if not bankcardNo:
            bankcardNo = self.bankcardNo
        if not registerLocation:
            registerLocation = self.registerLocation
        if not agentName:
            agentName = self.agentName

        # TODO 不加回调函数的请求参数
        apply_data = {"certId": certId, "phone": phone, "productId": self.productId, "sceneId": self.sceneId,
                      "userName": userName,
                      "applyId": self.applyId, "applyTime": self.applyTime, "loanProduct": self.loanProduct,
                      "loanAmount": self.loanAmount, "loanTerm": self.loanTerm, "vehicleType": self.vehicleType,
                      "age": self.age, "registerLocation": registerLocation, "gender": self.gender,
                      "maritalStatus": self.maritalStatus, "agentName": agentName,
                      "czcbGeneralScore": self.czcbGeneralScore, "czcbDebtScore": self.czcbDebtScore,
                      "czcbOverdueScore": self.czcbOverdueScore, "bankcardNo": bankcardNo,
                      "czcbGeneralRiskResult":czcbGeneralRiskResult,"czcbDebtRiskResult":czcbDebtRiskResult,
                      "czcbOverdueRiskResult":czcbOverdueRiskResult,"czcbRiskNote":self.czcbRiskNote,
                      "outOfAuthorizedDistrict":self.outOfAuthorizedDistrict,"idCardAppearCount":self.idCardAppearCount,
                      "idCardExpired":self.idCardExpired,"isLcv":self.isLcv,"pbocInfo":self.pbocInfo,"pbocResult":self.pbocResult,
                      "guarantorIdNumber":self.guarantorIdNumber,"spouseIdNumber":self.spouseIdNumber,"noRelationContactCnt":self.noRelationContactCnt,
                      "netPrice":self.netPrice,"guarantorPhone":self.guarantorPhone,"greenChannel":self.greenChannel,"pbocReason":self.pbocReason,
                      "hasSpouse":self.hasSpouse,"hasGuarantor":self.hasGuarantor,"spousePhone":self.spousePhone,"spouseName":self.spouseName,
                      "guarantorName":self.guarantorName,"familyProvince":self.familyProvince,"familyCity":self.familyCity,"homeProvince":self.homeProvince,
                      "homeCity":self.homeCity,"workProvince":self.workProvince,"workCity":self.workCity,"dealerName":self.dealerName,"rejectCode":self.rejectCode,
                      "pbocWhite":self.pbocWhite}
        # TODO 不加回调函数
        requestSign=""
        applykeys=apply_data.keys()
        applykeys.sort()
        for key in applykeys:
            requestSign=requestSign+str(key)+'='+str(apply_data.get(key))+'&'
        requestSign=requestSign+self.salt

        m = hashlib.md5()
        m.update(requestSign)
        header_sign = m.hexdigest()
        headers = {'content-type': 'application/x-www-form-urlencoded', 'sign': header_sign.upper()}
        if self.env=='Online':
            r = requests.post(url='https://{0}/skynet-bridge/bridge/makeDecision'.format(self.host), data=apply_data,
                          headers=headers)
        else:
            r = requests.post(url='http://{0}:5003/skynet-bridge/bridge/makeDecision'.format(self.host), data=apply_data,
                          headers=headers)
        if r.status_code == 200:
            if r.json().get('serialNo'):
                return r.json().get('serialNo')
            else:
                print r.json().get('message')
                return
        else:
            print r.json()
            return

    def makeDecisionTransaction(self,vehicleIdNumber='', certId='', phone='', userName=''):
        data={"certId": certId, "phone": phone, "productId": self.productId, "sceneId": self.sceneId,"userName": userName,"applyId": self.applyId, "applyTime": self.applyTime,"vehicleIdNumber":vehicleIdNumber}

        if self.env=='Online':
            rq= requests.post(url='https://{0}/skynet-bridge/bridge/makeDecision'.format(self.host), data=data,headers=self.headers)
        else:
            rq = requests.post('http://{0}:5003/skynet-bridge/bridge/makeDecision'.format(self.host),data=data,headers=self.headers)
        if rq.status_code == 200:
            if rq.json().get('serialNo'):
                return rq.json().get('serialNo')
            else:
                print rq.json().get('message')
                return
        else:
            print rq.text
            print rq.json()
            return

    def getDecisionResult(self, serial_no):
        """
        :param serial_no: 获取风控结果的serial_no
        :return:
        """
        requestSign = "productId={0}&sceneId={1}&serialNo={2}&".format(self.productId, self.sceneId,
                                                                       serial_no) + self.salt
        m = hashlib.md5()
        m.update(requestSign)
        header_sign = m.hexdigest()
        headers = {'content-type': 'application/x-www-form-urlencoded', 'sign': header_sign.upper()}
        if self.env=='Online':
            rq = requests.post(url='https://'+self.host+'/skynet-bridge/bridge/getDecisionResult',
                           data={"productId": self.productId, "sceneId": self.sceneId, "serialNo": serial_no},
                           headers=headers)
        else:
            rq = requests.post(url='http://{0}:5003/skynet-bridge/bridge/getDecisionResult'.format(self.host),
                           data={"productId": self.productId, "sceneId": self.sceneId, "serialNo": serial_no},
                           headers=headers)
        return json.dumps(rq.json(), indent=4, ensure_ascii=False)

if __name__ == '__main__':
    env = 'T1'
    test = CarDecisionApiAuto(env='T1', productId='CDW', sceneId='transaction_approval')
    print test.makeDecisionTransaction(vehicleIdNumber='fwaf1111111111111',certId='371312198808046937', phone='13355495678', userName='王立吉')
    # print test.makeDecision(certId='371312198808046937', phone='13355495678', userName='王立吉')
    # print test.getDecisionResult('1537322032425-70C6CF89F19647F96569B613708BF5E4')
