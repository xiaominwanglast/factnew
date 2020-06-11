# -*- coding: UTF-8 -*-
import pymongo,time
from bson.objectid import ObjectId
from utils.Setting import *
from utils.otherUtil import *
from utils.DES import Des
import json
class MongoUntil:
    def __init__(self, env):

        self.mongo_client_lake = pymongo.MongoClient(SETTING[env]['MONGO']['lake'])
        self.mongo_client_skynet = pymongo.MongoClient(SETTING[env]['MONGO']['skynet'])
        self.mongo_client_galaxy = pymongo.MongoClient(SETTING[env]['MONGO']['galaxy'])
        self.mongo_client_xdoor = pymongo.MongoClient(SETTING[env]['MONGO']['skynet-xdoor'])
        self.mongo_client_skynet_feature=pymongo.MongoClient(SETTING[env]['MONGO']['skynet-feature'])
        self.mongo_client_feature_bone = pymongo.MongoClient(SETTING[env]['MONGO']['feature-bone'])
        # self.mongo_rota = pymongo.MongoClient(SETTING[env]['MONGO']['rota'])


        self.db_lake = self.mongo_client_lake['lake']
        self.db_skynet = self.mongo_client_skynet['skynet']
        self.db_galaxy = self.mongo_client_galaxy['galaxy']
        self.db_xdoor = self.mongo_client_xdoor['skynet-xdoor']
        self.db_skynet_feature=self.mongo_client_skynet_feature['skynet-feature']
        self.db_feature_bone = self.mongo_client_feature_bone['feature-bone']
        # self.db_rota = self.mongo_rota['rota']

    def __del__(self):

        self.mongo_client_lake.close()
        self.mongo_client_lake=None

        self.mongo_client_skynet.close()
        self.mongo_client_skynet = None

        self.mongo_client_galaxy.close()
        self.mongo_client_galaxy = None

        self.mongo_client_xdoor.close()
        self.mongo_client_xdoor = None

        self.mongo_client_skynet_feature.close()
        self.mongo_client_skynet_feature=None

        self.mongo_client_feature_bone.close()
        self.mongo_client_feature_bone=None

        # self.mongo_rota.close()
        # self.db_rota=None


    def query_by_user_id(self, db, collection, find):
        collect_lag=collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        ret = []
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret=self.public_get_gzip_data(ret,collect_lag)
        return ret

    def insert_by_user_id(self,db,collection,insertData):
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        try:
            collection.insert_many(insertData)
        except Exception as e:
            print (e)

    def query_by_user_id_sort_bymyself(self, db, collection, find,sort):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        ret = []
        for data in eval("collection.find(find).%s" % sort):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        return ret

    def queryall_by_table(self, db, collection, find):
        collect_lag = collection
        resultall = []
        for i in range(4):
            collection_new = collection.format(i)
            collection_new = eval("self.db_{0}['{1}']".format(db, collection_new))
            for data in collection_new.find(find).sort("_id", -1):
                resultall.append(data)
        resultall = self.public_get_gzip_data(resultall, collect_lag)
        return resultall

    def query_by_user_id_ndays(self, db, collection, find, serial_no, user_id="", days=30):
        collect_lag = collection
        data = self.db_skynet['skynet_user_info']
        if serial_no != "":
            factor = data.find({"serial_no": serial_no}).sort("_id", -1)[0]
        else:
            factor = data.find({"user_id": user_id}).sort("_id", -1)[0]
        date = factor['event_time'] #+ datetime.timedelta(hours=8)
        now_id = ObjectId.from_datetime(date)
        date = date - datetime.timedelta(days=days)
        pre30day = str(date)[0:10]
        pre30day = datetime.datetime.strptime(pre30day, "%Y-%m-%d")
        # print pre30day
        pre30_id = ObjectId.from_datetime(pre30day)
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        ret = []
        find["_id"] = {"$gt": pre30_id, "$lt": now_id}
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        return ret

    def query_by_user_id_30days(self, db, collection, find, serial_no):
        return self.query_by_user_id_ndays(db, collection, find, serial_no, user_id="", days=30)

    def query_by_user_id_180days(self, db, collection, find, serial_no):
        return self.query_by_user_id_ndays(db, collection, find, serial_no, user_id="", days=180)


    def query_by_user_id_ndays_by_create_time(self, db, collection, find, serial_no, user_id="", days=30):
        collect_lag = collection
        data = self.db_skynet['skynet_user_info']
        if serial_no != "":
            factor = data.find({"serial_no": serial_no}).sort("_id", -1)[0]
        else:
            factor = data.find({"user_id": user_id}).sort("_id", -1)[0]
        date = factor['create_time'] + datetime.timedelta(hours=8)
        now_id = ObjectId.from_datetime(date)
        date = date - datetime.timedelta(days=days)
        pre30day = str(date)[0:10]
        pre30day = datetime.datetime.strptime(pre30day, "%Y-%m-%d")
        pre30_id = ObjectId.from_datetime(pre30day)
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        ret = []
        find["_id"] = {"$gt": pre30_id, "$lt": now_id}
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        return ret

    def queryall_by_userId(self, db, collection, find):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        ret = []
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        return ret

    def query_last_by_userId(self, db, collection, find):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        ret=[]
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        return ret[0]

    def query_by_user_id_beforeEventTime(self, db, collection, find, serial_no, user_id=""):
        collect_lag = collection
        data = self.db_skynet['skynet_user_info']
        if serial_no != "":
            factor = data.find({"serial_no": serial_no}).sort("_id", -1)[0]
        else:
            factor = data.find({"user_id": user_id}).sort("_id", -1)[0]
        date = factor['event_time']
        now_id = ObjectId.from_datetime(date)
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        ret = []
        find["_id"] = { "$lt": now_id}
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        return ret

    def query_all_by_userId_beforeEvenTime_inXdays(self,db, collection, find, serial_no,days):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        info = self.db_skynet['skynet_user_info'].find({"serial_no": serial_no}).sort("_id", -1)[0]
        event_time = info['event_time']
        now_id = ObjectId.from_datetime(event_time)
        find["_id"] = {"$lt": now_id}
        start_date = event_time - datetime.timedelta(days=abs(days))
        start_id = ObjectId.from_datetime(start_date)
        ret = []
        find["_id"] = {"$gt": start_id, "$lt": now_id}
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        return ret

    def query_all_by_userId_beforeEvenTimeAdd1min_inXdays(self,db, collection, find, serial_no,days):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        info = self.db_skynet['skynet_user_info'].find({"serial_no": serial_no}).sort("_id", -1)[0]
        event_time = info['event_time']
        now_id = ObjectId.from_datetime(event_time)
        find["_id"] = {"$lt": now_id}
        start_date = event_time - datetime.timedelta(days=days)
        end_date=event_time + datetime.timedelta(seconds=60)
        start_id = ObjectId.from_datetime(start_date)
        end_id=ObjectId.from_datetime(end_date)
        ret = []
        find["_id"] = {"$gt": start_id, "$lt": end_id}
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        return ret

    def query_all_by_userId_inXdays(self,db, collection, find, serial_no,start_days=0,start_time="",end_days=0,end_time='',s_start_id="",s_end_id=""):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        info = self.db_skynet['skynet_user_info'].find({"serial_no": serial_no}).sort("_id", -1)[0]
        event_time = info['event_time']
        now_id = ObjectId.from_datetime(event_time)
        find["_id"] = {"$lt": now_id}
        if len(start_time)==0:
            start_date = event_time - datetime.timedelta(days=start_days)
        else:
            event_time_add8 = event_time- datetime.timedelta(days=start_days) + datetime.timedelta(hours=8)
            start_day = str(event_time_add8)[0:10]+' '+start_time
            start_date_add8 = datetime.datetime.strptime(start_day, "%Y-%m-%d %H:%M:%S")
            start_date = start_date_add8- datetime.timedelta(hours=8)
        if s_start_id:
            start_id=s_start_id
        else:
            start_id = ObjectId.from_datetime(start_date)
        if len(end_time)==0:
            end_date=event_time + datetime.timedelta(days=end_days)
        else:
            event_time_add8= event_time + datetime.timedelta(days=end_days)+ datetime.timedelta(hours=8)
            end_day = str(event_time_add8)[0:10] + ' ' + end_time
            end_date_add8 = datetime.datetime.strptime(end_day, "%Y-%m-%d %H:%M:%S")
            end_date = end_date_add8 - datetime.timedelta(hours=8)
        if s_end_id:
            end_id=s_end_id
        else:
            end_id = ObjectId.from_datetime(end_date)
        ret = []
        find["_id"] = {"$gt": start_id, "$lt": end_id}
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        return ret

    def query_all_by_userId_inOneHour(self,db, collection, find, serial_no):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        info = self.db_skynet['skynet_user_info'].find({"serial_no": serial_no}).sort("_id", -1)[0]
        event_time = info['event_time']
        now_id = ObjectId.from_datetime(event_time)
        find["_id"] = {"$lt": now_id}
        start_day = str(event_time)[0:14]+"00:00"
        start_date = datetime.datetime.strptime(start_day, "%Y-%m-%d %H:%M:%S")
        start_id = ObjectId.from_datetime(start_date)
        end_day = str(event_time)[0:14] + "59:59"
        end_date = datetime.datetime.strptime(end_day, "%Y-%m-%d %H:%M:%S")
        end_id = ObjectId.from_datetime(end_date)
        ret = []
        find["_id"] = {"$gt": start_id, "$lt": end_id}
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        return ret

    def query_all_by_create_time(self,db, collection,find,event_time,days_,start_time_hour="00:00:00"):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        end_time=event_time
        start_time=event_time-datetime.timedelta(days=days_)
        start_time=str(start_time)[0:10]+" "+start_time_hour
        start_time=datetime.datetime.strptime(start_time,"%Y-%m-%d %H:%M:%S")
        # print start_time,end_time
        find['create_time']={"$gt": start_time, "$lt": end_time}
        ret = []
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        return ret

    def query_phone_max5_beforeEvenTime_inXdays(self,db, collection, find, serial_no,days,validTime):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        info = self.db_skynet['skynet_user_info'].find({"serial_no": serial_no}).sort("_id", -1)[0]
        event_time = info['event_time']
        now_id = ObjectId.from_datetime(event_time)
        find["_id"] = {"$lt": now_id}
        start_date = event_time - datetime.timedelta(days=days)
        start_id = ObjectId.from_datetime(start_date)
        ret = []
        find["_id"] = {"$gt": start_id, "$lt": now_id}
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        phoneDic = {}
        if not ret:
            return 'No DATA'
        for everyId in ret:
            for line in everyId['actions']:
                phone = phoneClear(line["callNumber"])
                phone = phone_clean(phone)
                if phone!= None and line.get("callTime")>validTime:
                    if phone not in phoneDic:
                        phoneDic[phone] = [line["callTime"]]
                    else:
                        if line["callTime"] not in phoneDic[phone]:
                            phoneDic[phone].append(line["callTime"])
        temp = []
        for k, v in phoneDic.items():
            temp.append([len(set(v)),max(v),k])
        temp.sort(reverse=True)
        return [str(phone[2]) for phone in temp[:5]]

    def query_app_list_beforeEvenTime_inXdays(self,db, collection, find, serial_no,days):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        info = self.db_skynet['skynet_user_info'].find({"serial_no": serial_no}).sort("_id", -1)[0]
        event_time = info['event_time']
        now_id = ObjectId.from_datetime(event_time)
        find["_id"] = {"$lt": now_id}
        start_date = event_time - datetime.timedelta(days=days)
        start_id = ObjectId.from_datetime(start_date)
        ret = []
        new_ret=[]
        find["_id"] = {"$gt": start_id, "$lt": now_id}
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        if not ret:
            return 'No DATA'
        for data in ret:
            for app in data.get('mobileApp'):
                new_ret.append(app.get('appName'))
        list_app = list(set(new_ret))
        return list_app

    def query_contact_action_list_beforeEvenTime_inXdays(self,db, collection, find, serial_no,days):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        info = self.db_skynet['skynet_user_info'].find({"serial_no": serial_no}).sort("_id", -1)[0]
        event_time = info['event_time']
        now_id = ObjectId.from_datetime(event_time)
        find["_id"] = {"$lt": now_id}
        start_date = event_time - datetime.timedelta(days=days)
        start_id = ObjectId.from_datetime(start_date)
        ret = []
        new_ret=[]
        find["_id"] = {"$gt": start_id, "$lt": now_id}
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        if not ret:
            return 'No DATA'
        for everyId in ret:
            for line in everyId['actions']:
                if line not in new_ret:
                    new_ret.append(line)
        return new_ret

    def query_contact_list_beforeEvenTime_inXdays(self,db, collection, find, serial_no,days,clean=True,allData=True):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        info = self.db_skynet['skynet_user_info'].find({"serial_no": serial_no}).sort("_id", -1)[0]
        event_time = info['event_time']
        now_id = ObjectId.from_datetime(event_time)
        find["_id"] = {"$lt": now_id}
        start_date = event_time - datetime.timedelta(days=days)
        start_id = ObjectId.from_datetime(start_date)
        ret = []
        new_ret=[]
        find["_id"] = {"$gt": start_id, "$lt": now_id}
        if allData:
            for data in collection.find(find).sort("_id", -1):
                ret.append(data)
        else:
            try:
                ret.append(collection.find(find).sort("_id", -1)[0])
            except Exception as e:
                return 'No DATA'
        ret = self.public_get_gzip_data(ret, collect_lag)
        if not ret:
            return 'No DATA'
        for everyId in ret:
            for line in everyId['contacts']:
                if line not in new_ret:
                    new_ret.append(line)
        contact_num_list=[]
        if clean:
            for contact in new_ret:
                phone1 = contact.get('phone1')
                phone2 = contact.get('phone2')
                phone3 = contact.get('phone3')

                phone1 = phoneClear(phone1)
                phone2 = phoneClear(phone2)
                phone3 = phoneClear(phone3)

                phone1 = phone_clean(phone1)
                phone2 = phone_clean(phone2)
                phone3 = phone_clean(phone3)

                if phone1 and phone1 not in contact_num_list: contact_num_list.append(phone1)
                if phone2 and phone2 not in contact_num_list: contact_num_list.append(phone2)
                if phone3 and phone3 not in contact_num_list: contact_num_list.append(phone3)
        else:
            for contact in new_ret:
                phone1 = contact.get('phone1')
                phone2 = contact.get('phone2')
                phone3 = contact.get('phone3')
                if phone1 and phone1 not in contact_num_list: contact_num_list.append(phone1)
                if phone2 and phone2 not in contact_num_list: contact_num_list.append(phone2)
                if phone3 and phone3 not in contact_num_list: contact_num_list.append(phone3)
        return contact_num_list

    def query_sms_list_beforeEvenTime_inXdays(self,db, collection, find, serial_no,days):
        collect_lag = collection
        collection = eval("self.db_{0}['{1}']".format(db, collection))
        info = self.db_skynet['skynet_user_info'].find({"serial_no": serial_no}).sort("_id", -1)[0]
        event_time = info['event_time']
        now_id = ObjectId.from_datetime(event_time)
        find["_id"] = {"$lt": now_id}
        start_date = event_time - datetime.timedelta(days=days)
        start_id = ObjectId.from_datetime(start_date)
        ret = []
        new_ret = []
        find["_id"] = {"$gt": start_id, "$lt": now_id}
        for data in collection.find(find).sort("_id", -1):
            ret.append(data)
        ret = self.public_get_gzip_data(ret, collect_lag)
        if not ret:
            return 'No DATA'
        for row in ret:
            for sub_row in row.get('mobileSms'):
                if sub_row not in new_ret:
                    new_ret.append(sub_row)
        return new_ret

    def public_get_gzip_data(self,dataList,collection):
        """手机用户通讯录、手机用户通话记录、手机用户短信、手机ppList"""
        new_dataList=[]
        for data in dataList:
            if 's_user_mobile_sms_list' in collection:
                if data.get('is_gzip') and data.get('is_gzip') == 1:
                    if data.get('content'):
                        dump=Des().unGzip(data.get('content'))
                        if isinstance(dump,str) or isinstance(dump,unicode):
                            dump=json.loads(dump)
                        data['mobileSms']=dump
                        del data['is_gzip']
                        del data['content']
                    else:
                        data['mobileSms'] = {}
                        del data['is_gzip']
                    new_dataList.append(data)
                else:
                    new_dataList.append(data)
            if 's_user_mobile_app_list' in collection:
                if data.get('is_gzip') and data.get('is_gzip') == 1:
                    if data.get('content'):
                        dump=Des().unGzip(data.get('content'))
                        if isinstance(dump,str) or isinstance(dump,unicode):
                            dump=json.loads(dump)
                        data['mobileApp']=dump
                        del data['is_gzip']
                        del data['content']
                    else:
                        data['mobileApp'] ={}
                        del data['is_gzip']
                    new_dataList.append(data)
                else:
                    new_dataList.append(data)
            if 's_user_mobile_contact' in collection and '_action' not in collection:
                if data.get('is_gzip') and data.get('is_gzip') == 1:
                    if data.get('content'):
                        dump=Des().unGzip(data.get('content'))
                        if isinstance(dump,str) or isinstance(dump,unicode):
                            dump=json.loads(dump)
                        data['contacts']=dump
                        del data['is_gzip']
                        del data['content']
                    else:
                        data['contacts'] = {}
                        del data['is_gzip']
                    new_dataList.append(data)
                else:
                    new_dataList.append(data)
            if 's_user_mobile_contact_action' in collection:
                if data.get('is_gzip') and data.get('is_gzip') == 1:
                    if data.get('content'):
                        dump=Des().unGzip(data.get('content'))
                        if isinstance(dump,str) or isinstance(dump,unicode):
                            dump=json.loads(dump)
                        data['actions']=dump
                        del data['is_gzip']
                        del data['content']
                        for action in dump:
                            if isinstance(action.get('callTime'), long):
                                action['callTime'] = datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(action.get('callTime') / 1000)),'%Y-%m-%d %H:%M:%S')
                    else:
                        data['actions'] = {}
                        del data['is_gzip']
                    new_dataList.append(data)
                else:
                    new_dataList.append(data)
            if collection in ["mx_alipay_bills_data", "mx_alipay_report", "mx_carrier_bills_notify","mx_carrier_report_notify", "mx_carrier_smses", "mx_carrier_nets","","mx_email_bills","mx_email_report"]:
                if data.get('is_gzip') and data.get('is_gzip') == 1:
                    if data.get('content'):
                        dump = Des().unGzip(data.get('content'))
                        if isinstance(dump,str) or isinstance(dump,unicode):
                            dump=json.loads(dump)
                        data["response"]=dump
                        del data['is_gzip']
                        del data['content']
                    else:
                        data['response'] = {}
                        del data['is_gzip']
                    new_dataList.append(data)
                else:
                    new_dataList.append(data)
            if "mx_carrier_calls" in collection:
                if data.get('is_gzip') and data.get('is_gzip') == 1:
                    if data.get('content'):
                        dump = Des().unGzip(data.get('content'))
                        if isinstance(dump,str) or isinstance(dump,unicode):
                            dump=json.loads(dump)
                        data["items"]=dump
                        del data['is_gzip']
                        del data['content']
                    else:
                        data['items'] = {}
                        del data['is_gzip']
                    new_dataList.append(data)
                else:
                    new_dataList.append(data)

            else:
                if data not in new_dataList:
                    new_dataList.append(data)
        return new_dataList

    def id2time(self,object_id):
        result=datetime.datetime.fromtimestamp(time.mktime(object_id.generation_time.timetuple()))+datetime.timedelta(hours=8)
        return result

if __name__=="__main__":

    pass