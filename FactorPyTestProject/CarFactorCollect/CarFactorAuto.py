#!/usr/bin/python
# -*- coding: UTF-8 -*-
from FrameRunner.FactorInit import CarFactorInit
from utils.threeDES import factor_encrypt_identity,factor_decrypt_identity
import datetime,json
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
        sub = int(self.info.event_time_add8h.strftime('%Y%m%d')) - int(self.info.cert_id[6:14])
        return int(str(sub)[:-4])

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
                                            find={'cardId':factor_encrypt_identity(self.info.cert_id),
                                                  'phone':factor_encrypt_identity(self.info.phone),
                                                  'cardNo':factor_encrypt_identity(self.info.result.get('data').get('bankcardNo')),
                                                  'realName':factor_encrypt_identity(self.info.user_name)})
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
        return results[0].get('final_score')

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
                                            find={'cardId':factor_encrypt_identity(self.info.cert_id),
                                                  'phone':factor_encrypt_identity(self.info.phone),
                                                  'realName':factor_encrypt_identity(self.info.user_name)})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result[0].get('result')=='-1':
            return self.SET_DEFAULT_VALUE_INT_9999999
        content=json.loads(factor_decrypt_identity(result[0].get('content')))
        if not content:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not content.get('data').get('RSL'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for i in content.get('data').get('RSL'):
            if i.get('IFT')=='A3':
                if not i.get('RS').get('code'):
                    return self.SET_DEFAULT_VALUE_INT_9999996
                return i.get('RS').get('code')
        return self.SET_DEFAULT_VALUE_INT_9999999

    def geoPhoneSelfMatch(self):
        """geoPhoneSelfMatch 手机为本人实名认证 String"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='geo_record',
                                            find={'cardId':factor_encrypt_identity(self.info.cert_id),
                                                  'phone':factor_encrypt_identity(self.info.phone),
                                                  'realName':factor_encrypt_identity(self.info.user_name)})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result[0].get('result')=='-1':
            return self.SET_DEFAULT_VALUE_INT_9999999
        content=json.loads(factor_decrypt_identity(result[0].get('content')))
        if not content:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not content.get('data').get('RSL'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for i in content.get('data').get('RSL'):
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
                                            find={'cardId':factor_encrypt_identity(self.info.cert_id),
                                                  'phone':factor_encrypt_identity(self.info.phone),
                                                  'realName':factor_encrypt_identity(self.info.user_name)})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if result[0].get('result')=='-1':
            return self.SET_DEFAULT_VALUE_INT_9999999
        content=json.loads(factor_decrypt_identity(result[0].get('content')))
        if not content:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not content.get('data').get('RSL'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for i in content.get('data').get('RSL'):
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

        if self.info.result.get('data').get('agentName')=='' or not  self.info.result.get('data').get('agentName'):
            return self.SET_DEFAULT_VALUE_INT_9999999
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
        if not self.info.result.get('data').get('czcbOverdueRiskResult'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('czcbOverdueRiskResult')

    def cdwCzcbRiskNote(self):
        """cdwCzcbRiskNote 稠银征信返回的备注信息"""
        if not self.info.result.get('data').get('czcbRiskNote'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('czcbRiskNote'))

    def cdwOutOfAuthorizedDistrict(self):
        """cdwOutOfAuthorizedDistrict 是否超出授权区域范围"""
        if not self.info.result.get('data').get('outOfAuthorizedDistrict'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(self.info.result.get('data').get('outOfAuthorizedDistrict'))

    def cdwIdCardAppearCount(self):
        """cdwIdCardAppearCount 车贷系统的身份证号出现次数"""
        if not self.info.result.get('data').get('idCardAppearCount'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(self.info.result.get('data').get('idCardAppearCount'))

    def cdwIdCardExpired(self):
        """cdwIdCardExpired 身份证号是否超出有效期"""
        if not self.info.result.get('data').get('idCardExpired'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(self.info.result.get('data').get('idCardExpired'))

    def cdwIsLcv(self):
        """cdwIsLcv 是否为轻型商用车"""
        if not self.info.result.get('data').get('isLcv'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(self.info.result.get('data').get('isLcv'))

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
        return int(self.info.result.get('data').get('noRelationContactCnt'))

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
        results = self.mongo.query_by_user_id(db='galaxy', collection="td_record",
                                            find={"realName": factor_encrypt_identity(self.info.user_name),"cardId":factor_encrypt_identity(self.info.cert_id),"phone":factor_encrypt_identity(self.info.phone)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        tdReportResponse=json.loads(factor_decrypt_identity(results[0].get('content')))
        if not tdReportResponse:
            return self.SET_DEFAULT_VALUE_INT_9999996
        for row in tdReportResponse.get('risk_itaEr')2
            il roW.7aw('ktemWkd�i==sr,atem_id):
     ((  ! 0    retu2l su6SED[DEFAULT_VALU_IN1�  ! (! pmturn self.SET_DCFAULT_V�LUe_IN�_!
  4 den0risyI�u�23w.222({elf):
���    "&b*�mckItei2966023	�+���諁吽中高H��镩Ņ�滨���单""
"    $  �dtUr. wE�f.[tde;}lt��tem_ad}2976620)
, 0 Daf�rIskI4mo2976610(sehb	:
( "$   `2*2rHskKtem0�72$阋仝쯁����地������高������������中��0e�#"#"`! $   rgv�rj 3�lf.__tdR-sult(Itg�_)��2976r10) �( d�n r)ckHTem:876264(RelV):` " " p"" RicKItEm297>42 手�*受ㅭ츍��(����共�呍单"�#  " !  "zedeRl8�elc.__T$Vusult(i4Em_�f]29w62749

   "de$ �is{I4dm�=?62�f(sehf);
1      $#�"risihta��625 䁋�ܸ�#㕽��通d��小号���c""J �� �" (2e$}rn s�,G*__u`Res�ntitee]!`=z�7�4
*!(0 def 2iskItem2=7386(self!: 	�  # (B""zirkHue-2936187 �,�䘀́��3�����份证ͱ�帥泔院������吏Ꮥ=h��亰b"" � " $  rmpurn se�f�_tdrGsqlt(ite�OiL�0976s8�9

  !8d�f rasKYtem256�89,selF->
    !` """"ris�I|amr9'63(��,���ꅔ�3���身亝���命䲭䳕ə�≧�+名孕@""
`      8ReuWrn {dlv.^_tdBesul|(itam]Id=2952388)

 " bef ri�kIt�e6)wv392(s5lb	:  (     ""2biskItdm:9769 第d�����ﳻ຺��廽���命���׊�祪阚缍吉单"#"
        retuZn sel&.__tdVesuhu(kuee_if<3974392)

  ! Deo riSkItem:=76396,3e|f):  ` $ ( ""#2i�nite-396386!���一联���仺身�����屽中���贷���朞� �e���""* !  "   vet}sn�se�f.O_tdS�ctlu(h4E-_kd?2�76396)

 $  def �isk�tei2�76�8 yeld)
p`  "  0$""r�skItem29�6�9( Ǭ�丂聖䳻侪手✲厷��中���起���期�单"""�       return sel&>__t`Resuld(itd-_id=29'�399i

    @et rirk�|em"17>$42self	:
        2""�IskIteM2)64 �0礬������系为扉G��号噼中�:���号硁爖����小䏷��""

 ! p  @rMttrn �e,f.]_xdZe3un4(itEm]ad<2)74402�

   $dev clwC~cb�R/#Requ�T(Self-:
      ("6"c�wCzcbPbocRD;ult 综合樀�>银衍返�����免츨�;�恬做���个泼嘈滓(��"""
        i� s5l&.i.Fo�zeSult.get('daty').ce4('�zcbWeNEralyskR%sul4') r se-v.	~f_.resultlget('D��`').get('cjkbDt�eRys�Zesult') or self.EnFo.verultfgeT(%d�w1'),'Et
'#Zc`Over�ueRk�iSe�ult')(/s!jnt(self,inm.vtrumt�gep,uati')/wEt�'czkfGnE2AlScgze'		$< 0&or floet(sen&.ibdovesU�d�e|-'dada&!.get(#cZsb6g�duES#g3a')( $8 0>
   �   $ $  reuurn "N"
``"$ " �i&"3elf�hnfm.Fe��d"fe�('dqt!/)*eEd-'#zc"e�lraLPi2kRe{Wdv'- /r"3elg.infn.rerulu.Geuh%dat�')*get(&czcfDgbtBiSkpsultg) Or ceLginfk.besult/w�u('fAta').Get('c�c`Kv%sdeeZiskReSqlv'	:
 "   $  (!  re$qb. D"
 0�0�   if s�lg.	nv/.result.wetgdat`').g�t('czcbGenerc�RisKRgsel|'h anl�se4f.k~fore{udt$wDt*'dat�'(.f�th'bxCcDebtR9wbRgsuld�)�a~d se(~.i�f/6r%qu|d.'et('Tada'(*cEt,'g:c`oveZeueZi�k�esunt'	z
  (      $  Rej}rn ""
( 0    (ce|uvn "G"
�   d%f #dgV�hache	fLumberApreasSOuj6 sel�-:
  "    " "cdw^ehiclfI4NemfqrAp�%��CounT(���?�7变��抄歡䕰"""
   &  ( sul}"SELEC CO]NT(*) as cnt NRMM lg]aPply]AAc LEfT JOMn"|b_q`p,y_,a),$! NN aaqbh = cLasqbx�SHeSE ACJH!=`�%s$$AFD dArUJUEM` I^ ('03%, '061/l '�', &08&, #89'<�'�0/=relf.info.rgsux|.ge78!dA�a'	<e(t"v%xisleIeNu�beR )
  &     r%s�|4*= sedf.myqql�ueryone�jy|st�meq_ie*db='zuYC�e// spl=Sal+ (  *   ""new_sql"{ele't�counu*
h �s0c~t4nrom eAppl{ igft jo)n��_kaP on e�ppl{,�e!� e_cab.ap�ly_yd �thgrg s�r_rin!=0'%3' andb#�zrent]jo$e`$in 8y� 56,109,11�12>s )�"�elf/iffo.result.get(/$aua'�.get(�Vei%cldOuebar")*   (($  nEwOsqh"SENMAD KOUNT(.) DRKM�e_gqp�i a LEB JOIL%a_car eC1$MN a&id�=!%c!,eppbY_id WHZA eg1&cqs]wiN =1'%� An@ an�pp|y_st!tus!HN  %< v. - x-"%�elf.infk.seswlt.get(�fata%).iel("v)HicleId]mB!R#)!  �"   ne7�RQselt  self.my�ql.qeeP�Onm_jy_custo��z|il*db='a5to_dOin_entsy_tert'( sql=oEw]sql)
" �    0setupn rE;dt.g�t "klt`)0+ new_r%�ul4,eet("�np")
  0daf gbeajChanne�i{elf9Z (($�   """g2eEjCh!.nel!���`��ǻ�色���道�""*   �  0`if no� sdl�.invo.resu|t.�mt('tbta').geT('gp�efC
annul'k kr s1tf.Info.reswht.gnp(data'	.g�$('greenChanne,')=':   0    "  rk4a2n ye�f.SET[DEF@ULT_VALUE_IN�_9)999;�    $ ` rex5rn {fp)redf.info.rese,0get('dcta')Oet(#gre%nChanngl$)+

8  deo pbokReason(S�lj)*
"       ""tbocecron ���ɂ�徃�!�;����h��m����拒绝���原�(昞组""b
(  $   ig!fot�s%m"�ifn.rewuhd.cat('data'	>ge|('p�oJea3on'+
   �    ! ! sEpurn�welf.SEP_�dGEUlPVALUE_I^P_9999��( "  $ (rt4url s%ln*info.besudt>get(gdat!&).gdt('�bncRd!so&g)

   #24!92212
 `  d%d"applisantstk5rd{pm(%ld-
 $ `    "2"applicanDSpouseyqe ǔ��ϯ亻��没月配偶"""�     "  ig ogt 3eLf�inng/r�ult.gdt('eaTa').oeT(&haswpoeqm")*
 $          setuSn selvNSETODEF	GD_VADUE_IT_911195�
 %  `  retUrj �nt�a,filbk.sesu|4.oet('data'-.g%t("@es�pous%�))
    leb$Spou3eFe�Th�n�Le.`8sdlf)*
      ("""�touseGeoThoneLkn  集���0据,配呵���朊孒属�԰"" 
 (    0 stfus�M$Nt-b�r$4 rtlf.)�gojs!sult.dt `�ta?	�ged('spkuseI��wlBEr�)`` ` `  spousgph�~e =selbilgO,zEstlt.we4('daxa&	get*'{ro=s�Phole'(
   0� *0cpoureN!lu 0=seIf.h*�k.r%sqmp>get�'&at`	.get('spo�suNa}e')
"     "rm�uh\=s'|f.molg.�Uery_`y[tseq_id� db)gamcxy',
�  " !      `   $       �!(         (" �20 $c/llg�tion?'feo_s��mfd?l
  
   a    `!  !  !�    `  "�     (     0 $�fhnd={/cabdId:st~%seIdNpmber$'p(one�*srotsmP�Onq,#reulLam%':wQmwseNam`|)
     0  )g(no��re{ult:  p  �  0 ` r%turv 3tl'.WT�F�FauLT_T��U�_A^P_18=+99	
      9if n�t r!sulK0](gmt("R%qpoo�e=0or!nou pg3uLq[].�et('{espon�e&i.det�5`atag),or nt!Result0U&ge4(&f�SPnose%+'gdt('�cda&)�geu /IRPNUM'):
0( $"  "    sat4rn {amf.QET_DEBAULDVF]E]LV_=19899
$   `   Bet}Rj(rasUlt[0.g'4('reSpm.se').e%t('daxa').get.'XSQLUO').we)qzkvInce"sel�nSeT_DEF�ULT_VC��E[iNT_)99�9Y6)
  $din(_OGeN�x�neBkrt(sul,IdNulbdrphon�)name)geoTy`e)  (     jesult=enf.i/nfk.qu2yby[usar_ad, db=galqx}m
   �  `(  $      "&0    $!  ! $ !    0   !)so,lu�t�oN='g�o_reikr�,
�  `     !$ ( �  (!�(� 0)"`" `  $   "      fyNd={7cqRdYd7{I$Lu�"es)&phene':`hone,'pEalN!me':naee}-     $!!)F no| z%swl\   0 ) 0   2�tuR~ {enf.SAWODAFAUDP_A\UE_	NT?99�9y99  (0`   if not rn�ulP[p].Gd�(3res`onsd") kr not result[�].fgt('pesponse'-.geph'davd'+ or net rdsultZ4].gEt resqon3eg)g�t('r`laf).get(#RRLgI:
 <         0ret5rn(wEl&*GP��ENAEL�_VALTE_MND_y;9919
 �  ` ( ff2 Code"i: `sultS0].g`t*'sespgjse#).gev(7daT`'!,gdt('sSL6):
 �(  $ ! � `if(C/ee>g�|(#xFV -==gegT�pe2    2`� $    �  rETur*"cod%*gdt"RS*).get("cote")
 $   �0 sepur� self.SEU��EFAULT_WAOUE[INT_)99=99=

  " def s�ouseGeohonaMnturatIN8Celfm:
      $  "3p�useGemX�,eA�tDuratIon 申��人配�6㚄獋机在g����?#"#
�  ! 0 dspo�qeXdNumbur = self.anfogSesulU.wet 'data').wet(%{pous%I$NUmber')
 !      sPotsePhGne�=cmLf.i~`o.rusuh�.get!'e ta').ge`(#sPOusePhole	
 �  "   spouseOaiG  =celg.hnfove[�l<.ges('�ata').get('spguSUN�me!
 $"     xetusn qelf/S_GmoRhgnmCoct*sqoureIdNulber,0sp�usePhone,4spkuseNe�e,geoTQpe='A#%
 0  def gu�ThonECnsd(Culf):
     ! ""�`eegPloneCoqt 集奥敐�ͮ��畳请�的✺⯕���輧单""#
0  ` !' IdNUmber se�f>anf.Cert_md ` " !  phone  =sAlf/hnbo.tiile!   "0 (namd  (5self$mnnk.urer_naoE
! (0    retwrj iulF.__GeoPh/�eCostIdNuMfqr<p`one$nam�,eekPYpe1'B5�)

   "def wpoDsor�eo@hmneC/st(sm|f)
 !  `( !2"crponcopGE/HjoneSost ���塥䇰��.中曅���为绂晋漺��i��贆噕"�"
        �ua�aotk2HdNuobd2�ce,v.ingo/Resu�t.gqt('dkt ')&ggd('guarantKrAdNumber')
""!  $ 0ctar!ntgrhone=qilg.yld/.result*ged('fate'/*dt*#guapalTOrPH�E'!   (0($ gu!raltOpName �sm,f.i�fϮresuhp.get 'data')ge|('g�aranuortmE'+
  `     return�self__GeohojECos�(eta2`ftorAdNueber,guar�n|bP /oa,uqarcnumbFa�eoeOTy`e='B1)

 �  l%� spou~eGwoPhonaCoqt�self->
 ! 0 �  "#�sp-}seegPhon�SgsU 雇e��数挮��遅ǁ�人g��f	�$��话�9�4�e��j""
        srous$It\em"e2 0send-nfc.result.Gmd gdat`G).gEt(#c�ouCeIfNumber')*a"     spNuseP(one <self>!nfm.result.get(gdata'�.�mt('ppousePhkn�%)
   ` 0  srouseJame` =selfnijfo.rt3a,t.git(/de4ag)&ogv,#rpwtsena)�'i
`"  (   r�p�pj selb._GEgPx�ndortspOuseIdNwebep,sp'%SePhone,spou3ENamm,%doDYqe='B ')

  `�leD spo5qeGeohmne%lfMat!h8sElf):J"   !  �""SpeureGeoPhkneSahgMauch 申讷�:配偶��扉眘右F��尦�!�镍偶`����=讁实Ő�验h����致"*        sp/uq�Id^u"er� sdlg.infM.ffs5`t,get('�atd'),gAV�'spguseIdNwebev'-
  ���   sp��3uPhne-relf.info.resu|y.geqh'dade&->-`t(';pouq�P`zne7)   "  qpous%Name 0=self,iNno.`%sult.g�t�/Data').get('spoUceam�'( !  *  `0ettrn se|F.__eoP(oNeAost,wpoes%YdN�m�er�spouseRhonm,rPouse\�ma�Guo�ype='B7!(
 "  l�&$spo~smvGenPxoneRedgMat�h(3%lf)F   �   !*`"gpmnsorGeoPj�neZenf]a5ch 担仝人瞄����޻珧Ɯ�吤喌揅余人人��������媚萍�诡���쇶2" "$    ( guaranuKsIdNu�ba2<semf/ilgo.res5Lt.'et(dCta' ./e|)'gu!rafd�RIeumber')J !  %   guqrantosPinne}se|�.info.seult.Ge0('v�T"')�ge4*'guaran|Obhone'+�  "$ �  guarcnpgrNamE�=se�F.i�vo.result'eu(&dauag)ngmt(�guarantrNleg')�  % (   vetuRn!cglF.__CeoPhojeGjst)g}qr�ftorId^tmbeb(�uarq�torP�one$gq!rentorName(oeoTYpe='B7%	

    he� sponsorType(semf):
   � "  **byqoncopTy�e 昧�&添�J����v��俽��:"""     " ()d8nkt`re�f.Infn.result/gEth�data').get<%)isqcselPor'):
   �  00  ! retubn Self&SMT_DGAULVADU�_IBT_9919999
    ,  HZeturn aNt(cmlf.ynf.susult.g�p('da}m').wet('hacGuav!ntmr')+
  !`�ef sponsobAgE(s�,f)2� (   &`#*"sponsosCge �˅保����并龄!*2
 0`   0$kf ngt`s%lf.il�o.rgsqdd.Geu('data').gat('gui��ntor�DN�ebe�'+:
*(      "$ �rmturn0Self.SETDNAULT_ALUEIJT[9)999)
"       GuqranvjrIdFumbgr`= Se|f.ingo/rusuot.Get(deti%-.Get('gUaranTmRHdNuM"}r')
 $!     sT�( int)3elf.knfo.FreSte_tymU&strf4iod('%I'}�d')�" ijd(gua�an4gSIdNumbez[6z14L)J !"   "`rg`trN i�t(cdz(qub	[��4]-

d$! def$cc�Cla��(Semf)8      0� *"barWlass`輔�ߞ��쯳Ẻ准骾��型"&"
 ` !"0  result�sIln.EnjgO.�uesy_b}u3�v_if(@dB='eah�xy$-` (   $  ` $      ! `! � !   `  00!0* b   collectioo=pi_rgcpD',
  !0    #`   "  � 0  @`$     �`   $!$      !gind�{'careMd#:ekTov_enbriptideftidq(selfhi.fo/ceruWid9,'phn�ebActKb}enaryqV_identidy(sel&*il&oNt`gna),'��alOa}e#8fa�vnr_eO#rypt_i`mopIvy(salf.yffo5wer]name9})
     "!1if notpesU�2
  1     ( "0retu�n!s�lv.QETDFA]\T_VnU�YIMT_999999    "   if �ot resu�tS0].gev('0yRecpo�se') Or nnTrUsul~_0].oet9%piQespnnse')gEw(&vETuslVa�}g') ]j`       �   or bot be3ulT[0]nget('py@e3qonse/).'Et('pAPUrnVqhu�').eet(�cisRgp�rt'�:
0    & � ` 2rmts.$palb.S�T_DEFAULTVcJUEINT191	939  `$    capClcss7zdsu}t[0].gd48'tySusponse').gUt #rE4uvnVa\ue').get('cisRepo~t'+Z0].oet 'dpiVerL)ce.qeAnvg7)>'et!%aqpBlacs/,self,CeT_DeFAU\DM@UE_KNT_9999))6)! �   " if cazKn@ss==wElf.SDT_DTQLTFALUG_IJT_99y;996 or not cabCm`qs:(    �2`    vetqcl s�lF.RET�DDOqM�_ALUm_IN�99+;96
     $  if 'A#(k. carSlass3
  !       !!p%tubN"7
   ( !  hf 'A2& ij ca�Clasw�((!   $  0�etuzn 4
        if B1& if cyrclq�S:
 $�   !!    retero 4
   &  $(ig /B2�in ca2Alasa:
       ( b`$r'Ttb> s
 �((    if$'A1' hn carCl`ss:
(    !   4  revurn 7 0��!  if '�'@in carAlass:
 �        % return 2
 0(     if"fC�' in carClcsw:
  ( $      !repqrn 3*  (  �  r��ern 4
   dEf dravyngD�bgjkeExp�RyTite(self)8
! � " � &""@riincLic`*cm�xpyr9Date ࿔回攳请为鱾�7�/�的��䁊��#""
    0! �resumt={edf.mgnog(q}lry^byZuseR_y$	`db?''alary'<
0      (0        �$`      �  �`� "  $      $Colngcpann=P�_Re�orf',
       ((        � !   �"   ` 2  ! !   ` 0 !fint-{�c@rdId':factope~k2yp|Sydg�vip}lcelf.iNf/.cezt_ad),'ph�ne':ficTnrenc`ypxidentityhself.info$phon),'realNaig&:bac�or_%ncrypT_ilentity(celg
ingo.usdb_name)=	
!�      �f not bu�u,tz
  (0 �   !002eturn s�lf.QE�[DEFAW\T_WALUE^INT_9999919
      p mf jot02esuh0Z8].get('�yRuspoose%) Nr&no|�zayu�tN0]eet('pyReS0once#).get�'TeturnV!due')0\
" ""        or not$re3qlu0_.get)'syRestonse/1.get)&rat�rnVamug')ge4 %cisReport'):
       �   $pettsl �edb.S�TlEFAULT_VANQE_INT_99999=0       UxpkryE�pe=rmsult_0_.oet('p}resp'nceg).geT)'seturnVaLud'	.ee4(/cisRepnpt')[2].get(%`riTerLhcense�.fo').'et('EppiryD-ue'<sanf.SETE�FA�LTURALuEOIN_999-96)
       0i&$exxiry@ave�=self.SET_DeFAU\DWVALUEW�NT^99999)6*
 2�        8ret]bo sehf.[ET_DEFAUNT_VQLTEILT[y99999&
 �   "  if`axp)ry!tg=9%':
    ` 0,    ru�ern 3Ulf.SET_dEFAUL\_VALUE^IN_9=1)9)6
`  �  ` r%turn det�t)me.datdtImE.sT2qtime(ex`i2y�ate, "%{-%}�'d"�

   $dad�dv�vingiaenceStaUts-S%l�):
`    ! b# dbhvIngLicgnce�`atus"h���ީ���菁状����&2
`  0    rmqult�edf.mmneo.yueRy_b;_usez_i%) d`}'gslax�'
     �  0     h       ` 0�           `  (0collegt�on=6�y_r$copd',
   `   ` %( ( �   !   "  `    `     `     � d)nd=k'cizdYd&:bQbtmr_enirypt_kdgntity(qdlf/info.fert_id-,'pxmnu':fca|orencrypt_ifelnhTy{elv,in&o*pHong!'rAlNi�e'fmcto�_encr]qt_Hdentity(self.in&/.usub_ncme)})
�` `   �& nod result:
 0       *0zeuur� s�,g,[DT[DF�Q\P_VCL^ANT_1�9999y
 ((  �$@+c`jot0r5�u,ts4]*gup('�+Re3phnse/) or�N�t besult[0U.�ev('pzRespoNku&).get 7�epub~Vahte%) \0   � ! $  $+r nMX(zesu|t[�U&wed('pyRec�onsu5!.gUt('retwpnvalum'9.g�|�'cisRgTord-z*`    `     ��uero,{elf.SET_EEFE�M�^VALUEOINV_999991y
   �!(�status=SEsulp[0].Get('pyVmqzol{�''get(7re$ur,^!lue')>Ggp('cisRePo:t')[ U/oet('u�iwebLiceoSeI.').get(�st!Tu�'.3e`f.SUTODEFAULT_RALUE_INT_99�99=6)

  !     i.�statt3=�self.ET[DEDAUDT^�AlUE[INT_9y99;96�ob`nmt rtatus:
 (  �  `  ruhurn self.QET[DMFEQLT_\ALU�iL�_9)9y)
 (0 (`  staUusList=[]  ` 8"  ib u'���庰& `n"statE3;J "!   2   " qtatuyNist>apxdjl(&1'+
  "�    i& u'ɶ�倆%(�� sTa|wS:
(h  �`$ 0(  statq�Li4.qqpen$'2'-*     "  if u'h��Ň�7 hj statu#:
`$    `��2  sta�5gLisT.i�ped('3')
%   !   iF t'昀f��w 9.({tatus:
b&     � 2 rt`|u{lmsV,appene(#4g)      "!iv u'撤ɔ�'0i
 ctap9s:      0(    statusliw|.AQp�ndh�='!
  % �  �Kf"}&�� ' ijst!twS:
0        $  statusLi{t,c�xg>d'6')
      (!i� u#注픀'$in stadus:
    $ !(  ( 3tat�sL`wt.�qtdnD�')8�"      �f u'���法未夕㐆'$in!Stetur2
 4 " "!"0   3tat1sNis��axpent' ')
$       mf0u'���f�使礈' in st`tUs9
 0       $ �SpapuS\ist&atp�f$(%9')
  $  ` $if u/专摄���Ŧ�g��' in statvs:J     $ 8! % sta|}sLiwt.gp0enfh##�'-*��     �i�5'���䟥' )N rtatt�8
 "!4   "   sUetusMi�t&append('11')� & p    if U'锁�' k~1�vasu3:
�   ( $ ! ` �tetus�ist�a`pe�`(925)�       !id W�i���8�昪捪证' i. cpaTq3;Z (    � "   ctatusL9sT.appeld($57'=
 �      if"5'嫾期��x��� in�s4a�uS:   !` h    (sTa4uwList,aqPen�,&14'+
 "@    !if0u'廖��������' mn �|auuC:
   ` ( " �a �dqtushqt/app�nl�'15%)
      ""If u"ɀ����未䵓惤'�In stadts8
 (� 0`    $(st!tuwLasT*apqend '10&-
 �$ $  mg u'Ʉ�搟未审验� i� statu�*J @    � "   s4!�}sist.ap`dnf('377)
   6 ` (if u��䫆/iN status:
  "         gdkv2sLkst.AtP%nf'8�9"     " if`u'�"e��' i~ rt�Dt98
   �   "   sdituSNisp*aprend('%��)�  �     i� lgt$suaDucJisd:)!  2    0$`return celf.STTGDMBAUlT]V��UEKINt_0(   �   vetUr�!7;7*jkin(3tatusHist)
 0  dg� bqouseFiNA|ScOZf8Selg)z
 !` !   """Spous�FAzalS�ore 申h��亪��e��的����>分"""
0    !  ypouseI$Nuober }(se\f/il.o.veqqlt.'ut 'diTe)ge�)ipouqeIdNymr�r+
    %   ~pmu3E�ho�e }sel".inno.rew�l�.glt('ti|y')/Cd| 'sp.uSePh/.e�)
        sPouSenama  -seld�i:foreRuxu.geq('atq'),f�t)'qp/useName')
  �(!  "rEsulTs = se,f.moNgk.5ueryWBy]user�hd f=7walAxy $gol�esi.n=�d_vecOrd`,fin`="pealLeie#z`f!cTor_gjcr8pt_iden�ivy rpo5cLane)<"Car`A`":fuc�ms_dn��9py_kde�tity(CrusdId^uerer)-&phkng :�i�por^d�cRyPt_{deN|ipy({p�useXhon�)=)
  ! "" md Fw� Resulds:
 ( � �      se5uv0salb.CET_DEV�W�UWVCLw_�N_99)9�9
(  $(|� if zd�5l|s[].get8%VaSult%)=?'%3':
$       $   betqrn!welf>SEL/DEBaU�TYVALUe^INT999Y99)
 ```  0�petu2n(REst4s[8].get('f)~AL_sco2e'-
   �d�f __tDReqelt_{ekure({e}�itel^id(;
    0 � ypeureIdNumc�z ��glf*ynfO.r�su�t&eet('eqta'+.ggt(s0�useMlNumveb�)
      ` S`kuS}phOnd 8sel$.ifgo2dsulu/get %dpte&)nge5('qpouwaH�d"!      ! {poqseJame  =sglf.info.ze3ultnget 'dat�%).ge4('wpusenQee')` #    drE�umpp < semf.-kngo.query`y_usmr[id(dc,'galux{'l coll�ctiOn<&tdR%gobd#,di.ds"pealNa-e"*!fa!potuocz{pt\identyd9(spouseNa}u	$"gardYd*>fag��_mncry d_idebt)uy�spu�eMdNu}bdr),"�xond":b�gtorOancrypv]identity sq/UseDho.e)}+
"  � $  if joT raqults"
   �    0 `retqrn$3e,F.Sm�_DMF�ULT_WCLUE_IFT898q91
    1 $ udR%0w�tRe�tonse = jcon.lkCds(f!cvkrd5Kviht_ydgndiuyhres}ltsQ].get(%ckn4an4'/))�  `�    �f nnt tdRdqorvBespo�se:
  $ (  !    retubn remn.CET_LEFAT_VALU[IFT^99�1996  �     For Zw in tdepOrpRdcpknsq.Gut(/ziskWitemsG):C  " !  "$  0if r�7.g%t(7it�mOad') - �t2�id%mhdiz `  " $"    � @ 2eturj sEnf.VET_FEF@ULTWVQLU_INT_0
       �rep4s."Self.SET_DEFEU�T_VA�UE_IVQ_0�
  ``dcf$stgeCeRisJIWem297��1p(s�`f�2
       "*"spouseRiskI�uL2?6r 由诧d������皔貫���证�����垺�	������风���ĸ2���Ĩ��0匸 ""
   �   Vevus,!seld.O_udReSelt_spousl(item_yd=297&010)
!   def stousMPaskA��m2976222(self):
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
        if not self.info.result.get('data').get('dealerName'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('dealerName')

    def carRoomAddressProvince(self):
        """carRoomAddress 取申请人的居住地址省份"""
        if not self.info.result.get('data').get('homeProvince'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('homeProvince'))

    def carRoomAddressCity(self):
        """carRoomAddressCity 取申请人的居住地址城市"""
        if not self.info.result.get('data').get('homeCity'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('homeCity'))

    def carHouseAddressProvince(self):
        """carHouseAddressProvince 取申请人的户籍地址省份"""
        if not self.info.result.get('data').get('familyProvince'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('familyProvince'))

    def carHouseAddressCity(self):
        """carHouseAddressCity 取申请人的户籍地址城市"""
        if not self.info.result.get('data').get('familyCity'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('familyCity'))

    def carWorkAddressProvince(self):
        """carWorkAddressProvince 取申请人的工作地址省份"""
        if not self.info.result.get('data').get('workProvince'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('workProvince'))

    def carWorkAddressCity(self):
        """carWorkAddressCity 取申请人的工作地址城市"""
        if not self.info.result.get('data').get('workCity'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('workCity'))

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
        if not self.info.result.get('data').get('rejectCode'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('rejectCode')

    def pbocWhite(self):
        """pbocWhite 外部数据-新网银行征信"""
        if not self.info.result.get('data').get('pbocWhite'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(self.info.result.get('data').get('pbocWhite'))

    def lastAuditResult(self):
        """lastAuditResult 车贷系统-最近一次审核结果"""
        return self.info.result.get('data').get("lastAuditResult",self.SET_DEFAULT_VALUE_INT_9999999)

    def topFourPhone(self):
        """topFourPhone 申请人手机号前4位"""
        return self.info.phone[:4]

    def spouseTopFourPhone(self):
        """spouseTopFourPhone 配偶手机号前4位"""
        if not self.info.result.get("data").get('spousePhone'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get("data").get('spousePhone')[:4]

    def spouseGeoCurStatus(self):
        """spouseGeoCurStatus 集奥-申请人配偶-手机号当前状态"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='geo_record',
                                            find={'cardId':self.info.result.get('data').get('spouseIdNumber'),'phone':self.info.result.get('data').get('spousePhone'),'realName':self.info.result.get('data').get('spouseName')})
        if not result or not result[0].get('response') or not result[0].get('response').get('data') or not result[0].get('response').get('data').get('RSL'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        for i in result[0].get('response').get('data').get('RSL'):
            if i.get('IFT')=='A4':
                if not i.get('RS').get('code'):
                    return self.SET_DEFAULT_VALUE_INT_9999996
                return i.get('RS').get('code')
        return self.SET_DEFAULT_VALUE_INT_9999999

    def gpsPrice(self):
        """gpsPrice 车贷系统-Gps价格"""
        return int(self.info.result.get('data').get("gpsPrice",self.SET_DEFAULT_VALUE_INT_9999999))

    def carPrice(self):
        """carPrice 车贷系统-车款"""
        return int(self.info.result.get('data').get("carPrice",self.SET_DEFAULT_VALUE_INT_9999999))

    def carInsurance(self):
        """carInsurance 车贷系统-保险"""
        return int(self.info.result.get('data').get("carInsurance",self.SET_DEFAULT_VALUE_INT_9999999))

    def carPurchaseTax(self):
        """carPurchaseTax 车贷系统-购置税"""
        return int(self.info.result.get('data').get("carPurchaseTax",self.SET_DEFAULT_VALUE_INT_9999999))

    def applicantNation(self):
        """applicantNation 车贷系统-民族"""
        return factor_encrypt_identity(self.info.result.get('data').get("applicantNation",self.SET_DEFAULT_VALUE_INT_9999999))

    def carProductType(self):
        """carProductType 直接判断申请件是否允许自动审批通过"""
        return int(self.info.result.get('data').get("carProductType",self.SET_DEFAULT_VALUE_INT_9999999))

    def carRandom(self):
        """carRandom 根据客户的身份证号做随机数，如果客户购买多台车，返回同一个随机数"""
        return hash(str(self.info.cert_id))%2+1

    def carLoanAmount(self):
        """carLoanAmount 放款金额"""
        return int(self.info.result.get('data').get("cdwMakeLoanAmount",self.SET_DEFAULT_VALUE_INT_9999999))

    def carZoneCode(self):
        """carZoneCode 大区代码"""
        code=self.info.result.get('data').get("carZoneCode")
        if not code:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if code=="内蒙古区" or code=="北京市" or code=="天津市" or code=="山西省" or code=="河北省":
            return 1
        if code=="吉林省" or code=="辽宁省" or code=="黑龙江省":
            return 2
        if code=="上海市" or code=="安徽省" or code=="山东省" or code=="江苏省" or code=="浙江省":
            return 3
        if code=="广东省" or code=="广西省" or code=="海南省" or code=="福建省":
            return 4
        if code=="江西省" or code=="河南省" or code=="湖北省" or code=="湖南省":
            return 5
        if code=="云南省" or code=="四川省" or code=="贵州省" or code=="重庆市" or code=="西藏区":
            return 6
        if code=="宁夏区" or code=="新疆区" or code=="甘肃省" or code=="陕西省" or code=="青海省":
            return 7
        if code=="香港特区" or code=="澳门特区":
            return 8
        return self.SET_DEFAULT_VALUE_INT_9999999

    def cdwPreRiskLevel(self):
        """cdwPreRiskLevel 预审等级"""
        return self.info.result.get('data').get("precallRisklevel", self.SET_DEFAULT_VALUE_INT_9999999)


if __name__ == "__main__":
    serial_no = "1566180648828-A42A7451C0F093DBDAEE5F53F65BFBAB"
    a = CarFactorAuto('T1', serial_no)
    print (a.geoPhoneSelfMatch())