# -*- coding: utf-8 -*-
import requests
from ProductApi.Property.DecisionApi import DecisionApi
from ProductApi.Property.NewDecisionProperty import NewDecisionProperty

class VIPDecisionApi(DecisionApi,NewDecisionProperty):
    def __init__(self, env, productId, sceneId):
        DecisionApi.__init__(self, env, productId, sceneId)
        NewDecisionProperty.__init__(self)

    def makeDecision(self,userId='',customerId='',borrowCount='',orderId='',billId='',extraDataStatus='',previousSerialNo='',extraData='',terminalType='',channelCode=''):
        """
        :param userId: 用户user_id（必传字段）
        :param customerId:用户customer_id(必传字段)
        :param borrowCount:借款次数
        :param orderId:订单号-re_credit提额接口使用
        :param billId:交易号-re_credit提额接口使用
        :param extraDataStatus:
        :param previousSerialNo:
        :param extraData:
        :param termialType:第三方类型
        :param channelCode: 渠道号
        :return:
        """
        IfNotExits = lambda Null, real: real if not Null else Null
        borrowCount=IfNotExits(borrowCount,self.borrowCount)
        orderId=IfNotExits(orderId,self.get_orderId)
        billId=IfNotExits(billId,self.get_billId)
        extraDataStatus = IfNotExits(extraDataStatus, self.extraDataStatus)
        previousSerialNo = IfNotExits(previousSerialNo, self.previousSerialNo)
        terminalType =IfNotExits(terminalType,self.terminalType)
        channelCode =IfNotExits(channelCode,self.channelCode)

        if self.sceneId=='credit':
            #TODO 首借测额环节
            data={"productId":self.productId,"sceneId":self.sceneId,"userId":userId,"customerId":customerId,"applyId":self.applyId,"applyTime":self.applyTime,"applyStatusId":self.applyStatusId,"terminalType":terminalType,"channelCode":channelCode}
        elif self.sceneId=='extra_credit':
            #TODO 二次进件环节
            data={"productId":self.productId,"sceneId":self.sceneId,"userId":userId,"customerId":customerId,"applyId":self.applyId,"applyTime":self.applyTime,
                  "extraDataStatus":extraDataStatus,"previousSerialNo":previousSerialNo,"extraData":extraData,"applyStatusId":self.applyStatusId}
        elif self.sceneId=='pre_borrow':
            #TODO borrow=0 首借测费环节(获取会员价)
            #TODO borrow>=1 复借环节
            data = {"productId": self.productId,"sceneId": self.sceneId,"userId": userId,"customerId": customerId,"borrowCount": borrowCount,"terminalType":terminalType,"channelCode":channelCode}
        elif self.sceneId=='transaction_antifraud':
            #TODO 交易反欺诈 借款环节
            data = {"productId": self.productId,"sceneId": self.sceneId,"userId": userId,"customerId": customerId,"borrowId":self.applyId,"borrowTime":self.applyTime}
        elif self.sceneId=='re_credit':
            #TODO 提额环节
            data = {"productId": self.productId,"sceneId": self.sceneId,"userId": userId,"customerId": customerId,"orderId":orderId,"billId":billId,"repaymentTime":self.repaymentTime}
        else:
            print (u'数据为空，无此阶段数据！')
            data={}
        headers = {'content-type': 'application/x-www-form-urlencoded','Cache-Control': 'no-cache'}
        rq = requests.post('http://{0}:5003/skynet-bridge/bridge/makeDecision'.format(self.host),data=data,headers=headers)
        if rq.status_code == 200:
            if rq.json().get('serialNo'):
                return (rq.json().get('serialNo'))
            else:
                print (rq.json().get('message'))
                return
        else:
            print (rq.text)
            print (rq.json())
            return

if __name__=="__main__":
    test=VIPDecisionApi(env='T1',productId='vip_loan',sceneId='credit')
    print (test.makeDecision(userId='12653370305',customerId='216684819158099751'))
    # print test.getDecisionResult('1539054151731-58B9D4485C21590C0007F5D9C138C33A')