#coding:utf-8
import pymongo
from Setting import SETTING
from bson.objectid import ObjectId
import datetime
class mongodbSkynetUntil:
    def __init__(self, env,db,collection):
        self.mongodb_client_skynet = pymongo.MongoClient(SETTING[env]['MONGO'][db])
        self.db_skynet = self.mongodb_client_skynet['skynet']
        self.collection=collection
        self.db=db
    def __del__(self):
        self.mongodb_client_skynet.close()
        print "["+str(datetime.datetime.now())[:19]+"]"+self.db+" 已关闭"

    def query(self,find):
        print "["+str(datetime.datetime.now())[:19]+"]"+self.db+" 正查询数据"
        try:
            return self.db_skynet[self.collection].find(find)
        except Exception as e:
            print e
            return []



if __name__=="__main__":
    result=mongodbSkynetUntil(env='Online',db='skynet_5084',collection='skynet_decision_result').query(find={"_id":{"$gte":ObjectId("5c8492c80000000000000000"),"$lt":ObjectId("5c84aee80000000000000000")}})