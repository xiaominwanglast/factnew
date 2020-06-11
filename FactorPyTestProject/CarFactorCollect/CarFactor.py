#!/usr/bin/python
# -*- coding: UTF-8 -*-
from FrameRunner.FactorInit import CarFactorInit
from utils.threeDES import factor_encrypt_identity
from utils.otherUtil import *
from utils.Mysql_heXin import Mysql_heXin
from utils.otherUtil import *

class CarFactor(CarFactorInit):
    def __init__(self, env, serial_no):
        super(CarFactor,self).__init__(env, serial_no)

    def __MiGuanJuLiXinResult(self):
        results = self.mongo.queryall_by_userId(db='galaxy', collection="miguan_record",
                                                find={"cardId": self.info.result.get('cert_id'),
                                                      "phone": self.info.result.get('phone'),
                                                      "realName": self.info.result.get('user_name')})

        if not results:
            return None
        for i in range(0,len(results)):
            miguan_time = results[i].get('createTime')
            decision_time = self.info.result.get('create_time')
            start_day = str(decision_time + datetime.timedelta(hours=8) - datetime.timedelta(days=29))[0:10] + ' ' + "00:00:00"
            start_date = datetime.datetime.strptime(start_day, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(hours=8)
            if miguan_time < start_date:
                continue
            if results[i].get('response') and results[i].get('code') == 'MIGUAN_SEARCH_SUCCESS' and  \
                    results[i].get('response').get('data') and results[i].get('response').get('code') == 'MIGUAN_SEARCH_SUCCESS':
                # print "i:",i
                return results[i].get('response').get('data')
        return None

    # def contactsClass1BlacklistCnt(self):
    #     """contactsClass1BlacklistCnt	直接联系人在黑名单的数量"""
    #     results=self.__MiGuanJuLiXinResult()
    #     if not results :
    #         return self.SET_DEFAULT_VALUE_INT_9999999
    #     contactsClass1BlacklistCnt=results.get('user_gray').get('contacts_class1_blacklist_cnt')
    #     if not  contactsClass1BlacklistCnt and not isinstance(contactsClass1BlacklistCnt,int):
    #         return -9999996
    #     return contactsClass1BlacklistCnt

    # def contactsClass2BlacklistCnt(self):
    #     """contactsClass2BlacklistCnt	间接联系人在黑名单的数量"""
    #     results = self.__MiGuanJuLiXinResult()
    #     if not results:
    #         return self.SET_DEFAULT_VALUE_INT_9999999
    #     contacts_class2_blacklist_cnt = results.get('user_gray').get('contacts_class2_blacklist_cnt')
    #     if not  contacts_class2_blacklist_cnt and not isinstance (contacts_class2_blacklist_cnt,int):
    #         return -9999996
    #     return contacts_class2_blacklist_cnt

    # def phoneGrayScore(self):
    #     """phoneGrayScore	手机号码灰度分数"""
    #     results = self.__MiGuanJuLiXinResult()
    #     if not results:
    #         return self.SET_DEFAULT_VALUE_INT_9999999
    #     phoneGrayScore = results.get('user_gray').get('phone_gray_score')
    #     if not  phoneGrayScore and not isinstance (phoneGrayScore,int):
    #         return -9999996
    #     return phoneGrayScore

    # def searchedOrgCnt(self):
    #     """searchedOrgCnt	被机构查询数量统计(去重后) 定义为X"""
    #     results = self.__MiGuanJuLiXinResult()
    #     if not results:
    #         return self.SET_DEFAULT_VALUE_INT_9999999
    #     searchedOrgCnt = results.get('user_searched_statistic').get('searched_org_cnt')
    #     if not  searchedOrgCnt and not isinstance (searchedOrgCnt,int):
    #         return -9999996
    #     return searchedOrgCnt

    # def blacklistNameWithPhone(self):
    #     """blacklistNameWithPhone	姓名和手机是否在黑名单"""
    #     results = self.__MiGuanJuLiXinResult()
    #     if not results:
    #         return self.SET_DEFAULT_VALUE_INT_9999999
    #     blacklist_name_with_phone=results.get('user_blacklist').get('blacklist_name_with_phone')
    #     if isinstance (blacklist_name_with_phone,bool):
    #         if blacklist_name_with_phone:
    #             return 1
    #         return 0
    #     return -9999996

    # def blacklistNameWithIdcard(self):
    #     """blacklistNameWithIdcard	身份证和姓名是否在黑名单"""
    #     results = self.__MiGuanJuLiXinResult()
    #     if not results:
    #         return self.SET_DEFAULT_VALUE_INT_9999999
    #     blacklistNameWithIdcard = results.get('user_blacklist').get('blacklist_name_with_idcard')
    #     if isinstance(blacklistNameWithIdcard, bool):
    #         if blacklistNameWithIdcard:
    #             return 1
    #         return 0
    #     return -9999996

    # def suspPhoneCnt(self):
    #     """suspPhoneCnt	身份证号码存疑"""
    #     results = self.__MiGuanJuLiXinResult()
    #     if not results:
    #         return self.SET_DEFAULT_VALUE_INT_9999999
    #     suspPhoneCnt = results.get('user_idcard_suspicion').get('idcard_with_other_phones')
    #     if isinstance(suspPhoneCnt,list):
    #         return len(suspPhoneCnt)
    #     return -9999996

    def __tdResult(self,item_id=0):
        results = self.mongo.queryall_by_userId(db='galaxy', collection="td_record",
                                            find={"serialNo": self.serial_no})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get('tdReportResponse') or not results[0].get('tdReportResponse').get('risk_items'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        if item_id==0:
            return results[0].get('tdReportResponse').get('risk_items')
        if item_id=='score':
            return results[0].get('tdReportResponse').get('final_score')
        for row in results[0].get('tdReportResponse').get('risk_items'):
            if row.get('item_id')==str(item_id):
                return row
        return self.SET_DEFAULT_VALUE_INT_0
    def __td_ResultBy_item_id(self,item_id):
        results = self.__tdResult(item_id=item_id)
        if results==self.SET_DEFAULT_VALUE_INT_9999999:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if results==self.SET_DEFAULT_VALUE_INT_9999996:
            return self.SET_DEFAULT_VALUE_INT_9999996
        if results==self.SET_DEFAULT_VALUE_INT_0:
            return self.SET_DEFAULT_VALUE_INT_0
        if item_id=='score':
            return results
        if not results or not results.get('item_detail'):
            return 0
        return 1

    def riskItem2976212(self):
        """riskItem2976212	身份证命中法院失信黑名单"""
        return self.__td_ResultBy_item_id(item_id=2976212)

    def riskItem2976214(self):
        """riskItem2976214	身份证命中犯罪通缉名单"""
        return self.__td_ResultBy_item_id(item_id=2976214)

    def riskItem2976216(self):
        """riskItem2976216	身份证命中法院执行名单"""
        return self.__td_ResultBy_item_id(item_id=2976216)

    def riskItem2976220(self):
        """riskItem2976220	身份证命中信贷逾期名单"""
        return self.__td_ResultBy_item_id(item_id=2976220)

    def riskItem2976224(self):
        """riskItem2976224	身份证命中车辆租赁违约名单"""
        return self.__td_ResultBy_item_id(item_id=2976224)

    def riskItem2976226(self):
        """riskItem2976226	身份证命中法院结案名单"""
        return self.__td_ResultBy_item_id(item_id=2976226)

    def riskItem2976254(self):
        """riskItem2976254	手机号命中虚假号码库"""
        return self.__td_ResultBy_item_id(item_id=2976254)

    def riskItem2976258(self):
        """riskItem2976258	手机号命中诈骗骚扰库"""
        return self.__td_ResultBy_item_id(item_id=2976258)

    def riskItem2976266(self):
        """riskItem2976266	手机号命中信贷逾期名单"""
        return self.__td_ResultBy_item_id(item_id=2976266)

    def riskItem2976268(self):
        """riskItem2976268	手机号命中车辆租赁违约名单"""
        return self.__td_ResultBy_item_id(item_id=2976268)

    def riskItem2976312(self):
        """riskItem2976312	单位名称疑似中介关键词"""
        return self.__td_ResultBy_item_id(item_id=2976312)

    def riskItem2976320(self):
        """riskItem2976320	3个月内身份证关联多个申请信息"""
        return self.__td_ResultBy_item_id(item_id=2976320)

    def riskItem2976322(self):
        """riskItem2976322	3个月内申请信息关联多个身份证"""
        return self.__td_ResultBy_item_id(item_id=2976322)

    def riskItem2976340(self):
        """riskItem2976340	7天内设备或身份证或手机号申请次数过多"""
        return self.__td_ResultBy_item_id(item_id=2976340)

    def riskItem2976354(self):
        """riskItem2976354	7天内申请人在多个平台申请借款"""
        return self.__td_ResultBy_item_id(item_id=2976354)

    def riskItem2976356(self):
        """riskItem2976356	1个月内申请人在多个平台申请借款"""
        return self.__td_ResultBy_item_id(item_id=2976356)

    def riskItem2976372(self):
        """riskItem2976372	3个月内申请人在多个平台被放款_不包含本合作方"""
        return self.__td_ResultBy_item_id(item_id=2976372)

    def finalScore(self):
        """finalScore 反欺诈分值"""
        return self.__td_ResultBy_item_id(item_id='score')

    def __hexin_bill(self, user_id, product_id, month):
        ResultList = []
        MonthBefore = getXmonthDate(self.info.event_time_add8h, month)
        billList=self.mongo.query_by_user_id(db='skynet_feature', collection='skynet_loan_info', find={'user_id':user_id,'product_id':product_id,'delete_flag':0})
        if not billList:
            return []
        billList=[bill for bill in billList if bill.get("borrow_approve_date")>=MonthBefore]
        for billRecord in billList:
            if not billRecord.get('settle_date'):
                settle_date = self.info.event_time_add8h
            else:
                settle_date = billRecord.get('settle_date')+datetime.timedelta(hours=8)
            ResultList.append([billRecord.get('borrow_approve_date')+datetime.timedelta(hours=8),
                               billRecord.get('repay_date')+datetime.timedelta(hours=8),
                               settle_date,
                               float(billRecord.get('total_principal')),
                               billRecord.get('stage_ret'),
                               str(billRecord.get("order_id")),
                               billRecord.get("loan_id")])
        ResultList.sort()
        return ResultList

    def __old_overdue_days(self,oldUserId,month):
        old_list=[]
        time1MonthBefore = str(getXmonthDate(self.info.event_time_add8h, month))
        sql="select * from all_fin_rownumber where user_id ='%s' and borrow_date >= '%s' order by rank ;"%(oldUserId,time1MonthBefore)
        result = self.mysql.queryall_by_customer_id('skynet_fact_material', sql)
        if result:
            for li in result:
                if not li.get('real_repayment_date'):
                    li['real_repayment_date'] = self.info.event_time_add8h
                if type(li['real_repayment_date'])==datetime.date:
                    realRepaymentDate=datetime.datetime.strptime(str(li.get('real_repayment_date')), '%Y-%m-%d')
                else:
                    realRepaymentDate=li['real_repayment_date']
                old_list.append([datetime.datetime.strptime(str(li.get('borrow_date')),'%Y-%m-%d') ,
                                 datetime.datetime.strptime(str(li.get('next_pay_date')),'%Y-%m-%d'),
                                 realRepaymentDate,li.get('amount')])
        return old_list

    def lateCnt(self):
        """lateCnt 逾期次数"""
        count=0
        sql="select user_id from s_user_identity where identity_card= '%s';"%self.info.cert_id
        result = self.mysql.queryone_by_customer_id('xinyongjin', sql)
        if result and result.get('user_id'):
            old_days_list=self.__old_overdue_days(result.get('user_id'),-36)
            for days in old_days_list:
                if return_strfYmd_date(days[2])>return_strfYmd_date(days[1]):
                    count+=1
        if str(self.info.cert_id)[-1].lower()=='x':
            i='x'
        else:
            i=int(str(self.info.cert_id)[-1])%10
        sql = "select customer_id from identiy_card_%s where identity_card='%s' and group_id =1;" % (i,factor_encrypt_identity(int(self.info.cert_id)))
        result = self.mysql.queryone_by_customer_id('customer_center', sql)
        if result and result.get('customer_id'):
            ljd_customer_id=result.get('customer_id')
            userId_sql="select * from customer where id ='%s'"%ljd_customer_id
            result = self.mysql.queryone_by_customer_id('customer_center', userId_sql)
            user_id=result.get('user_id')
            all_list_days=self.__hexin_bill(user_id,self.ljd_product_id,-12)+self.__hexin_bill(user_id,self.sxj_product_id,-12)+self.__hexin_bill(user_id,self.kdw_product_id,-12)
            for days in all_list_days:
                if return_strfYmd_date(days[2])>return_strfYmd_date(days[1]):
                    count+=1
        return count

    def maxLateDays(self):
        """maxLateDays 最大逾期天数"""
        overdue_list=[]
        sql="select user_id from s_user_identity where identity_card= '%s';"%self.info.cert_id
        result = self.mysql.queryone_by_customer_id('xinyongjin', sql)
        if result and result.get('user_id'):
            old_list = self.__old_overdue_days(result.get('user_id'), -36)
            for old in old_list:
                overdue_list.append((return_strfYmd_date(old[2]) - return_strfYmd_date(old[1])).days)
        if str(self.info.cert_id)[-1].lower()=='x':
            i='x'
        else:
            i=int(str(self.info.cert_id)[-1])%10
        sql = "select customer_id from identiy_card_%s where identity_card='%s' and group_id =1;" % (i,factor_encrypt_identity(int(self.info.cert_id)))
        result = self.mysql.queryone_by_customer_id('customer_center', sql)
        if result and result.get('customer_id'):
            ljd_customer_id=result.get('customer_id')
            userId_sql="select * from customer where id ='%s'"%ljd_customer_id
            result = self.mysql.queryone_by_customer_id('customer_center', userId_sql)
            user_id=result.get('user_id')
            new_list = self.__hexin_bill(user_id, self.ljd_product_id, -36)+\
                        self.__hexin_bill(user_id, self.sxj_product_id, -36)+\
                        self.__hexin_bill(user_id, self.kdw_product_id, -36)
            for new in new_list:
                overdue_list.append((return_strfYmd_date(new[2]) - return_strfYmd_date(new[1])).days)
        if not overdue_list or max(overdue_list)<=0:
            return 0
        return max(overdue_list)

    def lastBorrowLateDays(self):
        """lastBorrowLateDays 最后一次借款逾期天数"""
        old_list=[]
        new_list=[]
        sql="select user_id from s_user_identity where identity_card= '%s';"%self.info.cert_id
        result = self.mysql.queryone_by_customer_id('xinyongjin', sql)

        if result and result.get('user_id'):
            old_list = self.__old_overdue_days(result.get('user_id'), -36)
        if str(self.info.cert_id)[-1].lower()=='x':
            i='x'
        else:
            i=int(str(self.info.cert_id)[-1])%10
        sql = "select customer_id from identiy_card_%s where identity_card='%s' and group_id =1;" % (i,factor_encrypt_identity(int(self.info.cert_id)))
        result = self.mysql.queryone_by_customer_id('customer_center', sql)
        if result and result.get('customer_id'):
            ljd_customer_id=result.get('customer_id')
            userId_sql="select * from customer where id ='%s'"%ljd_customer_id
            result = self.mysql.queryone_by_customer_id('customer_center', userId_sql)
            user_id=result.get('user_id')
            new_list = self.__hexin_bill(user_id, self.ljd_product_id, -36)+\
                        self.__hexin_bill(user_id, self.sxj_product_id, -36)+\
                        self.__hexin_bill(user_id, self.kdw_product_id, -36)
        all_list_days=old_list+new_list
        all_list_days.sort()
        if not all_list_days:
            return 0
        return (return_strfYmd_date(all_list_days[-1][2]) - return_strfYmd_date(all_list_days[-1][1])).days

    def qhcsCreditScore(self):
        """qhcsCreditScore 前海2.0信用卡综合评分 Integer"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='qhcs_msc8262_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        last_one=result[0]
        if not last_one.get('qhcsMsc8262Info') or not last_one.get('qhcsMsc8262Info').get('credooScore'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return last_one.get('qhcsMsc8262Info').get('credooScore')

    def geoCurStatus(self):
        """geoCurStatus 集奥当前状态"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='geo_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result or not result[0].get('response') or not result[0].get('response').get('data') or not result[0].get('response').get('data').get('RSL'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        for i in result[0].get('response').get('data').get('RSL'):
            if i.get('IFT')=='A4':
                if not i.get('RS').get('code'):
                    return self.SET_DEFAULT_VALUE_INT_9999996
                return i.get('RS').get('code')
        return self.SET_DEFAULT_VALUE_INT_9999999

if __name__ == '__main__':
    serial_no = "1537336673799-4F44D4B8A1545698F6F4D0CC79C7305F"
    a = CarFactor('T2', serial_no)
    print (a.riskItem2976212())
