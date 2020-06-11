# coding:utf-8
from FrameRunner.FactorInit import NewFactorInit
from utils.otherUtil import *
from utils.TestInit import factor_encrypt_identity,factor_decrypt_identity
class MXFactor(NewFactorInit):
    def __init__(self, env, serial_no):
        super(MXFactor,self).__init__(env, serial_no)

    def user_authenticate_phone(self):
        """user_authenticate_phone 客户授权手机号"""
        data = self.mongo.query_by_user_id(db='galaxy',
                                           collection="mx_carrier_basic_message",
                                           find={"user_id": self.info.user_id})
        if len(data) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return data[0]['mobile']

    def user_phone_in_time_days(self):
        """user_phone_in_time_days 手机号入网时间"""
        data = self.mongo.query_by_user_id('galaxy', "mx_carrier_basic_message",{"user_id": self.info.user_id})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        open_time = data[0].get('open_time')
        if not open_time:
            return self.SET_DEFAULT_VALUE_INT_9999999
        open_time = datetime.datetime.strptime(open_time, "%Y-%m-%d")
        days = (self.info.event_time_add8h - open_time).days
        return days

    def call_detail_distinct_cnt_6m(self):
        """call_detail_distinct_cnt_6m 魔蝎详单通话手机号码个数"""
        data = self.mongo.query_by_user_id('galaxy', "mx_carrier_report_notify",
                                           {"user_id": self.info.user_id, "status": "1"})
        if len(data) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        last_one = data[0]
        if not last_one.get('response') or not last_one.get('response').get('active_degree'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        for active_degree in last_one.get('response').get('active_degree'):
            if active_degree['app_point'] == 'peer_num_cnt':
                return active_degree['item']['item_6m']
        return self.SET_DEFAULT_VALUE_INT_9999999

    def call_detail_cnt_6m(self):
        """call_detail_cnt_6m 魔蝎详单累计手机号码通话次数（不去重）（不包含通话时间为0）"""
        data = self.mongo.query_by_user_id(db='galaxy',
                                           collection="mx_carrier_report_notify",
                                           find={"user_id": self.info.user_id, "status": "1"})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not data[0].get("response") or not data[0].get("response").get("active_degree"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for active_degree in data[0]['response']['active_degree']:
            if active_degree['app_point'] == 'call_cnt':
                return active_degree['item']['item_6m']
        return self.SET_DEFAULT_VALUE_INT_9999999

    def phone_avg_fee_6m(self):
        """phone_avg_fee_6m 手机月均话费（单位:元，四舍五入精确到元）"""
        data = self.mongo.query_by_user_id(db='galaxy',
                                           collection="mx_carrier_report_notify",
                                           find={"user_id": self.info.user_id, "status":"1"})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not data[0].get("response") or not data[0].get("response").get("consumption_detail"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for consumption_detail in data[0]['response']['consumption_detail']:
            if consumption_detail['app_point'] == 'total_fee':
                return int(round(int(consumption_detail['item']['avg_item_6m']) / 100.0))
        return self.SET_DEFAULT_VALUE_INT_9999999

    def call_macao_cnt_6m(self):
        """call_macao_cnt_6m 澳门通话次数"""
        data = self.mongo.query_by_user_id(db='galaxy',
                                           collection="mx_carrier_report_notify",
                                           find={"user_id": self.info.user_id, "status":"1"})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not data[0].get("response") or not data[0].get("response").get("call_risk_analysis"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for call_risk in data[0]['response']['call_risk_analysis']:
            if call_risk['analysis_item'] == 'macao':
                return int(call_risk['analysis_point']['call_cnt_6m'])
        return self.SET_DEFAULT_VALUE_INT_9999999

    def contact_call_mutual_cnt_6m(self):
        """contact_call_mutual_cnt_6m 通讯录中互通过电话的手机号码数量"""
        data = self.mongo.query_by_user_id('galaxy', "mx_carrier_report_notify",
                                           {"user_id": self.info.user_id, "status": "1"})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        peer_num_list = []
        for call_contact_detail in data[0]['response']['call_contact_detail']:
            if call_contact_detail['dial_cnt_6m'] != 0 and call_contact_detail['dialed_cnt_6m'] != 0:
                peer_num_list.append(phoneClean(call_contact_detail['peer_num']))
        data = self.mongo.query_by_user_id_30days('lake', "s_user_mobile_contact_{0}".format(self.info.user_id % 4),
                                                  {"user_id": self.info.user_id}, self.serial_no)
        if len(data) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        contact_num_list = []
        if not data[0].get('contacts'):
            return 0
        for contact in data[0]['contacts']:
            phone1 = contact.get('phone1')
            phone2 = contact.get('phone2')
            phone3 = contact.get('phone3')
            phone1 = sxjPhoneVaild(phone1)
            phone2 = sxjPhoneVaild(phone2)
            phone3 = sxjPhoneVaild(phone3)

            if phone1 and phone1 not in contact_num_list: contact_num_list.append(phone1)
            if phone2 and phone2 not in contact_num_list: contact_num_list.append(phone2)
            if phone3 and phone3 not in contact_num_list: contact_num_list.append(phone3)

        contact_num_list = list(set(contact_num_list))
        union = list((set(peer_num_list).union(set(contact_num_list))) ^ (set(peer_num_list) ^ set(contact_num_list)))
        return len(union)


    def __call_contact_mx(self):
        data = self.mongo.query_by_user_id('galaxy', "mx_carrier_report_notify",{"user_id": self.info.user_id, "status": "1"})
        if not data:
            return
        return data[0]


    def call_relative_last_time(self):
        """call_relative_last_time 近6个月与联系人1最晚通话沟通时间 """
        # print self.info.relativeContact
        call_result=self.__call_contact_mx()
        if not call_result:
            return "0000-12-29 16:00:00"
        for call_contact_detail in call_result['response']['call_contact_detail']:
            if call_contact_detail['peer_num'] == self.info.relativeContact:
                return datetime.datetime.strptime(call_contact_detail['trans_end'],"%Y-%m-%d %H:%M:%S")-datetime.timedelta(hours=8)
        return "0000-12-29 16:00:00"

    def call_friend_last_time(self):
        """call_friend_last_time 近6个月与联系人2最晚通话沟通时间 """
        # print self.info.friendContact
        call_result=self.__call_contact_mx()
        if not call_result:
            return "0000-12-29 16:00:00"
        for call_contact_detail in call_result['response']['call_contact_detail']:
            if call_contact_detail['peer_num'] == self.info.friendContact:
                return datetime.datetime.strptime(call_contact_detail['trans_end'],"%Y-%m-%d %H:%M:%S")-datetime.timedelta(hours=8)
        return "0000-12-29 16:00:00"

    def call_colleague_last_time(self):
        """call_colleague_last_time 近6个月与联系人3最晚通话沟通时间"""
        # print self.info.colleagueContact
        call_result=self.__call_contact_mx()
        if not call_result:
            return "0000-12-29 16:00:00"
        for call_contact_detail in call_result['response']['call_contact_detail']:
            if call_contact_detail['peer_num'] == self.info.colleagueContact:
                return datetime.datetime.strptime(call_contact_detail['trans_end'],"%Y-%m-%d %H:%M:%S")-datetime.timedelta(hours=8)
        return "0000-12-29 16:00:00"

    def call_relative_cnt_6m(self):
        """call_relative_cnt_6m 近6个月与联系人1通话次数 """
        call_result=self.__call_contact_mx()
        if not call_result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        for call_contact_detail in call_result['response']['call_contact_detail']:
            if call_contact_detail['peer_num'] == self.info.relativeContact:
                return call_contact_detail['call_cnt_6m']
        return self.SET_DEFAULT_VALUE_INT_9999999

    def call_friend_cnt_6m(self):
        """call_friend_cnt_6m 近6个月与联系人2通话次数"""
        call_result=self.__call_contact_mx()
        if not call_result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        for call_contact_detail in call_result['response']['call_contact_detail']:
            if call_contact_detail['peer_num'] == self.info.friendContact:
                return call_contact_detail['call_cnt_6m']
        return self.SET_DEFAULT_VALUE_INT_9999999

    def call_colleague_cnt_6m(self):
        """call_colleague_cnt_6m 近6个月与联系人3通话次数"""
        call_result=self.__call_contact_mx()
        if not call_result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        for call_contact_detail in call_result['response']['call_contact_detail']:
            if call_contact_detail['peer_num'] == self.info.colleagueContact:
                return call_contact_detail['call_cnt_6m']
        return self.SET_DEFAULT_VALUE_INT_9999999

    def userinfo_phone_name(self):
        """userinfo_phone_name 客户授权手机号姓名"""
        data = self.mongo.query_by_user_id('galaxy', "mx_carrier_basic_message",
                                           {"user_id": self.info.user_id})
        if len(data) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return data[0]['name']

    def call_age(self):
        """call_age 最早通话日期与最晚通话日期差值+1"""
        data = self.mongo.query_by_user_id('galaxy', "mx_carrier_bills_notify",
                                           {"user_id": self.info.user_id, "status": "1"})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        time_list = []
        for calls in data[0]['response']['calls'][:4]:
            for items in calls['items']:
                item_time = datetime.datetime.strptime(items['time'], "%Y-%m-%d %H:%M:%S")
                date = datetime.date(item_time.year, item_time.month, item_time.day)
                time_list.append(date)
        # print max(time_list),min(time_list)
        diff_days = (max(time_list) - min(time_list)).days + 1
        return diff_days

    def silence_longest(self):
        """silence_longest 静默时长(近四个月)"""
        data = self.mongo.query_by_user_id('galaxy', "mx_carrier_bills_notify",
                                           {"user_id": self.info.user_id, "status": "1"})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        date_list = []
        for calls in data[0]['response']['calls'][:4]:
            for items in calls['items']:
                item_time = datetime.datetime.strptime(items['time'], "%Y-%m-%d %H:%M:%S")
                date = datetime.date(item_time.year, item_time.month, item_time.day)
                date_list.append(date)
        date_list = list(set(date_list))
        date_list.sort(reverse=True)
        diff_list = []
        for i in xrange(len(date_list) - 1):
            diff_list.append((date_list[i] - date_list[i + 1]).days)
        return max(diff_list)

    def rto_cnt_phe_duration90(self):
        """rto_cnt_phe_duration90 通话跨度大于等于90天的手机号码个数比"""
        data = self.mongo.query_by_user_id('galaxy', "mx_carrier_bills_notify",
                                           {"user_id": self.info.user_id, "status": "1"})
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        total_phone_list = {}
        peer_num_list = []
        for calls in data[0]['response']['calls'][:4]:
            for items in calls['items']:
                item_time = datetime.datetime.strptime(items['time'], "%Y-%m-%d %H:%M:%S")
                date = datetime.date(item_time.year, item_time.month, item_time.day)
                if phone_clean_new(items['peer_number'])and  phone_clean_new(items['peer_number'])in total_phone_list:
                    total_phone_list[phone_clean_new(items['peer_number'])].append(date)
                else:
                    total_phone_list[phone_clean_new(items['peer_number'])] = [date]
        for phone, date_list in total_phone_list.items():
            if (max(date_list) - min(date_list)).days >= 90:
                peer_num_list.append(phone)
        return len(peer_num_list) / float(len(total_phone_list))

    def rto_cnt_out_5s(self):
        """rto_cnt_out_5s 通话时长在5秒以内的呼出占总呼出次数比"""
        data = self.mongo.query_by_user_id('galaxy', "mx_carrier_bills_notify",
                                           {"user_id": self.info.user_id, "status": "1"})
        if not data:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        dial_count = 0
        dial_count_5s = 0
        for calls in data[0]['response']['calls'][:4]:
            for items in calls['items']:
                if items['dial_type'] == 'DIAL':
                    dial_count += 1
                    if items['duration'] <= 5:
                        dial_count_5s += 1
        if dial_count==0:
            return self.SET_DEFAULT_VALUE_INT_9999998
        # print dial_count,dial_count_5s
        return round(float(dial_count_5s) /dial_count,4)

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


    def call_macao_month_cnt_6m(self):
        """call_macao_month_cnt_6m 澳门通话出现的月数"""
        maxOverResult = self.mongo.query_by_user_id_sort_bymyself(db='galaxy',
                                                                  collection="mx_carrier_calls",
                                                                  find={"user_id": int(self.info.user_id)},
                                                                  sort="sort([('create_time',-1),('bill_month',-1)])"
                                                                  )[:6]
        if not maxOverResult:
            return self.SET_DEFAULT_VALUE_INT_9999999
        macao_phone_month = []
        aCount = 0
        for unit in maxOverResult:
            if unit.get('items'):
                for item in unit.get('items'):
                    if item.get('peer_number').startswith('00853') and item not in macao_phone_month:
                        aCount += 1
                        break
        return aCount

    def mxRtoCntNight(self):
        """mxRtoCntNight 夜间通话次数占比"""
        total_call_inXdays_list = []
        total_call_inXdays_call_time_list = []
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
                    timeinDb = datetime.datetime.strptime(subrow.get('time'), "%Y-%m-%d %H:%M:%S")
                    if timeinDb not in total_call_inXdays_call_time_list and timeinDb >= time179:
                        total_call_inXdays_list.append(subrow)
                        total_call_inXdays_call_time_list.append(timeinDb)
        cnt = 0
        for row in total_call_inXdays_call_time_list:
            callTime_h = int(row.strftime('%H'))
            if callTime_h in (0, 1, 2, 3, 4, 5, 6):
                cnt += 1
        if len(total_call_inXdays_call_time_list)==0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return float(cnt) / len(total_call_inXdays_call_time_list)

    def mxRtoPhePOut(self):
        """mxRtoPhePOut 呼出手机号码占比"""
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
        if len(total_call_inXdays_call_time_dic)==0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return float(len(total_call_inXdays_call_time_dic) - len(phoneIn)) / len(total_call_inXdays_call_time_dic)

    def mxUserinfoPhoneAuthenticatePhSame(self):
        """mxUserinfoPhoneAuthenticatePhSame 用户申请手机号与魔蝎认证号是否一致"""
        results = self.mongo.query_by_user_id(db='galaxy',
                                              collection="mx_carrier_basic_message",
                                              find={"user_id": int(self.info.user_id)}
                                              )
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
        results = self.mongo.query_by_user_id(db='galaxy',
                                              collection="mx_carrier_basic_message",
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        result = results[0]
        mxidcard = result.get('idcard')
        mxname = result.get('name')
        if not mxidcard and not mxname:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if mxidcard:
            mxidcard = re.compile(u'[\*|＊] {1,}').sub('.*', mxidcard)
            mxidcardpattern = re.compile(r'%s' % mxidcard)
            mxidcardmatch = mxidcardpattern.search(self.info.cert_id)
        else:
            mxidcardmatch = True
        if mxname:
            mxname = re.compile(u'[\*|＊]{1,}').sub('.*', mxname)
            mxnamepattern = re.compile(r'%s' % mxname)
            mxnamematch = mxnamepattern.search(self.info.user_name)
        else:
            mxnamematch = True
        if mxidcardmatch and mxnamematch:
            return 1
        return 0

    def mxUserPhoneInTimeDays(self):
        """mxUserPhoneInTimeDays 手机号入网天数"""
        results = self.mongo.query_by_user_id(db='galaxy',
                                              collection="mx_carrier_basic_message",
                                              find={"user_id": int(self.info.user_id)}
                                              )
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        opentime = results[0].get('open_time')
        createtime = results[0].get('create_time')
        if not opentime or not createtime:
            return self.SET_DEFAULT_VALUE_INT_9999999
        opentime = datetime.datetime.strptime(opentime[:10], "%Y-%m-%d")
        createtime = datetime.datetime.strptime(createtime[:10], "%Y-%m-%d")
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
        time90list = []
        time90before = create_time - datetime.timedelta(days=89)
        for row in results[:6]:
            if row.get('items'):
                for subrow in row.get('items'):
                    callTime = subrow.get('time')
                    if callTime:
                        callTime = datetime.datetime.strptime(callTime, "%Y-%m-%d %H:%M:%S")
                        timeList.append(callTime)
                        if callTime > time90before:
                            time90list.append(callTime)
        interval = (create_time - min(timeList)).days
        if interval < 30:
            return -1.0
        elif 30 <= interval < 90:
            return round(float(len(time90list)) / interval, 1)
        else:
            return round(float(len(time90list)) / 90, 1)

    def mxContactJyxCnt(self):
        """mxContactJyxCnt 联系人(亲属、朋友/同事)是交易性通话的个数"""
        results = self.mongo.query_by_user_id_sort_bymyself(db='galaxy',
                                                            collection="mx_carrier_calls",
                                                            find={"user_id": int(self.info.user_id)},
                                                            sort="sort([('create_time',-1),('bill_month',-1)])"
                                                            )
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        createtime = results[0].get('create_time')
        createtime = datetime.datetime.strptime(createtime[:10] + ' 00:00:00', "%Y-%m-%d %H:%M:%S")

        time7before = createtime - datetime.timedelta(days=6)
        relativeContact = self.info.relativeContact
        friendContact = self.info.friendContact
        phonedict = {}
        for row in results[:6]:
            if row.get("items"):
                for subrow in row.get("items"):
                    time1 = datetime.datetime.strptime(subrow.get('time'), "%Y-%m-%d %H:%M:%S")
                    if subrow.get('peer_number') not in phonedict:
                        phonedict[subrow.get('peer_number')] = [time1]
                    else:
                        phonedict[subrow.get('peer_number')].append(time1)

        matchphone = []
        for phone, calltime in phonedict.items():
            if phone in (friendContact, relativeContact) and min(calltime) >= time7before:
                matchphone.append([phone, min(calltime)])
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
        results = self.mongo.query_by_user_id_sort_bymyself(db='galaxy',
                                                            collection="mx_carrier_calls",
                                                            find={"user_id": int(self.info.user_id)},
                                                            sort="sort([('create_time',-1),('bill_month',-1)])"
                                                            )
        if results:
            return 1
        else:
            return 0

    def mxReferCarrierdays(self):
        """mxReferCarrierdays 提交运营商数据的天数"""
        results = self.mongo.query_by_user_id_sort_bymyself(db='galaxy',
                                                            collection="mx_carrier_calls",
                                                            find={"user_id": int(self.info.user_id)},
                                                            sort="sort([('create_time',-1),('bill_month',-1)])"
                                                            )

        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        createtime = results[0].get('create_time')
        createtime = datetime.datetime.strptime(createtime[:10] + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
        event_time = datetime.datetime.strptime(self.info.event_time.strftime("%Y-%m-%d") + ' 00:00:00',"%Y-%m-%d %H:%M:%S")
        return (event_time - createtime).days

    def __getMxCallList(self):
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

    def mxCallAge(self):
        """mxCallAge 详单跨度"""
        timeList = []
        list_data = self.__getMxCallList()
        if list_data == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            for i in list_data:
                timeList.append(datetime.datetime.strptime(i['time'],'%Y-%m-%d %H:%M:%S'))
            timeInterval = (max(timeList) - min(timeList)).days + 1
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
        count = 0
        list = self.__getCallList()
        if list == 0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        else:
            callage = self.mxCallAge()
            for i in list:
                if i['dial_type'] == 'DIAL':
                    count += 1
            if count == 0:
                return 0.0
            else:
                pDay = round(count/float(callage),5)
                return pDay

    def mxRtoCntOut5s(self):
        """mxRtoCntOut5s 通话时长在5秒以内的呼出占总呼出次数比"""
        count = 0
        count5 = 0
        list = self.__getMxCallList()
        if list == 0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        else:
            for i in list:
                if i['dial_type'] == 'DIAL':
                    count += 1
                    if i['duration'] <= 5:
                        count5 += 1
            if count == 0:
                return self.SET_DEFAULT_VALUE_INT_9999998
            else:
                return float(count5)/count

    def mxRtoCntOutNight(self):
        """mxRtoCntOutNight 夜间呼出占总呼出次数比"""
        count = 0
        countNight = 0
        list = self.__getMxCallList()
        if list == 0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        else:
            for i in list:
                if i['dial_type'] == 'DIAL':
                    count += 1
                    time = i['time']
                    time=datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                    time1 = str(time)[0:10] + " 00:00:00"
                    time1 = datetime.datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
                    time2 = str(time)[0:10] + " 07:00:00"
                    time2 = datetime.datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")
                    if time >= time1 and time <= time2:
                        countNight += 1
            if count == 0:
                return  self.SET_DEFAULT_VALUE_INT_9999998
            else:
                cntOutNight = countNight/float(count)
                return cntOutNight

    def mxRtoCntPheDuration90(self):
        """mxRtoCntPheDuration90 通话跨度大于等于90天的手机号码个数占比"""
        listPhone = []
        listPhone2 = []
        listPhoneRecord = []
        listPhoneRecord2=[]
        listCall = self.__getMxCallList()
        if listCall == 0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        else:
            for i in listCall:
                listPhone.append(i['peer_number'])
            listPhone = list(set(listPhone))
            for i in listPhone:
                i = sxjPhoneVaild(i)
                if i:
                    listPhone2.append(i)
            count = len(listPhone2)
            for i in listCall:
                for j in listCall:
                    time1 = str(i['time'])[0:10]
                    time3 = datetime.datetime.strptime(time1, "%Y-%m-%d")
                    time2 = str(j['time'])[0:10]
                    time4 = datetime.datetime.strptime(time2, "%Y-%m-%d")
                    if i['peer_number'] == j['peer_number'] and abs((time3-time4).days) >= 90:
                        listPhoneRecord.append(j['peer_number'])

            listPhoneRecord = list(set(listPhoneRecord))
            for i in listPhoneRecord:
                i = sxjPhoneVaild(i)
                if i:
                    listPhoneRecord2.append(i)
            count90 = len(listPhoneRecord2)
            cntDuration90 = count90/float(count)
            return cntDuration90

    def mxSilenceLongest(self):
        """mxSilenceLongest 静默时长"""
        listCall = self.__getMxCallList()
        timeList = []
        if listCall == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            listCall.sort(key = lambda x:x["time"])
            for i in listCall:
                time1 = str(i['time'])[0:10]
                time1 = datetime.datetime.strptime(time1, "%Y-%m-%d")
                timeList.append(time1)
            longest = max([timeList[i+1]-timeList[i] for i in range(len(timeList)-1)])
            return longest.days

    def mxContactTelephoneCnt(self):
        """mxContactTelephoneCnt 手机号的通话记录数  """
        result = self.__getCallList()
        if not result or result == self.SET_DEFAULT_VALUE_INT_9999999 or result == []:
            return self.SET_DEFAULT_VALUE_INT_9999999
        clean_phone=[]
        for i in result:
            if phone_clean(i.get('peer_number')):
                clean_phone.append(i.get('peer_number'))
        return len(clean_phone)

    def __getCallList_dial(self):
        list_item = []
        maxOverResult = self.mongo.query_by_user_id_sort_bymyself(  db='galaxy',
                                                                    collection="mx_carrier_calls",
                                                                    find={"user_id": int(self.info.user_id)},
                                                                    sort="sort([('create_time',-1),('bill_month',-1)])"
                                                                    )[:6]
        if not maxOverResult:
            return self.SET_DEFAULT_VALUE_INT_9999999
        create_time=maxOverResult[0].get('create_time')
        for i in maxOverResult:
            for j in i.get('items'):
                if j not in list_item and j.get('dial_type') == "DIAL":
                    if len(j['peer_number']) != 5 and not re.search("^(400)", j['peer_number']):
                        list_item.append(j)
        return list_item,datetime.datetime.strptime(create_time,"%Y-%m-%d %H:%M:%S")

    def mxDial3CallMonthCnt(self):
        """mxDial3CallMonthCnt 过去3个月内每月至少有3通外拨电话（排除5位数客服及400电话）的月份数"""
        if self.__getCallList_dial()==self.SET_DEFAULT_VALUE_INT_9999999:
            return self.SET_DEFAULT_VALUE_INT_9999999
        result,create_time = self.__getCallList_dial()
        if not result or result == self.SET_DEFAULT_VALUE_INT_9999999:
            return self.SET_DEFAULT_VALUE_INT_9999999
        time_list = []
        count = count_29 = count_59 = count_89 = 0
        time_29 = datetime.datetime.strptime(str(create_time - datetime.timedelta(days=29))[0:10] + " 00:00:00",
                                             "%Y-%m-%d %H:%M:%S")
        time_59 = datetime.datetime.strptime(str(create_time - datetime.timedelta(days=59))[0:10] + " 00:00:00",
                                             "%Y-%m-%d %H:%M:%S")
        time_89 = datetime.datetime.strptime(str(create_time - datetime.timedelta(days=89))[0:10] + " 00:00:00",
                                             "%Y-%m-%d %H:%M:%S")
        for i in result:
            time_list.append(i.get('time'))
        latest_day = sorted(time_list)[0]
        if time_89 < datetime.datetime.strptime(latest_day, "%Y-%m-%d %H:%M:%S"):
            return -1
        for i in time_list:
            if datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") >= time_29:
                count_29 += 1
            if time_29 > datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") >= time_59:
                count_59 += 1
            if time_59 > datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") >= time_89:
                count_89 += 1
        if count_29 >= 3:
            count += 1
        if count_59 >= 3:
            count += 1
        if count_89 >= 3:
            count += 1
        return count

    def mxDialCall1mCnt(self):
        """mxDialCall1mCnt 过去一个月外拨电话的通话次数"""
        if self.__getCallList_dial()==self.SET_DEFAULT_VALUE_INT_9999999:
            return self.SET_DEFAULT_VALUE_INT_9999999
        result,create_time = self.__getCallList_dial()
        if not result or result == self.SET_DEFAULT_VALUE_INT_9999999:
            return self.SET_DEFAULT_VALUE_INT_9999999
        time_list = []
        count_29 = 0
        time_29 = datetime.datetime.strptime(str(create_time - datetime.timedelta(days=29))[0:10] + " 00:00:00","%Y-%m-%d %H:%M:%S")
        for i in result:
            time_list.append(i.get('time'))

        latest_day = sorted(time_list)[0]
        if time_29 < datetime.datetime.strptime(latest_day, "%Y-%m-%d %H:%M:%S"):
            return -1
        for i in time_list:
            if datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") >= time_29:
                count_29 += 1
        return count_29

    def mxTelRegDistinctCnt(self):
        """mxTelRegDistinctCnt 手机号码是注册客户数（去重）"""
        result = self.__getCallList()
        mobilephone_list = []
        if not result or result == self.SET_DEFAULT_VALUE_INT_9999999 or result == []:
            return self.SET_DEFAULT_VALUE_INT_9999999
        phone_list = []
        for i in result:
            phone_list.append(i.get('peer_number'))
        phone_list = list(set(phone_list))
        if not phone_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
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
        """mxTelDistinctCnt 注册客户占比规则 详单手机号码数（去重）"""
        result = self.__getCallList()
        if not result or result == self.SET_DEFAULT_VALUE_INT_9999999 or result == []:
            return self.SET_DEFAULT_VALUE_INT_9999999
        phone_list = []
        for i in result:
            if phone_clean_new(i.get('peer_number')):
                phone_list.append(i.get('peer_number'))
        phone_list = list(set(phone_list))
        return len(phone_list)

    def ph_ent_mth(self):
        """ph_ent_mth 入网时长"""
        data = self.mongo.query_by_user_id(db='galaxy',
                                           collection="mx_carrier_basic_message",
                                           find={"user_id": self.info.user_id})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        open_time = data[0].get('open_time')
        if not open_time:
            return self.SET_DEFAULT_VALUE_INT_9999999
        open_time = datetime.datetime.strptime(open_time, "%Y-%m-%d")
        diff_month = calmonths(open_time, self.info.event_time_add8h)
        return diff_month

    def mxMissMonthCnt(self):
        """mxMissMonthCnt 魔蝎通话记录获取失败月份数"""
        result = self.mongo.query_by_user_id(db='galaxy',
                                           collection="mx_carrier_month_info",
                                           find={"user_id": self.info.user_id})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result[0].get("miss_month_count",self.SET_DEFAULT_VALUE_INT_9999996)

    def is_exist_credit_bills(self):
        """is_exist_credit_bills 信用卡账单相关因子"""
        data = self.mongo.query_by_user_id('galaxy', "mx_email_bills",
                                           {"customer_id": self.customer_id, "status": "1"})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_0
        if data[0].get("response") and data[0].get("response").get("bills"):
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def mxContactPhone1earlyCallAgoDays(self):
        """mxContactPhone1earlyCallAgoDays 联系人1与客户最早通话时间距今天数  --产品:2345借款因子"""
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        contactList=[]
        for call in call_contact_list:
            if call.get("peer_number")==str(self.info.relativeContact) and call.get("duration")>0:
                contactList.append(datetime.datetime.strptime(call.get("time"),"%Y-%m-%d %H:%M:%S"))
        if not contactList:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return (return_strfYmd_date(self.info.event_time_add8h) - return_strfYmd_date(min(contactList))).days

    def mxContactPhone1latterCallAgoDays(self):
        """mxContactPhone1latterCallAgoDays 联系人1与客户最晚通话时间距今天数  --产品:2345借款因子"""
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        contactList=[]
        for call in call_contact_list:
            if call.get("peer_number")==str(self.info.relativeContact) and call.get("duration")>0:
                contactList.append(datetime.datetime.strptime(call.get("time"),"%Y-%m-%d %H:%M:%S"))
        if not contactList:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return (return_strfYmd_date(self.info.event_time_add8h) - return_strfYmd_date(max(contactList))).days

    def mxContactPhone1CallCnt(self):
        """mxContactPhone1CallCnt 联系人1与客户通话次数  --产品:2345借款因子"""
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        contactList=[]
        for call in call_contact_list:
            if call.get("peer_number")==str(self.info.relativeContact) and call.get("duration")>0:
                contactList.append(call)
        if not contactList:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return len(contactList)

    def mxContactPhone1CallTime(self):
        """mxContactPhone1CallTime 联系人1与客户通话时长  --产品:2345借款因子"""
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        contactList=[]
        for call in call_contact_list:
            if call.get("peer_number")==str(self.info.relativeContact):
                contactList.append(call)
        if not contactList:
            return self.SET_DEFAULT_VALUE_INT_9999995
        contactDuration=[]
        for duration in contactList:
            contactDuration.append(duration.get("duration"))
        return sum(contactDuration)

    def mxContactPhone2earlyCallAgoDays(self):
        """mxContactPhone2earlyCallAgoDays 联系人2与客户最早通话时间距今天数  --产品:2345借款因子"""
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        contactList=[]
        for call in call_contact_list:
            if call.get("peer_number")==str(self.info.friendContact) and call.get("duration")>0:
                contactList.append(datetime.datetime.strptime(call.get("time"),"%Y-%m-%d %H:%M:%S"))
        if not contactList:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return (return_strfYmd_date(self.info.event_time_add8h) - return_strfYmd_date(min(contactList))).days

    def mxContactPhone2latterCallAgoDays(self):
        """mxContactPhone2latterCallAgoDays 联系人2与客户最晚通话时间距今天数  --产品:2345借款因子"""
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        contactList=[]
        for call in call_contact_list:
            if call.get("peer_number")==str(self.info.friendContact) and call.get("duration")>0:
                contactList.append(datetime.datetime.strptime(call.get("time"),"%Y-%m-%d %H:%M:%S"))
        if not contactList:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return (return_strfYmd_date(self.info.event_time_add8h) - return_strfYmd_date(max(contactList))).days

    def mxContactPhone2CallCnt(self):
        """mxContactPhone2CallCnt 联系人2与客户通话次数  --产品:2345借款因子"""
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        contactList=[]
        for call in call_contact_list:
            if call.get("peer_number")==str(self.info.friendContact) and call.get("duration")>0:
                contactList.append(call)
        if not contactList:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return len(contactList)

    def mxContactPhone2CallTime(self):
        """mxContactPhone2CallTime 联系人2与客户通话时长  --产品:2345借款因子"""
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        contactList=[]
        for call in call_contact_list:
            if call.get("peer_number")==str(self.info.friendContact):
                contactList.append(call)
        if not contactList:
            return self.SET_DEFAULT_VALUE_INT_9999995
        contactDuration=[]
        for duration in contactList:
            contactDuration.append(duration.get("duration"))
        return sum(contactDuration)

    def __HitBadPhone(self, phone):
        sql = "select * from rota_bad where phone='%s' and is_deleted=0" % phone
        rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        if rota_result:
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0


    def callPhoneHitBadPhoneCnt(self):
        """CallPhoneHitBadPhoneCnt 本地通话记录手机号命中不良号码名单个数  --产品:2345借款因子"""
        contactActionList=self.mongo.query_contact_action_list_beforeEvenTime_inXdays(db='lake',
                                                                                      collection="s_user_mobile_contact_action_{0}".format(int(self.user_id) % 4),
                                                                                      find={"user_id": int(self.user_id)},
                                                                                      serial_no=self.serial_no,
                                                                                      days=180)
        if contactActionList=="No DATA":
            return self.SET_DEFAULT_VALUE_INT_9999999
        contactList=[]
        for call in contactActionList:
            if phoneClear(call.get("callNumber")) and phone_clean_new(phoneClear(call.get("callNumber"))) and call.get("callDuration")>0:
                contactList.append(call)
        phoneDic={}
        for line in contactList:
            if line.get("callNumber") not in phoneDic:
                phoneDic[line.get("callNumber")] = [line["callTime"]]
            else:
                if line["callTime"] not in phoneDic[line.get("callNumber")]:
                    phoneDic[line.get("callNumber")].append(line["callTime"])
        temp = []
        for k, v in phoneDic.items():
            temp.append([max(v),k])
        temp.sort(reverse=True)
        callList999= [str(phone[1]) for phone in temp[:999]]
        badContactList=[]
        for phone in callList999:
            if self.__HitBadPhone(factor_encrypt_identity(phone)):
                badContactList.append(phone)
        return len(badContactList)

    def mxCallPhoneHitBadPhoneCnt(self):
        """mxCallPhoneHitBadPhoneCnt 魔蝎详单手机号命中不良号码名单个数  --产品:2345借款因子"""
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        contactList=[]
        for call in call_contact_list:
            if phoneClear(call.get("peer_number")) and phone_clean_new(phoneClear(call.get("peer_number"))) and call.get("duration")>0:
                contactList.append(call)
        phoneDic={}
        for line in contactList:
            if line.get("peer_number") not in phoneDic:
                phoneDic[line.get("peer_number")] = [datetime.datetime.strptime(line["time"],"%Y-%m-%d %H:%M:%S")]
            else:
                if datetime.datetime.strptime(line["time"],"%Y-%m-%d %H:%M:%S") not in phoneDic[line.get("peer_number")]:
                    phoneDic[line.get("peer_number")].append(datetime.datetime.strptime(line["time"],"%Y-%m-%d %H:%M:%S"))
        temp = []
        for k, v in phoneDic.items():
            temp.append([max(v),k])
        temp.sort(reverse=True)
        callList999= [str(phone[1]) for phone in temp[:999]]
        badContactList=[]
        for phone in callList999:
            if self.__HitBadPhone(factor_encrypt_identity(phone)):
                badContactList.append(phone)
        return len(badContactList)

    def contactPhoneHitBadPhoneCnt(self):
        """ContactPhoneHitBadPhoneCnt 通讯录手机号命中不良号码名单个数  --产品:2345借款因子"""
        contactActionList=self.mongo.query_contact_list_beforeEvenTime_inXdays(db='lake',
                                                                                      collection="s_user_mobile_contact_{0}".format(int(self.user_id) % 4),
                                                                                      find={"user_id": int(self.user_id)},
                                                                                      serial_no=self.serial_no,
                                                                                      days=180)
        if contactActionList=="No DATA":
            return self.SET_DEFAULT_VALUE_INT_9999999
        badContactList=[]
        for phone in contactActionList:
            if self.__HitBadPhone(factor_encrypt_identity(phone)):
                badContactList.append(phone)
        return len(badContactList)

    def mxMutualCallPhoneMxCallProportion(self):
        """mxMutualCallPhoneMxCallProportion 互通电话的手机号在详单中的占比  --产品:2345借款因子"""
        contactActionList=self.mongo.query_contact_list_beforeEvenTime_inXdays( db='lake',
                                                                                collection="s_user_mobile_contact_{0}".format(int(self.user_id) % 4),
                                                                                find={"user_id": int(self.user_id)},
                                                                                serial_no=self.serial_no,
                                                                                days=180,
                                                                                allData=False)
        if contactActionList=="No DATA":
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        contactList=[]
        for call in call_contact_list:
            if phoneClear(call.get("peer_number")) and phone_clean_new(phoneClear(call.get("peer_number"))) and call.get("duration")>0:
                contactList.append(call.get("peer_number"))
        bothHavaContact=[]
        for phone in contactActionList:
            if phone in contactList:
                bothHavaContact.append(phone)
        if not contactList:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round(float(len(bothHavaContact))/len(list(set(contactList))),4)

    def mxContactMutualCallPhoneCnt(self):
        """mxContactMutualCallPhoneCnt 互通电话的手机号数量  --产品:2345借款因子"""
        contactActionList=self.mongo.query_contact_list_beforeEvenTime_inXdays( db='lake',
                                                                                collection="s_user_mobile_contact_{0}".format(int(self.user_id) % 4),
                                                                                find={"user_id": int(self.user_id)},
                                                                                serial_no=self.serial_no,
                                                                                days=180,
                                                                                allData=False)
        # if contactActionList=="No DATA":
        #     return self.SET_DEFAULT_VALUE_INT_9999999
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            call_contact_list=[]
        contactList=[]
        for call in call_contact_list:
            if phoneClear(call.get("peer_number")) and phone_clean_new(phoneClear(call.get("peer_number"))) and call.get("duration")>0:
                contactList.append(call.get("peer_number"))
        bothHavaContact=[]
        for phone in contactActionList:
            if phone in contactList:
                bothHavaContact.append(phone)
        return len(bothHavaContact)

    def mxMutualCallPhoneContactProportion(self):
        """mxMutualCallPhoneContactProportion 互通电话的手机号在通讯录中的占比 --产品:2345借款因子"""
        contactActionList=self.mongo.query_contact_list_beforeEvenTime_inXdays( db='lake',
                                                                                collection="s_user_mobile_contact_{0}".format(int(self.user_id) % 4),
                                                                                find={"user_id": int(self.user_id)},
                                                                                serial_no=self.serial_no,
                                                                                days=180,
                                                                                allData=False)
        if contactActionList=="No DATA":
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        call_contact_list = self.__getMxCallList()
        if not call_contact_list:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        contactList=[]
        for call in call_contact_list:
            if phoneClear(call.get("peer_number")) and phone_clean_new(phoneClear(call.get("peer_number"))) and call.get("duration")>0:
                contactList.append(call.get("peer_number"))
        bothHavaContact=[]
        for phone in contactActionList:
            if phone in contactList:
                bothHavaContact.append(phone)
        return round(float(len(bothHavaContact))/len(contactActionList),4)

    def contactHit2ClassSensitiveCnt(self):
        """contactHit2ClassSensitiveCnt 通讯录命中二类敏感词次数"""
        data = self.mongo.query_by_user_id('lake', "s_user_mobile_contact_{0}".format(self.info.user_id%4),
                                           {"user_id": int(self.user_id)})
        phoneNameList = []
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        for line in data[0]['contacts']:
            phoneNameList.append(line.get("name"))
        keyWords=[u"贷款",u"身份证",u"放款",u"POS",u"中介",u"分期",u"信用卡",u"钱包",u"金融",u"代办信用卡",u"代办"]
        count=0
        for name in phoneNameList:
            for key in keyWords:
                if re.findall(key,name):
                    count+=1
                    break
        return count

    def contactHit1ClassSensitiveCnt(self):
        """contactHit1ClassSensitiveCnt 通讯录命中一类敏感词次数"""
        data = self.mongo.query_by_user_id('lake', "s_user_mobile_contact_{0}".format(self.info.user_id%4),
                                           {"user_id": int(self.user_id)})
        phoneNameList = []
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        for line in data[0]['contacts']:
            phoneNameList.append(line.get("name"))
        keyWords=[u"无前期",u"放米",u"包下款",u"鲁钱",u"私货",u"私借",u"空放",u"套现",u"黑户",u"养卡",u"白户",u"垫还",u"提额",u"口子",u"做流水",u"水钱",u"点位",u"网黑"]
        count=0
        for name in phoneNameList:
            for key in keyWords:
                if re.findall(key,name):
                    count+=1
                    break
        return count

    def residentialAddress(self):
        """residentialAddress 居住详细地址"""
        return self.info.result.get('data').get("homeProvince")+self.info.result.get('data').get("homeCity")+self.info.result.get('data').get("homeDistrict")+self.info.result.get('data').get("homeAddress")

    def ipAddress(self):
        """ipAddress IP地址"""
        result = self.mongo.query_by_user_id(db='lake',
                                            collection='s_user_mobile_device_info_{0}'.format(self.info.user_id % 4),
                                            find={"user_id": self.info.user_id})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result[0].get("ip",self.SET_DEFAULT_VALUE_INT_9999996)

    def companyAddress(self):
        """companyAddress 单位详细地址"""
        return self.info.result.get('data').get("unitsProvince")+self.info.result.get('data').get("unitsCity")+self.info.result.get('data').get("unitsDistrict")+self.info.result.get('data').get("unitsAddress")

if __name__ == "__main__":
    serial_no = "1544083539723-7679EFE94ECE32E577C068B1A24357BC"
    a = MXFactor('T1', serial_no)
    print a.call_age()