# coding:utf-8
from utils import Setting
from utils.DES import Des
import json
from utils.Mysql_heXin import Mysql_heXin
from utils.Mysql_Account import Mysql_account
from FrameRunner.FactorInit import NewFactorInit
from utils.otherUtil import *
from utils.TestInit import factor_encrypt_identity
from dateutil.relativedelta import relativedelta

class CreditLineFactor(NewFactorInit):
    def __init__(self, env, serial_no):
        super(CreditLineFactor, self).__init__(env, serial_no)

    def originalCreditKdw(self):
        """originalCreditKdw 卡贷王产品的初始额度"""
        sql = "select * from skynet_credit_line where user_id='%s' and product_id='%s'" % (
            self.info.user_id, self.kdw_product_id)
        result = self.mysql.queryone_by_customer_id('skynet_credit_line', sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result.get('initial_credit_line', self.SET_DEFAULT_VALUE_INT_9999999)

    def originalCreditLjd(self):
        """originalCreditLjd 立即贷产品的初始额度"""
        sql = "select * from skynet_credit_line where user_id='%s' and product_id='%s'" % (
            self.info.user_id, self.ljd_product_id)
        result = self.mysql.queryone_by_customer_id('skynet_credit_line', sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result.get('initial_credit_line', self.SET_DEFAULT_VALUE_INT_9999999)

    def originalCreditXj(self):
        """originalCreditXj 2345借款平台下产品的初始额度"""
        sql = "select initial_credit_line from skynet_credit_line where user_id='%s' and product_id in ('10002','102','109') and is_delete=0 order by create_at"%self.info.user_id
        result = self.mysql.queryone_by_customer_id('skynet_credit_line', sql)
        return result.get('initial_credit_line',self.SET_DEFAULT_VALUE_INT_9999999)


    def originalCreditSxj(self):
        """originalCreditSxj 随心借产品的初始额度"""
        sql = "select * from skynet_credit_line where user_id='%s' and product_id='%s'" % (
            self.info.user_id, self.sxj_product_id)
        result = self.mysql.queryone_by_customer_id('skynet_credit_line', sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result.get('initial_credit_line', self.SET_DEFAULT_VALUE_INT_9999999)

    def dealAmtSumKdw(self):
        """dealAmtSumKdw 卡贷王产品总成交金额"""
        KDW_result = self.__hexin_bill(self.info.user_id, self.kdw_product_id, -24)
        KDW_current_result = [cur[3] for cur in KDW_result]
        return int(sum(KDW_current_result))

    def dealAmtSumLjd(self):
        """dealAmtSumLjd 立即贷产品总成交金额"""
        VIP_result = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        VIP_current_result = [cur[3] for cur in VIP_result]
        return int(sum(VIP_current_result))

    def dealAmtSumXj(self):
        """dealAmtSumXj 2345借款平台下产品总成交金额"""
        old_days_list_36 = self.__old_overdue_days(self.info.old_user_id, -36)
        VIP_result = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        SXJ_result = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -24)
        QL_result  = self.__hexin_bill(self.info.user_id, self.ql_product_id, -24)
        new_list=old_days_list_36+VIP_result+SXJ_result+QL_result
        current_result = [cur[3] for cur in new_list]
        return int(sum(current_result))

    def last1BorrowLateDaysXj(self):
        """last1BorrowLateDaysXj 2345借款平台下产品倒数第一次成交借款的逾期天数"""
        old_days_list_36 = self.__old_overdue_days(self.info.old_user_id, -36)
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        ql_days_list_12 = self.__hexin_bill(self.info.user_id, self.ql_product_id, -12)
        new_list = old_days_list_36 + ljd_days_list_12 + sxj_days_list_12 + ql_days_list_12
        new_list.sort()
        if not new_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        last1Overday = (return_strfYmd_date(new_list[-1][2]) - return_strfYmd_date(new_list[-1][1])).days
        return last1Overday

    def maxOverdueDaysXj(self):
        """maxOverdueDaysXj 2345借款平台下产品历史最大逾期天数"""
        old_days_list_36 = self.__old_overdue_days(self.info.old_user_id, -36)
        VIP_result = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        SXJ_result = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -24)
        QL_result  = self.__hexin_bill(self.info.user_id, self.ql_product_id, -24)
        new_list=old_days_list_36+VIP_result+SXJ_result+QL_result
        max_list = []
        for ljd in new_list:
            max_list.append((return_strfYmd_date(ljd[2]) - return_strfYmd_date(ljd[1])).days)
        if not max_list:
            return 0
        return max(max_list)

    def maxXjCreditLine(self):
        """maxXjCreditLine 2345借款平台下产品最大额度"""
        sql="select max_credit_line from skynet_credit_line where user_id='{0}' and product_id in ('10002','109','102') and is_delete=0".format(self.info.user_id)
        result=self.mysql.queryall_by_table_new_only('skynet_credit_line',sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return max([int(line.get("max_credit_line")) for line in result])


    def maxVipCreditLine(self):
        """maxVipCreditLine 立即贷最大额度"""
        sql="select * from skynet_credit_line where user_id='{0}' and product_id=10002 and is_delete=0".format(self.info.user_id)
        result=self.mysql.queryall_by_table_new_only('skynet_credit_line',sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        line=result[0]
        return int(line.get("max_credit_line"))

    def dealAmtSumSxj(self):
        """dealAmtSumSxj 随心借产品总成交金额"""
        SXJ_result = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -24)
        SXJ_current_result = [cur[3] for cur in SXJ_result]
        return int(sum(SXJ_current_result))

    def histDealNumXj(self):
        """histDealNumXj 客户在我司历史累计成交次数"""
        old_days_list_36 = self.__old_overdue_days(self.info.old_user_id, -36)
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        sxj_days_list = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -24)
        ql_days_list = self.__hexin_bill(self.info.user_id, self.ql_product_id, -24)
        return len(old_days_list_36)+len(ljd_days_list)+len(sxj_days_list)+len(ql_days_list)

    def histDealNumMore(self):
        """histDealNumMore 立即贷及之后产品成交次数"""
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        ql_days_list = self.__hexin_bill(self.info.user_id, self.ql_product_id, -24)
        return len(ljd_days_list)+len(ql_days_list)

    def histDealProductNum(self):
        """histDealProductNum 客户在立即贷及之后产品成交过的产品数"""
        count=0
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        ql_days_list = self.__hexin_bill(self.info.user_id, self.ql_product_id, -24)
        if ljd_days_list:
            count+=1
        if ql_days_list:
            count+=1
        return count

    def dealAmtSumOld(self):
        """dealAmtSumOld 即刻贷&贷款王产品总成交金额"""
        sql = "select sum(amount) ODL_Amount from all_fin_rownumber where user_id='%s'" % (self.info.old_user_id,)
        result = self.mysql.queryone_by_customer_id('skynet_fact_material', sql)
        if not result or not result.get('ODL_Amount'):
            return self.SET_DEFAULT_VALUE_INT_0
        return int(result.get('ODL_Amount'))

    def currUnclearedLoan(self):
        """currUnclearedLoan 当前未还清的借款数  --产品:即刻贷、贷款王、立即贷、随心借"""
        count = 0
        if self.info.old_user_id:
            JKD_sql = "select * from all_fin_rownumber where user_id='{0}' and bank_type in (10002,10001) and (real_repayment_principal < amount or real_repayment_principal is null )".format(
                self.info.old_user_id)
            JKD_result = self.mysql.queryall_by_table_new_only('skynet_fact_material', JKD_sql)
            if JKD_result:
                count += 1
            DKW_sql = "select * from all_fin_rownumber where user_id='{0}' and bank_type NOT in (10002,10001) and (real_repayment_principal < amount or real_repayment_principal is null )".format(
                self.info.old_user_id)
            DKW_result = self.mysql.queryall_by_table_new_only('skynet_fact_material', DKW_sql)
            if DKW_result:
                count += 1
        if self.ljd_customer_id:
            VIP_result=self.__hexin_bill(self.info.user_id,self.ljd_product_id,-24)
            VIP_current_result=[cur for cur in VIP_result if cur[4] in (1,3)]
            if VIP_current_result:
                count += 1
        if self.sxj_customer_id:
            SXJ_result=self.__hexin_bill(self.info.user_id,self.sxj_product_id,-24)
            SXJ_current_result=[cur for cur in SXJ_result if cur[4] in (1,3)]
            if SXJ_current_result:
                count += 1
        return count

    def currentOverdueStatusPamth(self):
        """currentOverdueStatusPamth 客户当前预期状态  --产品:即刻贷、贷款王、立即贷、随心借、卡贷王、商贷王、车贷王、畅借款"""
        if self.info.old_user_id:
            sql = "select acct_status from s_user_finance_account where user_id=%s and acct_status in (22, 23, 24, 25)" % self.info.old_user_id
            OldOverdue = self.mysql.queryone_by_customer_id('xinyongjin', sql)
            if OldOverdue:
                return self.SET_DEFAULT_VALUE_INT_1
        if self.sxj_customer_id:
            SXJ_result=self.__hexin_bill(self.info.user_id,self.sxj_product_id,-24)
            SXJ_current_result=[cur for cur in SXJ_result if cur[4]==3]
            if SXJ_current_result:
                return self.SET_DEFAULT_VALUE_INT_1
        if self.ljd_customer_id:
            VIP_result=self.__hexin_bill(self.info.user_id,self.ljd_product_id,-24)
            VIP_current_result=[cur for cur in VIP_result if cur[4]==3]
            if VIP_current_result:
                return self.SET_DEFAULT_VALUE_INT_1
        if self.kdw_customer_id:
            KDW_result=self.__hexin_bill(self.info.user_id,self.kdw_product_id,-24)
            KDW_current_result=[cur for cur in KDW_result if cur[4]==3]
            if KDW_current_result:
                return self.SET_DEFAULT_VALUE_INT_1
        if self.ql_customer_id:
            KDW_result=self.__hexin_bill(self.info.user_id,self.ql_product_id,-24)
            KDW_current_result=[cur for cur in KDW_result if cur[4]==3]
            if KDW_current_result:
                return self.SET_DEFAULT_VALUE_INT_1
        # 商贷王
        if Setting.SETTING['cdw']['isCheck'] == 1:
            r = requests.post(url=Setting.SETTING['sdw']['url'], data={'idcard': self.info.cert_id})
            responseJson = r.json()
            if responseJson.get('tips') == 'success':
                isOverdue = responseJson.get("data").get("overdueDays")
                if isOverdue > 0:
                    return self.SET_DEFAULT_VALUE_INT_1
        # 车贷王
        if Setting.SETTING['cdw']['isCheck'] == 1:
            sql = "SELECT CASE WHEN COUNT(1) > 0 THEN 1 ELSE 0 END isOverdue FROM lb_apply_lessee_info a " \
                  "INNER JOIN lb_repay_plan b ON a.asqbh = b.asqbhWHERE azjhm = '%s' AND b.azt = 2" % self.info.cert_id
            CDWMaxDay = self.mysql.queryone_by_customer_id('zu_che', sql)
            if CDWMaxDay:
                CDWOverdue = CDWMaxDay['isOverdue']
                if CDWOverdue == 1:
                    return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def current_overdue_status(self):
        """current_overdue_status 客户当前预期状态 --产品:即刻贷、贷款王、立即贷、商贷王、车贷王"""
        if self.info.old_user_id:
            sql = "select acct_status from s_user_finance_account where user_id=%s and acct_status in (22, 23, 24, 25)" % self.info.old_user_id
            OldOverdue = self.mysql.queryone_by_customer_id('xinyongjin', sql)
            if OldOverdue:
                return 1
        if self.ljd_customer_id:
            VIP_result=self.__hexin_bill(self.info.user_id,self.ljd_product_id,-24)
            VIP_current_result=[cur for cur in VIP_result if cur[4]==3]
            if VIP_current_result:
                return 1
        # 商贷王
        if Setting.SETTING['cdw']['isCheck'] == 1:
            r = requests.post(url=Setting.SETTING['sdw']['url'], data={'idcard': self.info.cert_id})
            responseJson = r.json()
            if responseJson.get('tips') == 'success':
                isOverdue = responseJson.get("data").get("overdueDays")
                if isOverdue > 0:
                    return 1
        # 车贷王
        if Setting.SETTING['cdw']['isCheck'] == 1:
            sql = "SELECT CASE WHEN COUNT(1) > 0 THEN 1 ELSE 0 END isOverdue FROM lb_apply_lessee_info a " \
                  "INNER JOIN lb_repay_plan b ON a.asqbh = b.asqbhWHERE azjhm = '%s' AND b.azt = 2" % self.info.cert_id
            CDWMaxDay = self.mysql.queryone_by_customer_id('zu_che', sql)
            if CDWMaxDay:
                CDWOverdue = CDWMaxDay['isOverdue']
                if CDWOverdue == 1:
                    return 1
        return 0

    # def __hexin_bill(self, user_id, product_id, month):
    #     ResultList = []
    #     MonthBefore = str(getXmonthDate(self.info.event_time_add8h, month))
    #     sql = "SELECT l.user_id userId,l.prod_id productId,l.stage_ret overdueStatus,l.borrow_approve_date borrowDate,l.next_repay_date nextPayDate ," \
    #           "p.settle_date realPaymentDate, l.total_principal totalBorrowAmount,l.loan_no loanNo,l.id billId  FROM loan_info l JOIN repay_plan_info p ON l.id = p.loan_id  " \
    #           "AND l.user_id='%s' AND p.user_id='%s' AND l.prod_id= '%s' AND p.prod_id= '%s' AND l.borrow_approve_date  >= '%s'" \
    #           "AND l.delete_flag = 1 AND p.delete_flag = 1 ORDER BY l.borrow_approve_date" % (user_id, user_id, product_id, product_id, MonthBefore)
    #     billList = Mysql_heXin(self.env, user_id % 20).queryall_by_id(sql=sql)
    #     if not billList:
    #         return []
    #     for billRecord in billList:
    #         if not billRecord.get('realPaymentDate'):
    #             realPaymentDate = self.info.event_time_add8h
    #         else:
    #             realPaymentDate = billRecord.get('realPaymentDate')
    #         ResultList.append([billRecord.get('borrowDate'),
    #                            billRecord.get('nextPayDate'),
    #                            realPaymentDate,
    #                            billRecord.get('totalBorrowAmount'),
    #                            billRecord.get('overdueStatus'),
    #                            str(billRecord.get("loanNo")),
    #                            billRecord.get("billId")])
    #     return ResultList

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
                               billRecord.get("loan_id"),
                               float(billRecord.get('repay_principal'))]),
        ResultList.sort()
        return ResultList

    def __old_overdue_days(self, oldUserId, month):
        old_list = []
        time1MonthBefore = str(getXmonthDate(self.info.event_time_add8h, month))
        sql = "select * from all_fin_rownumber where user_id ='%s' and borrow_date >= '%s' order by rank ;" % (
        oldUserId, time1MonthBefore)
        result = self.mysql.queryall_by_customer_id('skynet_fact_material', sql)
        if result:
            for li in result:
                if not li.get('real_repayment_date'):
                    li['real_repayment_date'] = self.info.event_time_add8h
                if type(li['real_repayment_date']) == datetime.date:
                    realRepaymentDate = datetime.datetime.strptime(str(li.get('real_repayment_date')), '%Y-%m-%d')
                else:
                    realRepaymentDate = li['real_repayment_date']
                old_list.append([datetime.datetime.strptime(str(li.get('borrow_date')), '%Y-%m-%d'),
                                 datetime.datetime.strptime(str(li.get('next_pay_date')), '%Y-%m-%d'),
                                 realRepaymentDate,
                                 li.get('amount'),
                                 li.get('bank_type')])
        return old_list

    def last3BorrowLateDays(self):
        """last3BorrowLateDays 倒数第三次成交借款的逾期天数  --产品：即刻贷、贷款王、立即贷"""
        old_days_list_12 = []
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        ljd_days_list_12.sort()
        overdue_list = old_days_list_12 + ljd_days_list_12
        if not overdue_list or len(overdue_list) < 3:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return (return_strfYmd_date(overdue_list[-3][2]) - return_strfYmd_date(overdue_list[-3][1])).days

    def userMonerDaysAvgL1m(self):
        """userMonerDaysAvgL1m 近一个月平均用款天数  --产品：立即贷"""
        user_money_day = []
        ljd_days_list_1 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -1)
        if not ljd_days_list_1:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        for li in ljd_days_list_1:
            user_money_day.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        return round(float(sum(user_money_day)) / len(user_money_day), 4)

    def useMoneyDaysAvgL1mCjk(self):
        """useMoneyDaysAvgL1mCjk 畅借款近一个月平均用款天数"""
        user_money_day = []
        ql_days_list_1 = self.__hexin_bill(self.info.user_id, self.ql_product_id, -1)
        if not ql_days_list_1:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        for li in ql_days_list_1:
            user_money_day.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        return round(float(sum(user_money_day)) / len(user_money_day), 4)

    def useRpInterLes0MinL12m(self):
        """useRpInterLes0MinL12m 近十二个月小于0的最小借还款间隔  --产品：即刻贷、贷款王、立即贷"""
        old_days_list_12 = []
        max_12 = []
        old_12 = []
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        if len(old_days_list_12) > 1:
            for i in range(len(old_days_list_12) - 1):
                if (return_strfYmd_date(old_days_list_12[i + 1][0]) - return_strfYmd_date(
                        old_days_list_12[i][2])).days < 0:
                    old_12.append((return_strfYmd_date(old_days_list_12[i + 1][0]) - return_strfYmd_date(
                        old_days_list_12[i][2])).days)
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        if not ljd_days_list_12 and (len(ljd_days_list_12) + len(old_12)) <= 1 and not old_12:
            return self.SET_DEFAULT_VALUE_INT_9999995
        ljd_days_list_12.sort()
        for i in range(len(ljd_days_list_12) - 1):
            if (return_strfYmd_date(ljd_days_list_12[i + 1][0]) - return_strfYmd_date(ljd_days_list_12[i][2])).days < 0:
                max_12.append((return_strfYmd_date(ljd_days_list_12[i + 1][0]) - return_strfYmd_date(
                    ljd_days_list_12[i][2])).days)
        if not max_12 and not old_12:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return min(max_12 + old_12)

    def m0Amount6And12(self):
        """m0Amount6And12 近六个月的逾期借款金额占近十二个月的成交总金额的比例  --产品：即刻贷、贷款王、立即贷"""
        old_days_list_12 = []
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        money_list_12 = ljd_days_list_12 + old_days_list_12
        if not money_list_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        total_12_money = 0
        for day in money_list_12:
            total_12_money = total_12_money + day[3]
        old_days_list_6 = []
        ljd_days_list_6 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -6)
        if self.info.old_user_id:
            old_days_list_6 = self.__old_overdue_days(self.info.old_user_id, -6)
        money_list_6 = old_days_list_6 + ljd_days_list_6
        total_6_money = 0
        for day in money_list_6:
            if (return_strfYmd_date(day[2]) - return_strfYmd_date(day[1])).days > 0:
                total_6_money = total_6_money + day[3]
        return round(total_6_money / total_12_money, 4)

    def dealAmountAvgL12m(self):
        """dealAmountAvgL12m 近十二个月的平均成交金额  --产品：即刻贷、贷款王、立即贷"""
        old_days_list_12 = []
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        money_list_12 = ljd_days_list_12 + old_days_list_12
        if not money_list_12:
            return self.SET_DEFAULT_VALUE_INT_9999998
        total_12_money = 0
        for day in money_list_12:
            total_12_money = total_12_money + day[3]
        return int(total_12_money / len(money_list_12))

    def useMoneyIntervalMinL1m(self):
        """useMoneyIntervalMinL1m 近一个月最小用款间隔   --产品：立即贷"""
        new_days_list_1 = []
        old_days_list_1 = []
        ljd_days_list_1 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        for i in range(len(ljd_days_list_1)):
            if ljd_days_list_1[i][0] >= getXmonthDate(self.info.event_time_add8h, -1):
                new_days_list_1.append(ljd_days_list_1[i])
            else:
                old_days_list_1.append(ljd_days_list_1[i])
        old_days_list_1.sort()
        if old_days_list_1:
            new_days_list_1.append(old_days_list_1[-1])
        new_days_list_1.sort()
        if not new_days_list_1 or len(new_days_list_1) <= 1:
            return self.SET_DEFAULT_VALUE_INT_9999995
        user_money_day = []
        for i in range(len(new_days_list_1) - 1):
            user_money_day.append(
                (return_strfYmd_date(new_days_list_1[i + 1][0]) - return_strfYmd_date(new_days_list_1[i][0])).days)
        return min(user_money_day)

    def borrowAmountL2m(self):
        """borrowAmountL2m 近两个月总成交金额   --产品：立即贷"""
        ljd_days_list_2 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -2)
        total_2_money = 0
        for day in ljd_days_list_2:
            total_2_money = total_2_money + day[3]
        return int(total_2_money)

    def useMoneyDaysAvgL1mLjd(self):
        """useMoneyDaysAvgL1mLjd 立即贷近一个月平均用款天数  --产品：立即贷"""
        user_money_day = []
        ljd_days_list_1 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -1)
        if not ljd_days_list_1:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        for li in ljd_days_list_1:
            user_money_day.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        return round(float(sum(user_money_day)) / len(user_money_day), 4)

    def rtoMaxRpInterL1mLjdSxj(self):
        """rtoMaxRpInterL1mLjdSxj 近一个月的最大借还款间隔/历史最大借还款间隔  --产品：即刻贷、贷款王、立即贷、随心借"""
        # 1个月
        max_1 = []
        old_all_days_list_1 = []
        new_all_days_list_1 = []
        ljd_days_list_1 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_1 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        all_days_list_1 = ljd_days_list_1 + sxj_days_list_1
        for i in range(len(all_days_list_1)):
            if all_days_list_1[i][0] >= getXmonthDate(self.info.event_time_add8h, -1):
                new_all_days_list_1.append(all_days_list_1[i])
            else:
                old_all_days_list_1.append(all_days_list_1[i])
        old_all_days_list_1.sort()
        if old_all_days_list_1:
            new_all_days_list_1.append(old_all_days_list_1[-1])
        if new_all_days_list_1 and len(new_all_days_list_1) > 1:
            new_all_days_list_1.sort()
            for i in range(len(new_all_days_list_1) - 1):
                max_1.append((return_strfYmd_date(new_all_days_list_1[i + 1][0]) - return_strfYmd_date(
                    new_all_days_list_1[i][2])).days)
        # 12个月
        old_days_list_12 = []
        max_12 = []
        old_12 = []
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        if len(old_days_list_12) > 1:
            for i in range(len(old_days_list_12) - 1):
                old_12.append((return_strfYmd_date(old_days_list_12[i + 1][0]) - return_strfYmd_date(
                    old_days_list_12[i][2])).days)
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        all_days_list_12 = ljd_days_list_12 + sxj_days_list_12
        if not all_days_list_12 and len(all_days_list_12) <= 1 and not old_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        all_days_list_12.sort()
        for i in range(len(all_days_list_12) - 1):
            max_12.append(
                (return_strfYmd_date(all_days_list_12[i + 1][0]) - return_strfYmd_date(all_days_list_12[i][2])).days)
        if not (max_12 + old_12) or max(max_12 + old_12) == 0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        if not max_1:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(float(max(max_1)) / max(max_12 + old_12), 4)

    def rtoMaxRpInterL1mXj(self):
        """rtoMaxRpInterL1mXj 用户近一个月的最大借还款间隔/近十二个月最大借还款间隔  --产品：立即贷、随心借、畅快借"""
        # 1个月
        max_1 = []
        old_all_days_list_1 = []
        new_all_days_list_1 = []
        ljd_days_list_1 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_1 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        ql_days_list_1 = self.__hexin_bill(self.info.user_id, self.ql_product_id, -12)
        all_days_list_1 = ljd_days_list_1 + sxj_days_list_1+ql_days_list_1
        for i in range(len(all_days_list_1)):
            if all_days_list_1[i][0] >= getXmonthDate(self.info.event_time_add8h, -1):
                new_all_days_list_1.append(all_days_list_1[i])
            else:
                old_all_days_list_1.append(all_days_list_1[i])
        old_all_days_list_1.sort()
        if old_all_days_list_1:
            new_all_days_list_1.append(old_all_days_list_1[-1])
        if new_all_days_list_1 and len(new_all_days_list_1) > 1:
            new_all_days_list_1.sort()
            for i in range(len(new_all_days_list_1) - 1):
                max_1.append((return_strfYmd_date(new_all_days_list_1[i + 1][0]) - return_strfYmd_date(
                    new_all_days_list_1[i][2])).days)
        # 12个月
        old_days_list_12 = []
        max_12 = []
        old_12 = []
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        if len(old_days_list_12) > 1:
            for i in range(len(old_days_list_12) - 1):
                old_12.append((return_strfYmd_date(old_days_list_12[i + 1][0]) - return_strfYmd_date(
                    old_days_list_12[i][2])).days)
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        ql_days_list_12 = self.__hexin_bill(self.info.user_id, self.ql_product_id, -12)
        all_days_list_12 = ljd_days_list_12 + sxj_days_list_12+ql_days_list_12
        if not all_days_list_12 and len(all_days_list_12) <= 1 and not old_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        all_days_list_12.sort()
        for i in range(len(all_days_list_12) - 1):
            max_12.append(
                (return_strfYmd_date(all_days_list_12[i + 1][0]) - return_strfYmd_date(all_days_list_12[i][2])).days)
        if not (max_12 + old_12) or max(max_12 + old_12) == 0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        if not max_1:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(float(max(max_1)) / max(max_12 + old_12), 4)

    def rtoMaxRpInterL1mLjd(self):
        """rtoMaxRpInterL1mLjd 立即贷产品近一个月的最大借还款间隔/历史最大借还款间隔   --产品：即刻贷、贷款王、立即贷"""
        # 1个月
        max_1 = []
        old_ljd_days_list_1 = []
        new_ljd_days_list_1 = []
        ljd_days_list_1 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        for i in range(len(ljd_days_list_1)):
            if ljd_days_list_1[i][0] >= getXmonthDate(self.info.event_time_add8h, -1):
                new_ljd_days_list_1.append(ljd_days_list_1[i])
            else:
                old_ljd_days_list_1.append(ljd_days_list_1[i])
        old_ljd_days_list_1.sort()
        if old_ljd_days_list_1:
            new_ljd_days_list_1.append(old_ljd_days_list_1[-1])

        if new_ljd_days_list_1 and len(new_ljd_days_list_1) > 1:
            new_ljd_days_list_1.sort()
            for i in range(len(new_ljd_days_list_1) - 1):
                max_1.append((return_strfYmd_date(new_ljd_days_list_1[i + 1][0]) - return_strfYmd_date(
                    new_ljd_days_list_1[i][2])).days)

        # 12个月
        old_days_list_12 = []
        max_12 = []
        old_12 = []
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        if len(old_days_list_12) > 1:
            for i in range(len(old_days_list_12) - 1):
                old_12.append((return_strfYmd_date(old_days_list_12[i + 1][0]) - return_strfYmd_date(
                    old_days_list_12[i][2])).days)
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        if not ljd_days_list_12 and len(ljd_days_list_12) <= 1 and not old_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        ljd_days_list_12.sort()
        for i in range(len(ljd_days_list_12) - 1):
            max_12.append(
                (return_strfYmd_date(ljd_days_list_12[i + 1][0]) - return_strfYmd_date(ljd_days_list_12[i][2])).days)
        if not (max_12 + old_12) or max(max_12 + old_12) == 0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        if not max_1:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(float(max(max_1)) / max(max_12 + old_12), 4)

    def rtoMaxRpInterL1mSxj(self):
        """rtoMaxRpInterL1mSxj 随心借近一个月的最大借还款间隔/历史最大借还款间隔  --产品：即刻贷、贷款王、随心借"""
        # 1个月
        max_1 = []
        old_sxj_days_list_1 = []
        new_sxj_days_list_1 = []
        sxj_days_list_1 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        for i in range(len(sxj_days_list_1)):
            if sxj_days_list_1[i][0] >= getXmonthDate(self.info.event_time_add8h, -1):
                new_sxj_days_list_1.append(sxj_days_list_1[i])
            else:
                old_sxj_days_list_1.append(sxj_days_list_1[i])
        old_sxj_days_list_1.sort()
        if old_sxj_days_list_1:
            new_sxj_days_list_1.append(old_sxj_days_list_1[-1])
        if new_sxj_days_list_1 and len(new_sxj_days_list_1) > 1:
            new_sxj_days_list_1.sort()
            for i in range(len(new_sxj_days_list_1) - 1):
                max_1.append((return_strfYmd_date(new_sxj_days_list_1[i + 1][0]) - return_strfYmd_date(
                    new_sxj_days_list_1[i][2])).days)
        # 12个月
        old_days_list_12 = []
        max_12 = []
        old_12 = []
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        if len(old_days_list_12) > 1:
            for i in range(len(old_days_list_12) - 1):
                old_12.append((return_strfYmd_date(old_days_list_12[i + 1][0]) - return_strfYmd_date(
                    old_days_list_12[i][2])).days)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        if not sxj_days_list_12 and len(sxj_days_list_12) <= 1 and not old_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        sxj_days_list_12.sort()
        for i in range(len(sxj_days_list_12) - 1):
            max_12.append(
                (return_strfYmd_date(sxj_days_list_12[i + 1][0]) - return_strfYmd_date(sxj_days_list_12[i][2])).days)
        if not (max_12 + old_12) or max(max_12 + old_12) == 0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        if not max_1:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(float(max(max_1)) / max(max_12 + old_12), 4)

    def rtoMaxUseMoneyDaysL3mLjdSxj(self):
        """rtoMaxUseMoneyDaysL3mLjdSxj 近3个月的最大用款天数/历史最大用款天数   --产品：即刻贷、贷款王、立即贷、随心借"""
        old_days_list_12 = []
        max_3 = []
        max_12 = []
        ljd_days_list_3 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -3)
        sxj_days_list_3 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -3)
        all_days_list_3 = ljd_days_list_3 + sxj_days_list_3
        for li in all_days_list_3:
            max_3.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        all_days_list_12 = old_days_list_12 + ljd_days_list_12 + sxj_days_list_12
        if not all_days_list_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        for li in all_days_list_12:
            max_12.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        if max_12 and not max_3:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(float(max(max_3)) / max(max_12), 4)

    def rtoMaxUseMoneyDaysL3mXj(self):
        """rtoMaxUseMoneyDaysL3mXj 用户近3个月的最大用款天数/近十二个月最大用款天数"""
        old_days_list_12 = []
        max_3 = []
        max_12 = []
        ljd_days_list_3 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -3)
        sxj_days_list_3 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -3)
        ql_days_list_3 = self.__hexin_bill(self.info.user_id, self.ql_product_id, -3)
        all_days_list_3 = ljd_days_list_3 + sxj_days_list_3+ql_days_list_3
        for li in all_days_list_3:
            max_3.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        ql_days_list_12 = self.__hexin_bill(self.info.user_id, self.ql_product_id, -12)
        all_days_list_12 = old_days_list_12 + ljd_days_list_12 + sxj_days_list_12+ql_days_list_12
        if not all_days_list_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        for li in all_days_list_12:
            max_12.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        if max_12 and not max_3:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(float(max(max_3)) / max(max_12), 4)

    def rtoMaxUseMoneyDaysL3mLjd(self):
        """rtoMaxUseMoneyDaysL3mLjd 立即贷近3个月的最大用款天数/历史最大用款天数   --产品：即刻贷、贷款王、立即贷"""
        old_days_list_12 = []
        max_3 = []
        max_12 = []
        ljd_days_list_3 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -3)
        for li in ljd_days_list_3:
            max_3.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        all_days_list_12 = old_days_list_12 + ljd_days_list_12
        if not all_days_list_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        for li in all_days_list_12:
            max_12.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        if max_12 and not max_3:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(float(max(max_3)) / max(max_12), 4)

    def rtoMaxUseMoneyDaysL3mSxj(self):
        """rtoMaxUseMoneyDaysL3mSxj 随心借近3个月的最大用款天数/历史最大用款天数  --产品：即刻贷、贷款王、随心借"""
        old_days_list_12 = []
        max_3 = []
        max_12 = []
        sxj_days_list_3 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -3)
        for li in sxj_days_list_3:
            max_3.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        all_days_list_12 = old_days_list_12 + sxj_days_list_12
        if not all_days_list_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        for li in all_days_list_12:
            max_12.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        if not max_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        if not max_3:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(float(max(max_3)) / max(max_12), 4)

    def last3BorrowLateDaysPamth(self):
        """last3BorrowLateDaysPamth 倒数第三次成交借款的逾期天数  --产品：即刻贷、贷款王、立即贷、随心借"""
        old_days_list_12 = []
        new_days_list = []
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        for ljd in ljd_days_list_12:
            if ljd[4] == 2:
                new_days_list.append(ljd)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        for sxj in sxj_days_list_12:
            if sxj[4] == 2:
                new_days_list.append(sxj)
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        new_days_list.sort()
        overdue_list = old_days_list_12 + new_days_list
        if not overdue_list or len(overdue_list) < 3:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return (return_strfYmd_date(overdue_list[-3][2]) - return_strfYmd_date(overdue_list[-3][1])).days

    def useMoneyDaysAvgL1mAmth(self):
        """useMoneyDaysAvgL1mAmth 近一个月平均用款天数  --产品：随心借"""
        user_money_day = []
        sxj_days_list_1 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -1)
        if not sxj_days_list_1:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        for li in sxj_days_list_1:
            user_money_day.append((return_strfYmd_date(li[2]) - return_strfYmd_date(li[0])).days)
        return round(float(sum(user_money_day)) / len(user_money_day), 4)

    def useRpInterLes0MinL12mPamth(self):
        """useRpInterLes0MinL12mPamth 近十二个月小于0的最小借还款间隔 产品：即刻贷、贷款王、立即贷、随心借"""
        old_days_list_12 = []
        max_12 = []
        old_12 = []
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        if len(old_days_list_12) > 1:
            for i in range(len(old_days_list_12) - 1):
                if (return_strfYmd_date(old_days_list_12[i + 1][0]) - return_strfYmd_date(
                        old_days_list_12[i][2])).days < 0:
                    old_12.append((return_strfYmd_date(old_days_list_12[i + 1][0]) - return_strfYmd_date(
                        old_days_list_12[i][2])).days)
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        new_list = ljd_days_list_12 + sxj_days_list_12

        if not new_list and (len(new_list) + len(old_12)) <= 1 and not old_12:
            return self.SET_DEFAULT_VALUE_INT_9999995
        new_list.sort()
        for i in range(len(new_list) - 1):
            if (return_strfYmd_date(new_list[i + 1][0]) - return_strfYmd_date(new_list[i][2])).days < 0:
                max_12.append((return_strfYmd_date(new_list[i + 1][0]) - return_strfYmd_date(new_list[i][2])).days)
        if not max_12 and not old_12:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return min(max_12 + old_12)

    def rtoDefAmtL6mToDealAmtL12m(self):
        """rtoDefAmtL6mToDealAmtL12m 近六个月的逾期借款金额占近十二个月的成交总金额的比例  产品：即刻贷、贷款王、立即贷、随心借"""
        old_days_list_12 = []
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        money_list_12 = ljd_days_list_12 + sxj_days_list_12 + old_days_list_12
        if not money_list_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        total_12_money = 0
        for day in money_list_12:
            total_12_money = total_12_money + day[3]

        old_days_list_6 = []
        ljd_days_list_6 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -6)
        sxj_days_list_6 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -6)
        if self.info.old_user_id:
            old_days_list_6 = self.__old_overdue_days(self.info.old_user_id, -6)
        money_list_6 = old_days_list_6 + ljd_days_list_6 + sxj_days_list_6

        total_6_money = 0
        for day in money_list_6:
            if (return_strfYmd_date(day[2]) - return_strfYmd_date(day[1])).days > 0:
                total_6_money = total_6_money + day[3]
        return round(total_6_money / total_12_money, 4)

    def dealAmountAvgL12mPamth(self):
        """dealAmountAvgL12mPamth 近十二个月的平均成交金额  --产品：即刻贷、贷款王、立即贷、随心借"""
        old_days_list_12 = []
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        if self.info.old_user_id:
            old_days_list_12 = self.__old_overdue_days(self.info.old_user_id, -12)
        money_list_12 = ljd_days_list_12 + sxj_days_list_12 + old_days_list_12
        if not money_list_12:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        total_12_money = 0
        for day in money_list_12:
            total_12_money = total_12_money + day[3]
        return round(float(total_12_money) / len(money_list_12), 4)

    def useMoneyIntervalMinL1mPamth(self):
        """useMoneyIntervalMinL1m 近一个月最小用款间隔   --产品：立即贷、随心借"""
        old_days_list = []
        new_days_list = []
        ljd_days_list_1 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_1 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        new_list = ljd_days_list_1 + sxj_days_list_1
        for i in range(len(new_list)):
            if new_list[i][0] >= getXmonthDate(self.info.event_time_add8h, -1):
                new_days_list.append(new_list[i])
            else:
                old_days_list.append(new_list[i])
        old_days_list.sort()
        if old_days_list:
            new_days_list.append(old_days_list[-1])
        new_days_list.sort()
        if not new_days_list or len(new_days_list) <= 1:
            return self.SET_DEFAULT_VALUE_INT_9999995
        user_money_day = []
        for i in range(len(new_days_list) - 1):
            user_money_day.append(
                (return_strfYmd_date(new_days_list[i + 1][0]) - return_strfYmd_date(new_days_list[i][0])).days)
        return min(user_money_day)

    def borrowAmountL2mPamth(self):
        """borrowAmountL2mPamth 近两个月总成交金额   --产品：立即贷、随心借"""
        ljd_days_list_2 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -2)
        sxj_days_list_2 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -2)
        new_list = ljd_days_list_2 + sxj_days_list_2
        total_2_money = 0
        for day in new_list:
            total_2_money = total_2_money + day[3]
        return int(total_2_money)

    def __get_contact_old_userId(self, contactPerson):
        contact = self.info.result.get('data').get(contactPerson)
        if contact:
            result = self.mysql.queryone_by_customer_id(db="xinyongjin",
                                                        sql="select id from s_user where mobilephone ='%s'" % contact)
            if not result:
                return False
            return result.get('id')
        else:
            return "Error"

    def __get_contact_new_userId(self, contactPerson):
        contact = self.info.result.get('data').get(contactPerson)
        if contact:
            result = self.mysql.queryone_by_customer_id(db='customer_center',
                                                        sql="SELECT id FROM `user` WHERE mobilephone = '%s'" % factor_encrypt_identity(
                                                            contact))
            if not result:
                return False
            return result.get('id')
        else:
            return "Error"

    def relaFamilyOverdueDays(self):
        """relaFamilyOverdueDays 直系亲属联系人-历史借款最大逾期天数  --产品：即刻贷、贷款王、立即贷"""
        if self.__get_contact_old_userId("relativeContact") == 'Error' or self.__get_contact_new_userId(
                "relativeContact") == 'Error':
            return self.SET_DEFAULT_VALUE_INT_9999999
        overdue_list = []
        if self.__get_contact_old_userId("relativeContact"):
            old_list = self.__old_overdue_days(self.__get_contact_old_userId("relativeContact"), -36)
            for old in old_list:
                overdue_list.append((return_strfYmd_date(old[2]) - return_strfYmd_date(old[1])).days)
        if self.__get_contact_new_userId("relativeContact"):
            new_list = self.__hexin_bill(self.__get_contact_new_userId("relativeContact"), self.ljd_product_id, -36)+\
                       self.__hexin_bill(self.__get_contact_new_userId("friendContact"), self.sxj_product_id, -36)+\
                       self.__hexin_bill(self.__get_contact_new_userId("friendContact"), self.ql_product_id, -36)
            for new in new_list:
                overdue_list.append((return_strfYmd_date(new[2]) - return_strfYmd_date(new[1])).days)
        if not overdue_list:
            return 0
        if max(overdue_list) < 0:
            return 0
        return max(overdue_list)

    def relaOtherOverdueDays(self):
        """relaOtherOverdueDays 其他联系人-历史借款最大逾期天数  --产品：即刻贷、贷款王、立即贷 (立即贷其它联系人默认是朋友非同事)"""
        if self.__get_contact_old_userId("friendContact") == 'Error' or self.__get_contact_new_userId(
                "friendContact") == 'Error':
            return self.SET_DEFAULT_VALUE_INT_9999999
        overdue_list = []
        if self.__get_contact_old_userId("friendContact"):
            old_list = self.__old_overdue_days(self.__get_contact_old_userId("friendContact"), -36)
            for old in old_list:
                overdue_list.append((return_strfYmd_date(old[2]) - return_strfYmd_date(old[1])).days)
        if self.__get_contact_new_userId("friendContact"):
            new_list = self.__hexin_bill(self.__get_contact_new_userId("friendContact"), self.ljd_product_id, -36)+\
                       self.__hexin_bill(self.__get_contact_new_userId("friendContact"), self.sxj_product_id, -36)+\
                       self.__hexin_bill(self.__get_contact_new_userId("friendContact"), self.ql_product_id, -36)
            for new in new_list:
                overdue_list.append((return_strfYmd_date(new[2]) - return_strfYmd_date(new[1])).days)
        if not overdue_list:
            return 0
        if max(overdue_list) < 0:
            return 0
        return max(overdue_list)

    def kinshipContactFirstOverdueDays(self):
        """kinshipContactFirstOverdueDays 直系亲属联系人-首次借款逾期天数  --产品：即刻贷、贷款王、立即贷、随心借、卡贷王 """
        if self.__get_contact_old_userId("relativeContact") == 'Error' or self.__get_contact_new_userId(
                "relativeContact") == 'Error':
            return self.SET_DEFAULT_VALUE_INT_9999999
        old_list = []
        ljd_list = []
        sxj_list =[]
        ql_list = []
        if self.__get_contact_old_userId("relativeContact"):
            old_list = self.__old_overdue_days(self.__get_contact_old_userId("relativeContact"), -36)
        if self.__get_contact_new_userId("relativeContact"):
            ljd_list = self.__hexin_bill(self.__get_contact_new_userId("relativeContact"), self.ljd_product_id, -36)
            sxj_list = self.__hexin_bill(self.__get_contact_new_userId("relativeContact"), self.sxj_product_id, -36)
            ql_list = self.__hexin_bill(self.__get_contact_new_userId("relativeContact"), self.ql_product_id, -36)
        overdue_list = old_list + ljd_list+sxj_list+ql_list
        overdue_list.sort()
        if not overdue_list:
            return 0
        overdue_days = (return_strfYmd_date(overdue_list[0][2]) - return_strfYmd_date(overdue_list[0][1])).days
        if overdue_days < 0:
            return 0
        return overdue_days

    def otherContactsFirstOverdueDays(self):
        """otherContactsFirstOverdueDays 其他联系人-首次借款逾期天数  --产品：即刻贷、贷款王、立即贷、随心借、卡贷王  (立即贷其它联系人默认是朋友非同事)"""
        if self.__get_contact_old_userId("friendContact") == 'Error' or self.__get_contact_new_userId(
                "friendContact") == 'Error':
            return self.SET_DEFAULT_VALUE_INT_9999999
        old_list = []
        new_list = []
        if self.__get_contact_old_userId("friendContact"):
            old_list = self.__old_overdue_days(self.__get_contact_old_userId("friendContact"), -36)
        if self.__get_contact_new_userId("friendContact"):
            new_list = self.__hexin_bill(self.__get_contact_new_userId("friendContact"), self.ljd_product_id, -36) + \
                       self.__hexin_bill(self.__get_contact_new_userId("friendContact"), self.sxj_product_id, -36) + \
                       self.__hexin_bill(self.__get_contact_new_userId("friendContact"), self.kdw_product_id, -36)
        overdue_list = old_list + new_list
        overdue_list.sort()
        if not overdue_list:
            return 0
        overdue_days = (return_strfYmd_date(overdue_list[0][2]) - return_strfYmd_date(overdue_list[0][1])).days
        if overdue_days < 0:
            return 0
        return overdue_days

    def relaFamilyFirstOverdueDays(self):
        """relaFamilyFirstOverdueDays  直系亲属联系人-首次借款逾期天数  --产品：即刻贷、贷款王、立即贷"""
        if self.__get_contact_old_userId("relativeContact") == 'Error' or self.__get_contact_new_userId(
                "relativeContact") == 'Error':
            return self.SET_DEFAULT_VALUE_INT_9999999
        old_list = []
        ljd_list = []
        sxj_list =[]
        ql_list = []
        if self.__get_contact_old_userId("relativeContact"):
            old_list = self.__old_overdue_days(self.__get_contact_old_userId("relativeContact"), -36)
        if self.__get_contact_new_userId("relativeContact"):
            ljd_list = self.__hexin_bill(self.__get_contact_new_userId("relativeContact"), self.ljd_product_id, -36)
            sxj_list = self.__hexin_bill(self.__get_contact_new_userId("relativeContact"), self.sxj_product_id, -36)
            ql_list = self.__hexin_bill(self.__get_contact_new_userId("relativeContact"), self.ql_product_id, -36)
        overdue_list = old_list + ljd_list+sxj_list+ql_list
        overdue_list.sort()
        if not overdue_list:
            return 0
        overdue_days = (return_strfYmd_date(overdue_list[0][2]) - return_strfYmd_date(overdue_list[0][1])).days
        if overdue_days < 0:
            return 0
        return overdue_days

    def relaOtherFirstOverdueDays(self):
        """relaOtherFirstOverdueDays  其他联系人-首次借款逾期天数   --产品：即刻贷、贷款王、立即贷"""
        if self.__get_contact_old_userId("friendContact") == 'Error' or self.__get_contact_new_userId("friendContact") == 'Error':
            return self.SET_DEFAULT_VALUE_INT_9999999
        old_list = []
        ljd_list = []
        sxj_list =[]
        ql_list = []
        if self.__get_contact_old_userId("friendContact"):
            old_list = self.__old_overdue_days(self.__get_contact_old_userId("friendContact"), -36)
        if self.__get_contact_new_userId("friendContact"):
            ljd_list = self.__hexin_bill(self.__get_contact_new_userId("friendContact"), self.ljd_product_id, -36)
            sxj_list = self.__hexin_bill(self.__get_contact_new_userId("friendContact"), self.sxj_product_id, -36)
            ql_list = self.__hexin_bill(self.__get_contact_new_userId("friendContact"), self.ql_product_id, -36)
        overdue_list = old_list + ljd_list + sxj_list + ql_list
        overdue_list.sort()
        if not overdue_list:
            return 0
        overdue_days = (return_strfYmd_date(overdue_list[0][2]) - return_strfYmd_date(overdue_list[0][1])).days
        if overdue_days < 0:
            return 0
        return overdue_days

    def last1BorrowLateDaysLjd(self):
        """last1BorrowLateDaysLjd 立即贷倒数第一次成交借款的逾期天数　--产品：立即贷"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        ljd_days_list_12.sort()
        if not ljd_days_list_12:
            return self.SET_DEFAULT_VALUE_INT_9999995
        last1Overday = (
                    return_strfYmd_date(ljd_days_list_12[-1][2]) - return_strfYmd_date(ljd_days_list_12[-1][1])).days
        return last1Overday

    def last1BorrowLateDaysSxj(self):
        """last1BorrowLateDaysSxj 随心借倒数第一次成交借款的逾期天数   --产品：随心借"""
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        sxj_days_list_12.sort()
        if not sxj_days_list_12:
            return self.SET_DEFAULT_VALUE_INT_9999995
        last1Overday = (
                    return_strfYmd_date(sxj_days_list_12[-1][2]) - return_strfYmd_date(sxj_days_list_12[-1][1])).days
        return last1Overday

    def last1BorrowLateDaysLjdSxj(self):
        """last1BorrowLateDaysLjdSx 倒数第一次成交借款的逾期天数  --产品：随心借、立即贷"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        new_list = ljd_days_list_12 + sxj_days_list_12
        new_list.sort()
        if not new_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        last1Overday = (return_strfYmd_date(new_list[-1][2]) - return_strfYmd_date(new_list[-1][1])).days
        return last1Overday

    def allMaxOverdueDaysPamth(self):
        """allMaxOverdueDaysPamth 历史最大逾期天数  --产品：贷款王、即刻贷、立即贷、随心借、车贷王、商代王"""
        maxDays = []
        old_days_list_36 = self.__old_overdue_days(self.info.old_user_id, -36)
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        all_days_list = old_days_list_36 + ljd_days_list_12 + sxj_days_list_12
        for overdue in all_days_list:
            maxDays.append((return_strfYmd_date(overdue[2]) - return_strfYmd_date(overdue[1])).days)
        SDWMaxDay = 0
        if Setting.SETTING['sdw']['isCheck'] == 1:
            url = Setting.SETTING['sdw']['url']
            data = {'idcard': self.info.cert_id}
            r = requests.post(url, data=data)
            responseJson = r.json()
            if responseJson.get('tips') == 'success':
                SDWMaxDay = responseJson.get("data").get("historyMaxOverdueDays")
        CDWMaxDay = 0
        if Setting.SETTING['cdw']['isCheck'] == 1:
            CDWList = []
            sql = "SELECT DATEDIFF(DSKRQ,DZZRQ) overdueDays FROM lb_apply_lessee_info a INNER JOIN lb_repay_plan b ON a.asqbh = b.asqbh WHERE azjhm ='%s' AND b.azt = 3 AND DSKRQ > DZZRQ ORDER BY overdueDays DESC LIMIT 1" % self.info.cert_id
            CDW_MaxDay = self.mysql.queryone_by_customer_id('zu_che', sql)
            if CDW_MaxDay:
                CDWList.append(CDW_MaxDay['overdueDays'])
            sql = " SELECT DATEDIFF(NOW(),DZZRQ) overdueDays FROM lb_apply_lessee_info a INNER JOIN lb_repay_plan b ON a.asqbh = b.asqbh WHERE azjhm ='%s' AND b.azt = 2 ORDER BY overdueDays DESC LIMIT 1" % self.info.cert_id
            CDWMaxDay_Current = self.mysql.queryone_by_customer_id('zu_che', sql)
            if CDWMaxDay_Current:
                CDWList.append(CDWMaxDay_Current['overdueDays'])
            if CDWList:
                CDWMaxDay = max(CDWList)
        if not maxDays:
            return max(CDWMaxDay, SDWMaxDay)
        return max(max(maxDays), CDWMaxDay, SDWMaxDay)

    def maxOverdueDaysDkw(self):
        """maxOverdueDaysDkw 贷款王最大预期天数  --产品：贷款王"""
        sql = "SELECT max(late_days) as cnt FROM all_fin_rownumber WHERE user_id = '%s' AND bank_type != 10002" % self.info.old_user_id
        result = self.mysql.queryall_by_customer_id('skynet_fact_material', sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get('cnt'):
            return 0
        else:
            return result[0].get('cnt')

    def maxOverdueDaysJkd(self):
        """maxOverdueDaysJkd 即刻贷最大预期天数  --产品：即刻贷"""
        sql = "SELECT max(late_days) as cnt FROM all_fin_rownumber WHERE user_id = '%s' AND bank_type = 10002" % self.info.old_user_id
        result = self.mysql.queryall_by_customer_id('skynet_fact_material', sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get('cnt'):
            return 0
        else:
            return result[0].get('cnt')

    def maxOverdueDaysLjd(self):
        """maxOverdueDaysLjd  立即贷最大预期天数--产品：立即贷"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        max_list = []
        for ljd in ljd_days_list_12:
            max_list.append((return_strfYmd_date(ljd[2]) - return_strfYmd_date(ljd[1])).days)
        if not max_list:
            return 0
        return max(max_list)

    def maxOverdueDaysSxj(self):
        """maxOverdueDaysSxj  随心借最大逾期天数  --产品：随心借"""
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        max_list = []
        for sxj in sxj_days_list_12:
            max_list.append((return_strfYmd_date(sxj[2]) - return_strfYmd_date(sxj[1])).days)
        if not max_list:
            return 0
        return max(max_list)

    def all_max_overdue_days(self):
        """all_max_overdue_days 历史最大逾期天数  --产品：贷款王、即刻贷、立即贷、车贷王、商代王"""
        maxDays = []
        old_days_list_36 = self.__old_overdue_days(self.info.old_user_id, -36)
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        all_days_list = old_days_list_36 + ljd_days_list_12
        for overdue in all_days_list:
            maxDays.append((return_strfYmd_date(overdue[2]) - return_strfYmd_date(overdue[1])).days)
        SDWMaxDay = 0
        if Setting.SETTING['sdw']['isCheck'] == 1:
            url = Setting.SETTING['sdw']['url']
            data = {'idcard': self.info.cert_id}
            r = requests.post(url, data=data)
            responseJson = r.json()
            if responseJson.get('tips') == 'success':
                SDWMaxDay = responseJson.get("data").get("historyMaxOverdueDays")
        CDWMaxDay = 0
        if Setting.SETTING['cdw']['isCheck'] == 1:
            CDWList = []
            sql = "SELECT DATEDIFF(DSKRQ,DZZRQ) overdueDays FROM lb_apply_lessee_info a INNER JOIN lb_repay_plan b ON a.asqbh = b.asqbh WHERE azjhm ='%s' AND b.azt = 3 AND DSKRQ > DZZRQ ORDER BY overdueDays DESC LIMIT 1" % self.info.cert_id
            CDW_MaxDay = self.mysql.queryone_by_customer_id('zu_che', sql)
            if CDW_MaxDay:
                CDWList.append(CDW_MaxDay['overdueDays'])
            sql = " SELECT DATEDIFF(NOW(),DZZRQ) overdueDays FROM lb_apply_lessee_info a INNER JOIN lb_repay_plan b ON a.asqbh = b.asqbh WHERE azjhm ='%s' AND b.azt = 2 ORDER BY overdueDays DESC LIMIT 1" % self.info.cert_id
            CDWMaxDay_Current = self.mysql.queryone_by_customer_id('zu_che', sql)
            if CDWMaxDay_Current:
                CDWList.append(CDWMaxDay_Current['overdueDays'])
            if CDWList:
                CDWMaxDay = max(CDWList)
        if not maxDays:
            return max(CDWMaxDay, SDWMaxDay)
        return max(max(maxDays), CDWMaxDay, SDWMaxDay)

    def ljdRepayCnt(self):
        """ljdRepayCnt 立即贷已还清借款次数  --产品：立即贷"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        clean_list = []
        for ljd in ljd_days_list_12:
            if ljd[4]==2:
                clean_list.append(ljd)
        return len(clean_list)

    def sxjRepayCnt(self):
        """sxjRepayCnt 随心借已还清借款次数  --产品：随心借"""
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        clean_list = []
        for sxj in sxj_days_list_12:
            if sxj[4] ==2:
                clean_list.append(sxj)
        return len(clean_list)

    def dkwRepayCnt(self):
        """dkwRepayCnt 贷款王已还清借款次数  --产品：贷款王"""
        if not self.info.old_user_id:
            return self.SET_DEFAULT_VALUE_INT_0
        sql = "select * from all_fin_rownumber where user_id =%s and  bank_type!=10002 and  real_repayment_date  is not null and real_repayment_principal >= amount" % (
        self.info.old_user_id)
        borrowList = self.mysql.queryall_by_customer_id("skynet_fact_material", sql)
        if not borrowList:
            return self.SET_DEFAULT_VALUE_INT_0
        return len(borrowList)

    def jkdRepayCnt(self):
        """jkdRepayCnt 即刻贷已还清借款次数  --产品：即刻贷"""
        if not self.info.old_user_id:
            return self.SET_DEFAULT_VALUE_INT_0
        sql = "select * from all_fin_rownumber where user_id =%s and  bank_type=10002 and real_repayment_date  is not null and real_repayment_principal >= amount" % (
        self.info.old_user_id)
        borrowList = self.mysql.queryall_by_customer_id("skynet_fact_material", sql)
        if not borrowList:
            return self.SET_DEFAULT_VALUE_INT_0
        return len(borrowList)

    def __deviceFirstOverdueDays_core(self, imei, idfa):
        if idfa:
            # 查询旧的相同设备id的old_user_id
            sql = "SELECT * from s_user_device where ifa='%s' and create_at<='%s'" % (idfa, self.info.event_time_add8h)
            result = self.mysql.queryall_by_table('xinyongjin', sql)
            old_user_ids = list(set([str(data['user_id']) for data in result]))
            old_user_ids_str = "','".join(old_user_ids)
            # 查询旧的相同设备id的new_user_id
            result = self.mongo.queryall_by_table('lake', "s_user_mobile_device_info_{0}", {"idfa": idfa})
            new_user_ids = list(set([str(data['user_id']) for data in result]))
            new_user_ids_str = "','".join(new_user_ids)
            # print new_user_ids
        elif imei:
            # 查询旧的相同设备id的old_user_id
            sql = "SELECT * from s_user_device where imei='%s' and create_at<='%s'" % (imei, self.info.event_time_add8h)
            result = self.mysql.queryall_by_table('xinyongjin', sql)
            old_user_ids = list(set([str(data['user_id']) for data in result]))
            old_user_ids_str = "','".join(old_user_ids)
            # 查询旧的相同设备id的new_user_id
            result = self.mongo.queryall_by_table('lake', "s_user_mobile_device_info_{0}", {"imei": imei})
            new_user_ids = list(set([str(data['user_id']) for data in result]))
            new_user_ids_str = "','".join(new_user_ids)
        else:
            return self.SET_DEFAULT_VALUE_INT_9999999
        # old 转 new
        sql = "SELECT * from user_transfer_from_{0} where old_user_id in ('%s') and group_id=1" % (old_user_ids_str)
        result = self.mysql.queryall_by_table_new_only('customer_center', sql)
        new_user_ids2 = list(set([str(data['current_user_id']) for data in result]))
        # new 转 old
        sql = "SELECT * from user_transfer_from_{0} where current_user_id in ('%s') and group_id=1" % (
            new_user_ids_str)
        result = self.mysql.queryall_by_table_new_only('customer_center', sql)
        old_user_ids2 = list(set([str(data['old_user_id']) for data in result]))
        old_user_id_all = old_user_ids + old_user_ids2
        old_user_id_all_str = "','".join(old_user_id_all)
        new_user_id_all = new_user_ids + new_user_ids2
        new_user_id_all_str = "','".join(new_user_id_all)
        sql = "SELECT * from s_user_product_audit_status where audit_status in (1,190) and product_mst_id not in (2,3,4) and user_id in ('%s') and create_at<='%s'" % (
            old_user_id_all_str, self.info.event_time_add8h)
        result = self.mysql.queryall_by_table_new_only('xinyongjin', sql)
        earliest_audit_old = [[data['approve_time'], data['user_id'], 'old'] for data in result if data['approve_time']]
        # userid查customerid
        sql = "SELECT * FROM customer WHERE user_id in ('%s')" % (new_user_id_all_str)
        result = self.mysql.queryall_by_table_new_only('customer_center', sql)
        customer_ids = list(set([str(data['id']) for data in result]))
        customer_ids_str = "','".join(customer_ids)
        # print "customer_ids_str:{0}".format(customer_ids_str)
        sql = "SELECT * from a_customer_apply_status_{0} where apply_status in (190) and customer_group_id =1 and customer_id in ('%s') and  create_at<='%s'" % (
            customer_ids_str, self.info.event_time_add8h)
        result = self.mysql.queryall_by_table_new_only('apply_center', sql)
        earliest_audit = [[data['approve_time'], data['customer_id']] for data in result]
        earliest_audit.sort()
        if not earliest_audit:
            earliest_audit_new = []
        else:
            for i in earliest_audit:
                sql = "SELECT user_id FROM customer WHERE id ='%s'" % i[1]
                result = self.mysql.queryone_by_customer_id('customer_center', sql)
                earliest_audit_new = [[i[0], result.get('user_id'), 'new']]
        earliest_audit = earliest_audit_old + earliest_audit_new
        earliest_audit.sort()
        if len(earliest_audit) > 1000:
            return self.SET_DEFAULT_VALUE_INT_9999997
        # 找出最早的一条记录
        if not earliest_audit:
            return 0
        earliest = earliest_audit[0]
        if earliest[2] == 'old':
            result = self.__old_overdue_days(earliest[1], -36)
            if not result:
                return 0
            overdue_day = (return_strfYmd_date(result[0][2]) - return_strfYmd_date(result[0][1])).days
            if overdue_day <= 0:
                return 0
            else:
                return overdue_day
        elif earliest[2] == 'new':
            result = self.__hexin_bill(earliest[1], self.ljd_product_id, -12) + \
                     self.__hexin_bill(earliest[1], self.sxj_product_id, -12) + \
                     self.__hexin_bill(earliest[1], self.kdw_product_id, -12)
            result.sort()
            if not result:
                return 0
            overdue_day = (return_strfYmd_date(result[0][2]) - return_strfYmd_date(result[0][1])).days
            if overdue_day <= 0:
                return 0
            else:
                return overdue_day
        else:
            return self.SET_DEFAULT_VALUE_INT_9999999

    def deviceFirstOverdueDays(self):
        """deviceFirstOverdueDays 同一设备(imei或ifa)对应首个开户用户-首次借款的逾期天数"""
        data = self.mongo.query_by_user_id('lake', "s_user_mobile_device_info_{0}".format(self.info.user_id % 4),
                                           {"user_id": self.info.user_id})
        if len(data) == 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        idfa = data[0].get('idfa')
        imei = data[0].get('imei')
        if idfa and idfa != '':
            return self.__deviceFirstOverdueDays_core(None, idfa)
        elif imei and imei != '':
            return self.__deviceFirstOverdueDays_core(imei, None)
        else:
            return self.SET_DEFAULT_VALUE_INT_9999999

    def ruleContactMax5M2(self):
        """ruleContactMax5M2 通话记录中通话次数最多的5个手机号码，其中有任意一个是首借M2以上  --产品：即刻贷、贷款王、立即贷、隨心借、卡贷王"""
        phone5Max = self.mongo.query_phone_max5_beforeEvenTime_inXdays(db='lake',
                                                                       collection="s_user_mobile_contact_action_{0}".format(
                                                                           int(self.user_id) % 4),
                                                                       find={"user_id": int(self.user_id)},
                                                                       serial_no=self.serial_no, days=30)
        if phone5Max == 'No DATA':
            return 0
        phone_result = []
        for phone in phone5Max:
            sql = "select id from s_user where mobilephone ='%s'" % phone
            result = self.mysql.queryone_by_customer_id('xinyongjin', sql)
            if result:
                phone_result.append(result)
        for i in phone_result:
            sql = "select * from all_fin_rownumber where user_id=%s and rank=1 and late_days>30" % i["id"]
            result = self.mysql.queryall_by_customer_id('skynet_fact_material', sql)
            if len(result) > 0:
                return 1
        new_result = []
        for phone in phone5Max:
            sql = "select id from `user` where mobilephone = '%s' and delete_flag=0 " % factor_encrypt_identity(phone)
            resultId = self.mysql.queryone_by_customer_id('customer_center', sql)
            if resultId:
                new_result.append(resultId)
        if not new_result:
            return 0
        result_max5 = []

        if new_result:
            userIdStr = [data['id'] for data in new_result]
            for userID in userIdStr:
                result = self.__hexin_bill(userID, self.ljd_product_id, -12) + \
                         self.__hexin_bill(userID, self.sxj_product_id, -12) + \
                         self.__hexin_bill(userID, self.kdw_product_id, -12)
                result.sort()
                if result:
                    result_max5.append(result[0])
        for day in result_max5:
            overdue_day = (return_strfYmd_date(day[2]) - return_strfYmd_date(day[1])).days
            if overdue_day > 30:
                return 1
        return 0

    def rule_contact_max5_m2(self):
        """rule_contact_max5_m2 通话记录中通话次数最多的5个手机号码，其中有任意一个是首借M2以上  --产品：即刻贷、贷款王"""
        phone5Max = self.mongo.query_phone_max5_beforeEvenTime_inXdays(db='lake',
                                                                       collection="s_user_mobile_contact_action_{0}".format(
                                                                           int(self.user_id) % 4),
                                                                       find={"user_id": int(self.user_id)},
                                                                       serial_no=self.serial_no, days=30,
                                                                       validTime=self.info.event_time_add8h-datetime.timedelta(days=180))
        if phone5Max == 'No DATA':
            return 0
        phone_result = []
        for phone in phone5Max:
            sql = "select id from s_user where mobilephone ='%s'" % phone
            result = self.mysql.queryone_by_customer_id('xinyongjin', sql)
            if result:
                phone_result.append(result)
        # if not phone_result:
        #     return 0
        for i in phone_result:
            sql = "select * from all_fin_rownumber where user_id=%s and rank=1 and late_days>30" % i["id"]
            result = self.mysql.queryall_by_customer_id('skynet_fact_material', sql)
            if len(result) > 0:
                return 1
        new_result = []
        for phone in phone5Max:
            sql = "select id from `user` where mobilephone = '%s' and delete_flag=0 ;" % factor_encrypt_identity(phone)
            resultId = self.mysql.queryone_by_customer_id('customer_center', sql)
            if resultId:
                new_result.append(resultId)
        if not new_result:
            return 0
        result_max5 = []
        if new_result:
            userIdStr = [data['id'] for data in new_result]
            for userID in userIdStr:
                result = self.__hexin_bill(userID, self.ljd_product_id, -12)+\
                         self.__hexin_bill(userID, self.sxj_product_id, -12)+\
                         self.__hexin_bill(userID, self.ql_product_id, -12)
                result.sort()
                if result:
                    result_max5.append(result[0])
        for day in result_max5:
            overdue_day = (return_strfYmd_date(day[2]) - return_strfYmd_date(day[1])).days
            if overdue_day > 30:
                return 1
        return 0

    def avgCollectCntOfDueCntLjd(self):
        """ avgCollectCntOfDueCntLjd 立即贷平均催收记录数"""
        #注意bill表数据和order数据要准备
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -36)
        if not ljd_days_list:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        ljd_days_list_12_remove_current=[bill for bill in ljd_days_list if bill[2]!=self.info.event_time_add8h]
        if not ljd_days_list_12_remove_current:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        ljd_overdueDays=[bill for bill in ljd_days_list_12_remove_current if (return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days>0]
        callList=self.__getCaseIdFromBillAndOrder(self.info.user_id)
        caseIds=list(set([i.get('caseId') for i in callList]))
        collection=[]
        for caseId in caseIds:
            collection.extend(self.__getCallFromCaseId(caseId))
        return round(float(len(collection))/len(ljd_overdueDays),4)

    def avgCalltimeGt0CntOfDueCntLjd(self):
        """ avgCalltimeGt0CntOfDueCntLjd 立即贷平均催收接通次数"""
        # 注意bill表数据和order数据要准备
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -36)
        if not ljd_days_list:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        ljd_days_list_12_remove_current=[bill for bill in ljd_days_list if bill[2]!=self.info.event_time_add8h]
        if not ljd_days_list_12_remove_current:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        ljd_overdueDays=[bill for bill in ljd_days_list_12_remove_current if (return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days>0]
        callList=self.__getCaseIdFromBillAndOrder(self.info.user_id)
        caseIds=list(set([i.get('caseId') for i in callList]))
        collection=[]
        for caseId in caseIds:
            collection.extend(self.__getCallFromCaseId(caseId))
        collection_timeGt0=[call for call in collection if call.get("call_time")>0]
        return round(float(len(collection_timeGt0))/len(ljd_overdueDays),4)

    def avgDueDaysOfDueCntLjd(self):
        """avgDueDaysOfDueCntLjd 立即贷平均逾期天数"""
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -36)
        if not ljd_days_list:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        ljd_days_list_12_remove_current=[bill for bill in ljd_days_list if bill[2]!=self.info.event_time_add8h]
        if not ljd_days_list_12_remove_current:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        ljd_overdueDays=[(return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days for bill in ljd_days_list_12_remove_current if (return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days>0]
        if not ljd_overdueDays:
            return self.SET_DEFAULT_VALUE_FLOAT_9999995
        return round(float(sum(ljd_overdueDays))/len(ljd_overdueDays),4)

    def rtoGoodRemarkCntOfDueCntLjd(self):
        """rtoGoodRemarkCntOfDueCntLjd 立即贷第一天入催且好评的逾期数占比"""
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -36)
        if not ljd_days_list:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        ljd_days_list.sort()
        ljd_days_list_12_remove_current=[bill for bill in ljd_days_list if bill[2]!=self.info.event_time_add8h]
        if not ljd_days_list_12_remove_current:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        ljd_overdueDays=[bill for bill in ljd_days_list_12_remove_current if (return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days>0]
        if not ljd_overdueDays:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        callList=self.__getCaseIdFromBillAndOrder(self.info.user_id)
        callList_remove_current=[bill for bill in callList if bill.get("orderId")!=ljd_days_list[-1][5]]
        caseIds=list(set([i.get('caseId') for i in callList_remove_current]))
        ljd_overdueDays_first_collection=[return_strfYmd_date(i.get('createTime')) for i in callList_remove_current]
        if not ljd_overdueDays_first_collection:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        collection=[]
        for caseId in caseIds:
            collection.extend(self.__getCallFromCaseId(caseId))
        count=0
        for col in ljd_overdueDays_first_collection:
            call_first=[call for call in collection if call.get("result_desc") in [1,3,4,5,21,22,27] and return_strfYmd_date(call.get("create_at"))==col]
            if call_first:
                count+=1
        return round(float(count)/len(ljd_overdueDays_first_collection),4)

    def currDueBillId(self):
        """currDueBillId 当前逾期账单ID"""
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -36)
        if not ljd_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        ljd_days_list.sort()
        return ljd_days_list[-1][6]

    def lastRaiseLimitTime(self):
        """lastRaiseLimitTime 当前产品(立即贷，畅借款)上次提额时间"""
        sql_vip="select * from skynet_credit_line where user_id='{0}' and product_id='{1}' and is_delete=0".format(self.info.user_id,self.ljd_product_id)
        result_vip=self.mysql.queryall_by_table_new_only('skynet_credit_line',sql_vip)
        sql_ql="select * from skynet_credit_line where user_id='{0}' and product_id='{1}' and is_delete=0".format(self.info.user_id,self.ql_product_id)
        result_ql=self.mysql.queryall_by_table_new_only('skynet_credit_line',sql_ql)
        if not result_vip and not result_ql:
            return self.SET_DEFAULT_VALUE_STRING_DATETIME
        if not result_vip and result_ql:
            line=result_ql[0]
            if not line.get("last_up_credit_line_date"):
                return line.get("create_at",self.SET_DEFAULT_VALUE_STRING_DATETIME)
            return line.get("last_up_credit_line_date")
        if not result_ql and result_vip:
            line=result_vip[0]
            if not line.get("last_up_credit_line_date"):
                return line.get("create_at",self.SET_DEFAULT_VALUE_STRING_DATETIME)
            return line.get("last_up_credit_line_date")
        line_vip=result_vip[0]
        line_ql=result_ql[0]
        if not line_vip.get("last_up_credit_line_date") and not line_ql.get("last_up_credit_line_date"):
            return max([line_vip.get("create_at"),line_ql.get("create_at")])
        if not line_vip.get("last_up_credit_line_date") and line_ql.get("last_up_credit_line_date"):
            return line_ql.get("last_up_credit_line_date")
        if not line_ql.get("last_up_credit_line_date") and line_vip.get("last_up_credit_line_date"):
            return line_vip.get("last_up_credit_line_date")
        return max([line_ql.get("last_up_credit_line_date"),line_vip.get("last_up_credit_line_date")])

    def __getCallFromCaseId(self,caseId):
        sql="select case_id,call_time,phone,status,`type`,result_desc,create_at from d_call_project_call_record where case_id='%s' " \
            "UNION ALL select case_id,call_time,phone,status,`type`,result_desc,create_at from d_call_project_call_record_his_1 where case_id='%s'" \
            "UNION ALL select case_id,call_time,phone,status,`type`,result_desc,create_at from d_call_project_call_record_his_2 where case_id='%s'" \
            "UNION ALL select case_id,call_time,phone,status,`type`,result_desc,create_at from d_call_project_call_record_his_3 where case_id='%s'" \
            "UNION ALL select case_id,call_time,phone,status,`type`,result_desc,create_at from d_call_project_call_record_his_4 where case_id='%s'" \
            "UNION ALL select case_id,call_time,phone,status,`type`,result_desc,create_at from d_call_project_call_record_his_5 where case_id='%s'" \
            "UNION ALL select case_id,call_time,phone,status,`type`,result_desc,create_at from d_call_project_call_record_his_6 where case_id='%s'" \
            "UNION ALL select case_id,call_time,phone,status,`type`,result_desc,create_at from d_call_project_call_record_his_7 where case_id='%s'" \
            "UNION ALL select case_id,call_time,phone,status,`type`,result_desc,create_at from d_call_project_call_record_his_8 where case_id='%s'" \
            "UNION ALL select case_id,call_time,phone,status,`type`,result_desc,create_at from d_call_project_call_record_his_9 where case_id='%s'" \
            "UNION ALL select case_id,call_time,phone,status,`type`,result_desc,create_at from d_call_project_call_record_his_10 where case_id='%s'"%(caseId,caseId,caseId,caseId,caseId,
                                                                                                                                                  caseId,caseId,caseId,caseId,caseId,caseId)
        result=self.mysql.queryall_by_customer_id(db='collection',sql=sql)
        return result

    def __getCaseIdFromBillAndOrder(self,user_id):
        sql="SELECT u.user_id userId,o.product_id productId,b.case_id caseId,b.loan_order_id orderId,b.create_at createTime FROM bill b " \
            "INNER JOIN d_case_user u ON b.case_id = u.case_id and u.user_id='%s' " \
            "INNER JOIN `order` o ON o.id = b.order_id and o.loan_order_id = b.loan_order_id " \
            "INNER JOIN s_case_product p ON p.id=o.product_id and p.product_system_product_id='10002' " \
            "UNION All " \
            "SELECT u.user_id userId,o.product_id productId,b.case_id caseId,b.loan_order_id orderId,b.create_at createTime FROM bill b " \
            "INNER JOIN d_case_user_his u ON b.case_id = u.case_id and u.user_id='%s' " \
            "INNER JOIN `order` o ON o.id = b.order_id and o.loan_order_id = b.loan_order_id " \
            "INNER JOIN s_case_product p ON p.id=o.product_id and p.product_system_product_id='10002' "%(user_id,user_id)
        result=self.mysql.queryall_by_customer_id(db="collection",sql=sql)
        return result

    def isReLoan(self):
        """isReLoan 当前产品首复借标签  产品：立即贷、随心借、卡贷王"""
        currentBill=self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if currentBill:
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def last2BorrowLateDaysLjd(self):
        """last2BorrowLateDaysLjd 立即贷倒数第二次成交借款的逾期天数  产品：立即贷、随心借、卡贷王"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        ljd_days_list_12.sort()
        if len(ljd_days_list_12)<=1:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return (return_strfYmd_date(ljd_days_list_12[-2][2]) - return_strfYmd_date(ljd_days_list_12[-2][1])).days

    def collectCntLjd(self):
        """collectCntLjd 立即贷近十二个月总电话催收记录数"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        if not ljd_days_list_12:
            return self.SET_DEFAULT_VALUE_INT_9999998
        ljd_overdueDays = [bill for bill in ljd_days_list_12 if(return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days > 0]
        if not ljd_overdueDays:
            return self.SET_DEFAULT_VALUE_INT_9999998
        callList=self.__getCaseIdFromBillAndOrder(self.info.user_id)
        if not callList:
            return self.SET_DEFAULT_VALUE_INT_0
        call_12=[]
        for call in callList:
            if call.get("createTime")>=self.info.event_time-relativedelta(months=12):
                call_12.append(call)
        if not call_12:
            return self.SET_DEFAULT_VALUE_INT_0
        caseIds=list(set([i.get('caseId') for i in call_12]))
        collection_12=[]
        for caseId in caseIds:
            collection_12.extend(self.__getCallFromCaseId(caseId))
        return len(collection_12)

    def dueCntLjd(self):
        """dueCntLjd 立即贷近十二个月总逾期账单数"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        if not ljd_days_list_12:
            return self.SET_DEFAULT_VALUE_INT_9999998
        overdueBillId=[]
        for bill in ljd_days_list_12:
            if (return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days>0:
                overdueBillId.append(bill[-1])
        if not overdueBillId:
            return self.SET_DEFAULT_VALUE_INT_0
        return len(overdueBillId)

    def avgUseMoneyDaysLjdC(self):
        """avgUseMoneyDaysLjdC 立即贷近十二个月平均用款天数"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        ljd_days_list_12_remove_current=[bill for bill in ljd_days_list_12 if bill[2]!=self.info.event_time_add8h]
        if not ljd_days_list_12_remove_current:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        userMoneyList=[(return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[0])).days for bill in ljd_days_list_12_remove_current]
        return round(float(sum(userMoneyList))/len(userMoneyList),4)

    def maxOverDueDaysLjdSxjC(self):
        """maxOverDueDaysLjdSxjC 立即贷、随心借近十二个月最大逾期天数（立即贷、随心借产品）"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        sxj_days_list_12 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -12)
        ljd_days_list_12_remove_current=[bill for bill in ljd_days_list_12 if bill[2] !=self.info.event_time_add8h]
        sxj_days_list_12_remove_current=[bill for bill in sxj_days_list_12 if bill[2] !=self.info.event_time_add8h]
        if not ljd_days_list_12_remove_current and not sxj_days_list_12_remove_current:
            return self.SET_DEFAULT_VALUE_INT_9999998
        overdueDaysList=[]
        overdueDaysList.extend([(return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days for bill in ljd_days_list_12_remove_current])
        overdueDaysList.extend([(return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days for bill in sxj_days_list_12_remove_current])
        if max(overdueDaysList)<=0:
            return self.SET_DEFAULT_VALUE_INT_0
        return max(overdueDaysList)

    def sumCollectTimeLjd(self):
        """sumCollectTimeLjd 立即贷近十二个月总电话催收时长"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        if not ljd_days_list_12:
            return self.SET_DEFAULT_VALUE_INT_9999998
        ljd_overdueDays = [bill for bill in ljd_days_list_12 if(return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days > 0]
        if not ljd_overdueDays:
            return self.SET_DEFAULT_VALUE_INT_9999998
        callList=self.__getCaseIdFromBillAndOrder(self.info.user_id)
        if not callList:
            return self.SET_DEFAULT_VALUE_INT_0
        call_12=[]
        for call in callList:
            if call.get("createTime")>=self.info.event_time-relativedelta(months=12):
                call_12.append(call)
        if not call_12:
            return self.SET_DEFAULT_VALUE_INT_0
        caseIds=list(set([i.get('caseId') for i in call_12]))
        collection_12=[]
        for caseId in caseIds:
            collection_12.extend(self.__getCallFromCaseId(caseId))
        if not collection_12:
            return self.SET_DEFAULT_VALUE_INT_0
        callTimeList=[call.get("call_time") for call in collection_12 if call.get("call_time")]
        return sum(callTimeList)

    def badRemarkCntLjd(self):
        """badRemarkCntLjd 立即贷近十二个月总的坏评价催收记录数"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        if not ljd_days_list_12:
            return self.SET_DEFAULT_VALUE_INT_9999998
        ljd_overdueDays = [bill for bill in ljd_days_list_12 if(return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days > 0]
        if not ljd_overdueDays:
            return self.SET_DEFAULT_VALUE_INT_9999998
        callList=self.__getCaseIdFromBillAndOrder(self.info.user_id)
        if not callList:
            return self.SET_DEFAULT_VALUE_INT_0
        call_12=[]
        for call in callList:
            if call.get("createTime")>=self.info.event_time-relativedelta(months=12):
                call_12.append(call)
        if not call_12:
            return self.SET_DEFAULT_VALUE_INT_0
        caseIds=list(set([i.get('caseId') for i in call_12]))
        collection_12=[]
        for caseId in caseIds:
            collection_12.extend(self.__getCallFromCaseId(caseId))
        if not collection_12:
            return self.SET_DEFAULT_VALUE_INT_0
        callBadDesc=[call for call in collection_12 if call.get("result_desc") and call.get("result_desc") in [7,8,10,12,13,14,17,23]]
        return len(callBadDesc)

    def sumDueDaysLjd(self):
        """sumDueDaysLjd 立即贷近十二个月总逾期天数"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        if not ljd_days_list_12:
            return self.SET_DEFAULT_VALUE_INT_9999998
        overdueDaysList=[(return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days for bill in ljd_days_list_12 if (return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[1])).days>0]
        return sum(overdueDaysList)

    def sumUseMoneyDaysLjd(self):
        """sumUseMoneyDaysLjd 立即贷近十二个月总用款天数"""
        ljd_days_list_12 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -12)
        if not ljd_days_list_12:
            return self.SET_DEFAULT_VALUE_INT_9999998
        overdueDaysList=[(return_strfYmd_date(bill[2]) - return_strfYmd_date(bill[0])).days for bill in ljd_days_list_12]
        return sum(overdueDaysList)

    def ljdFirstOverdueDay(self):
        """ljdFirstOverdueday 立即贷首次借款逾期天数"""
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if not ljd_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        overdueDay=(return_strfYmd_date(ljd_days_list[0][2])-return_strfYmd_date(ljd_days_list[0][1])).days
        return overdueDay if overdueDay>0 else self.SET_DEFAULT_VALUE_INT_0

    def vipDealCnt(self):
        """vipDealCnt 客户成交立即贷次数"""
        ljd_days_list=self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        return len(ljd_days_list)

    def cjkDealCnt(self):
        """cjkDealCnt 截止到申请时，畅借款成交次数"""
        lq_days_list=self.__hexin_bill(self.info.user_id, self.ql_product_id, -24)
        return len(lq_days_list)

    def firstProductName(self):
        """firstProductName 客户首次借款产品名称"""
        ljd_days_list=self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        ql_days_list=self.__hexin_bill(self.info.user_id, self.ql_product_id, -24)
        all_days_list=ql_days_list+ljd_days_list
        all_days_list.sort()
        if not all_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if all_days_list[0] in ljd_days_list:
            return "vip_loan"
        else:
            return "ql_loan"

    def creditNum(self):
        """creditNum 立即贷及之后产品开户数,包括立即贷、畅借款"""
        sql="select count(*) as cnt from skynet_user_apply_status where user_id='{0}' and product_id in ('109','10002') and delete_flag=0".format(self.info.user_id)
        result=self.mysql.queryone_by_customer_id(db='skynet_fact_material',sql=sql)
        return result.get('cnt')

    def sxjDealCnt(self):
        """sxjDealCnt 客户成交随心借次数"""
        sxj_days_list=self.__hexin_bill(self.info.user_id, self.sxj_product_id, -24)
        return len(sxj_days_list)

    def dkwDealCnt(self):
        """dkwDealCnt 客户成交贷款王次数"""
        if not self.info.old_user_id:
            return self.SET_DEFAULT_VALUE_INT_0
        sql = "SELECT COUNT(*) AS count FROM all_fin_rownumber WHERE user_id = %s AND bank_type <> 10002 "%self.info.old_user_id
        result = self.mysql.queryall_by_customer_id('skynet_fact_material',sql)
        return result[0].get('count')

    def jkdDealCnt(self):
        """jkdDealCnt 客户成交即刻贷次数"""
        if not self.info.old_user_id:
            return self.SET_DEFAULT_VALUE_INT_0
        sql = "SELECT COUNT(*) AS count FROM all_fin_rownumber WHERE user_id = %s AND bank_type = 10002" %self.info.old_user_id
        result = self.mysql.queryall_by_customer_id('skynet_fact_material', sql)
        return result[0].get('count')

    def histDealNumPamth(self):
        """histDealNumPamth 客户成交总笔数  产品：贷款王、即刻贷、立即贷、随心借"""
        old_days_list_36 = self.__old_overdue_days(self.info.old_user_id, -36)
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        sxj_days_list = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -24)

        return len(old_days_list_36)+len(ljd_days_list)+len(sxj_days_list)

    def dealProductTypePamth(self):
        """dealProductTypePamth 成交产品类型：即刻贷、贷款王、立即贷、随心借"""
        productGroup = []
        old_days_list_36 = self.__old_overdue_days(self.info.old_user_id, -36)
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        sxj_days_list = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -24)
        old_product_list_10002=[pro[-1] for pro in old_days_list_36 if pro[-1]==10002]
        old_product_list_other = [pro[-1] for pro in old_days_list_36 if pro[-1] !=10002]
        if old_product_list_other:
            productGroup.append('dkw')
        if old_product_list_10002:
            productGroup.append('jkd')
        if sxj_days_list:
            productGroup.append('sxj')
        if ljd_days_list:
            productGroup.append('ljd')
        if not productGroup:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return '|'.join(productGroup)

    def histDealNum(self):
        """histDealNum 历史成交笔数 int --产品：贷款王、即刻贷、立即贷"""
        old_days_list_36 = self.__old_overdue_days(self.info.old_user_id, -36)
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        return len(old_days_list_36)+len(ljd_days_list)

    def __get_user_id_from_customer_center(self,phone):
        sql="select * from `user` where mobilephone='%s' and delete_flag=0"%factor_encrypt_identity(phone)
        result=self.mysql.queryone_by_customer_id(db='customer_center',sql=sql)
        if not result:
            return
        return result.get('id')

    def __get_phone_list_from_lake(self):
        result_contact_action=self.mongo.query_by_user_id(  db='lake',
                                                            collection='s_user_mobile_contact_action_%d'%(int(self.info.user_id)%4),
                                                            find={'user_id':self.info.user_id})
        result_contact =self.mongo.query_by_user_id(db='lake',
                                                    collection='s_user_mobile_contact_%d'%(int(self.info.user_id)%4),
                                                    find={'user_id':self.info.user_id})
        result_sms_list=self.mongo.query_by_user_id(db='lake',
                                                    collection='s_user_mobile_sms_list_%d'%(int(self.info.user_id)%4),
                                                    find={'user_id':self.info.user_id})
        if not result_contact_action and not result_contact and not result_sms_list:
            return self.SET_DEFAULT_VALUE_INT_9999995

        contact_action_list_list=[]
        contact_list_clean =[]
        sms_list_list=[]

        if result_contact_action:
            contact_action_list=[action for action in result_contact_action[0].get("actions")]
            contact_action_list_clean_six_month=[action for action in contact_action_list if action.get("callTime")>(self.info.event_time_add8h-datetime.timedelta(days=179)) and action.get("callDuration")>5 and phoneClear(action.get("callNumber")) and phone_clean_new(phoneClear(action.get("callNumber")))]
            contact_action_list_list=[[action.get("callTime"),phone_clean_new(phoneClear(action.get("callNumber")))]for action in contact_action_list_clean_six_month]

        if result_contact:
            contact_list = [contact for contact in result_contact[0].get("contacts")]
            for contact in contact_list:
                if phone_clean_new(phoneClear(contact.get('phone1'))):
                    contact_list_clean.append(phone_clean_new(phoneClear(contact.get('phone1'))))
                if phone_clean_new(phoneClear(contact.get('phone2'))):
                    contact_list_clean.append(phone_clean_new(phoneClear(contact.get('phone2'))))
                if phone_clean_new(phoneClear(contact.get('phone3'))):
                    contact_list_clean.append(phone_clean_new(phoneClear(contact.get('phone3'))))

        if result_sms_list:
            sms_list =[sms for sms in result_sms_list[0].get("mobileSms") ]
            sms_list_clean_six_month=[sms for sms in sms_list if datetime.datetime.fromtimestamp(float(sms.get("date"))/1000)>(self.info.event_time_add8h-datetime.timedelta(days=179)) and sms.get("smsBody")!="" and phoneClear(sms.get("phoneNum")) and phone_clean_new(phoneClear(sms.get("phoneNum")))]
            sms_list_list=[[datetime.datetime.fromtimestamp(float(sms.get("date"))/1000),phone_clean_new(phoneClear(sms.get("phoneNum")))] for sms in sms_list_clean_six_month]

        contact_action_list_list.sort(reverse=True)
        sms_list_list.sort(reverse=True)
        contact_list_clean.sort(reverse=True)

        phone_bill_list=[action[1] for action in contact_action_list_list]+[sms[1] for sms in sms_list_list]+contact_list_clean
        return phone_bill_list

    def contactsDealCnt(self):
        """contactsDealCnt 通讯录、短信、通话记录综合去重有效手机号的成交人数   --大王贷"""
        phone_bill_list=self.__get_phone_list_from_lake()
        if phone_bill_list==self.SET_DEFAULT_VALUE_INT_9999995:
            return self.SET_DEFAULT_VALUE_INT_9999995
        if not phone_bill_list:
            return self.SET_DEFAULT_VALUE_INT_0
        phone_bill_list_remove=[]
        for phone in phone_bill_list:
            if phone not in phone_bill_list_remove:
                phone_bill_list_remove.append(phone)
        userId_list=[]
        for phone in phone_bill_list_remove:
            if self.__get_user_id_from_customer_center(phone):
                userId_list.append(self.__get_user_id_from_customer_center(phone))
        if len(userId_list)>20:
            return self.SET_DEFAULT_VALUE_INT_9999997
        count=0
        for userId in userId_list[:20]:
            ljd_days_list = self.__hexin_bill(userId, self.ljd_product_id, -12)
            sxj_days_list = self.__hexin_bill(userId, self.sxj_product_id, -12)
            if ljd_days_list or sxj_days_list:
                count+=1
        return count

    def contactsOverdue1Cnt(self):
        """contactsOverdue1Cnt 通讯录、短信、通话记录综合去重有效手机号的成交且逾期1+人数   --大王贷"""
        phone_bill_list=self.__get_phone_list_from_lake()
        if phone_bill_list==self.SET_DEFAULT_VALUE_INT_9999995:
            return self.SET_DEFAULT_VALUE_INT_9999995
        if not phone_bill_list:
            return self.SET_DEFAULT_VALUE_INT_0
        phone_bill_list_remove=[]
        for phone in phone_bill_list:
            if phone not in phone_bill_list_remove:
                phone_bill_list_remove.append(phone)
        userId_list=[]
        for phone in phone_bill_list_remove:
            if self.__get_user_id_from_customer_center(phone):
                userId_list.append(self.__get_user_id_from_customer_center(phone))
        if len(userId_list)>20:
            return self.SET_DEFAULT_VALUE_INT_9999997
        count=0
        for userId in userId_list[:20]:
            ljd_days_list = self.__hexin_bill(userId, self.ljd_product_id, -12)
            sxj_days_list = self.__hexin_bill(userId, self.sxj_product_id, -12)
            ljd_overdue_list=[(return_strfYmd_date(i[2]) - return_strfYmd_date(i[1])).days for i in ljd_days_list if (return_strfYmd_date(i[2]) - return_strfYmd_date(i[1])).days >=1]
            sxj_overdue_list=[(return_strfYmd_date(i[2]) - return_strfYmd_date(i[1])).days for i in sxj_days_list if (return_strfYmd_date(i[2]) - return_strfYmd_date(i[1])).days >=1]
            if ljd_overdue_list or sxj_overdue_list:
                count+=1
        return count

    def contactsOverdue6Cnt(self):
        """contactsOverdue6Cnt 通讯录、短信、通话记录综合去重有效手机号的成交且逾期6+人数   --大王贷"""
        phone_bill_list=self.__get_phone_list_from_lake()
        if phone_bill_list==self.SET_DEFAULT_VALUE_INT_9999995:
            return self.SET_DEFAULT_VALUE_INT_9999995
        if not phone_bill_list:
            return self.SET_DEFAULT_VALUE_INT_0
        phone_bill_list_remove=[]
        for phone in phone_bill_list:
            if phone not in phone_bill_list_remove:
                phone_bill_list_remove.append(phone)
        userId_list=[]
        for phone in phone_bill_list_remove:
            if self.__get_user_id_from_customer_center(phone):
                userId_list.append(self.__get_user_id_from_customer_center(phone))
        if len(userId_list)>20:
            return self.SET_DEFAULT_VALUE_INT_9999997
        count=0
        for userId in userId_list[:20]:
            ljd_days_list = self.__hexin_bill(userId, self.ljd_product_id, -12)
            sxj_days_list = self.__hexin_bill(userId, self.sxj_product_id, -12)
            ljd_overdue_list=[(return_strfYmd_date(i[2]) - return_strfYmd_date(i[1])).days for i in ljd_days_list if (return_strfYmd_date(i[2]) - return_strfYmd_date(i[1])).days >=6]
            sxj_overdue_list=[(return_strfYmd_date(i[2]) - return_strfYmd_date(i[1])).days for i in sxj_days_list if (return_strfYmd_date(i[2]) - return_strfYmd_date(i[1])).days >=6]
            if ljd_overdue_list or sxj_overdue_list:
                count+=1
        return count

    def __borrow_tz_record(self,factor):
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if len(ljd_days_list)<=3:
            results = self.mongo.query_by_user_id(db='galaxy', collection="tz_record",find={"serialNo": self.serial_no})
            if not results:
                return self.SET_DEFAULT_VALUE_INT_9999999
            if not results[0].get("tzResponse") or not results[0].get("tzResponse").get("mbInfos") or not results[0].get("tzResponse").get("mbInfos"):
                return self.SET_DEFAULT_VALUE_INT_9999996
            if not results[0].get("tzResponse").get("mbInfos")[0].get("creditInfo") or not results[0].get("tzResponse").get("mbInfos")[0].get("creditInfo").get("refInfos"):
                return self.SET_DEFAULT_VALUE_INT_9999996
            for info in results[0].get("tzResponse").get("mbInfos")[0].get("creditInfo").get("refInfos"):
                if info.get("sliceName")=="m1":
                    if factor=="tzmrAverageOverdueAmount1mV1":
                        if info.get('aveOverdueAmountLevel')=='null':
                            return self.SET_DEFAULT_VALUE_INT_9999996
                        return info.get('aveOverdueAmountLevel',self.SET_DEFAULT_VALUE_INT_9999996)
                    if factor=="tzmrAverageOverdueLength1mV1":
                        if info.get("aveOverdueDelayLevel")=='null':
                            return self.SET_DEFAULT_VALUE_INT_9999996
                        return info.get("aveOverdueDelayLevel",self.SET_DEFAULT_VALUE_INT_9999996)
                    if factor=="tzmrMaximumOverdueAmount1mV1":
                        if info.get("maxOverdueAmountLevel")=='null':
                            return self.SET_DEFAULT_VALUE_INT_9999996
                        return info.get("maxOverdueAmountLevel",self.SET_DEFAULT_VALUE_INT_9999996)
                    if factor=="tzmrMaxOverdueLength1mV1":
                        if info.get("maxOverdueDelayLevel")=='null':
                            return self.SET_DEFAULT_VALUE_INT_9999996
                        return info.get("maxOverdueDelayLevel",self.SET_DEFAULT_VALUE_INT_9999996)
            if not results[0].get("tzResponse").get("mbInfos")[0].get("creditInfo") or not results[0].get("tzResponse").get("mbInfos")[0].get("creditInfo").get("eveSums"):
                return self.SET_DEFAULT_VALUE_INT_9999996
            for info in results[0].get("tzResponse").get("mbInfos")[0].get("creditInfo").get("eveSums"):
                if info.get("sliceName")=="m1":
                    if factor=="tzmrRejectionEvents1mV1":
                        return info.get("applyRejectSum",self.SET_DEFAULT_VALUE_INT_9999996)
                    if factor=="tzmrRegistrationEvent1mV1":
                        return info.get("registerSum",self.SET_DEFAULT_VALUE_INT_9999996)
                    if factor=="tzmrNotificationEvent1mV1":
                        return info.get("verifSum",self.SET_DEFAULT_VALUE_INT_9999996)
            if not results[0].get("tzResponse").get("mbInfos")[0].get("creditInfo") or not results[0].get("tzResponse").get("mbInfos")[0].get("creditInfo").get("platformInfos"):
                return self.SET_DEFAULT_VALUE_INT_9999996
            for info in results[0].get("tzResponse").get("mbInfos")[0].get("creditInfo").get("platformInfos"):
                if info.get("sliceName") == "m1":
                    if factor=="tzmrRegistrationPlatform1mV1":
                        return info.get("registerCount",self.SET_DEFAULT_VALUE_INT_9999996)
                    if factor=="tzmrNotificationPlatform1mV1":
                        return info.get("verifCount",self.SET_DEFAULT_VALUE_INT_9999996)
        return self.SET_DEFAULT_VALUE_INT_9999995

    def tzmrAverageOverdueAmount1mV1(self):
        """tzmrAverageOverdueAmount1mV1 近一个月平均逾期金额V1"""
        return self.__borrow_tz_record(factor="tzmrAverageOverdueAmount1mV1")

    def tzmrAverageOverdueLength1mV1(self):
        """tzmrAverageOverdueLength1mV1 近一个月平均逾期时长V1"""
        return self.__borrow_tz_record(factor="tzmrAverageOverdueLength1mV1")

    def tzmrMaximumOverdueAmount1mV1(self):
        """tzmrMaximumOverdueAmount1mV1 近一个月最大逾期金额V1"""
        return self.__borrow_tz_record(factor="tzmrMaximumOverdueAmount1mV1")

    def tzmrMaxOverdueLength1mV1(self):
        """tzmrMaxOverdueLength1mV1 近一个月最大逾期时长V1"""
        return self.__borrow_tz_record(factor="tzmrMaxOverdueLength1mV1")

    def tzmrRejectionEvents1mV1(self):
        """tzmrRejectionEvents1mV1 近一个月拒绝事件V1"""
        return self.__borrow_tz_record(factor="tzmrRejectionEvents1mV1")

    def tzmrRegistrationEvent1mV1(self):
        """tzmrRegistrationEvent1mV1 近一个月注册事件V1"""
        return self.__borrow_tz_record(factor="tzmrRegistrationEvent1mV1")

    def tzmrNotificationEvent1mV1(self):
        """tzmrNotificationEvent1mV1 近一个月验证码通知事件V1"""
        return self.__borrow_tz_record(factor="tzmrNotificationEvent1mV1")

    def tzmrRegistrationPlatform1mV1(self):
        """tzmrRegistrationPlatform1mV1 近一个月注册平台V1"""
        return self.__borrow_tz_record(factor="tzmrRegistrationPlatform1mV1")

    def tzmrNotificationPlatform1mV1(self):
        """tzmrNotificationPlatform1mV1 近一个月验证码通知平台V1"""
        return self.__borrow_tz_record(factor="tzmrNotificationPlatform1mV1")

    def ljdMaxLimitBorrowCnt(self):
        """ljdMaxLimitBorrowCnt 立即贷3000及以上借款次数"""
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if not ljd_days_list:
            return self.SET_DEFAULT_VALUE_INT_0
        count=0
        for bill in ljd_days_list:
            if bill[3]>=300000:
                count+=1
        return count

    def __get_bjtz_score_record(self,factor):
        """冰鉴探知 查询当前产品的借款次数"""
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if len(ljd_days_list)<=3:
            results = self.mongo.query_by_user_id(db='galaxy', collection="bjtz_score_record",find={"userId": self.info.user_id})
            if not results or not results[0].get("bjTzResponse"):
                return self.SET_DEFAULT_VALUE_INT_9999999
            bjTzResponse=Des().unGzip(results[0].get("bjTzResponse"))
            if isinstance(bjTzResponse, str) or isinstance(bjTzResponse, unicode):
                bjTzResponse = json.loads(bjTzResponse)
            if factor=="bjAppUseTimes7Days":
                return bjTzResponse.get("result").get("apply_result").get("app_use_times_D7",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjAppUseTimes1M":
                return bjTzResponse.get("result").get("apply_result").get("app_use_times_M1",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjAppUseTimes3M":
                return bjTzResponse.get("result").get("apply_result").get("app_use_times_M3",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjMaxAppUseTimes1M":
                return bjTzResponse.get("result").get("apply_result").get("app_use_times_max_daily_M1",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjMaxAppUseTimes3M":
                return bjTzResponse.get("result").get("apply_result").get("app_use_times_max_daily_M3",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjMaxContinuityAppUseTimes1M":
                return bjTzResponse.get("result").get("apply_result").get("app_con_use_times_max_daily_M1",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjNightAppUseTimes7Days":
                return bjTzResponse.get("result").get("apply_result").get("app_use_times_night_D7",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjNightAppUseTimes1M":
                return bjTzResponse.get("result").get("apply_result").get("app_use_times_night_M1",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjNightAppUseTimes3M":
                return bjTzResponse.get("result").get("apply_result").get("app_use_times_night_M3",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjAppUseCnt7Days":
                return bjTzResponse.get("result").get("apply_result").get("app_use_num_D7",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjMassHighAppUseCnt7Days":
                return bjTzResponse.get("result").get("apply_result").get("app_mass_high_num_D7",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjAppUseCnt1M":
                return bjTzResponse.get("result").get("apply_result").get("app_use_num_M1",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjMassHighAppUseCnt7M":
                return bjTzResponse.get("result").get("apply_result").get("app_mass_high_num_M1",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjAppUseCnt3M":
                return bjTzResponse.get("result").get("apply_result").get("app_use_num_M3",self.SET_DEFAULT_VALUE_INT_9999996)
            if factor=="bjMassHighAppUseCnt3M":
                return bjTzResponse.get("result").get("apply_result").get("app_mass_high_num_M3",self.SET_DEFAULT_VALUE_INT_9999996)
        return self.SET_DEFAULT_VALUE_INT_9999995

    def bjAppUseTimes7Days(self):
        """bjAppUseTimes7Days 近7日APP使用次数"""
        return self.__get_bjtz_score_record(factor="bjAppUseTimes7Days")
    def bjAppUseTimes1M(self):
        """bjAppUseTimes1M 近1个月APP使用次数"""
        return self.__get_bjtz_score_record(factor="bjAppUseTimes1M")
    def bjAppUseTimes3M(self):
        """bjAppUseTimes3M 近3个月APP使用次数"""
        return self.__get_bjtz_score_record(factor="bjAppUseTimes3M")
    def bjMaxAppUseTimes1M(self):
        """bjMaxAppUseTimes1M 近1个月单日最大APP使用次数"""
        return self.__get_bjtz_score_record(factor="bjMaxAppUseTimes1M")
    def bjMaxAppUseTimes3M(self):
        """bjMaxAppUseTimes3M 近3个月单日最大APP使用次数"""
        return self.__get_bjtz_score_record(factor="bjMaxAppUseTimes3M")
    def bjMaxContinuityAppUseTimes1M(self):
        """bjMaxContinuityAppUseTimes1M 近1个月按天最大连续使用APP次数"""
        return self.__get_bjtz_score_record(factor="bjMaxContinuityAppUseTimes1M")
    def bjNightAppUseTimes7Days(self):
        """bjNightAppUseTimes7Days 近7天夜间APP使用次数"""
        return self.__get_bjtz_score_record(factor="bjNightAppUseTimes7Days")
    def bjNightAppUseTimes1M(self):
        """bjNightAppUseTimes1M 近1个月夜间APP使用次数"""
        return self.__get_bjtz_score_record(factor="bjNightAppUseTimes1M")
    def bjNightAppUseTimes3M(self):
        """bjNightAppUseTimes3M 近3个月夜间APP使用次数"""
        return self.__get_bjtz_score_record(factor="bjNightAppUseTimes3M")
    def bjAppUseCnt7Days(self):
        """bjAppUseCnt7Days 近7日APP使用个数"""
        return self.__get_bjtz_score_record(factor="bjAppUseCnt7Days")
    def bjMassHighAppUseCnt7Days(self):
        """bjMassHighAppUseCnt7Days 近7日大众高粘性APP使用个数"""
        return self.__get_bjtz_score_record(factor="bjMassHighAppUseCnt7Days")
    def bjAppUseCnt1M(self):
        """bjAppUseCnt1M 近1个月APP使用个数"""
        return self.__get_bjtz_score_record(factor="bjAppUseCnt1M")
    def bjMassHighAppUseCnt7M(self):
        """bjMassHighAppUseCnt7M 近1个月大众高粘性APP使用个数"""
        return self.__get_bjtz_score_record(factor="bjMassHighAppUseCnt7M")
    def bjAppUseCnt3M(self):
        """bjAppUseCnt3M 近3个月APP使用个数"""
        return self.__get_bjtz_score_record(factor="bjAppUseCnt3M")
    def bjMassHighAppUseCnt3M(self):
        """bjMassHighAppUseCnt3M 近3个月大众高粘性APP使用个数"""
        return self.__get_bjtz_score_record(factor="bjMassHighAppUseCnt3M")


    def __get_mxmz_report_record(self,factor):
        """魔蝎魔帐 查询当前产品的借款次数"""
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if len(ljd_days_list)<=3:
            results = self.mongo.query_by_user_id(db='galaxy', collection="mxmz_report_record",find={"userId": self.info.user_id})
            if not results or not results[0].get("reportResponse"):
                return self.SET_DEFAULT_VALUE_INT_9999999
            reportResponse=Des().unGzip(results[0].get("reportResponse"))
            if isinstance(reportResponse, str) or isinstance(reportResponse, unicode):
                reportResponse = json.loads(reportResponse)
            queried_analyze_List=reportResponse.get("data").get("auth_queried_detail").get("queried_analyze")
            for l in queried_analyze_List:
                if l.get("org_type")=="P2P":
                    if factor=="mzP2p90dCnt":
                        return l.get("loan_cnt_90d")
                    if factor=="mzP2p30dCnt":
                        return l.get("loan_cnt_30d")
                    if factor=="mzP2p15dCnt":
                        return l.get("loan_cnt_15d")
                if l.get("org_type")=="CONSUMSTAGE":
                    if factor=="mzConsumstage90dCnt":
                        return l.get("loan_cnt_90d")
                    if factor=="mzConsumstage30dCnt":
                        return l.get("loan_cnt_30d")
                    if factor=="mzConsumstage15dCnt":
                        return l.get("loan_cnt_15d")
                if l.get("org_type")=="CASH_LOAN":
                    if factor=="mzCashLoan90dCnt":
                        return l.get("loan_cnt_90d")
                    if factor=="mzCashLoan30dCnt":
                        return l.get("loan_cnt_30d")
                    if factor=="mzCashLoan15dCnt":
                        return l.get("loan_cnt_15d")
            if factor=="mzOrgCnt":
                return reportResponse.get("data").get("auth_queried_detail").get("register_info").get("org_count")
            return self.SET_DEFAULT_VALUE_INT_9999996
        return self.SET_DEFAULT_VALUE_INT_9999995
    def mzP2p90dCnt(self):
        """mzP2p90dCnt """
        return self.__get_mxmz_report_record(factor="mzP2p90dCnt")

    def mzConsumstage90dCnt(self):
        """mzConsumstage90dCnt """
        return self.__get_mxmz_report_record(factor="mzConsumstage90dCnt")

    def mzCashLoan90dCnt(self):
        """mzCashLoan90dCnt """
        return self.__get_mxmz_report_record(factor="mzCashLoan90dCnt")

    def mzP2p30dCnt(self):
        """mzP2p30dCnt """
        return self.__get_mxmz_report_record(factor="mzP2p30dCnt")

    def mzConsumstage30dCnt(self):
        """mzConsumstage30dCnt """
        return self.__get_mxmz_report_record(factor="mzConsumstage30dCnt")

    def mzCashLoan30dCnt(self):
        """mzCashLoan30dCnt """
        return self.__get_mxmz_report_record(factor="mzCashLoan30dCnt")

    def mzP2p15dCnt(self):
        """mzP2p15dCnt """
        return self.__get_mxmz_report_record(factor="mzP2p15dCnt")

    def mzConsumstage15dCnt(self):
        """mzConsumstage15dCnt """
        return self.__get_mxmz_report_record(factor="mzConsumstage15dCnt")

    def mzCashLoan15dCnt(self):
        """mzCashLoan15dCnt """
        return self.__get_mxmz_report_record(factor="mzCashLoan15dCnt")

    def mzOrgCnt(self):
        """mzOrgCnt """
        return self.__get_mxmz_report_record(factor="mzOrgCnt")

    def viploanLimit(self):
        sql = "select * from skynet_credit_line where user_id='%s' and product_id=10002" % (
        self.info.user_id)
        result = self.mysql.queryone_by_customer_id('skynet_credit_line', sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(result.get('credit_line', self.SET_DEFAULT_VALUE_INT_9999999))

    def lastBorrowDays(self):
        """lastBorrowDays 立即贷最近一次借款距今天数  --产品：2345借款"""
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -36)
        if not ljd_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return (return_strfYmd_date(ljd_days_list[-1][0])-return_strfYmd_date(self.info.event_time_add8h)).days

    def vipLoanBalance(self):
        """vipLoanBalance 当前立即贷产品剩余未还款金额  --产品：2345借款"""
        ljd_days_list = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -36)
        if not ljd_days_list:
            return self.SET_DEFAULT_VALUE_INT_0
        return int((ljd_days_list[-1][3]-ljd_days_list[-1][7]))

    def newBigBalance(self):
        """newBigBalance 用户在2345借款剩余未还款金额  --产品：2345借款"""
        JK_days_list=self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        current_loanInfo= JK_days_list[-1][6]
        current_orderInfo=[order for order in JK_days_list if JK_days_list[-1][6]==current_loanInfo]
        total_principal=[principal[3] for principal in current_orderInfo]
        repay_principal=[principal[7] for principal in current_orderInfo]
        return int(sum(total_principal)-sum(repay_principal))

    def newBigCurrLimit(self):
        """newBigCurrLimit 用户在2345借款当前授信额度  --产品：2345借款"""
        sql = "select * from skynet_credit_line where user_id='%s' and product_id='%s'" % (self.info.user_id, self.JK_product_id)
        result = self.mysql.queryone_by_customer_id('skynet_credit_line', sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(result.get('credit_line', self.SET_DEFAULT_VALUE_INT_9999999))

    def instalTerm(self):
        """instalTerm 当前订单借款期限　--产品：2345借款"""
        return self.info.result.get('data').get('periods',self.SET_DEFAULT_VALUE_INT_9999999)

    def mob(self):
        """mob 在册时长　--产品：2345借款"""
        sql="select * from customer_loan_progress_{0} where  customer_id='{1}' and status='1' and delete_flag=0".format(self.info.customer_id%20,self.info.customer_id)
        result=self.mysql.queryone_by_customer_id_sxj(db='apply_center',sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int((return_strfYmd_date(self.info.event_time_add8h)-return_strfYmd_date(result.get("update_at"))).days/30)

    def newBigMostOverdueDaysHis(self):
        """newBigMostOverdueDaysHis 2345借款产品历史最大逾期天数　--产品：2345借款"""
        JK_days_list = self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        overduedays=[(return_strfYmd_date(jk[2])-return_strfYmd_date(jk[1])).days for jk in JK_days_list]
        return max(overduedays)

    def newBigLastOverdueDaysHis(self):
        """newBigLastOverdueDaysHis 2345借款产品历史最长逾期期数　--产品：2345借款"""
        JK_days_list = self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        settle_date_list=[jk[2] for jk in JK_days_list if jk[2]>jk[1]]
        settle_date_only=list(set(settle_date_list))
        settle_date_count=[settle_date_list.count(jk) for jk in settle_date_only]
        return max(settle_date_count)

    def newBigHasPartialRepayment(self):
        """newBigHasPartialRepayment 逾期账户是否存在部分还款　--产品：2345借款"""
        JK_days_list=self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        current_loanInfo= JK_days_list[-1][6]
        current_orderInfo=[order for order in JK_days_list if JK_days_list[-1][6]==current_loanInfo]
        overdue_money=[round((jk[3]-jk[7])/jk[3],4) for jk in current_orderInfo]
        if max(overdue_money)>0.2:
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def newBigLastOverdueDaysLast(self):
        """newBigLastOverdueDayslast 2345借款产品最近一次借款最长逾期期数  --产品：2345借款"""
        JK_days_list = self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        current_loanInfo= JK_days_list[-1][6]
        current_orderInfo=[order for order in JK_days_list if order[6]==current_loanInfo]
        settle_date_list=[jk[2] for jk in current_orderInfo if jk[2]>jk[1]]
        settle_date_only=list(set(settle_date_list))
        settle_date_count=[settle_date_list.count(jk) for jk in settle_date_only]
        return max(settle_date_count)

    def newBigLastOverdueAmLast(self):
        """newBigLastOverdueAmLast 2345借款产品历史提前还款总次数  --产品：2345借款"""
        JK_days_list = self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        date_list=[jk for jk in JK_days_list if jk[1]>jk[2]]
        return len(date_list)

    def newBigLastBfBackTime(self):
        """newBigLastBfBackTime 2345借款产品最近一次借款提前还款次数  --产品：2345借款"""
        JK_days_list = self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        current_loanInfo= JK_days_list[-1][6]
        current_orderInfo=[order for order in JK_days_list if order[6]==current_loanInfo]
        date_list=[jk for jk in current_orderInfo if jk[1]>jk[2]]
        return len(date_list)


    def accountStatus(self):
        """accountStatus 2345借款产品当前账户状态  --产品：2345借款"""
        sql="select * from user_account where user_id='{0}' and product_id={1} and is_delete=0".format(self.info.user_id,self.JK_product_id)
        result=Mysql_account(env=self.env,bill=self.info.user_id%20).queryone_by_id(sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result.get("account_status")


    def newBigCurrOverdueDays(self):
        """newBigCurrOverdueDays 2345借款产品当前逾期天数  --产品：2345借款"""
        JK_days_list = self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        JK_days_list.sort(reverse=True)
        overdue_list=[]
        for jk in JK_days_list:
            if jk[3]!=jk[7]:
                overdue_list.append(jk[1])
            else:
                break
        if not overdue_list:
            return self.SET_DEFAULT_VALUE_INT_0
        return (return_strfYmd_date(self.info.event_time_add8h)-return_strfYmd_date(min(overdue_list))).days


    def newBigHistoryAll(self):
        """newBigHistoryAll 2345借款产品历史还款表现  --产品：2345借款"""
        JK_days_list = self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return ""
        current_loanInfo= JK_days_list[-1][6]
        current_orderInfo=[order for order in JK_days_list if order[6]==current_loanInfo]
        bx_list=[]
        for jk in current_orderInfo:
            if return_strfYmd_date(jk[2])==return_strfYmd_date(jk[1]):
                bx_list.append('/')
            if return_strfYmd_date(jk[2])<return_strfYmd_date(jk[1]):
                bx_list.append('T')
            if return_strfYmd_date(jk[2])>return_strfYmd_date(jk[1]):
                if (return_strfYmd_date(jk[2])-return_strfYmd_date(jk[1])).days%30==0:
                    bx_list.append(int(float((return_strfYmd_date(jk[2]) - return_strfYmd_date(jk[1])).days) / 30))
                else:
                    bx_list.append(int(float((return_strfYmd_date(jk[2]) - return_strfYmd_date(jk[1])).days) / 30) + 1)
        new_bx_list=[str(i) for i in bx_list]
        return ''.join(new_bx_list)


    def newBigLastOverdueAmt(self):
        """newBigLastOverdueAmt 2345借款产品最近一笔逾期金额  --产品：2345借款"""
        JK_days_list = self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return self.SET_DEFAULT_VALUE_INT_0
        current_loanInfo= JK_days_list[-1][6]
        current_orderInfo=[order for order in JK_days_list if order[6]==current_loanInfo]
        money_list=[(jk[3]-jk[7]) for jk in current_orderInfo]
        return int(sum(money_list))

    def newBigCurrAmount(self):
        """newBigCurrtAmount 2345借款产品借款本次借款本金  --产品：2345借款"""
        JK_days_list = self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return self.SET_DEFAULT_VALUE_INT_0
        current_loanInfo= JK_days_list[-1][6]
        current_orderInfo=[order for order in JK_days_list if order[6]==current_loanInfo]
        money_list=[jk[3] for jk in current_orderInfo]
        return int(sum(money_list))

    def newBigCurrTerm(self):
        """newBigCurrtErm 2345借款产品当前还款期数  --产品：2345借款"""
        JK_days_list = self.__hexin_bill(self.info.user_id, self.JK_product_id, -36)
        if not JK_days_list:
            return self.SET_DEFAULT_VALUE_INT_9999995
        current_loanInfo= JK_days_list[-1][6]
        current_orderInfo=[order for order in JK_days_list if order[6]==current_loanInfo]
        date_list=[jk for jk in current_orderInfo if jk[2]!=self.info.event_time_add8h]
        if not date_list:
            return self.SET_DEFAULT_VALUE_INT_0
        return len(date_list)+1

    def newBigLimitAdjustDays(self):
        """newBigLimitAdjustDays 最近一次额度调整距今天数  --产品：2345借款"""
        sql = "select * from skynet_credit_line where user_id='{0}' and product_id='{1}' and is_delete=0".format(
            self.info.user_id, self.JK_product_id)
        result = self.mysql.queryone_by_customer_id_sxj(db='skynet_credit_line', sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result.get("last_up_credit_line_date") and not result.get("last_reduce_credit_line_date"):
            return self.SET_DEFAULT_VALUE_INT_9999995
        if result.get("last_up_credit_line_date") and not result.get("last_reduce_credit_line_date"):
            return (return_strfYmd_date(self.info.event_time_add8h) - return_strfYmd_date(result.get("last_up_credit_line_date"))).days
        if not result.get("last_up_credit_line_date") and result.get("last_reduce_credit_line_date"):
            return (return_strfYmd_date(self.info.event_time_add8h) - return_strfYmd_date(result.get("last_reduce_credit_line_date"))).days
        updays = (return_strfYmd_date(self.info.event_time_add8h) - return_strfYmd_date(result.get("last_up_credit_line_date"))).days
        reducedays = (return_strfYmd_date(self.info.event_time_add8h) - return_strfYmd_date(result.get("last_reduce_credit_line_date"))).days
        return min(updays, reducedays)

    #立即贷需求
    def creditLengthLjd(self):
        """creditLengthLjd 立即贷开户时长"""
        sql="select * from customer_loan_progress_{0} where customer_id='{1}' and product_id='10002' and status='1' and delete_flag=0".format(self.info.customer_id%20,self.info.customer_id)
        result=self.mysql.queryone_by_customer_id_sxj(db='apply_center',sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int((return_strfYmd_date(self.info.event_time_add8h)-return_strfYmd_date(result.get("update_at"))).days/30)

    def histOverdueCntLjd(self):
        """histOverdueCntLjd 立即贷逾期次数"""
        ljd_days_list_24 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if not ljd_days_list_24:
            return self.SET_DEFAULT_VALUE_INT_0
        overdue_list=[ljd for ljd in ljd_days_list_24 if return_strfYmd_date(ljd[2])>return_strfYmd_date(ljd[1])]
        return len(overdue_list)

    def histOverdue2CntLjd(self):
        """histOverdue2CntLjd 立即贷逾期天数超过2天的逾期次数"""
        ljd_days_list_24 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if not ljd_days_list_24:
            return self.SET_DEFAULT_VALUE_INT_0
        overdue_list=[ljd for ljd in ljd_days_list_24 if (return_strfYmd_date(ljd[2])-return_strfYmd_date(ljd[1])).days >= 2]
        return len(overdue_list)

    def histOverdue3CntLjd(self):
        """histOverdue3CntLjd 立即贷逾期天数超过3天的逾期次数"""
        ljd_days_list_24 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if not ljd_days_list_24:
            return self.SET_DEFAULT_VALUE_INT_0
        overdue_list = [ljd for ljd in ljd_days_list_24 if (return_strfYmd_date(ljd[2])-return_strfYmd_date(ljd[1])).days >= 3]
        return len(overdue_list)

    def histOverdue4CntLjd(self):
        """histOverdue4CntLjd 立即贷逾期天数超过4天的逾期次数"""
        ljd_days_list_24 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if not ljd_days_list_24:
            return self.SET_DEFAULT_VALUE_INT_0
        overdue_list = [ljd for ljd in ljd_days_list_24 if (return_strfYmd_date(ljd[2])-return_strfYmd_date(ljd[1])).days  >= 4]
        return len(overdue_list)

    def histOverdue5CntLjd(self):
        """histOverdue5CntLjd 立即贷逾期天数超过5天的逾期次数"""
        ljd_days_list_24 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if not ljd_days_list_24:
            return self.SET_DEFAULT_VALUE_INT_0
        overdue_list = [ljd for ljd in ljd_days_list_24 if (return_strfYmd_date(ljd[2])-return_strfYmd_date(ljd[1])).days >= 5]
        return len(overdue_list)

    def histOverdue6CntLjd(self):
        """histOverdue6CntLjd 立即贷逾期天数超过6天的逾期次数"""
        ljd_days_list_24 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        if not ljd_days_list_24:
            return self.SET_DEFAULT_VALUE_INT_0
        overdue_list = [ljd for ljd in ljd_days_list_24 if (return_strfYmd_date(ljd[2])-return_strfYmd_date(ljd[1])).days >= 6]
        return len(overdue_list)

    def histDealCnt(self):
        """histDealCnt 历史成交次数"""
        if self.info.old_user_id:
            old_days_list_36 = self.__old_overdue_days(self.info.old_user_id, -36)
        else:
            old_days_list_36=[]
        ljd_days_list_24 = self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24)
        sxj_days_list_24 = self.__hexin_bill(self.info.user_id, self.sxj_product_id, -24)
        kdw_days_list_24 = self.__hexin_bill(self.info.user_id, self.kdw_product_id, -24)
        kdw_days_list_order=[order[6] for order in kdw_days_list_24]
        return len(old_days_list_36)+len(ljd_days_list_24)+len(sxj_days_list_24)+len(list(set(kdw_days_list_order)))

    def histOverdueCntToDealCntLjd(self):
        """histOverdueCntToDealCntLjd 立即贷借款逾期频率"""
        histOverdueCntLjd=self.histOverdueCntLjd()
        vipDealCnt=self.vipDealCnt()
        if vipDealCnt==0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        if histOverdueCntLjd==self.SET_DEFAULT_VALUE_INT_9999995:
            return self.SET_DEFAULT_VALUE_INT_9999995
        return round(float(histOverdueCntLjd)/vipDealCnt,4)

    def __lateCnt(self):
        """__lateCnt 逾期次数"""
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
        sql = "select customer_id from identiy_card_%s where identity_card='%s' and delete_flag=0;" % (i,factor_encrypt_identity(int(self.info.cert_id)))
        result = self.mysql.queryone_by_customer_id('customer_center', sql)
        if result and result.get('customer_id'):
            ljd_customer_id=result.get('customer_id')
            userId_sql="select * from customer where id ='%s'"%ljd_customer_id
            result = self.mysql.queryone_by_customer_id('customer_center', userId_sql)
            user_id=result.get('user_id')
            all_list_days=self.__hexin_bill(user_id,self.ljd_product_id,-24)+self.__hexin_bill(user_id,self.sxj_product_id,-24)+self.__hexin_bill(user_id,self.kdw_product_id,-24)
            for days in all_list_days:
                if return_strfYmd_date(days[2])>return_strfYmd_date(days[1]):
                    count+=1
        return count

    def histOverdueCntToDealCnt(self):
        """histOverdueCntToDealCnt 历史借款逾期频率"""
        lateCnt=self.__lateCnt()
        histDealCnt=self.histDealCnt()
        if histDealCnt==0:
            return self.SET_DEFAULT_VALUE_FLOAT_9999998
        return round(float(lateCnt)/histDealCnt,4)

    def borrowCnt(self):
        """borrowCnt 当前产品的借款次数   来源：反欺诈3.0"""
        return  len(self.__hexin_bill(self.info.user_id, self.ljd_product_id, -24))

if __name__ == "__main__":
    serial_no = "5bd28c91004f9e736cbbdca3"
    a = CreditLineFactor('T1', serial_no)
    print a.avgCollectCntOfDueCntLjd()
    print a.avgCalltimeGt0CntOfDueCntLjd()
    # print a.rule_contact_max5_m2()
    # print a.useRpInterLes0MinL12mPamth()
    # print a.last1BorrowLateDaysLjd()
    # print a.rule_contact_max5_m2()||||||| .r2911
    serial_no = "5b9fa815000dffff0edf3322"
    a = CreditLineFactor('T2', serial_no)
    print a.kinshipContactFirstOverdueDays()
    # print a.rule_contact_max5_m2()
    # print a.useRpInterLes0MinL12mPamth()
    # print a.last1BorrowLateDaysLjd()
    # print a.rule_contact_max5_m2()=======
    serial_no = "1551857903000-3C348568F78BEE91D61B07EA1EEDDAD0"
    a = CreditLineFactor('T3', serial_no)

