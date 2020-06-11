# coding:utf-8
from FrameRunner.FactorInit import NewFactorInit
from utils.otherUtil import *
import numpy as np
from utils.TestInit import factor_encrypt_identity,factor_decrypt_identity
import datetime
class MXFactorV2(NewFactorInit):
    def __init__(self, env, serial_no):
        super(MXFactorV2,self).__init__(env, serial_no)

    def user_authenticate_phone(self):
        """user_authenticate_phone 客户授权手机号"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                           find={"_id": int(self.info.user_id)})
        if len(data) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return data[0]['mobile']

    def user_phone_in_time_days(self):
        """user_phone_in_time_days 手机号入网时间"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                           find={"_id": int(self.info.user_id)})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        open_time = data[0].get('openTime')
        if not open_time:
            return self.SET_DEFAULT_VALUE_INT_9999999
        open_time = datetime.datetime.strptime(open_time, "%Y-%m-%d")
        days = (self.info.event_time_add8h - open_time).days
        return days

    def call_detail_distinct_cnt_6m(self):
        """call_detail_distinct_cnt_6m 魔蝎详单通话手机号码个数"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                           find={"_id": int(self.info.user_id)})
        if len(data) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not data[0].get('pheCnt6m'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return data[0].get('pheCnt6m')

    def call_detail_cnt_6m(self):
        """call_detail_cnt_6m 魔蝎详单累计手机号码通话次数（不去重）（不包含通话时间为0）"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                           find={"_id": int(self.info.user_id)})
        if len(data) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not data[0].get('callCnt6m'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return data[0].get('callCnt6m')

    def phone_avg_fee_6m(self):
        """phone_avg_fee_6m 手机月均话费（单位:元，四舍五入精确到元）"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                           find={"_id": int(self.info.user_id)})
        if len(data) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not data[0].get('avgFee6m'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        avgFee6m=data[0].get('avgFee6m')
        return int(round(int(avgFee6m)/ 100.0))

    def call_macao_month_cnt_6m(self):
        """call_macao_month_cnt_6m 澳门通话出现的月数"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                           find={"_id": int(self.info.user_id)})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(data[0].get('callMacaoMonthCnt6m'))

    def contact_call_mutual_cnt_6m(self):
        """contact_call_mutual_cnt_6m 通讯录中互通过电话的手机号码数量"""
        call_result = self.__call_contact_mx()
        if not call_result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        peer_num_list = []
        ccd_dic = call_result['callContactDetail']
        for k in ccd_dic:
            if ccd_dic[k]['dial_cnt_6m'] != 0 and ccd_dic[k]['dialed_cnt_6m'] != 0:
                peer_num_list.append(phoneClean(ccd_dic[k]['peer_num']))
        data = self.mongo.query_by_user_id('feature_bone', "user_contact",
                                                  {"_id": self.info.user_id})
        if len(data) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        contact_num_list = []
        if not data[0].get('contacts'):
            return 0
        for contact in data[0]['contacts']:
            phone1 = contact.get('peerNum')
            phone1 = phoneClean(phone1)
            if phone1 and phone1 not in contact_num_list:
                contact_num_list.append(phone1)
        contact_num_list = list(set(contact_num_list))
        union = list((set(peer_num_list).union(set(contact_num_list))) ^ (set(peer_num_list) ^ set(contact_num_list)))
        return len(union)


    def __call_contact_mx(self):
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_report_fact",
                                           find={"_id": int(self.info.user_id)})
        if not data:
            return
        return data[0]


    def call_relative_last_time(self):
        """call_relative_last_time 近6个月与联系人1最晚通话沟通时间 """
        call_result=self.__call_contact_mx()
        if not call_result:
            return "0000-12-29 16:00:00"
        ccd_dic=call_result['callContactDetail']
        for k in ccd_dic:
            if k==self.info.relativeContact:
                return datetime.datetime.strptime(ccd_dic[k]['trans_end'], "%Y-%m-%d %H:%M:%S")
        return "0000-12-29 16:00:00"

    def call_friend_last_time(self):
        """call_friend_last_time 近6个月与联系人2最晚通话沟通时间 """
        # print self.info.friendContact
        call_result=self.__call_contact_mx()
        if not call_result:
            return "0000-12-29 16:00:00"
        ccd_dic=call_result['callContactDetail']
        for k in ccd_dic:
            if k==self.info.friendContact:
                return datetime.datetime.strptime(ccd_dic[k]['trans_end'], "%Y-%m-%d %H:%M:%S")
        return "0000-12-29 16:00:00"

    def call_colleague_last_time(self):
        """call_colleague_last_time 近6个月与联系人3最晚通话沟通时间"""
        # print self.info.colleagueContact
        call_result=self.__call_contact_mx()
        if not call_result:
            return "0000-12-29 16:00:00"
        ccd_dic=call_result['callContactDetail']
        if not self.info.colleagueContact:
            return "0000-12-29 16:00:00"
        for k in ccd_dic:
            if k==self.info.colleagueContact:
                return datetime.datetime.strptime(ccd_dic[k]['trans_end'], "%Y-%m-%d %H:%M:%S") - datetime.timedelta(
                hours=8)
        return "0000-12-29 16:00:00"
    def call_relative_cnt_6m(self):
        """call_relative_cnt_6m 近6个月与联系人1通话次数 """
        call_result=self.__call_contact_mx()
        if not call_result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        ccd_dic = call_result['callContactDetail']
        for k in ccd_dic:
            if k==self.info.relativeContact:
                return ccd_dic[k]['call_cnt_6m']
        return self.SET_DEFAULT_VALUE_INT_9999999

    def call_friend_cnt_6m(self):
        """call_friend_cnt_6m 近6个月与联系人2通话次数"""
        call_result=self.__call_contact_mx()
        if not call_result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        ccd_dic = call_result['callContactDetail']
        for k in ccd_dic:
            if k==self.info.friendContact:
                return ccd_dic[k]['call_cnt_6m']
        return self.SET_DEFAULT_VALUE_INT_9999999


    def call_colleague_cnt_6m(self):
        """call_colleague_cnt_6m 近6个月与联系人3通话次数"""
        call_result=self.__call_contact_mx()
        if not call_result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        ccd_dic = call_result['callContactDetail']
        for k in ccd_dic:
            if k==self.info.colleagueContact:
                return ccd_dic[k]['call_cnt_6m']
        return self.SET_DEFAULT_VALUE_INT_9999999

    def userinfo_phone_name(self):
        """userinfo_phone_name 客户授权手机号姓名"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if len(data) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return data[0]['name']

    def call_age(self):
        """call_age 最早通话日期与最晚通话日期差值+1"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                           find={"_id": int(self.info.user_id)})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        calls= data[0]['callStatistic4m']
        transStart = calls['transStart']
        transStart = datetime.date(transStart.year, transStart.month, transStart.day)
        transEnd= calls['transEnd']
        transEnd=datetime.date(transEnd.year, transEnd.month, transEnd.day)
        diff_days = (transEnd - transStart).days + 1
        return diff_days

    def silence_longest(self):
        """silence_longest 静默时长(近四个月)"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                           find={"_id": int(self.info.user_id)})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return data[0].get('callSilenceDays4m')

    def rto_cnt_phe_duration90(self):
        """rto_cnt_phe_duration90 通话跨度大于等于90天的手机号码个数比"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                           find={"_id": int(self.info.user_id)})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return data[0].get('rtoPheDuration90d4m')

    def rto_cnt_out_5s(self):
        """rto_cnt_out_5s 通话时长在5秒以内的呼出占总呼出次数比"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                           find={"_id": int(self.info.user_id)})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        calls= data[0]['callStatistic4m']
        dailCntIn5s = calls['dailCntIn5s']
        dailCnt= calls['dailCnt']
        return float(dailCntIn5s) /dailCnt

    def rto_cnt_out_night(self):
        """rto_cnt_out_night 夜间呼出占总呼出次数比"""
        data = self.mongo.query_by_user_id('galaxy', "mx_carrier_bills_notify",
                                           {"user_id": self.info.user_id, "status": "1"})
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        dial_count = 0
        dial_count_night = 0
        for calls in data[0]['response']['calls'][:4]:
            for items in calls['items']:
                item_time = datetime.datetime.strptime(items['time'], "%Y-%m-%d %H:%M:%S")
                if items['dial_type'] == 'DIAL':
                    dial_count += 1
                    if 0 <= item_time.hour <= 6:
                        dial_count_night += 1
        if dial_count==0:
            return self.SET_DEFAULT_VALUE_INT_9999998
        return float(dial_count_night) /dial_count

    def cnt_out_pday(self):
        """cnt_out_pday 日均呼出次数"""
        data = self.mongo.query_by_user_id('galaxy', "mx_carrier_bills_notify",
                                           {"user_id": self.info.user_id, "status": "1"})
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        time_list = []
        for calls in data[0]['response']['calls'][:4]:
            for items in calls['items']:
                item_time = datetime.datetime.strptime(items['time'], "%Y-%m-%d %H:%M:%S")
                date = datetime.date(item_time.year, item_time.month, item_time.day)
                time_list.append(date)
        diff_days = (max(time_list) - min(time_list)).days + 1
        dial_count = 0
        dialed_count =0
        for calls in data[0]['response']['calls'][:4]:
            for items in calls['items']:
                if items['dial_type'] == 'DIAL':
                    dial_count += 1
                if items['dial_type'] =='DIALED':
                    dialed_count+=1
        return float(dial_count) /diff_days


    def call_macao_cnt_6m(self):
        """call_macao_cnt_6m澳门通话次数"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                           find={"_id": int(self.info.user_id)})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(data[0].get('callCntMacao6m'))

    def mxRtoCntNight(self):
        """mxRtoCntNight 夜间通话次数占比"""
        results = self.mongo.query_by_user_id(db='feature_bone',collection="mx_carrier_bill_fact",find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        time179 = self.info.event_time - datetime.timedelta(days=179)
        time179 = str(time179)[0:10] + " 00:00:00"
        time179 = datetime.datetime.strptime(time179, "%Y-%m-%d %H:%M:%S")
        totalcallcnt=0
        totalcallCntOnNight=0
        for row in results:
            if row.get('statistic7Daily6M'):
                for subrow in row.get('statistic7Daily6M'):
                    if subrow.get('callDate')>=time179:
                        callcnt=subrow.get('callCnt')
                        totalcallcnt=totalcallcnt+callcnt
                for subrow in row.get('statistic7Daily6M'):
                    if subrow.get('callDate') >=time179:
                        callCntOnNight=subrow.get('callCntOnNight')
                        totalcallCntOnNight=totalcallCntOnNight+callCntOnNight
        if totalcallcnt==0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return float(totalcallCntOnNight)/float(totalcallcnt)

    def mxRtoPhePOut(self):
    #     """mxRtoPhePOut 呼出手机号码占比"""
        total_call_inXdays_call_time_dic = {}
        results = self.mongo.query_by_user_id_sort_bymyself(db='galaxy',
                                                            collection="mx_carrier_calls",
                                                            find={"user_id": int(self.info.user_id)},
                                                            sort="sort([('create_time',-1),('bill_month',-1)])"
                                                            )
        time179 = self.info.event_time - datetime.timedelta(days=179)
        time179 = str(time179)[0:10] + " 00:00:00"
        time179 = datetime.datetime.strptime(time179, "%Y-%m-%d %H:%M:%S")
        if not results:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        for row in results[:6]:
            if row.get('items'):
                for subrow in row.get('items'):
                    collectnumber = sxjPhoneVaild(subrow.get('peer_number'))
                    if collectnumber:
                        timeinDb = datetime.datetime.strptime(subrow.get('time'), "%Y-%m-%d %H:%M:%S")
                        if collectnumber not in total_call_inXdays_call_time_dic and timeinDb >= time179:
                            total_call_inXdays_call_time_dic[collectnumber] = subrow.get('dial_type')
                        elif collectnumber in total_call_inXdays_call_time_dic and timeinDb >= time179 and subrow.get(
                                'dial_type') == 'DIALED':
                            total_call_inXdays_call_time_dic[collectnumber] = subrow.get('dial_type')
        phoneIn = []
        for k, v in total_call_inXdays_call_time_dic.items():
            if v == 'DIALED':
                phoneIn.append(k)
        if len(total_call_inXdays_call_time_dic) == 0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return float(len(total_call_inXdays_call_time_dic) - len(phoneIn)) / len(total_call_inXdays_call_time_dic)

    def mxUserinfoPhoneAuthenticatePhSame(self):
        """mxUserinfoPhoneAuthenticatePhSame 用户申请手机号与魔蝎认证号是否一致"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        result = results[0]
        mxmobile = result.get('mobile')
        ourmobile = self.info.phone
        if mxmobile == ourmobile:
            return 1
        return 0

    def mxUserinfoIdAuthenticateIdSame(self):
        """mxUserinfoIdAuthenticateIdSame 用户申请手机号和姓名与魔蝎认证是否一致"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        result = results[0]
        mxidcard = result.get('idcard')
        mxname = result.get('name')
        if not mxidcard and not mxname:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if mxidcard:
            mxidcard = re.compile(u'[\*|＊]{1,}').sub('.*', mxidcard)
            mxidcardpattern = re.compile(r'%s' % mxidcard)
            mxidcardmatch = mxidcardpattern.search(self.info.cert_id)
        else:
            mxidcardmatch = True
        if mxname:
            mxname=mxname.encode('utf-8')
            mxname=mxname.replace('*','').replace('＊','')
            mxnamematch = re.search(r'%s' % mxname,self.info.user_name)
        else:
            mxnamematch = True
        if mxidcardmatch and mxnamematch:
            return 1
        return 0

    def mxUserPhoneInTimeDays(self):
        """mxUserPhoneInTimeDays 手机号入网天数"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        opentime = results[0].get('openTime')
        createtime = results[0].get('dataTime')
        if not opentime or not createtime:
            return self.SET_DEFAULT_VALUE_INT_9999999
        opentime = datetime.datetime.strptime(opentime[:10], "%Y-%m-%d")
        # createtime = datetime.datetime.strptime(createtime[:10], "%Y-%m-%d")
        return (createtime - opentime).days

    def mxMean7dCallCnt(self):
        """mxMean7dCallCnt 最近7天日均通话记录数"""
        results = self.mongo.query_by_user_id_sort_bymyself(db='galaxy',
                                                            collection="mx_carrier_calls",
                                                            find={"user_id": int(self.info.user_id)},
                                                            sort="sort([('create_time',-1),('bill_month',-1)])"
                                                            )

        if not results:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        create_time = results[0].get('create_time')
        if not create_time:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        create_time = datetime.datetime.strptime(create_time[:10] + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
        timeList = []
        time7list = []
        time7before = create_time - datetime.timedelta(days=6)
        for row in results[:6]:
            if row.get('items'):
                for subrow in row.get('items'):
                    callTime = subrow.get('time')
                    if callTime:
                        callTime = datetime.datetime.strptime(callTime, "%Y-%m-%d %H:%M:%S")
                        timeList.append(callTime)
                        if callTime > time7before:
                            time7list.append(callTime)

        interval = (create_time - min(timeList)).days
        if interval < 7:
            return -1.0
        return round(float(len(time7list)) / 7, 1)

    def mxMean90dCallCnt(self):
        """mxMean90dCallCnt 最近90天的日均通话记录数"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        create_time = results[0].get('dataTime')
        if not create_time:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        create_time = return_strfYmd_date(create_time)
        timeList = []
        time90list = []
        time90before = create_time - datetime.timedelta(days=89)
        totalcount=0
        for row in results:
            if row.get('statistic7Daily6M'):
                for subrow in row.get('statistic7Daily6M'):
                    callTime = subrow.get('callDate')
                    if callTime:
                        timeList.append(callTime)
                        if callTime > time90before:
                            callCnt=subrow.get('callCnt')
                            totalcount=totalcount+callCnt
                            time90list.append(callTime)
        interval = (create_time - min(timeList)).days
        if interval < 30:
            return -1.0
        elif 30 <= interval < 90:
            return round(float(totalcount) / interval, 1)
        else:
            return round(results[0].get('avgCallCnt90d'),1)

    def mxContactJyxCnt(self):
        """mxContactJyxCnt 联系人(亲属、朋友/同事)是交易性通话的个数"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        createtime = results[0].get('dataTime')
        createtime = return_strfYmd_date(createtime)
        # time7before = createtime - datetime.timedelta(days=6)
        relativeContact = self.info.relativeContact
        friendContact = self.info.friendContact
        phone_list=results[0].get('pheJyx6m')
        matchphone = []
        for phone in phone_list:
            if phone ==relativeContact or phone==friendContact:
                matchphone.append(phone)
        return len(matchphone)

    def mxIsRequired(self):
        """mxIsRequired 是否是10%的注册客户"""
        sql = "select status from account_diff_record_{0} where customer_id=%s" % self.info.customer_id
        results = self.mysql.queryone_table("facade_center", sql, self.info.customer_id)
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999996
        status = results[0].get('status')
        if status == 1:
            return 0
        if status == 0:
            return 1

    def mxIsExistCarrier(self):
        """mxIsExistCarrier 是否抓取到运营商数据"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if results:
            return 1
        else:
            return 0

    def mxReferCarrierdays(self):
        """mxReferCarrierdays 提交运营商数据的天数"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        createtime = results[0].get('dataTime')
        createtime = return_strfYmd_date(createtime)
        event_time = datetime.datetime.strptime(self.info.event_time.strftime("%Y-%m-%d") + ' 00:00:00',"%Y-%m-%d %H:%M:%S")
        return (event_time - createtime).days

    def __getMxCallList(self):
        list_result = []
        maxOverResult = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not maxOverResult:
            return 0
        else:
            for i in maxOverResult[0].get('statistic7Daily6M'):
                    list_result.append(i)
        return list_result

    def mxCallAge(self):
        """mxCallAge 详单跨度"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})

        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        timelist=[]
        for row in results:
            if row.get('statistic7Daily6M'):
                for subrow in row.get('statistic7Daily6M'):
                    if subrow.get('callDate'):
                        callDate=subrow.get('callDate')
                        timelist.append(callDate)
        timeInterval = (max(timelist) - min(timelist)).days + 1
        return timeInterval

    def __getCallList(self):
        list = []
        envTime = self.info.event_time
        time179 = envTime - datetime.timedelta(days=179)
        time179 = str(time179)[0:10] + " 00:00:00"
        time179 = datetime.datetime.strptime(time179, "%Y-%m-%d %H:%M:%S")
        maxOverResult = self.mongo.query_by_user_id_sort_bymyself(db='galaxy',
                                                            collection="mx_carrier_calls",
                                                            find={"user_id": int(self.info.user_id)},
                                                            sort="sort([('create_time',-1),('bill_month',-1)])"
                                                            )[:6]
        if not maxOverResult:
            return 0
        else:
            for i in maxOverResult:
                for j in i.get('items'):
                    j['time'] = datetime.datetime.strptime(j['time'], "%Y-%m-%d %H:%M:%S")
                    if j['time'] >= time179:
                        list.append(j)
        return list

    def mxCntOutPday(self):
        """mxCntOutPday 日均呼出次数"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        timelist=[]
        totalpheCntDail=0
        for row in results:
            if row.get('statistic7Daily6M'):
                for subrow in row.get('statistic7Daily6M'):
                    if subrow.get('callDate'):
                        callDate=subrow.get('callDate')
                        timelist.append(callDate)
                    if subrow.get('pheCntDail'):
                        callCnt=subrow.get('pheCntDail')
                        totalpheCntDail=totalpheCntDail+callCnt
        timeInterval = (max(timelist) - min(timelist)).days + 1
        if timeInterval == 0:
            return 0.0
        else:
            pDay = round(totalpheCntDail / float(timeInterval),5)
            return pDay

    def mxRtoCntOut5s(self):
        """mxRtoCntOut5s 通话时长在5秒以内的呼出占总呼出次数比"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        count=0
        count5=0
        for row in results:
            if row.get('statistic7Daily6M'):
                for subrow in row.get('statistic7Daily6M'):
                    if subrow.get('dailCntIn5s'):
                        dailCntIn5s=subrow.get('dailCntIn5s')
                        count5=count5+dailCntIn5s
                    if subrow.get('dailCnt'):
                        dailCnt=subrow.get('dailCnt')
                        count=count+dailCnt
            if count == 0:
                return self.SET_DEFAULT_VALUE_INT_9999998
            else:
                return float(count5)/count

    def mxRtoCntOutNight(self):
        """mxRtoCntOutNight 夜间呼出占总呼出次数比"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        count=0
        countNight=0
        for row in results:
            if row.get('statistic7Daily6M'):
                for subrow in row.get('statistic7Daily6M'):
                    if subrow.get('dailCntOnNight'):
                        dailCntOnNight=subrow.get('dailCntOnNight')
                        countNight=countNight+dailCntOnNight
                    if subrow.get('dailCnt'):
                        dailCnt=subrow.get('dailCnt')
                        count=count+dailCnt
            if count == 0:
                return  self.SET_DEFAULT_VALUE_INT_9999998
            else:
                cntOutNight = countNight/float(count)
                return cntOutNight

    # def mxRtoCntPheDuration90(self):
    #     """mxRtoCntPheDuration90 通话跨度大于等于90天的手机号码个数占比"""
    #     results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
    #                                           find={"_id": int(self.info.user_id)})
    #     if not results:
    #         return self.SET_DEFAULT_VALUE_FLOAT_9999999
    #     return results[0].get('rtoPheDuration90d4m')

    def mxSilenceLongest(self):
        """mxSilenceLongest 静默时长"""
        listCall = self.__getMxCallList()
        timeList = []
        if listCall == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            listCall.sort(key = lambda x:x["callDate"])
            for i in listCall:
                time1 = str(i['callDate'])[0:10]
                time1 = datetime.datetime.strptime(time1, "%Y-%m-%d")
                timeList.append(time1)
            if len(timeList)>1:
                longest = max([timeList[i+1]-timeList[i] for i in range(len(timeList)-1)])
                return longest.days
            else:
                return 0

    def mxContactTelephoneCnt(self):
        """mxContactTelephoneCnt 手机号的通话记录数  """
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        totalcount=0
        for row in results:
            if row.get('statistic7Daily6M'):
                for subrow in row.get('statistic7Daily6M'):
                    if subrow.get('pheCntDail'):
                        pheCntDail=subrow.get('pheCntDail')
                        totalcount=totalcount+pheCntDail
                    if subrow.get('pheCntDailed'):
                        pheCntDailed=subrow.get('pheCntDailed')
                        totalcount=totalcount+pheCntDailed
        return totalcount
    # def __getCallList_dial(self):
    #     list_item = []
    #     maxOverResult = self.mongo.query_by_user_id_sort_bymyself(  db='galaxy',
    #                                                                 collection="mx_carrier_calls",
    #                                                                 find={"user_id": int(self.info.user_id)},
    #                                                                 sort="sort([('create_time',-1),('bill_month',-1)])"
    #                                                                 )[:6]
    #     if not maxOverResult:
    #         return self.SET_DEFAULT_VALUE_INT_9999999
    #     create_time=maxOverResult[0].get('create_time')
    #     for i in maxOverResult:
    #         for j in i.get('items'):
    #             if j not in list_item and j.get('dial_type') == "DIAL":
    #                 if len(j['peer_number']) != 5 and not re.search("^(400)", j['peer_number']):
    #                     list_item.append(j)
    #     return list_item,datetime.datetime.strptime(create_time,"%Y-%m-%d %H:%M:%S")

    def mxDial3CallMonthCnt(self):
        """mxDial3CallMonthCnt 过去3个月内每月至少有3通外拨电话（排除5位数客服及400电话）的月份数"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        return results[0].get('dial3MonthCnt90d')

    def mxDialCall1mCnt(self):
        """mxDialCall1mCnt 过去一个月外拨电话的通话次数"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        return results[0].get('dialCnt30d')

    def mxTelRegDistinctCnt(self):
        """mxTelRegDistinctCnt 手机号码是注册客户数（去重）"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results or results[0].get('phe6m')==[]:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        phone_list = results[0].get('phe6m')
        if not phone_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        mobilephone_list = []
        for i in phone_list:
            sql = "select mobilephone from `user` where mobilephone='{0}'".format(factor_encrypt_identity(i))
            sql_result = self.mysql.queryall_by_table_new_only(db='customer_center', sql=sql)
            if sql_result:
                for j in sql_result:
                    mobilephone_list.append(factor_decrypt_identity(j['mobilephone']))
            sql_old = "select mobilephone from s_user where mobilephone='{0}'".format(i)
            sql_old_result = self.mysql.queryall_by_table_new_only(db='xinyongjin', sql=sql_old)
            if sql_old_result:
                for j in sql_old_result:
                    mobilephone_list.append(j['mobilephone'])
        return len(list(set(mobilephone_list)))

    def mxTelDistinctCnt(self):
        """mxTelDistinctCnt 详单手机号码数（去重）"""
        results = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not results or results[0].get('phe6m')==[]:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        phone_list = results[0].get('phe6m')
        return len(phone_list)

    def ph_ent_mth(self):
        """ph_ent_mth 入网时长"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        open_time = data[0].get('openTime')
        if not open_time:
            return self.SET_DEFAULT_VALUE_INT_9999999
        open_time = datetime.datetime.strptime(open_time, "%Y-%m-%d")
        diff_month = calmonths(open_time, self.info.event_time_add8h)
        return diff_month

    def mxMissMonthCnt(self):
        """mxMissMonthCnt 魔蝎通话记录获取失败月份数"""
        result = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",
                                              find={"_id": int(self.info.user_id)})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result[0].get("missMonthCnt",self.SET_DEFAULT_VALUE_INT_9999996)

    # def is_exist_credit_bills(self):
    #     """is_exist_credit_bills 信用卡账单相关因子"""
    #     data = self.mongo.query_by_user_id('galaxy', "mx_email_bills",
    #                                        {"customer_id": self.customer_id, "status": "1"})
    #     if not data:
    #         return self.SET_DEFAULT_VALUE_INT_0
    #     if data[0].get("response") and data[0].get("response").get("bills"):
    #         return self.SET_DEFAULT_VALUE_INT_1
    #     return self.SET_DEFAULT_VALUE_INT_0
    # def __deviceIdTimesShareCnt(self,days,hours):
    #     result=self.mongo.query_by_user_id(db='galaxy',
    #                                           collection="td_risk_service_record",
    #                                           find={"userId": int(self.info.user_id)}
    #                                           )
    #     if not result:
    #         return self.SET_DEFAULT_VALUE_INT_9999999
    #     devece_id_list = []
    #     for i in range(0,len(result)):
    #         ylzh_time = result[i].get('createTime')
    #         decision_time = self.info.result.get('event_time')
    #         if hours!=0:
    #             start_day = decision_time - datetime.timedelta(hours=hours)
    #         if days!=0:
    #             start_day = decision_time - datetime.timedelta(days=days)
    #         if ylzh_time >= start_day and ylzh_time<=decision_time  and result[i].get('deviceId') and result[i].get('deviceId')!=None and result[i].get('deviceId')!="":
    #             devece_id_list.append(result[i].get('deviceId'))
    #     devece_id_list = list(set(devece_id_list))
    #     if devece_id_list==[]:
    #         return 0
    #     return devece_id_list
    def __deviceIdTimesShareCnt1(self,days,hours):
        result=self.mongo.query_by_user_id(db='galaxy',
                                              collection="td_risk_service_record",
                                              find={"userId": int(self.info.user_id)}
                                              )
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        devece_id_list = []
        for i in range(0,len(result)):
            ylzh_time = self.mongo.id2time(result[i].get('_id'))
            decision_time = self.info.result.get('event_time')+datetime.timedelta(hours=8)
            if hours!=0:
                start_day = decision_time - datetime.timedelta(hours=hours)
            if days!=0:
                start_day = decision_time - datetime.timedelta(days=days)
            if ylzh_time >= start_day and ylzh_time<=decision_time  and result[i].get('deviceId') and result[i].get('deviceId')!=None and result[i].get('deviceId')!="":
                devece_id_list.append(result[i].get('deviceId'))
        devece_id_list = list(set(devece_id_list))
        if devece_id_list==[]:
            return 0
        return devece_id_list

    def deviceId24HourShareCnt(self):
        """24h使用的deviceId-最大共用人数 --全产品"""
        # result=self.mongo.query_all_by_userId_beforeEvenTime_inXdays(db='galaxy', collection='td_risk_service_record', find={"userId": int(self.info.user_id)},serial_no=self.serial_no,days=1)
        # if not result:
        #     return self.SET_DEFAULT_VALUE_INT_9999999
        # devece_id_list=[]
        # for x in result:
        #     if x.get('deviceId') and x.get('deviceId')!=None and x.get('deviceId')!="":
        #         devece_id_list.append(x.get('deviceId'))
        # devece_id_list=list(set(devece_id_list))
        if self.__deviceIdTimesShareCnt1(days=1,hours=0)==self.SET_DEFAULT_VALUE_INT_9999999:
            return self.SET_DEFAULT_VALUE_INT_9999999
        elif self.__deviceIdTimesShareCnt1(days=1,hours=0)==0:
            return 0
        else:
            devece_id_list=self.__deviceIdTimesShareCnt1(days=1,hours=0)
        if len(devece_id_list)>5:
            return self.SET_DEFAULT_VALUE_INT_9999997
        count_result_list=[]
        count_list=[]
        for i in devece_id_list:
            count_result=self.mongo.query_all_by_userId_beforeEvenTime_inXdays(db='galaxy', collection='td_risk_service_record', find={"deviceId":i},serial_no=self.serial_no,days=179)
            for row in count_result:
                if row.get('userId'):
                    count_result_list.append(row.get('userId'))
                count_result_list=list(set(count_result_list))
                count_list.append(len(count_result_list))
        return max(count_list)

    def deviceId1HourShareCnt(self):
        """1h使用的deviceId-最大共用人数  --全产品"""
        if self.__deviceIdTimesShareCnt1(days=0,hours=1)==self.SET_DEFAULT_VALUE_INT_9999999:
            return self.SET_DEFAULT_VALUE_INT_9999999
        elif self.__deviceIdTimesShareCnt1(days=0,hours=1)==0:
            return 0
        else:
            devece_id_list=self.__deviceIdTimesShareCnt1(days=0,hours=1)
        if len(devece_id_list) > 5:
            return self.SET_DEFAULT_VALUE_INT_9999997
        count_result_list = []
        count_list = []
        for i in devece_id_list:
            count_result = self.mongo.query_all_by_userId_beforeEvenTime_inXdays(db='galaxy',
                                                                                 collection='td_risk_service_record',
                                                                                 find={"deviceId": i},
                                                                                 serial_no=self.serial_no, days=179)
            for row in count_result:
                if row.get('userId'):
                    count_result_list.append(row.get('userId'))
                count_result_list = list(set(count_result_list))
                count_list.append(len(count_result_list))
        return max(count_list)
    def deviceId24HourCnt(self):
        """24h内使用的设备个数"""
        if self.__deviceIdTimesShareCnt1(days=1,hours=0)==self.SET_DEFAULT_VALUE_INT_9999999:
            return self.SET_DEFAULT_VALUE_INT_9999999
        elif self.__deviceIdTimesShareCnt1(days=1,hours=0)==0:
            return 0
        elif len(self.__deviceIdTimesShareCnt1(days=1,hours=0))>=999:
            return 999
        else:
            devece_id_list=self.__deviceIdTimesShareCnt1(days=1,hours=0)
        return len(devece_id_list)
    def deviceId1HourCnt(self):
        """1h内使用的设备个数"""
        if self.__deviceIdTimesShareCnt1(days=0,hours=1)==self.SET_DEFAULT_VALUE_INT_9999999:
            return self.SET_DEFAULT_VALUE_INT_9999999
        elif self.__deviceIdTimesShareCnt1(days=0,hours=1)==0:
            return 0
        elif len(self.__deviceIdTimesShareCnt1(days=0,hours=1))>=999:
            return 999
        else:
            devece_id_list=self.__deviceIdTimesShareCnt1(days=0,hours=1)
        return len(devece_id_list)


    def __get_mx_carrier_report_fact(self):
        pass

    def __get_mx_carrier_bill_fact(self):
        result = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",find={"_id": int(self.info.user_id)})
        return result

    def billsBaseFee(self):
        """billsBaseFee 本机号码套餐及固定费  --产品:2345借款"""
        result =self.__get_mx_carrier_bill_fact()
        if not result:
            return self.SET_DEFAULT_VALUE_INT_0
        base_bill=[ bill.get("billBaseFee") for bill in result[0].get("billMonth") if bill.get("billBaseFee")]
        return sum(base_bill)

    def calls30dPeerNumberCitys(self):
        """calls30dPeerNumberCitys 近30天内不同通话城市的数量  --产品：2345借款"""
        result=self.__get_mx_carrier_bill_fact()
        if not result:
            return self.SET_DEFAULT_VALUE_INT_0
        city_list=[cell.get("cellLoc").get("city") for cell in result[0].get("pheStatistics") if cell.get("cellLoc") and cell.get("cellLoc").get("city") and  cell.get("callTime") and cell.get("callTime").get("max")+datetime.timedelta(hours=8)>(result[0].get("dataTime")+datetime.timedelta(hours=8)-datetime.timedelta(days=30))]
        return len(list(set(city_list)))

    def calls30dSmsPeernumberCntAvgd(self):
        """calls30dSmsPeernumberCntAvgd 近30天内魔蝎通话记录去重手机号与魔蝎短信里去重手机号交叉的手机号-平均每天通话数量  --产品：2345借款"""
        result=self.__get_mx_carrier_bill_fact()
        if not result:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        return round(result[0].get("calls30dSmsPeernumberCntAvgd"),4)

    def calls5mSmsPeerNumberCntRatio(self):
        """calls5mSmsPeerNumberCntRatio 近5个月魔蝎通话记录去重手机号与魔蝎短信里去重手机号交叉的手机号-通话总数占比  --产品：2345借款"""
        result=self.__get_mx_carrier_bill_fact()
        if not result:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        month_all=[ m.get("month") for m in result[0].get("billMonth")]
        if not month_all:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        max_month=max(month_all)
        callCnt=[call.get("callCnt") for call in result[0].get("statistic7Daily6M") if str(call.get("callDate")+datetime.timedelta(hours=8))[:7]!=max_month]
        phone_5=[phe.get("phe") for phe in result[0].get("pheStatistics") if phe.get("callTime") and phe.get("callTime").get("min") and str(phe.get("callTime").get("min")+datetime.timedelta(hours=8))[:7]!=max_month ]
        sms_phone=[phe.get("phe") for phe in result[0].get("pheStatistics") if phe.get("smsTime") and phe.get("smsTime").get("min") and str(phe.get("smsTime").get("min")+datetime.timedelta(hours=8))[:7]!=max_month]
        phone_set=list(set(phone_5).intersection(set(sms_phone)))
        if not callCnt:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round(float(len(phone_set))/sum(callCnt),4)

    def calls5mSmsPeerNumberRatio(self):
        """calls5mSmsPeerNumberRatio 近5个月魔蝎通话记录去重手机号与魔蝎短信里去重手机号交叉的手机号数占比  --产品：2345借款"""
        result=self.__get_mx_carrier_bill_fact()
        if not result:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        month_all=[ m.get("month") for m in result[0].get("billMonth")]
        if not month_all:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        max_month=max(month_all)
        phone_5=[phe.get("phe") for phe in result[0].get("pheStatistics") if phe.get("callTime") and phe.get("callTime").get("min") and str(phe.get("callTime").get("min"))<max_month]
        sms_phone=[phe.get("phe") for phe in result[0].get("pheStatistics") if phe.get("smsTime") and phe.get("smsTime").get("max")]
        phone_set=list(set(phone_5).intersection(set(sms_phone)))
        if not phone_5:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round(float(len(phone_set))/len(phone_5),4)

    def calls2type20PeerNumberRegisterCnt(self):
        """calls2type20PeerNumberRegisterCnt 魔蝎通话记录通话次数最多的20个手机号、通话时长最多的20个手机号去重后在2345注册的数量  --产品：2345借款"""
        result=self.__get_mx_carrier_bill_fact()
        if not result:
            return self.SET_DEFAULT_VALUE_INT_0
        callCnt=[[cell.get("callCnt"),cell.get("callTime").get("max"),cell.get("phe")] for cell in result[0].get("pheStatistics") if cell.get("callCnt") and cell.get("callTime")]
        callCnt.sort(reverse=True)
        callDuration=[[cell.get("callDuration"),cell.get("callTime").get("max"),cell.get("phe")] for cell in result[0].get("pheStatistics") if cell.get("callDuration") and cell.get("callTime")]
        callDuration.sort(reverse=True)
        phe_list=[str(i[2]) for i in callCnt[:20]]+[str(i[2]) for i in callDuration[:20]]
        phe_list_only=list(set(phe_list))
        phe_list_encrypt =[factor_encrypt_identity(i) for i in phe_list_only]
        cnt = self.mysql.queryone_by_customer_id('customer_center',"select count(*) as cnt from user where mobilephone in ('{0}') and delete_flag=0".format('\',\''.join(phe_list_encrypt)))
        return cnt.get("cnt")

    def __getOldMxCallList(self):
        list_result = []
        maxOverResult = self.mongo.query_by_user_id_sort_bymyself(db='galaxy',
                                                            collection="mx_carrier_calls",
                                                            find={"user_id": int(self.info.user_id)},
                                                            sort="sort([('create_time',-1),('bill_month',-1)])"
                                                            )[:6]
        if not maxOverResult:
            return 0
        for i in maxOverResult:
            for j in i.get('items'):
                if j not in list_result:
                    list_result.append(j)
        return list_result

    def callsBothPeerNumberDiff(self):
        """callsBothPeerNumberDiff  比较相同时间段内，魔蝎通话记录、内部通话记录的去重手机号数量差值 --产品：2345借款"""
        mx_result=self.__getOldMxCallList()
        if not mx_result:return self.SET_DEFAULT_VALUE_INT_9999999
        mx_call_time=[call.get("time") for call in mx_result]
        mx_min=datetime.datetime.strptime(min(mx_call_time), "%Y-%m-%d %H:%M:%S")
        mx_max=datetime.datetime.strptime(max(mx_call_time), "%Y-%m-%d %H:%M:%S")
        result_contact_action=self.mongo.query_by_user_id(  db='lake',
                                                            collection='s_user_mobile_contact_action_%d'%(int(self.info.user_id)%4),
                                                            find={'user_id':self.info.user_id})
        if not result_contact_action:
            return self.SET_DEFAULT_VALUE_INT_9999999
        lake_phone=[phone.get("callTime") for phone in result_contact_action[0].get("actions")]
        if not lake_phone:return self.SET_DEFAULT_VALUE_INT_9999999
        org_max_time=min([mx_max,max(lake_phone)])
        org_min_time=max([mx_min,min(lake_phone)])
        org_mx_phone=[phone_clean_new(phoneClear(call.get("peer_number"))) for call in mx_result if  org_min_time <=datetime.datetime.strptime(call.get("time"), "%Y-%m-%d %H:%M:%S")<= org_max_time and phoneClear(call.get("peer_number")) and phone_clean_new(phoneClear(call.get("peer_number")))]
        ord_lake_phone=[phone_clean_new(phoneClear(phone.get("callNumber"))) for phone in result_contact_action[0].get("actions") if org_min_time <= phone.get("callTime") <= org_max_time and phoneClear(phone.get("callNumber")) and phone_clean_new(phoneClear(phone.get("callNumber")))]
        return len(list(set(org_mx_phone))) -len(list(set(ord_lake_phone)))

    def nets30dDawnCntRatioAvgd(self):
        """nets30dDawnCntRatioAvgd 流量-近30天每天凌晨使用次数占比平均值  --产品：2345借款"""
        data = self.__get_mx_carrier_bill_fact()
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        nets_list = [[i.get("date"),i.get("cntOnNight"),i.get("cnt")] for i in data[0]["netDaily"]]
        if not nets_list:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        sum_nets_on_night = [ net[1] for net in nets_list if net[0]>(data[0].get("dataTime")+datetime.timedelta(hours=8) - datetime.timedelta(days=30))]
        sum_nets_cnt=[ net[2] for net in nets_list if net[0]>(data[0].get("dataTime")+datetime.timedelta(hours=8) - datetime.timedelta(days=30))]
        if sum(sum_nets_cnt)==0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round(float(sum(sum_nets_on_night))/sum(sum_nets_cnt),4)

    def netsCntStdd(self):
        """netsCntStdd 流量-每天使用次数标准差  --产品：2345借款"""
        data = self.__get_mx_carrier_bill_fact()
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_0
        nets_cnt_list = [i.get("cnt") for i in data[0]["netDaily"]]
        if not nets_cnt_list:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        if len(nets_cnt_list)==1:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(float(np.std(nets_cnt_list,ddof=1)),4)

    def netsDawnDurationRatioAvgd(self):
        """netsDawnDurationRatioAvgd 流量-每天凌晨使用时长占比平均值  --产品：2345借款"""
        data = self.__get_mx_carrier_bill_fact()
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        durationOnNight = [i.get("durationOnNight") for i in data[0]["netDaily"] if i.get("date") ]
        duration = [i.get("duration") for i in data[0]["netDaily"] if i.get("date")]
        if not duration or sum(duration)==0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round(float(sum(durationOnNight))/sum(duration),4)

    def packages5mFlowUseRatio(self):
        """packages5mFlowUseRatio 近5个月流量已使用占比  --产品：2345借款"""
        data = self.__get_mx_carrier_bill_fact()
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        bill_month = [[i.get("month"),i.get("netUsed"),i.get("netTotal")] for i in data[0]["billMonth"] if i.get("month")]
        if not bill_month:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        bill_month.sort()
        bill_month_5 = bill_month[-2::-1]
        sum_net_used  = [i[1] for i in bill_month_5 if i[1]]
        sum_net_total =[i[2] for i in bill_month_5 if i[2]]

        if not sum_net_total:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return  round(float(sum(sum_net_used))/sum(sum_net_total),4)

    def smses30dCntRatio(self):
        """smses30dCntRatio (近5个月平均每月魔蝎短信记录总数-近30天内的魔蝎短信记录总数)/近30天内的魔蝎短信记录总数  --产品：2345借款"""
        data = self.__get_mx_carrier_bill_fact()
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        bill_month = [[i.get("month"),i.get("smsCnt")] for i in data[0]["billMonth"] if i.get("month")]
        if not bill_month:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        bill_month.sort()
        if not bill_month:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        bill_month_5 = bill_month[-2::-1]
        if not bill_month_5:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        sum_net_used = [i[1] for i in bill_month_5 if i[1]]
        if not sum_net_used:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        avg_5_month=  round(float(sum(sum_net_used))/len(sum_net_used),4)
        pre_30_sms=[sms.get("cnt") for sms in data[0]["smsDaily"] if sms.get("date") and sms.get("date")> (data[0].get("dataTime")+datetime.timedelta(hours=8)-datetime.timedelta(days=30))]
        if not pre_30_sms:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round((avg_5_month-sum(pre_30_sms))/sum(pre_30_sms),4)

    def smses30dPeerNumberOutRatio(self):
        """smses30dPeerNumberOutRatio (近5个月发送平均每月魔蝎短信记录去重手机号总数-近30天内发送魔蝎短信记录去重手机号总数)/近30天内发送魔蝎短信记录去重手机号总数  --产品：2345借款"""
        data = self.__get_mx_carrier_bill_fact()
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        bill_month = [[i.get("month"),i.get("smsSendPheCnt")] for i in data[0]["billMonth"] if i.get("month")]
        if not bill_month:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        bill_month.sort()
        bill_month_5 = bill_month[-2::-1]
        sum_net_used = [i[1] for i in bill_month_5]
        if not sum_net_used:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        avg_5_month=  round(float(sum(sum_net_used))/len(sum_net_used),4)

        pre_30_smsSend=[ph.get("phe")for ph in data[0]["pheStatistics"] if ph.get("smsSendTime") and ph.get("smsSendTime").get("max")> (data[0].get("dataTime")+datetime.timedelta(hours=8)-datetime.timedelta(days=30))]
        if len(pre_30_smsSend)==0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round((avg_5_month-len(pre_30_smsSend))/len(pre_30_smsSend),4)

    def callsPeerNumberCitys(self):
        """callsPeerNumberCitys 不同通话城市的数量   --产品：2345借款"""
        data = self.__get_mx_carrier_bill_fact()
        if not data:
            return self.SET_DEFAULT_VALUE_INT_0
        city_list = [ph.get("cellLoc").get("city") for ph in data[0]["pheStatistics"] if ph.get("cellLoc") if ph.get("callTime")]
        return len(list(set(city_list)))

    def callsUnmatchedPeerNumberContactRatio(self):
        """callsUnmatchedPeerNumberContactRatio 比较相同时间段内，魔蝎通话记录未匹配数据-手机号在内部通讯录里的手机号总数占比"""
        data = self.__get_mx_carrier_bill_fact()
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        phone_min_max = []
        [phone_min_max.append([i.get("phe"), i.get("callTime").get("min"), i.get("callTime").get("max")]) for i in data[0]["pheStatistics"] if i.get("callTime")]
        result_contact_action = self.mongo.query_by_user_id(db='lake',
                                                            collection="s_user_mobile_contact_action_{0}".format(self.info.user_id % 4),
                                                            find={"user_id": int(self.info.user_id)})
        if not result_contact_action:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        contact_action_callTime=[phone.get("callTime") for phone in result_contact_action[0].get("actions") if phoneClear(phone.get("callNumber")) and phone_clean_new(phoneClear(phone.get("callNumber")))]
        if not contact_action_callTime:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        contact_list=self.mongo.query_contact_list_beforeEvenTime_inXdays(db='lake',
                                                                          collection="s_user_mobile_contact_{0}".format(self.info.user_id % 4),
                                                                          find={"user_id": int(self.info.user_id)},
                                                                          serial_no=self.serial_no,
                                                                          days=180,clean=False,allData=False)
        if contact_list=='No DATA':
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        mx_contact_list=[phe for phe in phone_min_max if phe[0] in contact_list and (phe[1] < min(contact_action_callTime) or phe[2] > max(contact_action_callTime))]
        if not contact_list:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round(float(len(mx_contact_list)) / len(contact_list), 4)

    def smsessPeerNumberRegisterCnt(self):
        """smsessPeerNumberRegisterCnt 魔蝎短信里的手机号在2345测额前注册的数量"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",find={"_id": int(self.info.user_id)})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_0
        phone_list = set()
        [phone_list.add(factor_encrypt_identity(ph.get("phe"))) for ph in data[0]["pheStatistics"] if "smsTime" in ph.keys()]
        cnt = self.mysql.queryone_by_customer_id('customer_center',"select count(*) as cnt from user where mobilephone in ('{0}') and delete_flag = 0" .format('\',\''.join(phone_list)))
        return cnt.get("cnt")

    def smsesSamecityPeerNumberRatio(self):
        """smsesSamecityPeerNumberRatio 相同魔蝎短信城市的魔蝎短信记录手机号数量占比"""
        data = self.mongo.query_by_user_id(db='feature_bone', collection="mx_carrier_bill_fact",find={"_id": int(self.info.user_id)})
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        user_city = self.mysql.queryone_by_customer_id('skynet','select city from dict_mobile_location where mobile = \'%s\'' % (data[0]["mobile"][:7]))
        phone_all = []
        [phone_all.append(ph.get("phe")) for ph in data[0]["pheStatistics"] if "smsTime" in ph.keys()]
        phone_list = []
        [phone_list.append([ph.get("phe"),ph.get("cellLoc").get("city")]) for ph in data[0]["pheStatistics"] if "smsTime" in ph.keys() and ph.get("cellLoc") and ph.get("cellLoc").get("city")==user_city.get("city")]
        if not phone_all:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round(float(len(phone_list))/len(phone_all),4)


if __name__ == "__main__":
    serial_no = "1552879603088-4962176DEA4B06B3394F61479C14BEB7"
    a = MXFactorV2('T1', serial_no)
    print a.calls2type20PeerNumberRegisterCnt()