#coding:utf-8
import requests
import json
class DecisionApi(object):
    def __init__(self,env,productId,sceneId):
        """
        :param env: 环境变量
        :param productId: product_code 产品代号
        :param sceneId: 决策环节
        """
        self.env=env
        self.productId=productId
        self.sceneId=sceneId

        self.headers = {'content-type': 'application/x-www-form-urlencoded', 'Cache-Control': 'no-cache'}
        self.host=self.getHost

    @property
    def getHost(self,host=''):
        if self.env=='T1':
            host= "172.16.0.141"
        if self.env=='T2':
            host = "172.16.0.143"
        if self.env=='T3':
            host = "172.16.0.145"
        if self.env=='Online':
            host= "riskdaikuan.2345.com"
        return host

    def makeDecision(self):
        """请求风控接口"""
        pass

    def getDecisionResult(self,serial_no):
        """
        :param serial_no: 获取风控结果的serial_no
        :return:
        """
        apply_data = {"productId":self.productId,"sceneId":self.sceneId,"serialNo":serial_no}
        if self.env=='Online':
            rq =requests.post(url='https://'+self.host+'/skynet-bridge/bridge/getDecisionResult',data=apply_data,headers=self.headers)
        else:
            rq = requests.post(url='http://{0}:5003/skynet-bridge/bridge/getDecisionResult'.format(self.host),data=apply_data,headers=self.headers)
        return json.dumps(rq.json(),indent=4,ensure_ascii=False)


