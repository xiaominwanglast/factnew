#coding:utf-8
from contact.localMysql import MysqlUntil
from contact.onlineGalaxy import mongodbGalaxyUntil
from contact.onlineLake import mongodbLakeUntil
from contact.onlineSkynet import mongodbSkynetUntil
from bson.objectid import ObjectId
import datetime
class onlineCheck(object):
    def __init__(self,env,product,startTime,endTime,step=30):
        """
        :param env: 环境
        :param mongodbSelect:mongodb数据库【skynet,lake,galaxy】
        :param startTime: 开始时间 【样式："2019-02-20 16:16:01"】
        :param endTime: 结束时间 【样式："2019-02-20 17:16:01"】
        :param step: 时间间隔，默认10分钟，单位分钟
        """
        self.env=env
        self.product=product
        self.startTime=datetime.datetime.strptime(startTime,"%Y-%m-%d %H:%M:%S")
        self.endTime=datetime.datetime.strptime(endTime,"%Y-%m-%d %H:%M:%S")
        self.step=step
        self.startObjectId=ObjectId.from_datetime(self.startTime)
        self.endObjectId=ObjectId.from_datetime(self.endTime)

    def get_skynet_data(self):
        result_all=[]
        result_5084 = mongodbSkynetUntil(env=self.env, db='skynet_5084', collection='skynet_decision_result').query(find={"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5085 = mongodbSkynetUntil(env=self.env, db='skynet_5085', collection='skynet_decision_result').query(find={"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5086 = mongodbSkynetUntil(env=self.env, db='skynet_5086', collection='skynet_decision_result').query(find={"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        [result_all.append(port) for port in result_5084]
        [result_all.append(port) for port in result_5085]
        [result_all.append(port) for port in result_5086]
        boolean=True
        while boolean:
            tempTime = self.startTime+ datetime.timedelta(minutes=self.step)
            credit_000=credit_001=credit_002=preBorrow_000=preBorrow_001=preBorrow_002=transaction_000=transaction_001=transaction_002=0
            if tempTime<self.endTime:
                tempData=[port for port in result_all if ObjectId.from_datetime(self.startTime)<=port.get("_id")<ObjectId.from_datetime(tempTime)]
                for temp in tempData:
                    if temp.get('scene_code')=="credit" and temp.get('product_code')==self.product and temp.get("status")=="SUCCESS":
                        if temp.get("data").get("decisionResult")=="000":
                            credit_000+=1
                        if temp.get("data").get("decisionResult")=="001":
                            credit_001+=1
                        if temp.get("data").get("decisionResult")=="002":
                            credit_002+=1
                    if temp.get('scene_code')=="pre_borrow" and temp.get('product_code')==self.product and temp.get("status")=="SUCCESS":
                        if temp.get("data").get("decisionResult")=="000":
                            preBorrow_000+=1
                        if temp.get("data").get("decisionResult")=="001":
                            preBorrow_001+=1
                        if temp.get("data").get("decisionResult")=="002":
                            preBorrow_002+=1
                    if temp.get('scene_code')=="transaction_antifraud" and temp.get('product_code')==self.product and temp.get("status")=="SUCCESS":
                        if temp.get("data").get("decisionResult")=="000":
                            transaction_000+=1
                        if temp.get("data").get("decisionResult")=="001":
                            transaction_001+=1
                        if temp.get("data").get("decisionResult")=="002":
                            transaction_002+=1
                MysqlUntil(env='local').insert_skynet_data(product_code=self.product,
                                                           time_over="["+str(self.startTime+datetime.timedelta(hours=8))+"]-["+str(tempTime+datetime.timedelta(hours=8))+"]",
                                                           scene_code='credit', decision_000_count=credit_000,
                                                           decision_001_count=credit_001, decision_002_count=credit_002)
                MysqlUntil(env='local').insert_skynet_data(product_code=self.product,
                                                           time_over="["+str(self.startTime+datetime.timedelta(hours=8))+"]-["+str(tempTime+datetime.timedelta(hours=8))+"]",
                                                           scene_code='pre_borrow', decision_000_count=preBorrow_000,
                                                           decision_001_count=preBorrow_001, decision_002_count=preBorrow_002)
                MysqlUntil(env='local').insert_skynet_data(product_code=self.product,
                                                           time_over="["+str(self.startTime+datetime.timedelta(hours=8))+"]-["+str(tempTime+datetime.timedelta(hours=8))+"]",
                                                           scene_code='transaction_antifraud', decision_000_count=transaction_000,
                                                           decision_001_count=transaction_001, decision_002_count=transaction_002)
                print "["+str(datetime.datetime.now())[:19]+"]"+str(self.startTime),'-',str(tempTime),u"数据处理完毕"
                self.startTime=tempTime
            else:
                boolean=False

    def get_galaxy_data(self):
        result_5084_bairong_record=mongodbGalaxyUntil(env=self.env,db='galaxy_5084',collection='bairong_record').query({"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_bd_score_record=mongodbGalaxyUntil(env=self.env,db='galaxy_5084',collection='bd_score_record').query({"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_bj_black_record=mongodbGalaxyUntil(env=self.env,db='galaxy_5084',collection='bj_black_record').query({"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_bj_hy_record=mongodbGalaxyUntil(env=self.env,db='galaxy_5084',collection='bj_hy_record').query({"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_bj_score_record=mongodbGalaxyUntil(env=self.env,db='galaxy_5084',collection='bj_score_record').query({"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_bjtz_score_record=mongodbGalaxyUntil(env=self.env,db='galaxy_5084',collection='bjtz_score_record').query({"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_bqs_record=mongodbGalaxyUntil(env=self.env,db='galaxy_5084',collection='bqs_record').query({"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_br_new_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='br_new_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_csec_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='csec_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_geo_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='geo_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_huifa_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='huifa_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_mx_alipay_bills_data = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='mx_alipay_bills_data').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_mx_alipay_report = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='mx_alipay_report').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_mx_carrier_calls = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='mx_carrier_calls').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_mx_carrier_report_notify = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='mx_carrier_report_notify').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_mx_carrier_report = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='mx_carrier_report').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_mx_carrier_task_submit = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='mx_carrier_task_submit').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_own_black_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='own_black_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_py_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='py_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_qhcs_msc8262_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='qhcs_msc8262_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_td_guard_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='td_guard_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_td_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='td_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_tz_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='tz_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_udsp_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='udsp_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_xy_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='xy_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_yf_pfv_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='yf_pfv_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_yf_score_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='yf_score_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_zm_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='zm_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_zzc_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='zzc_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        result_5084_zzc_score_record = mongodbGalaxyUntil(env=self.env, db='galaxy_5084',collection='zzc_score_record').query({"_id": {"$gte": self.startObjectId, "$lt": self.endObjectId}})
        if not result_5084_bairong_record:
            print u'galaxy_bairong_record 无数据进入'
        if not result_5084_bd_score_record:
            print u'galaxy_bd_score_record 无数据进入'
        if not result_5084_bj_black_record:
            print u"galaxy_bj_black_record 无数据进入"
        if not result_5084_bj_hy_record:
            print u"galaxy_bj_hy_record 无数据进入"
        if not result_5084_bj_score_record:
            print u"galaxy_bj_score_record 无数据进入"
        if not result_5084_bjtz_score_record:
            print u"galaxy_bjtz_score_record 无数据进入"
        if not result_5084_bqs_record:
            print u"galaxy_bqs_record 无数据进入"
        if not result_5084_br_new_record:
            print u"galaxy_br_new_record 无数据进入"
        if not result_5084_csec_record:
            print u"galaxy_csec_record 无数据进入"
        if not result_5084_geo_record:
            print u"galaxy_geo_record 无数据进入"
        if not result_5084_huifa_record:
            print u"galaxy_huifa_record 无数据进入"
        if not result_5084_mx_alipay_bills_data:
            print u"galaxy_mx_alipay_bills_data 无数据进入"
        if not result_5084_mx_alipay_report:
            print u"galaxy_mx_alipay_report 无数据进入"
        if not result_5084_mx_carrier_calls:
            print u"galaxy_mx_carrier_calls 无数据进入"
        if not result_5084_mx_carrier_report_notify:
            print u"galaxy_mx_carrier_report_notify 无数据进入"
        if not result_5084_mx_carrier_report:
            print u"galaxy_mx_carrier_report 无数据进入"
        if not result_5084_mx_carrier_task_submit:
            print u"galaxy_mx_carrier_task_submit 无数据进入"
        if not result_5084_own_black_record:
            print u"galaxy_own_black_record 无数据进入"
        if not result_5084_py_record:
            print u"galaxy_py_record 无数据进入"
        if not result_5084_qhcs_msc8262_record:
            print u"galaxy_qhcs_msc8262_record 无数据进入"
        if not result_5084_td_guard_record:
            print u"galaxy_td_guard_record 无数据进入"
        if not result_5084_td_record:
            print u"galaxy_td_record 无数据进入"
        if not result_5084_udsp_record:
            print u"galaxy_udsp_record 无数据进入"
        if not result_5084_tz_record:
            print u"galaxy_tz_record 无数据进入"
        if not result_5084_xy_record:
            print u"galaxy_xy_record 无数据进入"
        if not result_5084_yf_pfv_record:
            print u"galaxy_yf_pfv_record 无数据进入"
        if not result_5084_yf_score_record:
            print u"galaxy_yf_score_record 无数据进入"
        if not result_5084_zm_record:
            print u"galaxy_zm_record 无数据进入"
        if not result_5084_zzc_record:
            print u"galaxy_zzc_record 无数据进入"
        if not result_5084_zzc_score_record:
            print u"galaxy_zzc_score_record 无数据进入"

    def get_lake_data(self):
        result_5084_album = mongodbLakeUntil(env=self.env, db='lake_5084', collection='s_user_mobile_album_0').query(find={"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_app_list = mongodbLakeUntil(env=self.env, db='lake_5084', collection='s_user_mobile_app_list_0').query(find={"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_behavior = mongodbLakeUntil(env=self.env, db='lake_5084', collection='s_user_mobile_behavior_0').query(find={"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_contact = mongodbLakeUntil(env=self.env, db='lake_5084', collection='s_user_mobile_contact_0').query(find={"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_contact_action = mongodbLakeUntil(env=self.env, db='lake_5084', collection='s_user_mobile_contact_action_0').query(find={"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_device_info = mongodbLakeUntil(env=self.env, db='lake_5084', collection='s_user_mobile_device_info_0').query(find={"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        result_5084_sms_list= mongodbLakeUntil(env=self.env, db='lake_5084', collection='s_user_mobile_sms_list_0').query(find={"_id": {"$gte": self.startObjectId, "$lt":self.endObjectId}})
        if result_5084_album:
            print u'lake_album有数据进入'
        if result_5084_app_list:
            print u'lake_AppList有数据进入'
        if result_5084_behavior:
            print u'lake_behavior有数据进入'
        if result_5084_contact:
            print u'lake_contact有数据进入'
        if result_5084_contact_action:
            print u'lake_contact_action有数据进入'
        if result_5084_device_info:
            print u'lake_device_info有数据进入'
        if result_5084_sms_list:
            print u'lake_sms有数据进入'

if __name__=="__main__":
    onlineCheck(env="Online",product='ql_loan',startTime="2019-04-06 06:00:00",endTime="2019-04-06 09:00:00").get_skynet_data()
    # onlineCheck(env="Online",product='vip_loan',startTime="2019-04-02 10:50:00",endTime="2019-04-01 10:55:00").get_galaxy_data()

