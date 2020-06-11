#coding:utf-8
import requests
from ProductApi.Property.DecisionApi import DecisionApi
class CarDecisionApi(DecisionApi):
    def __init__(self,env,productId,sceneId):
        super(CarDecisionApi,self).__init__(env,productId,sceneId)

    def makeDecision(self,certId='',phone='',userName=''):
        """
        车贷王(三要素)
        :param certId:身份证编码
        :param phone: 手机号
        :param userName: 用户名
        :return:
        """
        if self.env=='Online':
            rq = requests.post('https://'+self.host+'/skynet-bridge/bridge/makeDecision',
                          data={"certId":certId,"phone":phone,"productId":self.productId,"sceneId":self.sceneId,"userName":userName,},headers=self.headers)
        else:
            rq = requests.post('http://'+self.host+':5003/skynet-bridge/bridge/makeDecision',
                          data={"certId":certId,"phone":phone,"productId":self.productId,"sceneId":self.sceneId,"userName":userName,},headers=self.headers)
        if rq.status_code == 200:
            if rq.json().get('serialNo'):
                return rq.json().get('serialNo')
            else:
                print rq.json().get('message')
                return
        else:
            print rq.json()
            return

if __name__ == '__main__':
    env='Online'
    test=CarDecisionApi(env='Online',productId='CDW',sceneId='pre_approval')
    print test.getDecisionResult('1554173266024-88F229952BEBD44E83E4D4924A177048')
