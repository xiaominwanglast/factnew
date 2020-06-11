#!/usr/bin/python
# -*- coding: UTF-8 -*-
from FrameRunner.FactorInit import CarFactorInit
from utils.TestInit import factor_encrypt_identity
import datetime
class CarFactorAuto(CarFactorInit):
    def __init__(self, env, serial_no):
        super(CarFactorAuto,self).__init__(env, serial_no)
    def __return_strfYmd_date(self,date):
        return datetime.datetime.strptime(date.strftime('%Y-%m-%d'),'%Y-%m-%d')

    def cdwLoanProduct(self):
        """cdwLoanProduct 车贷王中的贷款产品 String"""
        return self.info.result.get('data').get('loanProduct')

    def cdwLoanAmount(self):
        """cdwLoanAmount 车贷融资总额 Double"""
        return self.info.result.get('data').get('loanAmount')

    def cdwLoanTerm(self):
        """cdwLoanTerm 贷款期限 Integer"""
        return self.info.result.get('data').get('loanTerm')

    def cdwVehicleType(self):
        """cdwVehicleType 车辆类型：非能源汽车 String"""
        return self.info.result.get('data').get('vehicleType')

    def loanProductApplyStatus(self):
        """loanProductApplyStatus 我司申请消费贷款记录 Integer"""
        sql_xin="select * from s_user_product_audit where id_no='%s'"%self.info.cert_id
        result_xin=self.mysql.queryall_by_table_new_only(db='xinyongjin',sql=sql_xin)
        if result_xin:
            return 1
        if str(self.info.cert_id)[-1].lower()=='x' or str(self.info.cert_id)[-1].lower()=='X':
            i='x'
        else:
            i=int(str(self.info.cert_id)[-1])%10
        encrypt_cert_id=factor_encrypt_identity(self.info.cert_id)
        sql = "select customer_id from identiy_card_%s where identity_card='%s';" % (i, encrypt_cert_id)
        result = self.mysql.queryone_by_customer_id_sxj('customer_center', sql)
        if not result:
            return 0
        sql="select user_id from customer where id='%s' and delete_flag=0"%(result['customer_id'])
        result= self.mysql.queryone_by_customer_id_sxj('customer_center',sql)
        if not result:
            return 0
        sql="select id from customer where user_id='%s' and delete_flag=0"%result['user_id']
        result= self.mysql.queryall_by_table_new_only('customer_center',sql)
        customer_ids = list(set([str(data['id']) for data in result]))
        if not customer_ids:
            return 0
        customer_ids_string = ','.join(customer_ids)
        sql = "select * from a_customer_apply_{0} where customer_id in (%s) and delete_flag=0" %customer_ids_string
        result = self.mysql.queryall_by_table_new_only('apply_center', sql)
        if not result:
            return 0
        return 1

    def cdwLenderAge(self):
        """cdwLenderAge 贷款人的年龄 Integer"""
        return self.info.result.get('data').get('age')

    def cdwRegisterLocationMatchBlacklist(self):
        """cdwRegisterLocationMatchBlacklist 最终车辆上牌地区是否命中黑名单 Integer"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='cdw_city_black_record',
                                            find={'city':self.info.result.get('data').get('registerLocation')})
        if not result:
            return 0
        return 1

    def cdwLenderGender(self):
        """cdwLenderGender 贷款人性别 Integer"""
        return self.info.result.get('data').get('gender')

    def cdwMaritalStatus(self):
        """cdwMaritalStatus 贷款人婚姻状况 Integer"""
        return self.info.result.get('data').get('maritalStatus')

    def qhcsCreditScore(self):
        """qhcsCreditScore 前海2.0信用卡综合评分 Integer"""
        if  not self.info.result.get('data'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='qhcs_msc8262_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'cardNo':self.info.result.get('data').get('bankcardNo'),'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        last_one=result[0]
        if not last_one.get('qhcsMsc8262Info') or not last_one.get('qhcsMsc8262Info').get('credooScore'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return last_one.get('qhcsMsc8262Info').get('credooScore')

    def finalScore(self):
        """finalScore 同盾分 Integer"""
        results = self.mongo.query_by_user_id(db='galaxy', collection="td_record",find={"realName": factor_encrypt_identity(self.info.user_name),"cardId":factor_encrypt_identity(self.info.cert_id),"phone":factor_encrypt_identity(self.info.phone)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if results[0].get('result')=='-1':
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get('tdReportResponse'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return results[0].get('tdReportResponse').get('final_score')

    def cdwCzcbDebtScore(self):
        """cdwCzcbDebtScore 稠银-个人负债评分 Double"""
        return self.info.result.get('data').get('czcbDebtScore')

    def cdwCzcbGeneralScore(self):
        """cdwCzcbGeneralScore 稠银-个人综合评分 Double"""
        return self.info.result.get('data').get('czcbGeneralScore')

    def cdwCzcbOverdueScore(self):
        """cdwCzcbOverdueScore 稠银-个人逾期评分 Double"""
        return self.info.result.get('data').get('czcbOverdueScore')

    def geoPhoneEntDuration(self):
        """geoPhoneEntDuration 手机在网时间"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='geo_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result[0].get('result')=='-1':
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get('response') or not result[0].get('response').get('data'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        if  not result[0].get('response').get('data').get('RSL'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for i in result[0].get('response').get('data').get('RSL'):
            if i.get('IFT')=='A3':
                if not i.get('RS').get('code'):
                    return self.SET_DEFAULT_VALUE_INT_9999996
                return i.get('RS').get('code')
        return self.SET_DEFAULT_VALUE_INT_9999999

    def geoPhoneSelfMatch(self):
        """geoPhoneSelfMatch 手机为本人实名认证 String"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='geo_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result[0].get('result')=='-1':
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get('response') or not result[0].get('response').get('data') or not result[0].get('response').get('data').get('RSL'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for i in result[0].get('response').get('data').get('RSL'):
            if i.get('IFT')=='B7':
                if not i.get('RS').get('code'):
                    return self.SET_DEFAULT_VALUE_INT_9999996
                return i.get('RS').get('code')
        return self.SET_DEFAULT_VALUE_INT_9999999

    def phoneGrayScore(self):
        """phoneGrayScore 聚信立灰度分 Integer"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='miguan_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get('response') or not result[0].get('response').get('data') or not result[0].get('response').get('data').get('user_gray'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return result[0].get('response').get('data').get('user_gray').get('phone_gray_score')

    def hfRiskMsgNum(self):
        """hfRiskMsgNum 汇法是否命中 Integer"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='huifa_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result[0].get('response').get('fxmsgnum')==0:
            return 0
        if not result[0].get('response') or not result[0].get('response').get('fxmsgnum'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result[0].get('response').get('fxmsgnum')

    def cdwAgentNameMatchBlacklist(self):
        """cdwAgentNameMatchBlacklist 经销商是否命中黑名单 Integer"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='cdw_dealer_white_record',
                                            find={'dealer':self.info.result.get('data').get('agentName')})
        if not result:
            return 0
        return 1

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

    def cdwAgentNameMatchWhitelist(self):
        """cdwAgentNameMatchWhitelist 经销商是否命中白名单 Integer"""

        list_B = [1039,1067,1073,1074,1077,1086,1112,1115,1118,1128,1129,1131,1133,1149,1155,1156,1173,1177]
        list_A = [1045,1053,1059,1070,1072,1080,1087,1100,1104,1113,1116,1122,1127,1135,1137,1139,1141,1145,1158,1159,1165,1168,1169,1170,1176,1178,1179,1183,1184,1186,1187]
        list_C = [1023,1042,1044,1045,1047,1048,1069,1083,1089,1090,1092,1097,1105,1114,1120,1124,1126,1154,1161,1166]


        if int(self.info.result.get('data').get('agentName')) in list_A:
            return 1
        elif int(self.info.result.get('data').get('agentName')) in list_B:
            return 2
        elif int(self.info.result.get('data').get('agentName')) in list_C:
            return 3
        else:
            return 0

    def cdwCzcbDebtRiskResult(self):
        """czcbGeneralRiskResult 稠银-个人综合评定结果"""
        return self.info.result.get('data').get('czcbDebtRiskResult')

    def cdwCzcbGeneralRiskResult(self):
        """czcbDebtRiskResult 稠银-个人负债评定结果"""
        return self.info.result.get('data').get('czcbGeneralRiskResult')

    def cdwCzcbOverdueRiskResult(self):
        """czcbOverdueRiskResult 稠银-个人逾期评定结果"""
        return self.info.result.get('data').get('czcbOverdueRiskResult')

    def cdwCzcbRiskNote(self):
        """cdwCzcbRiskNote 稠银征信返回的备注信息"""
        return self.info.result.get('data').get('czcbRiskNote')

    def cdwOutOfAuthorizedDistrict(self):
        """cdwOutOfAuthorizedDistrict 是否超出授权区域范围"""
        return self.info.result.get('data').get('outOfAuthorizedDistrict')

    def cdwIdCardAppearCount(self):
        """cdwIdCardAppearCount 车贷系统的身份证号出现次数"""
        return self.info.result.get('data').get('idCardAppearCount')

    def cdwIdCardExpired(self):
        """cdwIdCardExpired 身份证号是否超出有效期"""
        return self.info.result.get('data').get('idCardExpired')

    def cdwIsLcv(self):
        """cdwIsLcv 是否为轻型商用车"""
        return self.info.result.get('data').get('isLcv')

    def __hf_result(self,style):
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='huifa_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get("response") or not result[0].get("response").get("fxcontent") or not result[0].get("response").get("fxcontent").get(style):
            return self.SET_DEFAULT_VALUE_INT_9999996
        status_list=[]
        if style=="zhixing":
            for zx in result[0].get("response").get("fxcontent").get(style):
                if zx.get("state") not in status_list:
                    if zx.get("state"):
                        status_list.append(zx.get("state"))
        if style=="caipan":
            for zx in result[0].get("response").get("fxcontent").get(style):
                if zx.get("casetopic") not in status_list and zx.get("pctype")==u"被告":
                    if zx.get("casetopic"):
                        status_list.append(zx.get("casetopic"))
        else:
            for zx in result[0].get("response").get("fxcontent").get(style):
                if zx.get("sx_jt") not in status_list:
                    status_list.append(zx.get("sx_jt"))
        status_list.sort()
        if not status_list:
            return self.SET_DEFAULT_VALUE_INT_9999996
        return ','.join([status for status in status_list if status])


    def hfExecutionState(self):
        """hfExecutionState 汇法[zhixing]案件状态"""
        return self.__hf_result(style='zhixing')

    def hfCaseTopic(self):
        """hfCaseTopic 汇法[caipan]涉案事由"""
        return self.__hf_result(style='caipan')

    def hfDishonestDetail(self):
        """hfDishonestDetail 汇法[shixin]具体情形"""
        return self.__hf_result(style='shixin')


    def __hf_month_money(self,style):
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='huifa_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get("response") or not result[0].get("response").get("fxcontent") or not result[0].get("response").get("fxcontent").get("zhixing"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        clear_status=[]
        sslong_time=[]
        for zx in result[0].get("response").get("fxcontent").get("zhixing"):
            clear_status.append(zx)
            sslong_time.append(datetime.datetime.strptime(zx.get("sslong"),"%Y-%m-%d"))
        if not clear_status or not sslong_time:
            return self.SET_DEFAULT_VALUE_INT_9999996
        if style=='month':
            for case in clear_status:
                if case.get("sslong") in str(max(sslong_time)):
                    return (self.__return_strfYmd_date(self.info.event_time_add8h).year-max(sslong_time).year)*12+self.__return_strfYmd_date(self.info.event_time_add8h).month-max(sslong_time).month
            return self.SET_DEFAULT_VALUE_INT_9999996
        elif style=='money':
            for case in clear_status:
                if case.get("sslong") in str(max(sslong_time)):
                    return float(case.get("money"))
            return self.SET_DEFAULT_VALUE_FLOAT_9999996
        else:
            return
    def hfExecutionTerm(self):
        """hfExecutionTerm 汇法[zhixing]执行期限"""
        return self.__hf_month_money(style="month")

    def hfExecutionMoney(self):
        """hfExecutionMoney  汇法[zhixing]执行标的"""
        return self.__hf_month_money(style="money")

    def pbocInfo(self):
        """pbocInfo """
        if not self.info.result.get('data').get('pbocInfo'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('pbocInfo')

    def pbocResult(self):
        """pbocResult"""
        if not self.info.result.get('data').get('pbocResult'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('pbocResult')

    def cdwApplicantIdCardAppearCount(self):
        """cdwApplicantIdCardAppearCount 申请人证件号出现次数"""
        new_sql="select count(*) as cnt from e_apply left join e_proposer ep2 on e_apply.id = ep2.apply_id and " \
                "case e_apply.apply_type when 0 then ep2.type = 2 and ep2.id = (select min(id) from e_proposer " \
                "where e_proposer.apply_id = e_apply.id) else ep2.type = 3 end where ep2.card_id = '%s' " \
                "and `current_node` in (9,10,101,11,12,13)"%self.info.cert_id
        old_sql="SELECT COUNT(*) as cnt FROM lb_apply_lessee_info b LEFT JOIN lb_apply_main a ON a.asqbh = b.asqbh WHERE a.azjhm = '%s' AND `ASQZTDM` IN ('01', '02', '03', '061', '06', '08', '09', '10');"%self.info.cert_id
        new_result=self.mysql.queryone_by_customer_id(db='auto_loan_entry_test',sql=new_sql)
        old_result = self.mysql.queryone_by_customer_id(db='zu_che',sql=old_sql)
        return new_result.get('cnt')+old_result.get("cnt")

    def cdwGuarantorIdCardAppearCount(self):
        """cdwGuarantorIdCardAppearCount 第一担保人的证件号出现次数"""
        if not self.info.result.get('data').get('guarantorIdNumber'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        new_sql="select count(*) as cnt from e_apply left join e_proposer ep2 on e_apply.id = ep2.apply_id and " \
                "case e_apply.apply_type when 0 then ep2.type = 2 and ep2.id = (select min(id) from e_proposer " \
                "where e_proposer.apply_id = e_apply.id) else ep2.type = 3 end where ep2.card_id = '%s' " \
                "and `current_node` in (9,10,101,11,12,13)"%self.info.result.get('data').get('guarantorIdNumber')
        old_sql="SELECT COUNT(*) as cnt FROM lb_apply_lessee_bondsman c LEFT JOIN lb_apply_main a ON a.asqbh = c.asqbh WHERE a.azjhm = '%s' AND `ASQZTDM` IN ('01', '02', '03', '061', '06', '08', '09', '10');"%self.info.result.get('data').get('guarantorIdNumber')
        new_result=self.mysql.queryone_by_customer_id(db='auto_loan_entry_test',sql=new_sql)
        old_result = self.mysql.queryone_by_customer_id(db='zu_che',sql=old_sql)
        return new_result.get('cnt') + old_result.get("cnt")

    def qhcsDefaultRiskScore(self):
        """qhcsDefaultRiskScore 前海征信-客户本人-失信风险评分"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='qhcs_msc8262_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        last_one=result[0]
        if not last_one.get('qhcsMsc8262Info') or not last_one.get('qhcsMsc8262Info').get('defaultRiskScore'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return last_one.get('qhcsMsc8262Info').get('defaultRiskScore')

    def cdwIsSpouseIdMatch(self):
        """cdwIsSpouseIdMatch 配偶身份证前6位与用户是否一致"""
        spouseIdNumber=self.info.result.get('data').get('spouseIdNumber')
        if not spouseIdNumber:
            return self.SET_DEFAULT_VALUE_INT_9999995
        if str(spouseIdNumber)[:6]==str(self.info.cert_id)[:6]:
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def cdwNoRelationContactCnt(self):
        """cdwNoRelationContactCnt 关系为0的联系人个数"""
        if not self.info.result.get('data').get('noRelationContactCnt'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('noRelationContactCnt')

    def cdwNetPrice(self):
        """cdwNetPrice （经销商填写）指导价"""
        if not self.info.result.get('data').get('netPrice'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('netPrice')

    def cdwIsGuarantorPhoneMatch(self):
        """cdwIsGuarantorPhoneMatch 担保人手机号前6位与用户是否一致"""
        guarantorPhone=self.info.result.get('data').get('guarantorPhone')
        if not guarantorPhone:
            return self.SET_DEFAULT_VALUE_INT_9999995
        if str(guarantorPhone)[:6]==str(self.info.phone)[:6]:
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def qhcsBehaviourScore(self):
        """qhcsBehaviourScore 前海征信-客户本人-行为特征评分"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='qhcs_msc8262_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        last_one=result[0]
        if not last_one.get('qhcsMsc8262Info') or not last_one.get('qhcsMsc8262Info').get('behaviourScore'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return last_one.get('qhcsMsc8262Info').get('behaviourScore')

    def __tdResult(self,item_id):
        results = self.mongo.queryall_by_userId(db='galaxy', collection="td_record",
                                            find={"realName": factor_encrypt_identity(self.info.user_name),"cardId":factor_encrypt_identity(self.info.cert_id),"phone":factor_encrypt_identity(self.info.phone)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get('tdReportResponse'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for row in results[0].get('tdReportResponse').get('risk_items'):
            if row.get('item_id')==str(item_id):
                return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def riskItem2976222(self):
        """riskItem2976222	身份证命中高风险关注名单"""
        return self.__tdResult(item_id=2976222)

    def riskItem2976210(self):
        """riskItem2976210 身份证归宿地位于高风险较为集中地区"""
        return self.__tdResult(item_id=2976210)

    def riskItem2976264(self):
        """riskItem2976264 手机号命中高风险关注名单"""
        return self.__tdResult(item_id=2976264)

    def riskItem2976256(self):
        """riskItem2976256 手机号命中通信小号库"""
        return self.__tdResult(item_id=2976256)

    def riskItem2976386(self):
        """riskItem2976386 第一联系人身份证命中法院失信名单-近亲"""
        return self.__tdResult(item_id=2976386)

    def riskItem2976388(self):
        """riskItem2976388 第一联系人身份证命中法院执行名单"""
        return self.__tdResult(item_id=2976388)

    def riskItem2976392(self):
        """riskItem2976392 第一联系人身份证命中犯罪通缉名单"""
        return self.__tdResult(item_id=2976392)

    def riskItem2976396(self):
        """riskItem2976396 第一联系人身份证命中信贷逾期名单"""
        return self.__tdResult(item_id=2976396)

    def riskItem2976398(self):
        """riskItem2976398 第一联系人手机号命中信贷逾期名单"""
        return self.__tdResult(item_id=2976398)

    def riskItem2976402(self):
        """riskItem2976402 第一联系人手机号命中虚假号码或通信小号库"""
        return self.__tdResult(item_id=2976402)

    def cdwCzcbPbocResult(self):
        """cdwCzcbPbocResult 综合稠州银行返回的六个信息做一个综合结论"""
        if self.info.result.get('data').get('czcbGeneralRiskResult') or self.info.result.get('data').get('czcbDebtRiskResult') or self.info.result.get('data').get('czcbOverdueRiskResult'):
            return "D"
        if self.info.result.get('data').get('czcbGeneralRiskResult') or self.info.result.get('data').get('czcbDebtRiskResult') or self.info.result.get('data').get('czcbOverdueRiskResult') or self.info.result.get('data').get('czcbGeneralScore')<0 or float(self.info.result.get('data').get('czcbOverdueScore'))>800:
            return "N"
        if self.info.result.get('data').get('czcbGeneralRiskResult') and self.info.result.get('data').get('czcbDebtRiskResult') and self.info.result.get('data').get('czcbOverdueRiskResult'):
            return "A"
        return "C"

    def cdwVehicleIdNumberAppearCount(self):
        """cdwVehicleIdNumberAppearCount 车架号出现的次数"""
        sql="SELECT COUNT(*) as cnt FROM lb_apply_CAR c LEFT JOIN lb_apply_main a ON a.asqbh = c.asqbh WHERE ACJH = '%s' AND `ASQZTDM` IN ('03', '061', '06', '08', '09', '10')"%self.info.result.get('data').get("vehicleIdNumber")
        result = self.mysql.queryone_by_customer_id(db='zu_che', sql=sql)
        # new_sql="select count(*) as cnt from e_apply left join e_car on e_apply.id = e_car.apply_id  where car_vin = '%s' and`current_node` in (9, 10,101,11,12,13 );"%self.info.result.get('data').get("vehicleIdNumber")
        new_sql="SELECT COUNT(*) FROM e_apply a LEFT JOIN e_car ec1 ON a.id = ec1.apply_id WHERE ec1.car_vin = '%s' AND a.apply_status IN (5, 6, 7, 8)"%self.info.result.get('data').get("vehicleIdNumber")
        new_result = self.mysql.queryone_by_customer_id(db='auto_loan_entry_test', sql=new_sql)
        return result.get("cnt") + new_result.get("cnt")

    def greenChannel(self):
        """greenChannel 车贷绿色通道"""
        if self.info.result.get('data').get('greenChannel') or self.info.result.get('data').get('greenChannel')=='':
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('greenChannel')

    def pbocReason(self):
        """pbocReason 众邦征信结果返回是拒绝的原因明细"""
        return self.info.result.get('data').get('pbocReason')

    #20190212
    def applicantSpouseType(self):
        """applicantSpouseType 申请人有没有配偶"""
        return self.info.result.get('data').get("hasSpouse")

    def spouseGeoPhoneLand(self):
        """spouseGeoPhoneLand 集奥数据-配偶-手机归属地"""
        spouseIdNumber = self.info.result.get('data').get('spouseIdNumber')
        spousePhone =self.info.result.get('data').get('spousePhone')
        spouseName  =self.info.result.get('data').get('spouseName')
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='geo_record',
                                            find={'cardId':spouseIdNumber,'phone':spousePhone,'realName':spouseName})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get("response") or not result[0].get('response').get('data') or not result[0].get('response').get('data').get('ISPNUM'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result[0].get('response').get('data').get('ISPNUM').get("province",self.SET_DEFAULT_VALUE_INT_9999996)

    def __GeoPhoneCost(self,IdNumber,phone,name,geoType):
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='geo_record',
                                            find={'cardId':IdNumber,'phone':phone,'realName':name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get("response") or not result[0].get('response').get('data') or not result[0].get('response').get('data').get('RSL'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        for code in result[0].get('response').get('data').get('RSL'):
            if code.get("IFT")==geoType:
                return code.get("RS").get("code")
        return self.SET_DEFAULT_VALUE_INT_9999999

    def spouseGeoPhoneEntDuration(self):
        """spouseGeoPhoneEntDuration 申请人配偶的手机在网时长"""
        spouseIdNumber = self.info.result.get('data').get('spouseIdNumber')
        spousePhone =self.info.result.get('data').get('spousePhone')
        spouseName  =self.info.result.get('data').get('spouseName')
        return self.__GeoPhoneCost(spouseIdNumber, spousePhone, spouseName,geoType='A3')

    def geoPhoneCost(self):
        """geoPhoneCost 集奥数据中申请人的手机话费账单"""
        IdNumber =self.info.cert_id
        phone  =self.info.phone
        name   =self.info.user_name
        return self.__GeoPhoneCost(IdNumber,phone,name,geoType='B1')

    def sponsorGeoPhoneCost(self):
        """sponsorGeoPhoneCost 集奥数据中担保人的手机话费账单"""
        guarantorIdNumber=self.info.result.get('data').get('guarantorIdNumber')
        guarantorPhone=self.info.result.get('data').get('guarantorPhone')
        guarantorName =self.info.result.get('data').get('guarantorName')
        return self.__GeoPhoneCost(guarantorIdNumber,guarantorPhone,guarantorName,geoType='B1')

    def spouseGeoPhoneCost(self):
        """spouseGeoPhoneCost 集奥数据中配偶人的手机话费账单"""
        spouseIdNumber = self.info.result.get('data').get('spouseIdNumber')
        spousePhone =self.info.result.get('data').get('spousePhone')
        spouseName  =self.info.result.get('data').get('spouseName')
        return self.__GeoPhoneCost(spouseIdNumber,spousePhone,spouseName,geoType='B1')

    def spouseGeoPhoneSelfMatch(self):
        """spouseGeoPhoneSelfMatch 申请人配偶的手机号是否其配偶身份证实名验证一致"""
        spouseIdNumber = self.info.result.get('data').get('spouseIdNumber')
        spousePhone =self.info.result.get('data').get('spousePhone')
        spouseName  =self.info.result.get('data').get('spouseName')
        return self.__GeoPhoneCost(spouseIdNumber,spousePhone,spouseName,geoType='B7')

    def sponsorGeoPhoneSelfMatch(self):
        """sponsorGeoPhoneSelfMatch 担保人的手机号是否和担保人本人身份证实名验证一致"""
        guarantorIdNumber=self.info.result.get('data').get('guarantorIdNumber')
        guarantorPhone=self.info.result.get('data').get('guarantorPhone')
        guarantorName =self.info.result.get('data').get('guarantorName')
        return self.__GeoPhoneCost(guarantorIdNumber,guarantorPhone,guarantorName,geoType='B7')

    def sponsorType(self):
        """sponsorType 是否添加了担保人"""
        return self.info.result.get('data').get('hasGuarantor')

    def sponsorAge(self):
        """sponsorAge 担保人的年龄"""
        guarantorIdNumber = self.info.result.get('data').get('guarantorIdNumber')
        sub = int(self.info.create_time.strftime('%Y%m%d')) - int(guarantorIdNumber[6:14])
        return int(str(sub)[:-4])

    def carClass(self):
        """carClass 返回申请人准驾车型"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='py_record',
                                            find={'cardId':factor_encrypt_identity(self.info.cert_id),'phone':factor_encrypt_identity(self.info.phone),'realName':factor_encrypt_identity(self.info.user_name)})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get('pyResponse') or not result[0].get('pyResponse').get('returnValue') \
            or not result[0].get('pyResponse').get('returnValue').get('cisReport'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        carClass=result[0].get('pyResponse').get('returnValue').get('cisReport')[0].get('driverLicenseInfo').get('carClass',self.SET_DEFAULT_VALUE_INT_9999996)
        if carClass==self.SET_DEFAULT_VALUE_INT_9999996 or not carClass:
            return self.SET_DEFAULT_VALUE_INT_9999996
        if 'A1' in carClass:
            return 7
        if 'A2' in carClass:
            return 6
        if 'A3' in carClass:
            return 5
        if 'B1' in carClass:
            return 4
        if 'B2' in carClass:
            return 3
        if 'C1' in carClass:
            return 2
        if 'C2' in carClass:
            return 1
        return 0

    def drivingLicenceExpiryDate(self):
        """drivingLicenceExpiryDate 返回申请人驾驶证的有效期"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='py_record',
                                            find={'cardId':factor_encrypt_identity(self.info.cert_id),'phone':factor_encrypt_identity(self.info.phone),'realName':factor_encrypt_identity(self.info.user_name)})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get('pyResponse') or not result[0].get('pyResponse').get('returnValue') \
            or not result[0].get('pyResponse').get('returnValue').get('cisReport'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        expiryDate=result[0].get('pyResponse').get('returnValue').get('cisReport')[0].get('driverLicenseInfo').get('expiryDate',self.SET_DEFAULT_VALUE_INT_9999996)
        if expiryDate==self.SET_DEFAULT_VALUE_INT_9999996:
            return self.SET_DEFAULT_VALUE_INT_9999996
        if expiryDate=='':
            return self.SET_DEFAULT_VALUE_INT_9999996
        return datetime.datetime.strptime(expiryDate, "%Y-%m-%d")

    def drivingLicenceStatus(self):
        """drivingLicenceStatus 返回驾驶证状态"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='py_record',
                                            find={'cardId':factor_encrypt_identity(self.info.cert_id),'phone':factor_encrypt_identity(self.info.phone),'realName':factor_encrypt_identity(self.info.user_name)})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get('pyResponse') or not result[0].get('pyResponse').get('returnValue') \
            or not result[0].get('pyResponse').get('returnValue').get('cisReport'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        status=result[0].get('pyResponse').get('returnValue').get('cisReport')[0].get('driverLicenseInfo').get('status',self.SET_DEFAULT_VALUE_INT_9999996)

        if status==self.SET_DEFAULT_VALUE_INT_9999996 or not status:
            return self.SET_DEFAULT_VALUE_INT_9999996
        statusList=[]
        if u'正常' in status:
            statusList.append('1')
        if u'超分' in status:
            statusList.append('2')
        if u'转出' in status:
            statusList.append('3')
        if u'暂扣' in status:
            statusList.append('4')
        if u'撤销' in status:
            statusList.append('5')
        if u'吊销' in status:
            statusList.append('6')
        if u'注销' in status:
            statusList.append('7')
        if u'违法未处理' in status:
            statusList.append('8')
        if u'停止使用' in status:
            statusList.append('9')
        if u'事故未处理' in status:
            statusList.append('10')
        if u'协查' in status:
            statusList.append('11')
        if u'锁定' in status:
            statusList.append('12')
        if u'逾期未换证' in status:
            statusList.append('13')
        if u'延期换证' in status:
            statusList.append('14')
        if u'延期体检' in status:
            statusList.append('15')
        if u'逾期未体检' in status:
            statusList.append('16')
        if u'逾期未审验' in status:
            statusList.append('17')
        if u'其他' in status:
            statusList.append('18')
        if u'扣留' in status:
            statusList.append('19')
        if not statusList:
            return self.SET_DEFAULT_VALUE_INT_0
        return ';'.join(statusList)

    def spouseFinalScore(self):
        """spouseFinalScore 申请人配偶的同盾分"""
        spouseIdNumber = self.info.result.get('data').get('spouseIdNumber')
        spousePhone =self.info.result.get('data').get('spousePhone')
        spouseName  =self.info.result.get('data').get('spouseName')
        results = self.mongo.query_by_user_id(db='galaxy', collection="td_record",find={"realName": factor_encrypt_identity(spouseName),"cardId":factor_encrypt_identity(spouseIdNumber),"phone":factor_encrypt_identity(spousePhone)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if results[0].get('result')=='-1':
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get('tdReportResponse'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return results[0].get('tdReportResponse').get('final_score')

    def __tdResult_spouse(self,item_id):
        spouseIdNumber = self.info.result.get('data').get('spouseIdNumber')
        spousePhone =self.info.result.get('data').get('spousePhone')
        spouseName  =self.info.result.get('data').get('spouseName')
        results = self.mongo.queryall_by_userId(db='galaxy', collection="td_record",find={"realName": factor_encrypt_identity(spouseName),"cardId":factor_encrypt_identity(spouseIdNumber),"phone":factor_encrypt_identity(spousePhone)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get('tdReportResponse'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for row in results[0].get('tdReportResponse').get('risk_items'):
            if row.get('item_id')==str(item_id):
                return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def spouseRiskItem2976210(self):
        """spouseRiskItem2976210 申请人配偶的身份证归宿地位于高风险较为集中地区"""
        return self.__tdResult_spouse(item_id=2976210)

    def spouseRiskItem2976222(self):
        """spouseRiskItem2976222 申请人配偶的身份证命中高风险关注名单"""
        return self.__tdResult_spouse(item_id=2976222)

    def spouseRiskItem2976256(self):
        """spouseRiskItem2976256 申请人配偶的手机号命中通信小号库"""
        return self.__tdResult_spouse(item_id=2976256)

    def spouseRiskItem2976264(self):
        """spouseRiskItem2976264 申请人配偶的手机号命中高风险关注名单"""
        return self.__tdResult_spouse(item_id=2976264)

    def spouseRiskItem2976386(self):
        """spouseRiskItem2976386 申请人配偶的第一联系人身份证命中法院失信名单-近亲"""
        return self.__tdResult_spouse(item_id=2976386)

    def spouseRiskItem2976388(self):
        """spouseRiskItem2976388 申请人配偶的第一联系人身份证命中法院执行名单"""
        return self.__tdResult_spouse(item_id=2976388)

    def spouseRiskItem2976392(self):
        """spouseRiskItem2976392 申请人配偶的第一联系人身份证命中犯罪通缉名单"""
        return self.__tdResult_spouse(item_id=2976392)

    def spouseRiskItem2976396(self):
        """spouseRiskItem2976396 申请人配偶的第一联系人身份证命中信贷逾期名单"""
        return self.__tdResult_spouse(item_id=2976396)

    def spouseRiskItem2976398(self):
        """spouseRiskItem2976398 申请人配偶的第一联系人手机号命中信贷逾期名单"""
        return self.__tdResult_spouse(item_id=2976398)

    def spouseRiskItem2976402(self):
        """spouseRiskItem2976402 申请人配偶的第一联系人手机号命中虚假号码或通信小号库"""
        return self.__tdResult_spouse(item_id=2976402)

    def spouseRiskItem2976212(self):
        """spouseRiskItem2976212 申请人配偶的身份证命中法院失信黑名单"""
        return self.__tdResult_spouse(item_id=2976212)

    def spouseRiskItem2976214(self):
        """spouseRiskItem2976214 申请人配偶的身份证命中犯罪通缉名单"""
        return self.__tdResult_spouse(item_id=2976214)

    def spouseRiskItem2976216(self):
        """spouseRiskItem2976216 申请人配偶的身份证命中法院执行名单"""
        return self.__tdResult_spouse(item_id=2976216)

    def spouseRiskItem2976220(self):
        """spouseRiskItem2976220 申请人配偶的身份证命中信贷逾期名单"""
        return self.__tdResult_spouse(item_id=2976220)

    def spouseRiskItem2976224(self):
        """spouseRiskItem2976224 申请人配偶的身份证命中车辆租赁违约名单"""
        return self.__tdResult_spouse(item_id=2976224)

    def spouseRiskItem2976226(self):
        """spouseRiskItem2976226 申请人配偶的身份证命中法院结案名单"""
        return self.__tdResult_spouse(item_id=2976226)

    def spouseRiskItem2976254(self):
        """spouseRiskItem2976254 申请人配偶的手机号命中虚假号码库"""
        return self.__tdResult_spouse(item_id=2976254)

    def spouseRiskItem2976258(self):
        """spouseRiskItem2976258 申请人配偶的手机号命中诈骗骚扰库"""
        return self.__tdResult_spouse(item_id=2976258)

    def spouseRiskItem2976266(self):
        """spouseRiskItem2976266 申请人配偶的手机号命中信贷逾期名单"""
        return self.__tdResult_spouse(item_id=2976266)

    def spouseRiskItem2976268(self):
        """spouseRiskItem2976268 申请人配偶的手机号命中车辆租赁违约名单"""
        return self.__tdResult_spouse(item_id=2976268)

    def spouseRiskItem2976312(self):
        """spouseRiskItem2976312 申请人配偶的单位名称疑似中介关键词"""
        return self.__tdResult_spouse(item_id=2976312)

    def spouseRiskItem2976320(self):
        """spouseRiskItem2976320 申请人配偶的3个月内身份证关联多个申请信息"""
        return self.__tdResult_spouse(item_id=2976320)

    def spouseRiskItem2976322(self):
        """spouseRiskItem2976322 申请人配偶的3个月内申请信息关联多个身份证"""
        return self.__tdResult_spouse(item_id=2976322)

    def spouseRiskItem2976340(self):
        """spouseRiskItem2976340 申请人配偶的7天内设备或身份证或手机号申请次数过多"""
        return self.__tdResult_spouse(item_id=2976340)

    def spouseRiskItem2976354(self):
        """spouseRiskItem2976354 申请人配偶的7天内申请人在多个平台申请借款"""
        return self.__tdResult_spouse(item_id=2976354)

    def spouseRiskItem2976356(self):
        """spouseRiskItem2976356 申请人配偶的1个月内申请人在多个平台申请借款"""
        return self.__tdResult_spouse(item_id=2976356)

    def spouseRiskItem2976372(self):
        """spouseRiskItem2976372 申请人配偶的3个月内申请人在多个平台被放款_不包含本合作方"""
        return self.__tdResult_spouse(item_id=2976372)

    def spouseCredooScore(self):
        """spouseCredooScore 前海征信中申请人配偶的综合评分"""
        spouseIdNumber = self.info.result.get('data').get('spouseIdNumber')
        spousePhone =self.info.result.get('data').get('spousePhone')
        spouseName  =self.info.result.get('data').get('spouseName')
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='qhcs_msc8262_record',
                                            find={'cardId':spouseIdNumber,'phone':spousePhone,'realName':spouseName})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        last_one=result[0]
        if not last_one.get('qhcsMsc8262Info') or not last_one.get('qhcsMsc8262Info').get('credooScore'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return last_one.get('qhcsMsc8262Info').get('credooScore')

    def spouseLawRiskMsgNum(self):
        """spouseLawRiskMsgNum 汇法是否命中"""
        spouseIdNumber = self.info.result.get('data').get('spouseIdNumber')
        spousePhone =self.info.result.get('data').get('spousePhone')
        spouseName  =self.info.result.get('data').get('spouseName')
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='huifa_record',
                                            find={'cardId':spouseIdNumber,'phone':spousePhone,'realName':spouseName})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result[0].get('response').get('fxmsgnum')==0:
            return 0
        if not result[0].get('response') or not result[0].get('response').get('fxmsgnum'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return result[0].get('response').get('fxmsgnum')

    def __hf_result_spouse(self,style):
        spouseIdNumber = self.info.result.get('data').get('spouseIdNumber')
        spousePhone =self.info.result.get('data').get('spousePhone')
        spouseName  =self.info.result.get('data').get('spouseName')
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='huifa_record',
                                            find={'cardId':spouseIdNumber,'phone':spousePhone,'realName':spouseName})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get("response") or not result[0].get("response").get("fxcontent") or not result[0].get("response").get("fxcontent").get(style):
            return self.SET_DEFAULT_VALUE_INT_9999996
        status_list=[]
        if style=="zhixing":
            for zx in result[0].get("response").get("fxcontent").get(style):
                if zx.get("state") not in status_list:
                    if zx.get("state"):
                        status_list.append(zx.get("state"))
        if style=="caipan":
            for zx in result[0].get("response").get("fxcontent").get(style):
                if zx.get("casetopic") not in status_list and zx.get("pctype")==u"被告":
                    if zx.get("casetopic"):
                        status_list.append(zx.get("casetopic"))
        else:
            for zx in result[0].get("response").get("fxcontent").get(style):
                if zx.get("sx_jt") not in status_list:
                    if zx.get("sx_jt"):
                        status_list.append(zx.get("sx_jt"))
        status_list.sort()
        if not status_list:
            return self.SET_DEFAULT_VALUE_INT_9999996
        return ','.join(status_list)

    def spouseLawExecutionState(self):
        """spouseLawExecutionState 汇法[zhixing]案件状态"""
        return self.__hf_result_spouse(style='zhixing')

    def spouseLawCaseTopic(self):
        """spouseLawCaseTopic 汇法[caipan]涉案事由"""
        return self.__hf_result_spouse(style='caipan')

    def spouseLawDishonestDetail(self):
        """spouseLawDishonestDetail 汇法[shixin]具体情形"""
        return self.__hf_result_spouse(style='shixin')

    def __hf_month_money_spouse(self,style):
        spouseIdNumber = self.info.result.get('data').get('spouseIdNumber')
        spousePhone =self.info.result.get('data').get('spousePhone')
        spouseName  =self.info.result.get('data').get('spouseName')
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='huifa_record',
                                            find={'cardId':spouseIdNumber,'phone':spousePhone,'realName':spouseName})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get("response") or not result[0].get("response").get("fxcontent") or not result[0].get("response").get("fxcontent").get("zhixing"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        clear_status=[]
        sslong_time=[]
        for zx in result[0].get("response").get("fxcontent").get("zhixing"):
            clear_status.append(zx)
            sslong_time.append(datetime.datetime.strptime(zx.get("sslong"),"%Y-%m-%d"))
        if not clear_status or not sslong_time:
            return self.SET_DEFAULT_VALUE_INT_9999996
        if style=='month':
            for case in clear_status:
                if case.get("sslong") in str(max(sslong_time)):
                    return (self.__return_strfYmd_date(self.info.event_time_add8h).year-max(sslong_time).year)*12+self.__return_strfYmd_date(self.info.event_time_add8h).month-max(sslong_time).month
            return self.SET_DEFAULT_VALUE_FLOAT_9999996
        elif style=='money':
            for case in clear_status:
                if case.get("sslong") in str(max(sslong_time)):
                    return float(case.get("money"))
            return self.SET_DEFAULT_VALUE_FLOAT_9999996
        else:
            return

    def spouseLawExecutionTerm(self):
        """spouseLawExecutionTerm 汇法[zhixing]执行期限"""
        return self.__hf_month_money_spouse(style="month")

    def spouseLawExecutionMoney(self):
        """spouseLawExecutionMoney  汇法[zhixing]执行标的"""
        return self.__hf_month_money_spouse(style="money")

    def carDealerName(self):
        """carDealerName 返回车辆经销商（sp）的名称"""
        return self.info.result.get('data').get('dealerName')

    def carRoomAddressProvince(self):
        """carRoomAddress 取申请人的居住地址省份"""
        return self.info.result.get('data').get('homeProvince')

    def carRoomAddressCity(self):
        """carRoomAddressCity 取申请人的居住地址城市"""
        return self.info.result.get('data').get('homeCity')

    def carHouseAddressProvince(self):
        """carHouseAddressProvince 取申请人的户籍地址省份"""
        return self.info.result.get('data').get('familyProvince')

    def carHouseAddressCity(self):
        """carHouseAddressCity 取申请人的户籍地址城市"""
        return self.info.result.get('data').get('familyCity')

    def carWorkAddressProvince(self):
        """carWorkAddressProvince 取申请人的工作地址省份"""
        return self.info.result.get('data').get('workProvince')

    def carWorkAddressCity(self):
        """carWorkAddressCity 取申请人的工作地址城市"""
        return self.info.result.get('data').get('workCity')

    def keepAppointmentCreditScorely(self):
        """keepAppointmentCreditScorely 前海征信中履约能力这一项得分"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='qhcs_msc8262_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        last_one=result[0]
        if not last_one.get('qhcsMsc8262Info') or not last_one.get('qhcsMsc8262Info').get('creditScore'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return last_one.get('qhcsMsc8262Info').get('creditScore')

    def rejectCode(self):
        """rejectCode 外部数据-新网征信拒绝原因码"""
        return self.info.result.get('data').get('rejectCode')

    def pbocWhite(self):
        """pbocWhite 外部数据-新网银行征信"""
        return self.info.result.get('data').get('pbocWhite')

if __name__ == "__main__":
    serial_no = "1545203176523-DB2997476D4E7E4DD6ED544F868EB559"
    a = CarFactorAuto('T1', serial_no)
    print a.hfDishonestDetail()
    # print a.cdwAgentNameMatchBlacklist()