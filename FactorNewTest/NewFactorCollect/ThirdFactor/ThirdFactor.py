# coding:utf-8
from FrameRunner.FactorInit import NewFactorInit
from utils.otherUtil import *
import re
import datetime
class ThirdFactor(NewFactorInit):
    def __init__(self, env, serial_no):
        super(ThirdFactor,self).__init__(env, serial_no)

    def bdScore(self):
        """bdScore 百度信用分"""
        results = self.mongo.query_by_user_id(db='galaxy', collection="bd_score_record",find={"serialNo": self.serial_no})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get('bdScoreResponse') or not results[0].get('bdScoreResponse').get('result'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        for data in results[0].get('bdScoreResponse').get('result'):
            if data.get('models')=='general_preA':
                if not data.get('score'):
                    return self.SET_DEFAULT_VALUE_INT_9999996
                return data.get('score')

    def __tz_1M_result(self,FactName):
        results = self.mongo.query_by_user_id(db='galaxy', collection="tz_record",find={"serialNo": self.serial_no})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        result=results[0]
        if FactName=='tzmrNotificationPlatform1M':
            if not result.get('tzResponse') or not result.get('tzResponse').get('mbInfos') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('platformInfos'):
                return self.SET_DEFAULT_VALUE_INT_9999999
            for info in result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('platformInfos'):
                if info.get('sliceName')=='m1':
                    return info.get('verifCount',self.SET_DEFAULT_VALUE_INT_9999996)
        if FactName=='tzmrRegistrationPlatform1M':
            if not result.get('tzResponse') or not result.get('tzResponse').get('mbInfos') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('platformInfos'):
                return self.SET_DEFAULT_VALUE_INT_9999999
            for info in result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('platformInfos'):
                if info.get('sliceName')=='m1':
                    return info.get('registerCount',self.SET_DEFAULT_VALUE_INT_9999996)
        if FactName=='tzmrNotificationEvent1M':
            if not result.get('tzResponse') or not result.get('tzResponse').get('mbInfos') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('eveSums'):
                return self.SET_DEFAULT_VALUE_INT_9999999
            for info in result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('eveSums'):
                if info.get('sliceName')=='m1':
                    return info.get('verifSum',self.SET_DEFAULT_VALUE_INT_9999996)
        if FactName=='tzmrRegistrationEvent1M':
            if not result.get('tzResponse') or not result.get('tzResponse').get('mbInfos') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('eveSums'):
                return self.SET_DEFAULT_VALUE_INT_9999999
            for info in result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('eveSums'):
                if info.get('sliceName')=='m1':
                    return info.get('registerSum',self.SET_DEFAULT_VALUE_INT_9999996)
        if FactName=='tzmrRejectionEvents1M':
            if not result.get('tzResponse') or not result.get('tzResponse').get('mbInfos') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('eveSums'):
                return self.SET_DEFAULT_VALUE_INT_9999999
            for info in result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('eveSums'):
                if info.get('sliceName')=='m1':
                    return info.get('applyRejectSum',self.SET_DEFAULT_VALUE_INT_9999996)
        if FactName=='tzmrMaxOverdueLength1M':
            if not result.get('tzResponse') or not result.get('tzResponse').get('mbInfos') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('refInfos'):
                return self.SET_DEFAULT_VALUE_INT_9999999
            for info in result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('refInfos'):
                if info.get('sliceName')=='m1':
                    if info.get('maxOverdueDelayLevel')=='null':
                        return self.SET_DEFAULT_VALUE_INT_9999996
                    return info.get('maxOverdueDelayLevel',self.SET_DEFAULT_VALUE_INT_9999996)
        if FactName=='tzmrMaximumOverdueAmount1M':
            if not result.get('tzResponse') or not result.get('tzResponse').get('mbInfos') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('refInfos'):
                return self.SET_DEFAULT_VALUE_INT_9999999
            for info in result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('refInfos'):
                if info.get('sliceName')=='m1':
                    if info.get('maxOverdueAmountLevel')=='null':
                        return self.SET_DEFAULT_VALUE_INT_9999996
                    return info.get('maxOverdueAmountLevel',self.SET_DEFAULT_VALUE_INT_9999996)
        if FactName=='tzmrAverageOverdueLength1M':
            if not result.get('tzResponse') or not result.get('tzResponse').get('mbInfos') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('refInfos'):
                return self.SET_DEFAULT_VALUE_INT_9999999
            for info in result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('refInfos'):
                if info.get('sliceName')=='m1':
                    if info.get('aveOverdueDelayLevel')=='null':
                        return self.SET_DEFAULT_VALUE_INT_9999996
                    return info.get('aveOverdueDelayLevel',self.SET_DEFAULT_VALUE_INT_9999996)
        if FactName=='tzmrAverageOverdueAmount1M':
            if not result.get('tzResponse') or not result.get('tzResponse').get('mbInfos') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo') or not result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('refInfos'):
                return self.SET_DEFAULT_VALUE_INT_9999999
            for info in result.get('tzResponse').get('mbInfos')[0].get('creditInfo').get('refInfos'):
                if info.get('sliceName')=='m1':
                    if info.get('aveOverdueAmountLevel')=='null':
                        return self.SET_DEFAULT_VALUE_INT_9999996
                    return info.get('aveOverdueAmountLevel',self.SET_DEFAULT_VALUE_INT_9999996)

    def tzmrNotificationPlatform1M(self):
        """tzmrNotificationPlatform1M 近一个月验证码通知平台"""
        return self.__tz_1M_result(FactName='tzmrNotificationPlatform1M')

    def tzmrRegistrationPlatform1M(self):
        """tzmrRegistrationPlatform1M 近一个月注册平台"""
        return self.__tz_1M_result(FactName='tzmrRegistrationPlatform1M')

    def tzmrNotificationEvent1M(self):
        """tzmrnotificationEvent1M 近一个月验证码通知事件"""
        return self.__tz_1M_result(FactName='tzmrNotificationEvent1M')

    def tzmrRegistrationEvent1M(self):
        """tzmrregistrationEvent1M 近一个月注册事件"""
        return self.__tz_1M_result(FactName='tzmrRegistrationEvent1M')

    def tzmrRejectionEvents1M(self):
        """tzmrrejectionEvents1M 近一个月拒绝事件"""
        return self.__tz_1M_result(FactName='tzmrRejectionEvents1M')

    def tzmrMaxOverdueLength1M(self):
        """tzmrmaxOverdueLength1M 近一个月最大逾期时长"""
        return self.__tz_1M_result(FactName='tzmrMaxOverdueLength1M')

    def tzmrMaximumOverdueAmount1M(self):
        """tzmrmaximumOverdueAmount1M 近一个月最大逾期金额"""
        return self.__tz_1M_result(FactName='tzmrMaximumOverdueAmount1M')

    def tzmrAverageOverdueLength1M(self):
        """tzmraverageOverdueLength1M 近一个月平均逾期时长"""
        return self.__tz_1M_result(FactName='tzmrAverageOverdueLength1M')

    def tzmrAverageOverdueAmount1M(self):
        """tzmraverageOverdueAmount1M 近一个月平均逾期金额"""
        return self.__tz_1M_result(FactName='tzmrAverageOverdueAmount1M')

    def tdBlacklistResult(self):
        """tdBlacklistResult 同盾黑名单"""
        return self.SET_DEFAULT_VALUE_INT_9999999

    def __tdResult(self):
        tdList=[]
        results = self.mongo.queryall_by_userId(db='galaxy', collection="td_guard_record",find={"serialNo": self.serial_no})
        if not results:
            return "No DATA"
        if not results or not results[0].get('tdGuardResponse') or not results[0].get('tdGuardResponse').get('result_desc') or not results[0].get('tdGuardResponse').get('result_desc').get("ANTIFRAUD"):
            return "No DATA"
        if results[0].get('tdGuardResponse').get('result_desc').get("ANTIFRAUD").get("risk_items")=="[]":
            return ""
        for row in results[0].get('tdGuardResponse').get('result_desc').get("ANTIFRAUD").get("risk_items"):
            tdList.append(int(row.get("rule_id")))
        return tdList

    def tdbbBlacklistResult(self):
        """tdBlacklistResult 同盾保镖黑名单"""
        #身份证命中法院失信名单   31489554
        #身份证命中犯罪通缉名单   31489694
        #身份证命中法院执行名单   31489834
        #身份证对应人存在助学贷款欠费历史   31489964
        #身份证命中信贷逾期名单     31490084
        #身份证命中车辆租赁违约名单  31490354
        #身份证命中法院结案名单    31490384
        #身份证_姓名命中信贷逾期模糊名单   31490444
        #身份证_姓名命中法院失信模糊名单   31490474
        #身份证_姓名命中法院执行模糊名单   31490494
        #身份证_姓名命中法院结案模糊名单   31490514
        #身份证命中故意违章乘车名单  31490554
        #身份证命中欠税名单  31490574
        #身份证命中欠税公司法人代表名单   31490594
        #身份证命中信贷逾期后还款名单    31490614
        #手机号命中虚假号码库   31489274
        #手机号命中通信小号库  31489354
        #手机号命中诈骗骚扰库     31489494
        #手机号命中信贷逾期名单      31490174
        #手机号命中车辆租赁违约名单      31490304
        #手机号疑似乱填   31490314
        #手机号命中欠款公司法人代表名单  31490364
        #手机号命中信贷逾期后还款名单   31490394
        #3个月内申请人身份证作为联系人身份证出现的次数大于等于2   31490744
        item_id_list=[31489554,31489694,31489834,31489964,31490084,31490354,31490384,31490444,31490474,31490494,31490514,31490554,
                      31490574,31490594,31490614,31489274,31489354,31489494,31490174,31490304,31490314,31490364,31490394,31490744]
        td_list=self.__tdResult()
        if td_list=='No DATA':
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not td_list:
            return ""
        new_list=list(set(td_list).intersection(set(item_id_list)))
        if not new_list:
            return ""
        return str(tuple(new_list))[1:-1].replace(" ","")

    def bjScore(self):
        """bjScore 冰鉴小额火眸分"""
        maxOverResult = self.mongo.queryall_by_userId(db='galaxy',
                                                      collection='bj_score_record',
                                                      find={"serialNo": self.serial_no})
        if not maxOverResult or len(maxOverResult) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        result = maxOverResult[0]
        if not result.get("bjScore") or not result.get("bjScoreResponse") or result.get("bjScoreResponse").get(
                "responseCode") != "00":
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result.get("bjScore")==u'无法评估':
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result.get("bjScore")

    def bjBlacklist(self):
        """bjBlacklist 冰鉴黑名单"""
        maxOverResult = self.mongo.queryall_by_userId(db='galaxy',
                                                      collection='bj_black_record',
                                                      find={"serialNo": self.serial_no})
        if not maxOverResult or len(maxOverResult) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        result = maxOverResult[0]
        if not result.get("hitStatus") or not result.get("bjBlackResponse") or result.get("bjBlackResponse").get(
                "responseCode") != '00':
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result.get("hitStatus") == '00':
            return 0
        if result.get("hitStatus") == '01':
            return 1

    def __br_new_record(self,factor):
        br_new_result = self.mongo.queryall_by_userId(db='galaxy',
                                                      collection='br_new_record',
                                                      find={"serialNo": self.serial_no})
        if not br_new_result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if factor=="als_d7_id_pdl_allnum":
            if not br_new_result[0].get("brResponse") or not br_new_result[0].get("brResponse").get("als_d7_id_pdl_allnum"):
                return self.SET_DEFAULT_VALUE_INT_9999996
            return br_new_result[0].get("brResponse").get("als_d7_id_pdl_allnum")
        if factor=="als_d7_cell_pdl_allnum":
            if not br_new_result[0].get("brResponse") or not br_new_result[0].get("brResponse").get("als_d7_cell_pdl_allnum"):
                return self.SET_DEFAULT_VALUE_INT_9999996
            return br_new_result[0].get("brResponse").get("als_d7_cell_pdl_allnum")
        if factor=="als_d7_id_nbank_allnum":
            if not br_new_result[0].get("brResponse") or not br_new_result[0].get("brResponse").get("als_d7_id_nbank_allnum"):
                return self.SET_DEFAULT_VALUE_INT_9999996
            return br_new_result[0].get("brResponse").get("als_d7_id_nbank_allnum")
        if factor=="ir_m1_id_x_cell_cnt":
            if not br_new_result[0].get("brResponse") or not br_new_result[0].get("brResponse").get("ir_m1_id_x_cell_cnt"):
                return self.SET_DEFAULT_VALUE_INT_9999996
            return br_new_result[0].get("brResponse").get("ir_m1_id_x_cell_cnt")
        if factor=="flag_execution":
            if not br_new_result[0].get("brResponse") or not br_new_result[0].get("brResponse").get("flag_execution"):
                return self.SET_DEFAULT_VALUE_INT_9999996
            return br_new_result[0].get("brResponse").get("flag_execution")
        else:
            return

    def brD7IdPdlAllnum(self):
        """br_D7_Id_Pdl_Allnum 身份证号近七天申请线上小额现金贷的次数"""
        return self.__br_new_record(factor="als_d7_id_pdl_allnum")

    def brD7CellPdlAllnum(self):
        """br_D7_Cell_Pdl_Allnum 手机号近七天申请线上小额现金贷的次数"""
        return self.__br_new_record(factor="als_d7_cell_pdl_allnum")

    def brD7IdNbankAllnum(self):
        """br_D7_Id_Nbank_Allnum 近七天在非银机构申请次数"""
        return self.__br_new_record(factor="als_d7_id_nbank_allnum")

    def brIrM1IdXCellCnt(self):
        """br_Ir_M1_Id_X_Cell_Cnt 近一个月身份证关联手机号"""
        return self.__br_new_record(factor="ir_m1_id_x_cell_cnt")

    def brFlagExecution(self):
        """br_Flag_Execution 法院执行人名单"""
        return self.__br_new_record(factor="flag_execution")

    def __get_mx_alipay_bills_data(self,factor):
        mx_alipay_bills_data = self.mongo.queryall_by_userId(db='galaxy',collection='mx_alipay_bills_data',find={"user_id": self.info.user_id})
        if not mx_alipay_bills_data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if factor=="zfbCertified":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("userinfo"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            if mx_alipay_bills_data[0].get("response").get("userinfo").get("certified")=="":
                return self.SET_DEFAULT_VALUE_INT_9999995
            if mx_alipay_bills_data[0].get("response").get("userinfo").get("certified"):
                return self.SET_DEFAULT_VALUE_INT_1
            return self.SET_DEFAULT_VALUE_INT_0
        if factor=="zfbNameAgreement":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("userinfo"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            if mx_alipay_bills_data[0].get("response").get("userinfo").get("user_name")=="":
                return self.SET_DEFAULT_VALUE_INT_9999995
            if self.info.user_name==mx_alipay_bills_data[0].get("response").get("userinfo").get("user_name"):
                return self.SET_DEFAULT_VALUE_INT_1
            return self.SET_DEFAULT_VALUE_INT_0
        if factor=="zfbIdCardNumberAgreement":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("userinfo"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            if mx_alipay_bills_data[0].get("response").get("userinfo").get("idcard_number")=="":
                return self.SET_DEFAULT_VALUE_INT_9999995
            clean_idcard_number_list=[]
            for num in mx_alipay_bills_data[0].get("response").get("userinfo").get("idcard_number"):
                if re.search('\d',num) or num in ('*','X'):
                    clean_idcard_number_list.append(num)
            clean_idcard_number=''.join(clean_idcard_number_list)
            if clean_idcard_number[0]=='*' or clean_idcard_number[-1]=="*":
                return self.SET_DEFAULT_VALUE_INT_9999995
            if clean_idcard_number[0]==self.info.cert_id[0] and clean_idcard_number[-1]==self.info.cert_id[-1]:
                return self.SET_DEFAULT_VALUE_INT_1
            return self.SET_DEFAULT_VALUE_INT_0
        if factor=="zfbPhoneNumberAgreement":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("userinfo"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            if mx_alipay_bills_data[0].get("response").get("userinfo").get("phone_number")=="":
                return self.SET_DEFAULT_VALUE_INT_9999995
            clean_phone_number_list=[]
            for num in mx_alipay_bills_data[0].get("response").get("userinfo").get("phone_number"):
                if re.search('\d',num) or num =='*':
                    clean_phone_number_list.append(num)
            clean_phone_number=''.join(clean_phone_number_list)
            if '*' in clean_phone_number[:3] or "*" in clean_phone_number[-2:]:
                return self.SET_DEFAULT_VALUE_INT_9999995
            if clean_phone_number[:3]==self.info.phone[:3] and clean_phone_number[-2:]==self.info.phone[-2:]:
                return self.SET_DEFAULT_VALUE_INT_1
            return self.SET_DEFAULT_VALUE_INT_0
        if factor=="zfbRegisterTimeAgoDay":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("userinfo"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            if mx_alipay_bills_data[0].get("response").get("userinfo").get("register_time")=="":
                return self.SET_DEFAULT_VALUE_INT_9999995
            return (return_strfYmd_date(self.info.event_time_add8h)-datetime.datetime.strptime(mx_alipay_bills_data[0].get("response").get("userinfo").get("register_time")[:10],"%Y-%m-%d")).days+1
        if factor=="zfbBankInfoCnt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("bankinfo"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            bankinfoList=[]
            for bankinfo in mx_alipay_bills_data[0].get("response").get("bankinfo"):
                bankinfoList.append(bankinfo.get("card_number"))
            return len(bankinfoList)
        if factor=="zfbCreditCnt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("bankinfo"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            bankinfoList=[]
            for bankinfo in mx_alipay_bills_data[0].get("response").get("bankinfo"):
                if u"信用卡" in bankinfo.get("card_type") or u"贷记卡" in bankinfo.get("card_type"):
                    bankinfoList.append(bankinfo.get("card_number"))
            return len(bankinfoList)
        if factor=="zfbRtoCreditCardOfBankCard":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("bankinfo"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            bankinfoList_all=[]
            bankinfoList=[]
            for bankinfo in mx_alipay_bills_data[0].get("response").get("bankinfo"):
                bankinfoList_all.append(bankinfo.get("card_number"))
            for bankinfo in mx_alipay_bills_data[0].get("response").get("bankinfo"):
                if u"信用卡" in bankinfo.get("card_type") or u"贷记卡" in bankinfo.get("card_type"):
                    bankinfoList.append(bankinfo.get("card_number"))
            if not bankinfoList_all:
                return self.SET_DEFAULT_VALUE_FLOAT_9999998
            return round(float(len(bankinfoList))/len(bankinfoList_all),4)
        if factor=="zfbRecentTradersCnt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("recenttraders"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            alipay_userid_list=[]
            for alipay in mx_alipay_bills_data[0].get("response").get("recenttraders"):
                alipay_userid_list.append(alipay.get("alipay_userid"))
            return len(alipay_userid_list)
        if factor=="zfbContactcnt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("alipaycontacts"):
                return self.SET_DEFAULT_VALUE_INT_9999999
            alipaycontactsList=[]
            for contact in mx_alipay_bills_data[0].get("response").get("alipaycontacts"):
                alipaycontactsList.append(contact.get("alipay_userid"))
            return len(alipaycontactsList)
        if factor=="zfbIncomeAmt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("tradeinfo"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999999
            tradeinfoSum=0.0
            for trade in mx_alipay_bills_data[0].get("response").get("tradeinfo"):
                if  re.match(u'已收入',trade.get("capital_status")) and u"退款" not in trade.get("capital_status") and u"退款" not in trade.get("comments") and u"退款" not in trade.get("counterparty") and u"退款" not in trade.get("product_name") and u"退款" not in trade.get("trade_number"):
                    tradeinfoSum=tradeinfoSum+float(trade.get("trade_amount"))
            if not tradeinfoSum:
                return self.SET_DEFAULT_VALUE_FLOAT_9999999
            return tradeinfoSum
        if factor=="zfbIncomeCnt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("tradeinfo"):
                return self.SET_DEFAULT_VALUE_INT_9999999
            trade_sum=0
            for trade in mx_alipay_bills_data[0].get("response").get("tradeinfo"):
                if re.match(u'已收入',trade.get("capital_status")) and u"退款" not in trade.get("comments") and u"退款" not in trade.get("counterparty") and u"退款" not in trade.get("product_name") and u"退款" not in trade.get("trade_number") and u"退款" not in trade.get("trade_status"):
                    trade_sum+=1
            return trade_sum
        if factor=="zfbMaxRepayAmt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("tradeinfo"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999999
            tradeinfoList=[]
            for trade in mx_alipay_bills_data[0].get("response").get("tradeinfo"):
                if trade.get("product_name") and u"还款" in trade.get("product_name"):
                    tradeinfoList.append(float(trade.get("trade_amount")))
            if not tradeinfoList:
                return self.SET_DEFAULT_VALUE_INT_9999999
            return max(tradeinfoList)
        if factor=="zfbOpenFpCardCnt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("bankinfo"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            open_sum=0
            for open_fpcard in mx_alipay_bills_data[0].get("response").get("bankinfo"):
                if open_fpcard.get("open_fpcard"):
                    open_sum+=1
            return open_sum
        if factor=="zfbPhoneCnt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            phone_number_list=[]
            for phone in mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"):
                phone_number_list.append(phone.get("phone_number"))
            return len(list(set(phone_number_list)))
        if factor=="zfbAddressCnt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            full_address_list=[]
            for full_address in mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"):
                full_address_list.append(full_address.get("full_address"))
            return len(full_address_list)
        if factor=="zfbRtoPhoneCntOfAddreCnt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            phone_number_list=[]
            for phone in mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"):
                phone_number_list.append(phone.get("phone_number"))
            if len(mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"))==0:
                return self.SET_DEFAULT_VALUE_FLOAT_9999998
            return round(float(len(list(set(phone_number_list))))/len(mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses")),4)
        if factor=="zfbRtoProvCntOfAddreCnt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            province_list=[]
            for province in mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"):
                province_list.append(province.get("province"))
            if len(mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"))==0:
                return self.SET_DEFAULT_VALUE_FLOAT_9999998
            return round(float(len(list(set(province_list))))/len(mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses")),4)
        if factor=="zfbCityCntOfAddreCnt":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            city_list=[]
            for province in mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"):
                city_list.append(province.get("city"))
            if len(mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses"))==0:
                return self.SET_DEFAULT_VALUE_FLOAT_9999998
            return round(float(len(list(set(city_list))))/len(mx_alipay_bills_data[0].get("response").get("alipaydeliveraddresses")),4)
        if factor=="zfbIncomeAmtAvg":
            if not mx_alipay_bills_data[0].get("response") or not mx_alipay_bills_data[0].get("response").get("tradeinfo"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            tradeinfoSum=0.0
            trade_sum=0
            for trade in mx_alipay_bills_data[0].get("response").get("tradeinfo"):
                if u"已收入" in trade.get("capital_status") and u"退款" not in trade.get("capital_status"):
                    trade_sum += 1
                    tradeinfoSum=tradeinfoSum+float(trade.get("trade_amount"))
            if trade_sum==0:
                return self.SET_DEFAULT_VALUE_FLOAT_9999998
            return round(tradeinfoSum/trade_sum,4)

    def __get_mx_alipay_report(self,factor):
        mx_alipay_report = self.mongo.queryall_by_userId(db='galaxy',collection='mx_alipay_report',find={"user_id": self.info.user_id})
        if not mx_alipay_report:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if factor=="zfbRegisterMonth":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("basic_info") or not mx_alipay_report[0].get("response").get("basic_info").get("user_and_account_basic_info"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            return mx_alipay_report[0].get("response").get("basic_info").get("user_and_account_basic_info").get("register_month")
        if factor=="zfbBalance":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("wealth_info") or not mx_alipay_report[0].get("response").get("wealth_info").get("total_assets"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            return float(mx_alipay_report[0].get("response").get("wealth_info").get("total_assets").get("balance"))
        if factor=="zfbYuEbao":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("wealth_info") or not mx_alipay_report[0].get("response").get("wealth_info").get("total_assets"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            return float(mx_alipay_report[0].get("response").get("wealth_info").get("total_assets").get("yu_e_bao"))
        if factor=="zfbTotConsumeCnt":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("total_consume_cnt"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            return mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("total_consume_cnt").get('sum')
        if factor=="zfbTotConsumeAvg":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("total_consume_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("total_consume_cnt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            total_consume_amt=mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("total_consume_amt").get('sum')
            total_consume_cnt=mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("total_consume_cnt").get('sum')
            if int(total_consume_cnt)==0:
                return self.SET_DEFAULT_VALUE_FLOAT_9999998
            return round(float(total_consume_amt)/float(total_consume_cnt),4)
        if factor=="zfbHuaBeiLimit":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("wealth_info") or not mx_alipay_report[0].get("response").get("wealth_info").get("total_assets"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            return float(mx_alipay_report[0].get("response").get("wealth_info").get("total_assets").get("huabai_limit"))
        if factor=="zfbOnlineShoppingCnt":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("online_shopping_cnt"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            if mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("online_shopping_cnt")=='':
                return self.SET_DEFAULT_VALUE_INT_9999999
            return int(mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("online_shopping_cnt").get("sum"))
        if factor=="zfbTotIncomeAmtL6m":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("basic_info") or not mx_alipay_report[0].get("response").get("basic_info").get("user_and_account_basic_info"):
                return self.SET_DEFAULT_VALUE_INT_9999995
            return float(mx_alipay_report[0].get("response").get("basic_info").get("user_and_account_basic_info").get("total_income_amt_6m"))
        if factor=="zfbCunJinBao":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("wealth_info") or not \
            mx_alipay_report[0].get("response").get("wealth_info").get("total_assets"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            return float(mx_alipay_report[0].get("response").get("wealth_info").get("total_assets").get("cun_jin_bao"))
        if factor=="zfbLifePayAvg":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("lifepay_cnt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("lifepay_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            lifepay_cnt=float(mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("lifepay_cnt").get("sum"))
            lifepay_amt=float(mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("lifepay_amt").get("sum"))
            if lifepay_cnt==0.0:
                return self.SET_DEFAULT_VALUE_FLOAT_9999998
            return round(lifepay_amt/lifepay_cnt,4)
        if factor=="zfbMaxConsumeAmtSum":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("max_consume_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            max_consume_amt_json=mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("max_consume_amt")
            if not max_consume_amt_json:
                return self.SET_DEFAULT_VALUE_FLOAT_9999999
            del max_consume_amt_json['sum']
            max_consume_amt_list=[]
            for max_consume_amt in max_consume_amt_json.values():
                max_consume_amt_list.append(float(max_consume_amt))
            return sum(max_consume_amt_list)
        if factor=="zfbMaxOutAmtSum":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("transfer_out_info") or not mx_alipay_report[0].get("response").get("major_expenditure").get("transfer_out_info").get("max_out_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            max_out_amt_json=mx_alipay_report[0].get("response").get("major_expenditure").get("transfer_out_info").get("max_out_amt")
            if not max_out_amt_json:
                return self.SET_DEFAULT_VALUE_FLOAT_9999999
            del max_out_amt_json['sum']
            max_out_amt_json_list=[]
            for max_consume_amt in max_out_amt_json.values():
                max_out_amt_json_list.append(float(max_consume_amt))
            return sum(max_out_amt_json_list)
        if factor=="zfbMaxTransInAmtSum":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("infolow_of_capital") or not mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info") or not mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info").get("max_transfer_in_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            max_transfer_in_amt_json=mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info").get("max_transfer_in_amt")
            if not max_transfer_in_amt_json:
                return self.SET_DEFAULT_VALUE_FLOAT_9999999
            del max_transfer_in_amt_json['sum']
            max_transfer_in_amt_json_list=[]
            for max_consume_amt in max_transfer_in_amt_json.values():
                max_transfer_in_amt_json_list.append(float(max_consume_amt))
            return sum(max_transfer_in_amt_json_list)
        if factor=="zfbTransInAvg":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("infolow_of_capital") or not mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info") or not mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info").get("transfer_in_cnt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("infolow_of_capital") or not mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info") or not mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info").get("transfer_in_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            transfer_in_cnt=float(mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info").get("transfer_in_cnt").get("sum"))
            transfer_in_amt=float(mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info").get("transfer_in_amt").get("sum"))
            if transfer_in_cnt ==0.0:
                return self.SET_DEFAULT_VALUE_FLOAT_9999998
            return round(transfer_in_amt/transfer_in_cnt,4)
        if factor=="zfbTransInAmtSum":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("infolow_of_capital") or not mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info") or not mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info").get("transfer_in_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            return float(mx_alipay_report[0].get("response").get("infolow_of_capital").get("transfer_in_info").get("transfer_in_amt").get("sum"))
        if factor=="zfbTakeOutAmtAvg":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("takeout_cnt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("takeout_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            takeout_amt=float(mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("takeout_amt").get("sum"))
            takeout_cnt=float(mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("takeout_cnt").get("sum"))
            if takeout_cnt==0.0:
                return self.SET_DEFAULT_VALUE_FLOAT_9999998
            return round(takeout_amt/takeout_cnt,4)
        if factor=="zfbOnlineShoppingAmt":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("online_shopping_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            return float(mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("online_shopping_amt").get("sum"))
        if factor=="zfbOnlineShoppingAvg":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("online_shopping_cnt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("online_shopping_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            online_shopping_amt=float(mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("online_shopping_amt").get("sum"))
            online_shopping_cnt=float(mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("online_shopping_cnt").get("sum"))
            if online_shopping_cnt==0.0:
                return self.SET_DEFAULT_VALUE_FLOAT_9999998
            return round(online_shopping_amt/online_shopping_cnt,4)
        if factor=="zfbTotConsumeAmtSum":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption") or not mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("total_consume_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            return float(mx_alipay_report[0].get("response").get("major_expenditure").get("consumption").get("total_consume_amt").get("sum"))
        if factor=="zfbCreditRepayAmtAvg":
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("repayment") or not mx_alipay_report[0].get("response").get("major_expenditure").get("repayment").get("credit_rpy_cnt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            if not mx_alipay_report[0].get("response") or not mx_alipay_report[0].get("response").get("major_expenditure") or not mx_alipay_report[0].get("response").get("major_expenditure").get("repayment") or not mx_alipay_report[0].get("response").get("major_expenditure").get("repayment").get("credit_rpy_amt"):
                return self.SET_DEFAULT_VALUE_FLOAT_9999995
            credit_rpy_amt=float(mx_alipay_report[0].get("response").get("major_expenditure").get("repayment").get("credit_rpy_cnt").get("sum"))
            credit_rpy_cnt=float(mx_alipay_report[0].get("response").get("major_expenditure").get("repayment").get("credit_rpy_amt").get("sum"))
            if credit_rpy_cnt==0.0:
                return self.SET_DEFAULT_VALUE_FLOAT_9999998
            return round(credit_rpy_amt/credit_rpy_cnt,4)

    def zfbCertified(self):
        """zfbCertified 支付宝是否实名认证"""
        return self.__get_mx_alipay_bills_data(factor="zfbCertified")

    def zfbNameAgreement(self):
        """zfbNameAgreement 支付宝用户姓名与注册客户姓名是否一致"""
        return self.__get_mx_alipay_bills_data(factor="zfbNameAgreement")

    def zfbIdCardNumberAgreement(self):
        """zfbIdCardNumberAgreement 支付宝用户身份证号码 与注册客户身份证号码是否一致"""
        return self.__get_mx_alipay_bills_data(factor="zfbIdCardNumberAgreement")

    def zfbPhoneNumberAgreement(self):
        """zfbPhoneNumberAgreement 绑定支付宝账号的手机号与注册客户手机号是否一致"""
        return self.__get_mx_alipay_bills_data(factor="zfbPhoneNumberAgreement")

    def zfbRegisterTimeAgoDay(self):
        """zfbRegisterTimeAgoDay 支付宝注册时间距申请日天数"""
        return self.__get_mx_alipay_bills_data(factor="zfbRegisterTimeAgoDay")

    def zfbOriginalData(self):
        """zfbReport 支付宝有无报告"""
        billList=self.mongo.query_all_by_userId_beforeEvenTime_inXdays(db='galaxy',
                                                                  collection='mx_alipay_bills_data',
                                                                  find={'user_id':self.info.user_id},
                                                                  serial_no=self.serial_no,
                                                                  days=365)
        bill_success=[]
        for bill in billList:
            if bill.get("status")==str(1) and bill.get("create_time")>=self.info.event_time_add8h-datetime.timedelta(hours=24):
               bill_success.append(bill)
        if not bill_success:
            return self.SET_DEFAULT_VALUE_INT_0
        return self.SET_DEFAULT_VALUE_INT_1

    def zfbAuthorization(self):
        """zfbAuthorization 支付宝是否授权  TODO改成当天凌晨开始--非24h"""
        sql="select * from scorpio_user_record_%s where customer_id='%s' and content_id=3 and delete_flag=0 order by id desc"%(self.info.customer_id%20,self.info.customer_id)
        result=self.mysql.queryall_by_customer_id(db="customer_center",sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result[0].get("status") in (1,2) and result[0].get("create_at")>=self.info.event_time_add8h-datetime.timedelta(hours=24):
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def twoEntry(self):
        """twoEntry 是否为二次进件客户"""
        return self.info.result.get('data', {}).get('extraDataStatus',self.SET_DEFAULT_VALUE_INT_0)

    def zfbBankInfoCnt(self):
        """zfbBankInfoCnt 用户银行卡数量"""
        return self.__get_mx_alipay_bills_data(factor="zfbBankInfoCnt")

    def zfbCreditCnt(self):
        """zfbCreditCnt 用户信用卡数量"""
        return self.__get_mx_alipay_bills_data(factor="zfbCreditCnt")

    def zfbRtoCreditCardOfBankCard(self):
        """zfbRtoCreditCardOfBankCard 用户信用卡或贷记卡数量/银行卡数量"""
        return self.__get_mx_alipay_bills_data(factor="zfbRtoCreditCardOfBankCard")

    def zfbRecentTradersCnt(self):
        """zfbRecentTradersCnt 用户交易联系人数量"""
        return self.__get_mx_alipay_bills_data(factor="zfbRecentTradersCnt")

    def zfbRegisterMonth(self):
        """zfbRegisterMonth 用户注册的时间距今的月份数"""
        return self.__get_mx_alipay_report(factor="zfbRegisterMonth")

    def zfbContactcnt(self):
        """zfbContactcnt 用户联系人数量"""
        return self.__get_mx_alipay_bills_data(factor="zfbContactcnt")

    def zfbBalance(self):
        """zfbBalance 当前该用户的账户余额金额"""
        return self.__get_mx_alipay_report(factor="zfbBalance")

    def zfbYuEbao(self):
        """zfbYuEbao 当前该用户的余额宝账户金额"""
        return self.__get_mx_alipay_report(factor="zfbYuEbao")

    def zfbTotConsumeCnt(self):
        """zfbTotConsumeCnt 用户通过平台，进行消费类交易的笔数之和"""
        return self.__get_mx_alipay_report(factor="zfbTotConsumeCnt")

    def zfbTotConsumeAvg(self):
        """zfbTotConsumeAvg 用户平均消费金额"""
        return self.__get_mx_alipay_report(factor="zfbTotConsumeAvg")

    def zfbHuaBeiLimit(self):
        """zfbHuaBeiLimit 用户花呗额度"""
        return self.__get_mx_alipay_report(factor="zfbHuaBeiLimit")

    def zfbIncomeAmt(self):
        """zfbIncomeAmt 用户资金转入收入总金额（不含自己资金的转移\退款金额）"""
        return self.__get_mx_alipay_bills_data(factor="zfbIncomeAmt")

    def zfbIncomeCnt(self):
        """zfbIncomeCnt 用户资金收入总次数（不含自己资金的转移\退款）"""
        return self.__get_mx_alipay_bills_data(factor="zfbIncomeCnt")

    def zfbMaxRepayAmt(self):
        """zfbMaxRepayAmt 用户单次最大还款金额"""
        return self.__get_mx_alipay_bills_data(factor="zfbMaxRepayAmt")

    def zfbOnlineShoppingCnt(self):
        """zfbOnlineShoppingCnt 用户通过平台，支付网购类交易的笔数之和"""
        return self.__get_mx_alipay_report(factor="zfbOnlineShoppingCnt")

    def zfbOpenFpCardCnt(self):
        """zfbOpenFpCardCnt 用户开通快捷支付的银行卡数量"""
        return self.__get_mx_alipay_bills_data(factor="zfbOpenFpCardCnt")

    def zfbPhoneCnt(self):
        """zfbPhoneCnt 用户不同收件手机号数量"""
        return self.__get_mx_alipay_bills_data(factor="zfbPhoneCnt")

    def zfbAddressCnt(self):
        """zfbAddressCnt 总收货地址数量"""
        return self.__get_mx_alipay_bills_data(factor="zfbAddressCnt")

    def zfbRtoPhoneCntOfAddreCnt(self):
        """zfbRtoPhoneCntOfAddreCnt 用户不同收件手机号数量/用户总收件地址数量"""
        return self.__get_mx_alipay_bills_data(factor="zfbRtoPhoneCntOfAddreCnt")

    def zfbRtoProvCntOfAddreCnt(self):
        """zfbRtoProvCntOfAddreCnt 用户不同收件省份数量/用户总收件地址数量"""
        return self.__get_mx_alipay_bills_data(factor="zfbRtoProvCntOfAddreCnt")

    def zfbCityCntOfAddreCnt(self):
        """zfbCityCntOfAddreCnt 用户收货地址为不同市的数量/用户总的收货地址数量"""
        return self.__get_mx_alipay_bills_data(factor="zfbCityCntOfAddreCnt")

    def zfbTotIncomeAmtL6m(self):
        """zfbTotIncomeAmtL6m 该用户平台最近6个月的交易中，收支类型为收入，且交易成功的交易金额之和"""
        return self.__get_mx_alipay_report(factor="zfbTotIncomeAmtL6m")

    def zfbCunJinBao(self):
        """zfbCunJinBao 用户存金宝余额"""
        return self.__get_mx_alipay_report(factor="zfbCunJinBao")

    def zfbLifePayAvg(self):
        """zfbLifePayAvg 用户通过平台，支付生活缴费类交易的金额之和/用户通过平台，支付生活缴费类交易的笔数之和"""
        return self.__get_mx_alipay_report(factor="zfbLifePayAvg")

    def zfbMaxConsumeAmtSum(self):
        """zfbMaxConsumeAmtSum 用户平台中的消费类交易里，最大单笔交易金额之和"""
        return self.__get_mx_alipay_report(factor="zfbMaxConsumeAmtSum")

    def zfbMaxOutAmtSum(self):
        """zfbMaxOutAmtSum 用户平台中的转出类交易中，最大单笔交易金额之和"""
        return self.__get_mx_alipay_report(factor="zfbMaxOutAmtSum")

    def zfbMaxTransInAmtSum(self):
        """zfbMaxTransInAmtSum 用户平台中的转入类交易中，最大单笔交易金额之和"""
        return self.__get_mx_alipay_report(factor="zfbMaxTransInAmtSum")

    def zfbIncomeAmtAvg(self):
        """zfbIncomeAmtAvg 用户资金转入收入总金额（不含自己资金的转移\退款金额）/用户资金收入总次数（不含自己资金的转移\退款）"""
        return self.__get_mx_alipay_bills_data(factor="zfbIncomeAmtAvg")

    def zfbTransInAvg(self):
        """zfbTransInAvg 用户平台中的交易，转入类交易的金额之和/用户平台中的交易，转入类交易的笔数之和"""
        return self.__get_mx_alipay_report(factor="zfbTransInAvg")

    def zfbTransInAmtSum(self):
        """zfbTransInAmtSum 用户平台中的交易，转入类交易的金额之和"""
        return self.__get_mx_alipay_report(factor="zfbTransInAmtSum")

    def zfbTakeOutAmtAvg(self):
        """zfbTakeOutAmtAvg 用户通过平台，支付外卖类交易的金额之和/用户通过平台，支付外卖类交易的次数之和"""
        return self.__get_mx_alipay_report(factor="zfbTakeOutAmtAvg")

    def zfbOnlineShoppingAmt(self):
        """zfbOnlineShoppingAmt 用户通过平台，支付网购类交易的金额之和"""
        return self.__get_mx_alipay_report(factor="zfbOnlineShoppingAmt")

    def zfbOnlineShoppingAvg(self):
        """zfbOnlineShoppingAvg 用户通过平台，支付网购类交易的平均金额"""
        return self.__get_mx_alipay_report(factor="zfbOnlineShoppingAvg")

    def zfbTotConsumeAmtSum(self):
        """zfbOnlineShoppingAvg 用户通过平台，进行消费类交易的金额之和"""
        return self.__get_mx_alipay_report(factor="zfbTotConsumeAmtSum")

    def zfbCreditRepayAmtAvg(self):
        """zfbCreditRepayAmtAvg 用户信用卡还款且交易成功的金额之和/信用卡还款且交易成功的次数之和"""
        return self.__get_mx_alipay_report(factor="zfbCreditRepayAmtAvg")

    def __get_udsp_record(self,factor):
        results = self.mongo.query_by_user_id(db='galaxy', collection="udsp_record", find={"serialNo": self.serial_no,'respCode':'00',"isFromVendor":False})
        if not results:
            if factor in ["c_no_mcc_L1m","c_mcc1_fin_unit_L6m","c_mcc1_credit_unit_L12m"]:
                return self.SET_DEFAULT_VALUE_INT_9999999
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        if not results[0].get("respData") or not results[0].get("respData").get("cardDataList") or not results[0].get("respData").get("cardDataList")[0].get("cardData"):
            return self.SET_DEFAULT_VALUE_INT_9999996

        cardData = results[0]['respData']['cardDataList'][0]['cardData']
        if not cardData.get(factor):
            if factor in ["c_no_mcc_L1m", "c_mcc1_fin_unit_L6m", "c_mcc1_credit_unit_L12m"]:
                return self.SET_DEFAULT_VALUE_INT_9999996
            return self.SET_DEFAULT_VALUE_FLOAT_9999996
        return float(cardData.get(factor)) if factor not in ["c_no_mcc_L1m", "c_mcc1_fin_unit_L6m", "c_mcc1_credit_unit_L12m"] else int(cardData.get(factor))

    def isHaveYlzt(self):
        """isHaveYlzt 是否有历史银联数据（有为：1，无为：0）"""
        results=self.mongo.query_by_user_id(db='galaxy', collection='udsp_record', find={"cardId": self.info.cert_id,'respCode':'00',"isFromVendor":True})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_0
        return self.SET_DEFAULT_VALUE_INT_1

    def isValidYlzt(self):
        """isValidYlzt 银联数据是否有效(有效为;1,无效为：0)"""
        results = self.mongo.query_by_user_id(db='galaxy', collection='udsp_record', find={"serialNo": self.serial_no,'respCode':'00',"isFromVendor":False})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_0
        return self.SET_DEFAULT_VALUE_INT_1

    def upoMcc2Fin1AmtL3mCache(self):
        """upoMcc2Fin1AmtL3mCache 银联掌亭缓存 卡片最近3个月金融-(理财和保险)交易金额"""
        return self.__get_udsp_record(factor='c_mcc2_fin1_amt_L3m')

    def upoNoMccL1mCache(self):
        """upoNoMccL1mCache 银联掌亭缓存 卡片最近1个月在多少个MCC上消费过"""
        return self.__get_udsp_record(factor='c_no_mcc_L1m')

    def upoCrSetlAmtL1mCache(self):
        """upoCrSetlAmtL1mCache 银联掌亭缓存 卡片最近1月贷方交易金额汇总"""
        return self.__get_udsp_record(factor='c_cr_setl_amt_L1m')

    def upoIncrSetlUnitL3mRCache(self):
        """upoIncrSetlUnitL3mRCache 银联掌亭缓存 卡片最近3个月交易笔数环比增长率"""
        return self.__get_udsp_record(factor='c_incr_setl_unit_L3m_r')

    def upoMcc1LiveAmtL3mCache(self):
        """upoMcc1LiveAmtL3mCache 银联掌亭缓存 卡片最近3个月居住交易金额"""
        return self.__get_udsp_record(factor='c_mcc1_live_amt_L3m')

    def upoDrIncrAmtL3mRCache(self):
        """upoDrIncrAmtL3mRCache 银联掌亭缓存 卡片最近3个月借方交易金额增长率"""
        return self.__get_udsp_record(factor='c_dr_incr_amt_L3m_r')

    def upoTrPayAmtL6mCache(self):
        """upoTrPayAmtL6mCache 银联掌亭缓存 卡片最近6个月代付交易金额"""
        return self.__get_udsp_record(factor='c_tr_pay_amt_L6m')

    def upoMcc1FinUnitL6mCache(self):
        """upoMcc1FinUnitL6mCache 银联掌亭缓存 卡片最近6个月金融交易笔数"""
        return self.__get_udsp_record(factor='c_mcc1_fin_unit_L6m')

    def upoMcc2FinCashAmtL3mCache(self):
        """upoMcc2FinCashAmtL3mCache 银联掌亭缓存 卡片最近3个月金融-现金业务交易金额"""
        return self.__get_udsp_record(factor='c_mcc2_fin_cash_amt_L3m')

    def upoMcc1CreditUnitL12mCache(self):
        """upoMcc1CreditUnitL12mCache 银联掌亭缓存 卡片最近12个月信用卡还款交易笔数"""
        return self.__get_udsp_record(factor='c_mcc1_credit_unit_L12m')

    def upoMcc2FinInsAmtL6mCache(self):
        """upoMcc2FinInsAmtL6mCache 银联掌亭缓存 卡片最近6个月金融保险交易金额"""
        return self.__get_udsp_record(factor='c_mcc2_fin_ins_amt_L6m')

    def upoBToTotAmtL6mRCache(self):
        """upoBToTotAmtL6mRCache 银联掌亭缓存 卡片最近6个月日常类消费金额占所有消费金额的比率"""
        return self.__get_udsp_record(factor='c_b_to_tot_amt_L6m_r')

    def upoSetlAmtPULl2mCache(self):
        """upoSetlAmtPULl2mCache 银联掌亭缓存 卡片最近12个月笔均交易金额"""
        return self.__get_udsp_record(factor='c_setl_amt_p_u_Ll2m')

    def upoMcc1CommAmtL12mCache(self):
        """upoMcc1CommAmtL12mCache 银联掌亭缓存 卡片最近12个月交通消费金额"""
        return self.__get_udsp_record(factor='c_mcc1_comm_amt_L12m')

    def upoMcc2FinInsAmtL12mCache(self):
        """upoMcc2FinInsAmtL12mCache 银联掌亭缓存 卡片最近12个月金融-保险交易金额"""
        return self.__get_udsp_record(factor='c_mcc2_fin_ins_amt_L12m')

    def zzcScore(self):
        """zzcScore 第三方外部数据中智诚雨点分"""
        zzcResult = self.mongo.query_by_user_id(db='galaxy',collection='zzc_score_record',find={"serialNo": self.serial_no})
        if not zzcResult:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return zzcResult[0].get("stratificationScore",self.SET_DEFAULT_VALUE_INT_9999996)

    def	yfAmapScore(self):
        """yfAmapScore 优分高知评分"""
        userAge =int(self.info.create_time.strftime('%Y')) - int(self.info.cert_id[6:10])
        if 20<=userAge<=22:
            yfResult = self.mongo.query_by_user_id(db='galaxy', collection='yf_score_record',find={"serialNo": self.serial_no})
            if yfResult[0].get("result")==str(-1):
                return self.SET_DEFAULT_VALUE_INT_9999999
            if not yfResult:
                return self.SET_DEFAULT_VALUE_INT_9999996
            return yfResult[0].get("score",self.SET_DEFAULT_VALUE_INT_9999996)
        return self.SET_DEFAULT_VALUE_INT_9999997

    def yfPersonalCheck(self):
        """yfPersonalCheck 优分铁路身份核验"""
        userAge =int(self.info.create_time.strftime('%Y')) - int(self.info.cert_id[6:10])
        if 20<=userAge<=22:
            yfResult = self.mongo.query_by_user_id(db='galaxy', collection='yf_pfv_record',find={"serialNo": self.serial_no})
            if not yfResult:
                return self.SET_DEFAULT_VALUE_INT_9999996
            if yfResult[0].get("s002")=="0":
                return self.SET_DEFAULT_VALUE_INT_1
            elif yfResult[0].get("s002")=="1":
                return self.SET_DEFAULT_VALUE_INT_0
            return yfResult[0].get("s002",self.SET_DEFAULT_VALUE_INT_9999996)
        return self.SET_DEFAULT_VALUE_INT_9999997

    def bjhyScore(self):
        """bjhyscore 冰鉴慧眼分"""
        bjHyResult= self.mongo.query_by_user_id(db='galaxy', collection='bj_hy_record',find={"serialNo": self.serial_no})
        if not bjHyResult:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return bjHyResult[0].get("bjScore",self.SET_DEFAULT_VALUE_INT_9999996)

    def __tdGuanResult(self,rule_id):
        results = self.mongo.query_by_user_id(db='galaxy', collection="td_guard_record",find={"serialNo": self.serial_no})
        if not results or not results[0].get('tdGuardResponse') or not results[0].get('tdGuardResponse').get('result_desc') or not results[0].get('tdGuardResponse').get('result_desc').get("ANTIFRAUD"):
            return self.SET_DEFAULT_VALUE_INT_9999999
        for row in results[0].get('tdGuardResponse').get('result_desc').get("ANTIFRAUD").get('risk_items'):
            if str(row.get('rule_id'))==str(rule_id):
                for lo in row.get('risk_detail'):
                    if lo.get("type")=="platform_detail":
                        return row.get('risk_detail')[0].get("platform_count",self.SET_DEFAULT_VALUE_INT_9999996)
                    return self.SET_DEFAULT_VALUE_INT_9999996
        return self.SET_DEFAULT_VALUE_INT_9999999

    def td7ApplyGuardCnt(self):
        """td7ApplyGuardCnt 同盾7天内申请人在多个平台申请借款"""
        return self.__tdGuanResult(rule_id='31490884')

    def td30ApplyGuardCnt(self):
        """td30ApplyGuardCnt 同盾1个月内申请人在多个平台申请借款"""
        return self.__tdGuanResult(rule_id='31490894')

    def td90ApplyGuardCnt(self):
        """td90ApplyGuardCnt 同盾3个月内申请人在多个平台申请借款"""
        return self.__tdGuanResult(rule_id='31490904')

    def tianqiScore(self):
        """tianqiScore 天启分"""
        result=self.mongo.query_by_user_id(db='galaxy', collection="tianqi_score",find={"serialNo": self.serial_no})
        if not result:
            return  self.SET_DEFAULT_VALUE_INT_9999999
        return result[0].get("score",self.SET_DEFAULT_VALUE_INT_9999996)

    def __get_alipay_bills_data(self):
        bills_data = self.mongo.queryall_by_userId(db='galaxy',collection='mx_alipay_bills_data',find={"user_id": self.info.user_id})
        return bills_data

    def zfbTiedCardIntervalDaysAvg(self):
        """zfbTiedCardIntervalDaysAvg 支付宝绑定银行卡的平均距今间隔"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("bankinfo"):
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        ToDayTime=[(return_strfYmd_date(self.info.event_time_add8h)-return_strfYmd_date(datetime.datetime.strptime(info.get("active_date")[:10],'%Y-%m-%d'))).days for info in billData[0].get("response").get("bankinfo") if info.get("active_date") and info.get("active_date")!=""]
        if not ToDayTime:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round(float(sum(ToDayTime))/len(ToDayTime),4)

    def zfbTiedCardIntervalDaysMax(self):
        """zfbTiedCardIntervalDaysMax 支付宝绑定银行卡距今最大间隔天数"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("bankinfo"):
            return self.SET_DEFAULT_VALUE_INT_9999995
        ToDayTime=[(return_strfYmd_date(self.info.event_time_add8h)-return_strfYmd_date(datetime.datetime.strptime(info.get("active_date")[:10],'%Y-%m-%d'))).days for info in billData[0].get("response").get("bankinfo") if info.get("active_date") and info.get("active_date")!=""]
        if not ToDayTime:
            return self.SET_DEFAULT_VALUE_INT_9999998
        return max(ToDayTime)

    def zfbTiedCardIntervalDaysMin(self):
        """zfbTiedCardIntervalDaysMin 支付宝绑定银行卡距今最小间隔天数"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("bankinfo"):
            return self.SET_DEFAULT_VALUE_INT_9999995
        ToDayTime=[(return_strfYmd_date(self.info.event_time_add8h)-return_strfYmd_date(datetime.datetime.strptime(info.get("active_date")[:10],'%Y-%m-%d'))).days for info in billData[0].get("response").get("bankinfo") if info.get("active_date") and info.get("active_date")!=""]
        if not ToDayTime:
            return self.SET_DEFAULT_VALUE_INT_9999998
        return min(ToDayTime)

    def zfbAppointedBankCardCnt(self):
        """zfbAppointedBankCardCnt 支付宝绑定工农中建交招银行卡数量"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("bankinfo"):
            return self.SET_DEFAULT_VALUE_INT_9999995
        bankList=[info.get("bank_name") for info in billData[0].get("response").get("bankinfo") if info.get("bank_name") and info.get("bank_name") in [u'中国工商银行',u'中国农业银行',u'中国建设银行',u'中国银行',u'交通银行',u'招商银行']]
        return len(bankList)

    def zfbAdrPhoneInContactsCnt(self):
        """zfbAdrPhoneInContactsCnt 支付宝收货地址号码和通讯录号码匹配数量"""
        contact=self.mongo.query_contact_list_beforeEvenTime_inXdays(db='lake',
                                                                      collection="s_user_mobile_contact_{0}".format(int(self.user_id) % 4),
                                                                      find={"user_id": int(self.user_id)}, serial_no=self.serial_no,days=180,clean=True,allData=False)
        if not contact:
            return self.SET_DEFAULT_VALUE_INT_9999999
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("alipaydeliveraddresses"):
            return self.SET_DEFAULT_VALUE_INT_9999995
        phoneNum=[info.get("phone_number") for info in billData[0].get("response").get("alipaydeliveraddresses") if info.get("phone_number") and info.get("phone_number")!=""]
        phoneList=[phone for phone in phoneNum if phone in contact]
        return len(phoneList)

    def zfbAdressInHomeCityCnt(self):
        """zfbAdressInHomeCityCnt 支付宝收货地址城市和用户居住城市一致个数"""
        homeCity=self.info.result.get("data").get("homeCity").replace(u"市","")
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("alipaydeliveraddresses"):
            return self.SET_DEFAULT_VALUE_INT_9999995
        addresses=[info.get("city").replace(u"市","") for info in billData[0].get("response").get("alipaydeliveraddresses") if info.get("city")]
        return addresses.count(homeCity)

    def zfbAdressCntDup(self):
        """zfbAdressCntDup 支付宝收货地址个数（去重）"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("alipaydeliveraddresses"):
            return self.SET_DEFAULT_VALUE_INT_9999995
        addresses=[info.get("address") for info in billData[0].get("response").get("alipaydeliveraddresses") if info.get("address")]
        return len(list(set(addresses)))

    def zfbAdrPhoneCntStartWithZero(self):
        """zfbAdrPhoneCntStartWithZero 支付宝中收货号码以“0”开头个数"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("alipaydeliveraddresses"):
            return self.SET_DEFAULT_VALUE_INT_9999995
        phoneNum=[info.get("phone_number") for info in billData[0].get("response").get("alipaydeliveraddresses") if info.get("phone_number") and info.get("phone_number")!=""]
        phoneList=[phone for phone in phoneNum if phone[:1]=="0"]
        return len(phoneList)

    def zfbAdressNameCnt(self):
        """zfbAdressNameCnt 支付宝不同收货人个数"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("alipaydeliveraddresses"):
            return self.SET_DEFAULT_VALUE_INT_9999995
        phoneNum=[info.get("name") for info in billData[0].get("response").get("alipaydeliveraddresses") if info.get("name")]
        return len(list(set(phoneNum)))

    def zfbRecentTradersCntDup(self):
        """zfbRecentTradersCntDup 支付宝不同交易联系人个数"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("recenttraders"):
            return self.SET_DEFAULT_VALUE_INT_9999995
        realName=[info.get("real_name") for info in billData[0].get("response").get("recenttraders") if info.get("real_name")]
        return len(list(set(realName)))

    def zfbBillDataOfYeb(self):
        """zfbBillDataOfYeb 支付宝余额宝内金额"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("wealth"):
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return float(billData[0].get("response").get("wealth").get("yeb",self.SET_DEFAULT_VALUE_FLOAT_9999998))

    def zfbBillDataOfYue(self):
        """zfbBillDataOfYue 支付宝用户在支付宝账户中的余额"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("wealth"):
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return float(billData[0].get("response").get("wealth").get("yue",self.SET_DEFAULT_VALUE_FLOAT_9999998))

    def zfbBillDataOfCjb(self):
        """zfbBillDataOfCjb 支付宝存金宝"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("wealth"):
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return float(billData[0].get("response").get("wealth").get("cjb",self.SET_DEFAULT_VALUE_FLOAT_9999998))

    def zfbBillDataOfHbBalance(self):
        """zfbBillDataOfHbBalance 支付宝花呗当前可用额度  H-kill 2,9,10  3,8"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("wealth"):
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return float(billData[0].get("response").get("wealth").get("huabai_balance",self.SET_DEFAULT_VALUE_FLOAT_9999998))

    def zfbBillDataOfHbLimit(self):
        """zfbBillDataOfHbLimit 支付宝花呗授信额度"""
        billData=self.__get_alipay_bills_data()
        if not billData:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        if not billData[0].get("response") or not billData[0].get("response").get("wealth"):
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return float(billData[0].get("response").get("wealth").get("huabai_limit",self.SET_DEFAULT_VALUE_FLOAT_9999998))

    def verificationResult(self):
        """verificationResult 是否有征信  --产品：2345借款"""
        result = self.mongo.query_by_user_id(db='galaxy',
                                             collection='ynxt_credit_apply',
                                             find={"serialNo": self.serial_no})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_0
        if result[0].get("result")=="0" :
            return result[0].get("verificationResult")
        return self.SET_DEFAULT_VALUE_INT_9999999

    def jkPbocResult(self):
        """jkPbocResult 我司征信规则结论  --产品：2345借款"""
        result = self.mongo.query_by_user_id(db='galaxy',
                                             collection='ynxt_credit_apply',
                                             find={"serialNo": self.serial_no})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result[0].get("result")=="0" and result[0].get("verificationResult")=="2":
            if result[0].get("ruleResult")[0]=='A':
                return 'A'
            else:
                return 'D'

        return self.SET_DEFAULT_VALUE_INT_9999999

    def jkPbocReason(self):
        """jkPbocReason 我司征信规则拒绝原因码  --产品：2345借款"""
        result = self.mongo.query_by_user_id(db='galaxy',
                                             collection='ynxt_credit_apply',
                                             find={"serialNo": self.serial_no})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result[0].get("result")=="-1":
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result[0].get("ruleResult")

    def creditScore(self):
        """creditScore 征信评分（联合建模返回评分） --产品：2345借款"""
        result = self.mongo.query_by_user_id(db='galaxy',
                                             collection='ynxt_credit_apply',
                                             find={"serialNo": self.serial_no})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result[0].get("result")=="0" and result[0].get("verificationResult")=="2":
            return result[0].get("scoreCard")
        return self.SET_DEFAULT_VALUE_INT_9999999

    def pbocFrom(self):
        """pbocFrom 征信来源银行名称  --产品：2345借款"""
        return "ynxt"

if __name__ == "__main__":
    serial_no = "1543218260681-412E4A7101EE286DD21924899E4805A7"
    a = ThirdFactor('T2', serial_no)
    print a.yfAmapScore()