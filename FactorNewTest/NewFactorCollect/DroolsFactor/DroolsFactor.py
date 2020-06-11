#coding:utf-8
import datetime,time
from FrameRunner.FactorInit import NewFactorInit
from utils.InfoHelper import *
from bson.objectid import ObjectId
from utils.otherUtil import *

class DroolsFactor(NewFactorInit):
    def __init__(self, env, serial_no):
        super(DroolsFactor,self).__init__(env, serial_no)

    def __pre_drools_result(self,user_id):
        drools_dict={}
        drools_dict["ljd_count"]=[]
        drools_dict["sxj_count"]=[]
        drools_dict["kdw_count"]=[]
        drools_dict["cjk_count"]=[]
        drools_dict["hjk_count"]=[]
        drools_dict["ljd_night_count"] = []
        drools_dict["sxj_night_count"] = []
        drools_dict["kdw_night_count"] = []
        drools_dict["cjk_night_count"] = []
        drools_dict["hjk_night_count"] = []
        drools_dict["ljd_pre_borrow_count"] = []
        drools_dict["sxj_pre_borrow_count"] = []
        drools_dict["kdw_pre_borrow_count"] = []
        drools_dict["cjk_pre_borrow_count"] = []
        drools_dict["hjk_pre_borrow_count"] = []
        drools_dict["ljd_refuse_count"] = []
        drools_dict["sxj_refuse_count"] = []
        drools_dict["kdw_refuse_count"] = []
        drools_dict["cjk_refuse_count"] = []
        drools_dict["hjk_refuse_count"] = []
        drools_dict["ljd_first_credit_time"] = []
        drools_dict["sxj_first_credit_time"] = []
        drools_dict["kdw_first_credit_time"] = []
        drools_dict["cjk_first_credit_time"] = []
        drools_dict["hjk_first_credit_time"] = []
        before_3days=str(return_strfYmd_date(self.info.event_time_add8h-datetime.timedelta(days=2)))[:10]
        mongo_drool_3days=self.mongo.query_by_user_id(db="skynet_feature",collection="skynet_drools_history",find={"user_id":user_id,'data_time':{"$gte":before_3days}})
        skynet_drools_precomputation=self.mysql.queryall_by_customer_id(db="skynet_fact_material",sql="select * from skynet_drools_precomputation where user_id='{0}' and data_time <'{1}'".format(self.info.user_id,before_3days))
        for drools in mongo_drool_3days:
            if drools.get("ljd_count"):
                drools_dict["ljd_count"].append(drools.get("ljd_count"))
            if drools.get("sxj_count"):
                drools_dict["sxj_count"].append(drools.get("sxj_count"))
            if drools.get("kdw_count"):
                drools_dict["kdw_count"].append(drools.get("kdw_count"))
            if drools.get("cjk_count"):
                drools_dict["cjk_count"].append(drools.get("cjk_count"))
            if drools.get("hjk_count"):
                drools_dict["hjk_count"].append(drools.get("hjk_count"))
            if drools.get("ljd_night_count"):
                drools_dict["ljd_night_count"].append(drools.get("ljd_night_count"))
            if drools.get("sxj_night_count"):
                drools_dict["sxj_night_count"].append(drools.get("sxj_night_count"))
            if drools.get("kdw_night_count"):
                drools_dict["kdw_night_count"].append(drools.get("kdw_night_count"))
            if drools.get("cjk_night_count"):
                drools_dict["cjk_night_count"].append(drools.get("cjk_night_count"))
            if drools.get("hjk_night_count"):
                drools_dict["hjk_night_count"].append(drools.get("hjk_night_count"))
            if drools.get("ljd_pre_borrow_count"):
                drools_dict["ljd_pre_borrow_count"].append(drools.get("ljd_pre_borrow_count"))
            if drools.get("sxj_pre_borrow_count"):
                drools_dict["sxj_pre_borrow_count"].append(drools.get("sxj_pre_borrow_count"))
            if drools.get("kdw_pre_borrow_count"):
                drools_dict["kdw_pre_borrow_count"].append(drools.get("kdw_pre_borrow_count"))
            if drools.get("cjk_pre_borrow_count"):
                drools_dict["cjk_pre_borrow_count"].append(drools.get("cjk_pre_borrow_count"))
            if drools.get("hjk_pre_borrow_count"):
                drools_dict["hjk_pre_borrow_count"].append(drools.get("hjk_pre_borrow_count"))
            if drools.get("ljd_refuse_count"):
                drools_dict["ljd_refuse_count"].append(drools.get("ljd_refuse_count"))
            if drools.get("sxj_refuse_count"):
                drools_dict["sxj_refuse_count"].append(drools.get("sxj_refuse_count"))
            if drools.get("kdw_refuse_count"):
                drools_dict["kdw_refuse_count"].append(drools.get("kdw_refuse_count"))
            if drools.get("cjk_refuse_count"):
                drools_dict["cjk_refuse_count"].append(drools.get("cjk_refuse_count"))
            if drools.get("hjk_refuse_count"):
                drools_dict["hjk_refuse_count"].append(drools.get("hjk_refuse_count"))
            if drools.get("ljd_first_credit_time"):
                drools_dict["ljd_first_credit_time"].append(drools.get("ljd_first_credit_time"))
            if drools.get("sxj_first_credit_time"):
                drools_dict["sxj_first_credit_time"].append(drools.get("sxj_first_credit_time"))
            if drools.get("kdw_first_credit_time"):
                drools_dict["kdw_first_credit_time"].append(drools.get("kdw_first_credit_time"))
            if drools.get("cjk_first_credit_time"):
                drools_dict["cjk_first_credit_time"].append(drools.get("cjk_first_credit_time"))
            if drools.get("hjk_first_credit_time"):
                drools_dict["hjk_first_credit_time"].append(drools.get("hjk_first_credit_time"))
        for drools in skynet_drools_precomputation:
            if drools.get("ljd_count"):
                drools_dict["ljd_count"].append(drools.get("ljd_count"))
            if drools.get("sxj_count"):
                drools_dict["sxj_count"].append(drools.get("sxj_count"))
            if drools.get("kdw_count"):
                drools_dict["kdw_count"].append(drools.get("kdw_count"))
            if drools.get("cjk_count"):
                drools_dict["cjk_count"].append(drools.get("cjk_count"))
            if drools.get("hjk_count"):
                drools_dict["hjk_count"].append(drools.get("hjk_count"))
            if drools.get("ljd_night_count"):
                drools_dict["ljd_night_count"].append(drools.get("ljd_night_count"))
            if drools.get("sxj_night_count"):
                drools_dict["sxj_night_count"].append(drools.get("sxj_night_count"))
            if drools.get("kdw_night_count"):
                drools_dict["kdw_night_count"].append(drools.get("kdw_night_count"))
            if drools.get("cjk_night_count"):
                drools_dict["cjk_night_count"].append(drools.get("cjk_night_count"))
            if drools.get("hjk_night_count"):
                drools_dict["hjk_night_count"].append(drools.get("hjk_night_count"))
            if drools.get("ljd_pre_borrow_count"):
                drools_dict["ljd_pre_borrow_count"].append(drools.get("ljd_pre_borrow_count"))
            if drools.get("sxj_pre_borrow_count"):
                drools_dict["sxj_pre_borrow_count"].append(drools.get("sxj_pre_borrow_count"))
            if drools.get("kdw_pre_borrow_count"):
                drools_dict["kdw_pre_borrow_count"].append(drools.get("kdw_pre_borrow_count"))
            if drools.get("cjk_pre_borrow_count"):
                drools_dict["cjk_pre_borrow_count"].append(drools.get("cjk_pre_borrow_count"))
            if drools.get("hjk_pre_borrow_count"):
                drools_dict["hjk_pre_borrow_count"].append(drools.get("hjk_pre_borrow_count"))
            if drools.get("ljd_refuse_count"):
                drools_dict["ljd_refuse_count"].append(drools.get("ljd_refuse_count"))
            if drools.get("sxj_refuse_count"):
                drools_dict["sxj_refuse_count"].append(drools.get("sxj_refuse_count"))
            if drools.get("kdw_refuse_count"):
                drools_dict["kdw_refuse_count"].append(drools.get("kdw_refuse_count"))
            if drools.get("cjk_refuse_count"):
                drools_dict["cjk_refuse_count"].append(drools.get("cjk_refuse_count"))
            if drools.get("hjk_refuse_count"):
                drools_dict["hjk_refuse_count"].append(drools.get("hjk_refuse_count"))
            if drools.get("ljd_first_credit_time"):
                drools_dict["ljd_first_credit_time"].append(drools.get("ljd_first_credit_time"))
            if drools.get("sxj_first_credit_time"):
                drools_dict["sxj_first_credit_time"].append(drools.get("sxj_first_credit_time"))
            if drools.get("kdw_first_credit_time"):
                drools_dict["kdw_first_credit_time"].append(drools.get("kdw_first_credit_time"))
            if drools.get("cjk_first_credit_time"):
                drools_dict["cjk_first_credit_time"].append(drools.get("cjk_first_credit_time"))
            if drools.get("hjk_first_credit_time"):
                drools_dict["hjk_first_credit_time"].append(drools.get("hjk_first_credit_time"))
        return drools_dict

    def __preBorrowCnt(self,dict):
        serial_list = []
        result = self.mongo.query_all_by_userId_inXdays(db='skynet',
                                                        collection='skynet_decision_result',
                                                        serial_no=self.serial_no,find=dict,
                                                        start_days=1000,
                                                        start_time="00:00:00",
                                                        end_days=0)
        if not result:
            return 0
        for serial in result:
            serial_list.append(serial['serial_no'])
        return len(list(set(serial_list)))

    def preBorrowCntOfDroolsKdw(self):
        """preBorrowCntOfDroolsKdw 卡贷王调用drools预借环节次数（包含缓存）"""
        return self.__preBorrowCnt(dict={"user_id":int(self.info.user_id),"scene_code":"pre_borrow","product_code":"kdw_loan"})

    def preBorrowCntOfDroolsLjd(self):
        """preBorrowCntOfDroolsLjd 立即贷调用drools预借环节次数（包含缓存）"""
        return self.__preBorrowCnt(dict={"user_id": int(self.info.user_id),"scene_code": "pre_borrow","product_code": "vip_loan"})

    def preBorrowCntOfDroolsXj(self):
        """preBorrowCntOfDroolsXj 2345借款平台调用drools预借环节次数（包含缓存）"""
        result = self.__pre_drools_result(self.info.user_id)
        return sum(result.get("sxj_pre_borrow_count"))+sum(result.get("ljd_pre_borrow_count"))+sum(result.get("cjk_pre_borrow_count"))+sum(result.get("hjk_pre_borrow_count"))

    def preBorrowCntOfDroolsSxj(self):
        """preBorrowCntOfDroolsSxj 随心借调用drools预借环节次数（包含缓存）"""
        return self.__preBorrowCnt(dict={"user_id": int(self.info.user_id),"scene_code": "pre_borrow","product_code": "sxj_loan"})

    def __nightCntOfDrools(self,dict):
        result = self.mongo.query_all_by_userId_inXdays(db='skynet',
                                                        collection='skynet_decision_result',
                                                        serial_no=self.serial_no,
                                                        find=dict,
                                                        start_days=1000,
                                                        start_time="00:00:00",
                                                        end_days=0)
        return result

    def nightCntOfDroolsKdw(self):
        """nightCntOfDroolsKdw 卡贷王夜间调用Drools次数（包含缓存）"""
        serial_no_decision = []
        serial_no_success=[]
        result=self.__nightCntOfDrools(dict={"user_id": int(self.info.user_id),"product_code":"kdw_loan"})
        if not result:
            return 0
        for decision in result:
            if decision.get('scene_code') in ('credit','pre_borrow') and decision.get('serial_no')!=self.serial_no:
                serial_no_decision.append([decision.get('serial_no'),decision.get('scene_code'),decision.get('create_time')+datetime.timedelta(hours=8)])
        for serial in serial_no_decision:
            if  0<=int(serial[2].strftime('%H'))<7:
                serial_no_success.append(serial[0])
        return len(list(set(serial_no_success)))

    def nightCntOfDroolsLjd(self):
        """nightCntOfDroolsLjd 立即贷夜间调用Drools次数（包含缓存）"""
        serial_no_decision = []
        serial_no_success=[]
        result=self.__nightCntOfDrools(dict={"user_id": int(self.info.user_id),"product_code":"vip_loan"})
        if not result:
            return 0
        for decision in result:
            if decision.get('scene_code') in ('credit','pre_borrow')  and decision.get('serial_no')!=self.serial_no:
                serial_no_decision.append([decision.get('serial_no'),decision.get('scene_code'),decision.get('create_time')+datetime.timedelta(hours=8)])
        for serial in serial_no_decision:
            if  0<=int(serial[2].strftime('%H'))<7:
                serial_no_success.append(serial[0])
        return len(list(set(serial_no_success)))

    def nightCntOfDroolsXj(self):
        """nightCntOfDroolsXj 2345借款平台下产品夜间调用Drools次数（包含缓存）"""
        result=self.__pre_drools_result(self.info.user_id)
        return sum(result.get("ljd_night_count"))+sum(result.get("sxj_night_count"))+sum(result.get("cjk_night_count"))+sum(result.get("hjk_night_count"))

    def nightCntOfDroolsSxj(self):
        """nightCntOfDroolsSxj 随心借夜间调用Drools次数（包含缓存）"""
        serial_no_decision = []
        serial_no_success=[]
        result=self.__nightCntOfDrools(dict={"user_id": int(self.info.user_id),"product_code":"sxj_loan"})
        if not result:
            return 0
        for decision in result:
            if decision.get('scene_code') in ('credit','pre_borrow') and decision.get('serial_no')!=self.serial_no:
                serial_no_decision.append([decision.get('serial_no'),decision.get('scene_code'),decision.get('create_time')+datetime.timedelta(hours=8)])
        for serial in serial_no_decision:
            if  0<=int(serial[2].strftime('%H'))<7:
                serial_no_success.append(serial[0])
        return len(list(set(serial_no_success)))

    def rtoRefuseOfDroolsLjdSxj(self):
        """rtoRefuseOfDroolsLjdSxj 调用drools被拒绝比例（包含缓存）"""
        serial_no = []
        refuse_no=[]
        results = self.mongo.query_by_user_id(db='skynet', collection="skynet_decision_result",
                                              find={'user_id': self.info.user_id})
        for res in results:
            if res.get('product_code') in ('vip_loan', 'sxj_loan') and res.get('scene_code') in ('credit', 'pre_borrow'):
                serial_no.append(res.get('serial_no'))
            if res.get('product_code') in ('vip_loan', 'sxj_loan') and res.get('scene_code') in ('credit', 'pre_borrow') and res.get('data').get('decisionResult')=='000':
                refuse_no.append(res.get('serial_no'))
        if not serial_no:
            return self.SET_DEFAULT_VALUE_INT_9999995
        if self.serial_no in serial_no:
            serial_no.remove(self.serial_no)
        refuse_len=float(len(list(set(refuse_no))))
        serial_len= len(list(set(serial_no)))
        if serial_len==0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(refuse_len/serial_len,4)

    def rtoRefuseOfDroolsXj(self):
        """rtoRefuseOfDroolsXj 2345借款平台下产品调用drools被拒绝比例（包含缓存）"""
        result=self.__pre_drools_result(self.info.user_id)
        refuse_sum= sum(result.get("ljd_refuse_count"))+sum(result.get("sxj_refuse_count"))+sum(result.get("cjk_refuse_count"))+sum(result.get("hjk_refuse_count"))
        count_sum = sum(result.get("ljd_count"))+sum(result.get("sxj_count"))+sum(result.get("cjk_count"))+sum(result.get("hjk_count"))
        if count_sum==1:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        #TODO 真实代码是round(float(refuse_sum)/count_sum,4)，因为脚本在风控调用之后，在mongo库里又增加一笔，所以通过时分母-1，或者拒绝时，分母-1，分子-1
        return round(float(refuse_sum)/(count_sum-1),4)

    def rtoRefuseOfDroolsLjd(self):
        """rtoRefuseOfDroolsLjd 立即贷调用drools被拒绝比例（包含缓存）"""
        serial_no = []
        refuse_no = []
        results = self.mongo.query_by_user_id(db='skynet', collection="skynet_decision_result",
                                              find={'user_id': self.info.user_id})
        for res in results:
            if res.get('product_code') in ('vip_loan',) and res.get('scene_code') in ('credit', 'pre_borrow'):
                serial_no.append(res.get('serial_no'))
            if res.get('product_code') in ('vip_loan',) and res.get('scene_code') in ('credit', 'pre_borrow') and res.get('data').get('decisionResult')=='000':
                refuse_no.append(res.get('serial_no'))
        if not serial_no:
            return self.SET_DEFAULT_VALUE_INT_9999995
        if self.serial_no in serial_no:
            serial_no.remove(self.serial_no)
        refuse_len=float(len(list(set(refuse_no))))
        serial_len= len(list(set(serial_no)))
        if serial_len==0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(refuse_len/serial_len,4)

    def rtoRefuseOfDroolsSxj(self):
        """rtoRefuseOfDroolsSxj 随心借调用drools被拒绝比例（包含缓存）"""
        serial_no = []
        refuse_no = []
        results = self.mongo.query_by_user_id(db='skynet', collection="skynet_decision_result",
                                              find={'user_id': self.info.user_id})
        for res in results:
            if res.get('product_code') in ('sxj_loan',) and res.get('scene_code') in ('credit', 'pre_borrow'):
                serial_no.append(res.get('serial_no'))
            if res.get('product_code') in ('sxj_loan',) and res.get('scene_code') in ('credit', 'pre_borrow') and res.get('data').get('decisionResult')=='000':
                refuse_no.append(res.get('serial_no'))
        if not serial_no:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        if self.serial_no in serial_no:
            serial_no.remove(self.serial_no)
        refuse_len=float(len(list(set(refuse_no))))
        serial_len= len(list(set(serial_no)))
        if serial_len==0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round(refuse_len/serial_len,4)

    def enterNumber(self):
        """enterNumber 进入人工次数"""
        decision_result=self.mongo.query_all_by_userId_inXdays( db='skynet',
                                                                collection='skynet_decision_result',
                                                                serial_no=self.serial_no,
                                                                find={"user_id":int(self.info.user_id)},
                                                                start_days=2,
                                                                start_time="00:00:00",
                                                                end_days=0)
        count=0
        for decision in decision_result:
            if decision.get("status")=="SUCCESS":
                if decision.get("data").get("decisionResult")=='001':
                    count+=1
        return count

    def artificialCheck(self):
        """artificialCheck 人工复核"""
        decision_result=self.mongo.query_all_by_userId_inXdays( db='skynet',
                                                                collection='skynet_decision_result',
                                                                serial_no=self.serial_no,
                                                                find={"user_id":int(self.info.user_id)},
                                                                start_days=2,
                                                                start_time="00:00:00",
                                                                end_days=0)
        if len(decision_result)==0:
            return 0
        last_one= decision_result[0]
        if not last_one:
            return 0
        if last_one.get("data").get("decisionResult")=='001':
            return 1
        else:
            return 0

    def measurementCreditDeviceNumber(self):
        """measurementCreditDeviceNumber 测额到当前授信的时间使用的设备总数"""
        decision_results = self.mongo.query_by_user_id(db='skynet',
                                                       collection="skynet_decision_result",
                                                       find={"user_id": int(self.info.user_id),
                                                             "product_code": "sxj_loan",
                                                             "scene_code": "credit",
                                                             "status" : "SUCCESS"})
        if not decision_results:
            return -9999999
        #取最后一条为最老一条数据
        s_start_id=decision_results[-1].get('_id')
        s_end_id=ObjectId.from_datetime(self.info.event_time)
        device_results = self.mongo.query_all_by_userId_inXdays(db='lake',
                                                                collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                                                find={"customer_id":int(self.info.customer_id)},
                                                                serial_no=self.serial_no, s_start_id=s_start_id,s_end_id=s_end_id)
        if not device_results:
            return 0
        device_list = []
        for r in device_results:
            device_ids = ''
            for field in ['idfa', 'imei', 'android_id', 'mac']:
                if r.get(field):
                    device_ids = device_ids + r.get(field)
            device_list.append(device_ids)
        return len(list(set(device_list)))


if __name__ == "__main__":
    serial_no = "1534821380871-BCCB915D39473E904B5A2B0561AA43F8"
    a = DroolsFactor('T1', serial_no)
    print a.nightCntOfDroolsLjd()