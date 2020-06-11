#coding:utf-8
import pymongo
from Setting import SETTING
import datetime
class mongodbGalaxyUntil:
    def __init__(self, env,db,collection):
        self.mongodb_client_galaxy = pymongo.MongoClient(SETTING[env]['MONGO'][db])
        self.db_galaxy = self.mongodb_client_galaxy['galaxy']
        self.collection=collection
        self.db=db
    def __del__(self):
        self.mongodb_client_galaxy.close()
        print "["+str(datetime.datetime.now())[:19]+"]"+self.db+" 已关闭"

    def query(self,find):
        print "["+str(datetime.datetime.now())[:19]+"]"+self.db+" 正查询数据"
        try:
            return self.db_galaxy[self.collection].find(find)
        except Exception as e:
            print e
            return []