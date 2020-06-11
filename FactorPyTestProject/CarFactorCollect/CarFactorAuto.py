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
        """cdwLoanProduct è½¦è´·ç‹ä¸­çš„è´·æ¬¾äº§å“ String"""
        return self.info.result.get('data').get('loanProduct')

    def cdwLoanAmount(self):
        """cdwLoanAmount è½¦è´·èèµ„æ€»é¢ Double"""
        return self.info.result.get('data').get('loanAmount')

    def cdwLoanTerm(self):
        """cdwLoanTerm è´·æ¬¾æœŸé™ Integer"""
        return self.info.result.get('data').get('loanTerm')

    def cdwVehicleType(self):
        """cdwVehicleType è½¦è¾†ç±»å‹ï¼šéèƒ½æºæ±½è½¦ String"""
        return self.info.result.get('data').get('vehicleType')

    def loanProductApplyStatus(self):
        """loanProductApplyStatus æˆ‘å¸ç”³è¯·æ¶ˆè´¹è´·æ¬¾è®°å½• Integer"""
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
        """cdwLenderAge è´·æ¬¾äººçš„å¹´é¾„ Integer"""
        sub = int(self.info.event_time_add8h.strftime('%Y%m%d')) - int(self.info.cert_id[6:14])
        return int(str(sub)[:-4])

    def cdwRegisterLocationMatchBlacklist(self):
        """cdwRegisterLocationMatchBlacklist æœ€ç»ˆè½¦è¾†ä¸Šç‰Œåœ°åŒºæ˜¯å¦å‘½ä¸­é»‘åå• Integer"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='cdw_city_black_record',
                                            find={'city':self.info.result.get('data').get('registerLocation')})
        if not result:
            return 0
        return 1

    def cdwLenderGender(self):
        """cdwLenderGender è´·æ¬¾äººæ€§åˆ« Integer"""
        return self.info.result.get('data').get('gender')

    def cdwMaritalStatus(self):
        """cdwMaritalStatus è´·æ¬¾äººå©šå§»çŠ¶å†µ Integer"""
        return self.info.result.get('data').get('maritalStatus')

    def qhcsCreditScore(self):
        """qhcsCreditScore å‰æµ·2.0ä¿¡ç”¨å¡ç»¼åˆè¯„åˆ† Integer"""
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
        """finalScore åŒç›¾åˆ† Integer"""
        results = self.mongo.query_by_user_id(db='galaxy', collection="td_record",find={"realName": factor_encrypt_identity(self.info.user_name),"cardId":factor_encrypt_identity(self.info.cert_id),"phone":factor_encrypt_identity(self.info.phone)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if results[0].get('result')=='-1':
            return self.SET_DEFAULT_VALUE_INT_9999999
        return results[0].get('final_score')

    def cdwCzcbDebtScore(self):
        """cdwCzcbDebtScore ç¨ é“¶-ä¸ªäººè´Ÿå€ºè¯„åˆ† Double"""
        return self.info.result.get('data').get('czcbDebtScore')

    def cdwCzcbGeneralScore(self):
        """cdwCzcbGeneralScore ç¨ é“¶-ä¸ªäººç»¼åˆè¯„åˆ† Double"""
        return self.info.result.get('data').get('czcbGeneralScore')

    def cdwCzcbOverdueScore(self):
        """cdwCzcbOverdueScore ç¨ é“¶-ä¸ªäººé€¾æœŸè¯„åˆ† Double"""
        return self.info.result.get('data').get('czcbOverdueScore')

    def geoPhoneEntDuration(self):
        """geoPhoneEntDuration æ‰‹æœºåœ¨ç½‘æ—¶é—´"""
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
        """geoPhoneSelfMatch æ‰‹æœºä¸ºæœ¬äººå®åè®¤è¯ String"""
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
        """phoneGrayScore èšä¿¡ç«‹ç°åº¦åˆ† Integer"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='miguan_record',
                                            find={'cardId':self.info.cert_id,'phone':self.info.phone,'realName':self.info.user_name})
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result[0].get('response') or not result[0].get('response').get('data') or not result[0].get('response').get('data').get('user_gray'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return result[0].get('response').get('data').get('user_gray').get('phone_gray_score')

    def hfRiskMsgNum(self):
        """hfRiskMsgNum æ±‡æ³•æ˜¯å¦å‘½ä¸­ Integer"""
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
        """cdwAgentNameMatchBlacklist ç»é”€å•†æ˜¯å¦å‘½ä¸­é»‘åå• Integer"""
        result=self.mongo.query_by_user_id( db='galaxy',
                                            collection='cdw_dealer_white_record',
                                            find={'dealer':self.info.result.get('data').get('agentName')})
        if not result:
            return 0
        return 1

    def geoCurStatus(self):
        """geoCurStatus é›†å¥¥å½“å‰çŠ¶æ€"""
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
        """cdwAgentNameMatchWhitelist ç»é”€å•†æ˜¯å¦å‘½ä¸­ç™½åå• Integer"""

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
        """czcbGeneralRiskResult ç¨ é“¶-ä¸ªäººç»¼åˆè¯„å®šç»“æœ"""
        return self.info.result.get('data').get('czcbDebtRiskResult')

    def cdwCzcbGeneralRiskResult(self):
        """czcbDebtRiskResult ç¨ é“¶-ä¸ªäººè´Ÿå€ºè¯„å®šç»“æœ"""
        return self.info.result.get('data').get('czcbGeneralRiskResult')

    def cdwCzcbOverdueRiskResult(self):
        """czcbOverdueRiskResult ç¨ é“¶-ä¸ªäººé€¾æœŸè¯„å®šç»“æœ"""
        if not self.info.result.get('data').get('czcbOverdueRiskResult'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('czcbOverdueRiskResult')

    def cdwCzcbRiskNote(self):
        """cdwCzcbRiskNote ç¨ é“¶å¾ä¿¡è¿”å›çš„å¤‡æ³¨ä¿¡æ¯"""
        if not self.info.result.get('data').get('czcbRiskNote'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('czcbRiskNote'))

    def cdwOutOfAuthorizedDistrict(self):
        """cdwOutOfAuthorizedDistrict æ˜¯å¦è¶…å‡ºæˆæƒåŒºåŸŸèŒƒå›´"""
        if not self.info.result.get('data').get('outOfAuthorizedDistrict'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(self.info.result.get('data').get('outOfAuthorizedDistrict'))

    def cdwIdCardAppearCount(self):
        """cdwIdCardAppearCount è½¦è´·ç³»ç»Ÿçš„èº«ä»½è¯å·å‡ºç°æ¬¡æ•°"""
        if not self.info.result.get('data').get('idCardAppearCount'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(self.info.result.get('data').get('idCardAppearCount'))

    def cdwIdCardExpired(self):
        """cdwIdCardExpired èº«ä»½è¯å·æ˜¯å¦è¶…å‡ºæœ‰æ•ˆæœŸ"""
        if not self.info.result.get('data').get('idCardExpired'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(self.info.result.get('data').get('idCardExpired'))

    def cdwIsLcv(self):
        """cdwIsLcv æ˜¯å¦ä¸ºè½»å‹å•†ç”¨è½¦"""
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
                if zx.get("casetopic") not in status_list and zx.get("pctype")==u"è¢«å‘Š":
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
        """hfExecutionState æ±‡æ³•[zhixing]æ¡ˆä»¶çŠ¶æ€"""
        return self.__hf_result(style='zhixing')

    def hfCaseTopic(self):
        """hfCaseTopic æ±‡æ³•[caipan]æ¶‰æ¡ˆäº‹ç”±"""
        return self.__hf_result(style='caipan')

    def hfDishonestDetail(self):
        """hfDishonestDetail æ±‡æ³•[shixin]å…·ä½“æƒ…å½¢"""
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
        """hfExecutionTerm æ±‡æ³•[zhixing]æ‰§è¡ŒæœŸé™"""
        return self.__hf_month_money(style="month")

    def hfExecutionMoney(self):
        """hfExecutionMoney  æ±‡æ³•[zhixing]æ‰§è¡Œæ ‡çš„"""
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
        """cdwApplicantIdCardAppearCount ç”³è¯·äººè¯ä»¶å·å‡ºç°æ¬¡æ•°"""
        new_sql="select count(*) as cnt from e_apply left join e_proposer ep2 on e_apply.id = ep2.apply_id and " \
                "case e_apply.apply_type when 0 then ep2.type = 2 and ep2.id = (select min(id) from e_proposer " \
                "where e_proposer.apply_id = e_apply.id) else ep2.type = 3 end where ep2.card_id = '%s' " \
                "and `current_node` in (9,10,101,11,12,13)"%self.info.cert_id
        old_sql="SELECT COUNT(*) as cnt FROM lb_apply_lessee_info b LEFT JOIN lb_apply_main a ON a.asqbh = b.asqbh WHERE a.azjhm = '%s' AND `ASQZTDM` IN ('01', '02', '03', '061', '06', '08', '09', '10');"%self.info.cert_id
        new_result=self.mysql.queryone_by_customer_id(db='auto_loan_entry_test',sql=new_sql)
        old_result = self.mysql.queryone_by_customer_id(db='zu_che',sql=old_sql)
        return new_result.get('cnt')+old_result.get("cnt")

    def cdwGuarantorIdCardAppearCount(self):
        """cdwGuarantorIdCardAppearCount ç¬¬ä¸€æ‹…ä¿äººçš„è¯ä»¶å·å‡ºç°æ¬¡æ•°"""
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
        """qhcsDefaultRiskScore å‰æµ·å¾ä¿¡-å®¢æˆ·æœ¬äºº-å¤±ä¿¡é£é™©è¯„åˆ†"""
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
        """cdwIsSpouseIdMatch é…å¶èº«ä»½è¯å‰6ä½ä¸ç”¨æˆ·æ˜¯å¦ä¸€è‡´"""
        spouseIdNumber=self.info.result.get('data').get('spouseIdNumber')
        if not spouseIdNumber:
            return self.SET_DEFAULT_VALUE_INT_9999995
        if str(spouseIdNumber)[:6]==str(self.info.cert_id)[:6]:
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def cdwNoRelationContactCnt(self):
        """cdwNoRelationContactCnt å…³ç³»ä¸º0çš„è”ç³»äººä¸ªæ•°"""
        if not self.info.result.get('data').get('noRelationContactCnt'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(self.info.result.get('data').get('noRelationContactCnt'))

    def cdwNetPrice(self):
        """cdwNetPrice ï¼ˆç»é”€å•†å¡«å†™ï¼‰æŒ‡å¯¼ä»·"""
        if not self.info.result.get('data').get('netPrice'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('netPrice')

    def cdwIsGuarantorPhoneMatch(self):
        """cdwIsGuarantorPhoneMatch æ‹…ä¿äººæ‰‹æœºå·å‰6ä½ä¸ç”¨æˆ·æ˜¯å¦ä¸€è‡´"""
        guarantorPhone=self.info.result.get('data').get('guarantorPhone')
        if not guarantorPhone:
            return self.SET_DEFAULT_VALUE_INT_9999995
        if str(guarantorPhone)[:6]==str(self.info.phone)[:6]:
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def qhcsBehaviourScore(self):
        """qhcsBehaviourScore å‰æµ·å¾ä¿¡-å®¢æˆ·æœ¬äºº-è¡Œä¸ºç‰¹å¾è¯„åˆ†"""
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
            il roW.7aw('ktemWkd‡i==sr,atem_id):
     ((  ! 0    retu2l su6SED[DEFAULT_VALU_IN1   ! (! pmturn self.SET_DCFAULT_VÁLUe_INÔ_!
  4 den0risyIöuï23w.222({elf):
       "&b*òmckItei2966023	è’+¤¹½è«å½ä¸­é«˜H£é•©Å…·æ»¨¥å•""
"    $  òdtUr. wEäf.[tde;}lt¨ètem_ad}2976620)
, 0 Daf rIskI4mo2976610(sehb	:
( "$   `2*2rHskKtem0¸72$é˜‹ä»ì¯åœÒå®ıåœ°ô½ôº†é«˜©çé™éì®ÂÀ¸¾ù¦ä¸­¥œ0e’#"#"`! $   rgvõrj 3¥lf.__tdR-sult(Itgï_)¤½2976r10)  ( dín r)ckHTem:876264(RelV):` " " p"" RicKItEm297>42 æ‰‹æœ*å—ã…­ì¸é«é(©™©å…±ò»¬å‘å•"¦#  " !  "zedeRl8óelc.__T$Vusult(i4Em_éf]29w62749

   "de$ âis{I4dm´=?62µf(sehf);
1      $#â"risihtaı¹625 ä‹æÜ¸ã#ã•½ä¸Íé€šd» å°å·Áº“c""J ªà  " (2e$}rn så,G*__u`Resõntitee]!`=z¹7²4
*!(0 def 2iskItem2=7386(self!: 	   # (B""zirkHue-2936187 ç,ìä˜€Ì”ç3»ä®ªš«ä»½è¯Í±½å¸¥æ³”é™¢õ´±ô¿¥åá•=h¿Áäº°b"" ¡ " $  rmpurn seîfû_tdrGsqlt(iteíOiL½0976s8¶9

  !8dåf rasKYtem256³89,selF->
    !` """"risëI|amr9'63( ÷,¬ä¸Äê…”ç3»äºúèº«äºø¯å‘½ä²­ä³•É™¢â‰§ì+åå­•@""
`      8ReuWrn {dlv.^_tdBesul|(itam]Id=2952388)

 " bef riÓkItÅe6)wv392(s5lb	:  (     ""2biskItdm:9769 ç¬¬d¸€ø”ï³»àººè³ëå»½ ¯å‘½¤¸¤×Š¯ç¥ªé˜šç¼å‰å•"#"
        retuZn sel&.__tdVesuhu(kuee_if<3974392)

  ! Deo riSkItem:=76396,3e|f):  ` $ ( ""#2iãnite-396386!÷¼¬ä¸€è”§·»ä»ºèº«¤²½¬å±½ä¸­„ÿ¡è´·©€¾æœå e•¢""* !  "   vet}sn seäf.O_tdSåctlu(h4E-_kd?2ù76396)

 $  def òiskÉtei2¹76£8 yeld)
p`  "  0$""réskItem29·6³9( Ç¬¬ä¸‚è–ä³»ä¾ªæ‰‹âœ²å·å½ä¸­†Ÿ¡èµ·©®æœŸí°å•"""¢       return sel&>__t`Resuld(itd-_id=29'·399i

    @et rirkÉ|em"17>$42self	:
        2""âIskIteM2)64 ’0ç¤¬¤¸€¨”ç³»ä¸ºæ‰‰Gœºå·å™¼ä¸­è™:¤‡å·ç¡çˆ–é€ô«¡å°ä·åºÓ""

 ! p  @rMttrn óe,f.]_xdZe3un4(itEm]ad<2)74402©

   $dev clwC~cbR/#RequìT(Self-:
      ("6"cäwCzcbPbocRD;ult ç»¼åˆæ¨€å·>é“¶è¡è¿”à‹¾ç’Äå…ì¸¨ä;±æ¬åš ø€ä¸ªæ³¼å˜ˆæ»“(®º"""
        iæ s5l&.i.FoÿzeSult.get('daty').ce4('£zcbWeNEralyskR%sul4') r se-v.	~f_.resultlget('Dáö`').get('cjkbDt¢eRysëZesult') or self.EnFo.verultfgeT(%dáw1'),'Et
'#Zc`OveräueRkóiSeóult')(/s!jnt(self,inm.vtrumtîgep,uati')/wEt¨'czkfGnE2AlScgze'		$< 0&or floet(sen&.ibdovesUìdãe|-'dada&!.get(#cZsb6gòduES#g3a')( $8 0>
       $ $  reuurn "N"
``"$ "  i&"3elfîhnfm.Feóìd"feõ('dqt!/)*eEd-'#zc"eîlraLPi2kRe{Wdv'- /r"3elg.infn.rerulu.Geuh%datÁ')*get(&czcfDgbtBiSkpsultg) Or ceLginfk.besult/wåu('fAta').Get('cúc`Kv%sdeeZiskReSqlv'	:
 "   $  (!  re$qb. D"
 0 0    if sålg.	nv/.result.wetgdat`').gåt('czcbGenercìRisKRgsel|'h anl se4f.k~fore{udt$wDt*'datá'(.fåth'bxCcDebtR9wbRgsuldç)°a~d se(~.iïf/6r%qu|d.'et('Tada'(*cEt,'g:c`oveZeueZiÑkÒesunt'	z
  (      $  Rej}rn ""
( 0    (ce|uvn "G"
    d%f #dgVçhache	fLumberApreasSOuj6 selæ-:
  "    " "cdw^ehiclfI4NemfqrApğ%áòCounT(è¹ææœ?í7å˜ïğæŠ„æ­¡ä•°"""
   &  ( sul}"SELEC CO]NT(*) as cnt NRMM lg]aPply]AAc LEfT JOMn"|b_q`p,y_,a),$! NN aaqbh = cLasqbx SHeSE ACJH!=`‡%s$$AFD dArUJUEM` I^ ('03%, '061/l '°', &08&, #89'<°'·0/=relf.info.rgsux|.ge78!dAõa'	<e(t"v%xisleIeNuíbeR )
  &     r%sõ|4*= sedf.myqqláueryoneÏjy|stímeq_ie*db='zuYCìe// spl=Sal+ (  *   ""new_sql"{ele't counu*
h ¡s0c~t4nrom eAppl{ igft jo)n¡¥_kaP on eáppl{,ée!½ e_cab.apğly_yd  thgrg sár_rin!=0'%3' andb#ôzrent]jo$e`$in 8y¬ 56,109,11¤12>s )ë"óelf/iffo.result.get(/$aua'©.get(¢Vei%cldOuebar")*   (($  nEwOsqh"SENMAD KOUNT(.) DRKM e_gqpäi a LEB JOIL%a_car eC1$MN a&id =!%c!,eppbY_id WHZA eg1&cqs]wiN =1'%ó An@ anápp|y_st!tus!HN  %< v. - x-"%¢elf.infk.seswlt.get(§fata%).iel("v)HicleId]mB!R#)!   "   ne7RQselt  self.myóql.qeePùOnm_jy_custoíåz|il*db='a5to_dOin_entsy_tert'( sql=oEw]sql)
" ¡    0setupn rE;dt.gåt "klt`)0+ new_r%ëul4,eet("ãnp")
  0daf gbeajChanneìi{elf9Z (($    """g2eEjCh!.nel!ø¼¦`´·Ç»¥è‰²ëÀšé“¢""*   ¢  0`if noô sdlä.invo.resu|t.åmt('tbta').geT('gpåefC
annul'k kr s1tf.Info.reswht.gnp(data'	.gå$('greenChanne,')=':   0    "  rk4a2n yeìf.SET[DEF@ULT_VALUE_INÔ_9)999;Š    $ ` rex5rn {fp)redf.info.rese,0get('dcta')Oet(#gre%nChanngl$)+

8  deo pbokReason(S¥lj)*
"       ""tbocecron ¤ş—É‚®å¾ƒä¿!ç;“¦œh»”m¶˜­æ‹’ç»÷š„åŸå›(æ˜ç»„""b
(  $   ig!fot s%m"¾ifn.rewuhd.cat('data'	>ge|('pâoJea3on'+
   ¤    ! ! sEpurn¢welf.SEP_ÄdGEUlPVALUE_I^P_9999¹( "  $ (rt4url s%ln*info.besudt>get(gdat!&).gdt('ğbncRd!so&g)

   #24!92212
 `  d%d"applisantstk5rd{pm(%ld-
 $ `    "2"applicanDSpouseyqe Ç”³èÏ¯äº»æœÍæ²¡æœˆé…å¶"""˜     "  ig ogt 3eLf®inng/råult.gdt('eaTa').oeT(&haswpoeqm")*
 $          setuSn selvNSETODEF	GD_VADUE_IT_911195¹
 %  `  retUrj ínt÷a,filbk.sesu|4.oet('data'-.g%t("@esÓpous%‚))
    leb$Spou3eFeëThïnåLe.`8sdlf)*
      ("""ótouseGeoThoneLkn  é›†õå§æ0æ®,é…å‘µæÁ‹æœŠå­’å±åÔ°"" 
 (    0 stfusåM$Nt-bår$4 rtlf.)îgojs!sult.dt `àta?	¬ged('spkuseIìÊwlBEr§)`` ` `  spousgphç~e =selbilgO,zEstlt.we4('daxa&	get*'{ro=såPhole'(
   0  *0cpoureN!lu 0=seIf.h*æk.r%sqmp>get¨'&at`	.get('spoÕsuNa}e')
"     "rmÑuh\=s'|f.molg.ñUery_`y[tseq_id¨ db)gamcxy',
   " !      `   $       ¤!(         ("  20 $c/llgãtion?'feo_säãmfd?l
  
   a    `!  !  !¸    `  "      (     0 $ˆfhnd={/cabdId:st~%seIdNpmber$'p(one·*srotsmPèOnq,#reulLam%':wQmwseNam`|)
     0  )g(noô re{ult:  p  ¡  0 ` r%turv 3tl'.WTßFÄFauLT_TÁÜUÅ_A^P_18=+99	
      9if nçt r!sulK0](gmt("R%qpooóe=0or!nou pg3uLq[].·et('{esponóe&i.det¨5`atag),or nt!Result0U&ge4(&fåSPnose%+'gdt('ğcda&)geu /IRPNUM'):
0( $"  "    sat4rn {amf.QET_DEBAULDVF]E]LV_=19899
$   `   Bet}Rj(rasUlt[0.g'4('reSpm.se').e%t('daxa').get.'XSQLUO').we)qzkvInce"selænSeT_DEFÁULT_VCÌÜE[iNT_)99¸9Y6)
  $din(_OGeNÔxïneBkrt(sul,IdNulbdrphonå)name)geoTy`e)  (     jesult=enf.i/nfk.qu2yby[usar_ad, db=galqx}m
      `(  $      "&0    $!  ! $ !    0   !)so,luãtéoN='gåo_reikrà¥,
à  `     !$ ( ¡  (! (  0)"`" `  $   "      fyNd={7cqRdYd7{I$Luì"es)&phene':`hone,'pEalN!me':naee}-     $!!)F no| z%swl\   0 ) 0   2åtuR~ {enf.SAWODAFAUDP_A\UE_	NT?99¹9y99  (0`   if not rnóulP[p].Gdº(3res`onsd") kr not result[°].fgt('pesponse'-.geph'davd'+ or net rdsultZ4].gEt resqon3eg)gÅt('r`laf).get(#RRLgI:
 <         0ret5rn(wEl&*GPßÄENAELÔ_VALTE_MND_y;9919
    ` ( ff2 Code"i: `sultS0].g`t*'sespgjse#).gev(7daT`'!,gdt('sSL6):
 ²(  $ ! ¤ `if(C/ee>gå|(#xFV -==gegTùpe2    2`  $    €  rETur*"cod%*gdt"RS*).get("cote")
 $    0 sepurì self.SEUßÄEFAULT_WAOUE[INT_)99=99=

  " def sğouseGeohonaMnturatIN8Celfm:
      $  "3pïuseGemXè¯,eAîtDuratIon ç”³è·äººé…å6ãš„ç‹æœºåœ¨g½‘î–¶©•?#"#
   ! 0 dspoõqeXdNumbur = self.anfogSesulU.wet 'data').wet(%{pous%I$NUmber')
 !      sPotsePhGne =cmLf.i~`o.rusuhô.get!'e ta').ge`(#sPOusePhole	
    "   spouseOaiG  =celg.hnfove[Õl<.ges('æata').get('spguSUNáme!
 $"     xetusn qelf/S_GmoRhgnmCoct*sqoureIdNulber,0spÏusePhone,4spkuseNeíe,geoTQpe='A#%
 0  def guïThonECnsd(Culf):
     ! ""¢`eegPloneCoqt é›†å¥¥æ•æÍ®ä¸íç•³è¯·äšçš„î‰™âœºâ¯•ü´¹è¼§å•""#
0  ` !' IdNUmber seìf>anf.Cert_md ` " !  phone  =sAlf/hnbo.tiile!   "0 (namd  (5self$mnnk.urer_naoE
! (0    retwrj iulF.__GeoPh/îeCostIdNuMfqr<p`one$namä,eekPYpe1'B5®)

   "def wpoDsorÆeo@hmneC/st(sm|f)
 !  `( !2"crponcopGE/HjoneSost Á›–å¡¥ä‡°æÍ.ä¸­æ›…¤¿ä¸ºç»‚æ™‹æ¼ºèİi”ùè´†å™•"¢"
        Çuaòaotk2HdNuobd2­ce,v.ingo/Resuét.gqt('dkt ')&ggd('guarantKrAdNumber')
""!  $ 0ctar!ntgrhone=qilg.yld/.result*ged('fate'/*dt*#guapalTOrPHîE'!   (0($ gu!raltOpName ¿sm,f.iêfÏ®resuhp.get 'data')ge|('gõaranuortmE'+
  `     return self__GeohojECos¶(eta2`ftorAdNueber,guarán|bP /oa,uqarcnumbFaíeoeOTy`e='B1)

    l%æ spou~eGwoPhonaCoqt¨self->
 ! 0    "#¢sp-}seegPhonåSgsU é›‡e…åæ•°æŒ®ä˜íé…Ç¶äººgš„f	‹$œºè¯é´9è4¦ej""
        srous$It\em"e2 0send-nfc.result.Gmd gdat`G).gEt(#cğouCeIfNumber')*a"     spNuseP(one <self>!nfm.result.get(gdata'©.çmt('ppousePhknå%)
   ` 0  srouseJame` =selfnijfo.rt3a,t.git(/de4ag)&ogv,#rpwtsena)å'i
`"  (   räpõpj selb._GEgPxïndortspOuseIdNwebep,sp'%SePhone,spou3ENamm,%doDYqe='B ')

  `¡leD spo5qeGeohmne%lfMat!h8sElf):J"   !  ¢""SpeureGeoPhkneSahgMauch ç”³è®·ä¾:é…å¶§šæ‰‰çœ˜å³F¸¯å°¦å!–é•å¶`º›¤Ÿ=è®å®ÅéªŒhåè€è‡´"*        sp/uqáId^u"er½ sdlg.infM.ffs5`t,get('äatd'),gAV¨'spguseIdNwebev'-
        spïõ3uPhne-relf.info.resu|y.geqh'dade&->-`t(';pouqÅP`zne7)   "  qpous%Name 0=self,iNno.`%sult.gåt¨/Data').get('spoUceamå'( !  *  `0ettrn se|F.__eoP(oNeAost,wpoes%YdNõmâer¬spouseRhonm,rPouse\áma¬GuoÔype='B7!(
 "  lå&$spo~smvGenPxoneRedgMatãh(3%lf)F   °   !*`"gpmnsorGeoPjïneZenf]a5ch æ‹…ä»äººç„ö‰‹æŞ»ç§Æœ¿å¤å–Œæ…ä½™äººîœŒäººéú»ä»ıü¯åªšèêªè¯¡¤º€ì‡¶2" "$    ( guaranuKsIdNuıba2<semf/ilgo.res5Lt.'et(dCta' ./e|)'gu!rafdïRIeumber')J !  %   guqrantosPinne}se|æ.info.seult.Ge0('váT"')®ge4*'guaran|Obhone'+Š  "$    guarcnpgrNamEÀ=se¬F.iîvo.result'eu(&dauag)ngmt(§guarantrNleg')Š  % (   vetuRn!cglF.__CeoPhojeGjst)g}qráftorId^tmbeb(ãuarqîtorPèone$gq!rentorName(oeoTYpe='B7%	

    heö sponsorType(semf):
   ª "  **byqoncopTyğe æ˜§å&æ·»åJ¤¤»†vŠ…ä¿½äú:"""     " ()d8nkt`reìf.Infn.result/gEth¥data').get<%)isqcselPor'):
   ¢  00  ! retubn Self&SMT_DGAULVADUÁ_IBT_9919999
    ,  HZeturn aNt(cmlf.ynf.susult.gåp('da}m').wet('hacGuav!ntmr')+
  !`äef sponsobAgE(så,f)2  (   &`#*"sponsosCge âË…ä¿äºúç„å¹¶é¾„!*2
 0`   0$kf ngt`s%lf.ilæo.rgsqdd.Geu('data').gat('guiğÁntorÉDN÷ebe²'+:
*(      "$  rmturn0Self.SETDNAULT_ALUEIJT[9)999)
"       GuqranvjrIdFumbgr`= Se|f.ingo/rusuot.Get(deti%-.Get('gUaranTmRHdNuM"}r')
 $!     sTâ( int)3elf.knfo.FreSte_tymU&strf4iod('%I'}¥d')±" ijd(guaòan4gSIdNumbez[6z14L)J !"   "`rg`trN iît(cdz(qub	[º­4]-

d$! def$ccòClaóó(Semf)8      0à *"barWlass`è¼”åßç³ì¯³áººå‡†éª¾ì¬çå‹"&"
 ` !"0  result½sIln.EnjgO.ñuesy_b}u3µv_if(@dB='eaháxy$-` (   $  ` $      ! `!   !   `  00!0* b   collectioo=pi_rgcpD',
  !0    #`   "    0  @`$     €`   $!$      !gind¿{'careMd#:ekTov_enbriptideftidq(selfhi.fo/ceruWid9,'phnşebActKb}enaryqV_identidy(sel&*il&oNt`gna),'òåalOa}e#8faãvnr_eO#rypt_i`mopIvy(salf.yffo5wer]name9})
     "!1if notpesUì´2
  1     ( "0retuğn!s¤lv.QETDFA]\T_VnUÅYIMT_999999    "   if îot resuìtS0].gev('0yRecpo®se') Or nnTrUsul~_0].oet9%piQespnnse')gEw(&vETuslVaì}g') ]j`           or bot be3ulT[0]nget('py@e3qonse/).'Et('pAPUrnVqhuå').eet(¥cisRgpïrt'‰:
0    &   ` 2rmts.$palb.SÅT_DEFAULTVcJUEINT191	939  `$    capClcss7zdsu}t[0].gd48'tySusponse').gUt #rE4uvnVa\ue').get('cisRepo~t'+Z0].oet 'dpiVerL)ce.qeAnvg7)>'et!%aqpBlacs/,self,CeT_DeFAU\DM@UE_KNT_9999))6)!    " if cazKn@ss==wElf.SDT_DTQLTFALUG_IJT_99y;996 or not cabCm`qs:(     2`    vetqcl s÷lF.RET×DDOqMÔ_ALUm_INİ99+;96
     $  if 'A#(k. carSlass3
  !       !!p%tubN"7
   ( !  hf 'A2& ij caòClasw®((!   $  0öetuzn 4
        if B1& if cyrclqóS:
 $¨   !!    retero 4
   &  $(ig /B2¨in ca2Alasa:
       ( b`$r'Ttb> s
  ((    if$'A1' hn carCl`ss:
(    !   4  revurn 7 0  !  if '°'@in carAlass:
 €        % return 2
 0(     if"fC²' in carClcsw:
  ( $      !repqrn 3*  (     råğern 4
   dEf dravyngDébgjkeExpèRyTite(self)8
! ğ "   &""@riincLic`*cmÅxpyr9Date à¿”å›æ”³è¯·ä¸ºé±¾à«7è/€çš„âœÉäŠæœß#""
    0!  resumt={edf.mgnog(q}lry^byZuseR_y$	`db?''alary'<
0      (0         $`          `  "  $      $Colngcpann=PÙ_Reãorf',
       ((          !    "   ` 2  ! !   ` 0 !fint-{‡c@rdId':factope~k2yp|Sydgşvip}lcelf.iNf/.cezt_ad),'phïne':ficTnrenc`ypxidentityhself.info$phon),'realNaig&:bacôor_%ncrypT_ilentity(celg
ingo.usdb_name)=	
!¡      éf not buóu,tz
  (0 ¢   !002eturn sõlf.QEÕ[DEFAW\T_WALUE^INT_9999919
      p mf jot02esuh0Z8].get('ÒyRuspoose%) Nr&no| zayuìtN0]eet('pyReS0once#).getª'TeturnV!due')0\
" ""        or not$re3qlu0_.get)'syRestonse/1.get)&ratõrnVamug')ge4 %cisReport'):
           $pettsl óedb.SÅTlEFAULT_VANQE_INT_99999=0       UxpkryEápe=rmsult_0_.oet('p}resp'nceg).geT)'seturnVaLud'	.ee4(/cisRepnpt')[2].get(%`riTerLhcenseù.fo').'et('EppiryD-ue'<sanf.SETEÅFAÕLTURALuEOIN_999-96)
       0i&$exxiry@ave½=self.SET_DeFAU\DWVALUEWÉNT^99999)6*
 2         8ret]bo sehf.[ET_DEFAUNT_VQLTEILT[y99999&
 ¢   "  if`axp)ry!tg=9%':
    ` 0,    ruğern 3Ulf.SET_dEFAUL\_VALUE^IN_9=1)9)6
`     ` r%turn detåt)me.datdtImE.sT2qtime(ex`i2yÄate, "%{-%}­'d"¹

   $dad dvùvingiaenceStaUts-S%lÒ):
`    ! b# dbhvIngLicgnceÓ`atus"h¿”å›Ş©©í©¶èçŠ¶ö€¢&2
`  0    rmqult½edf.mmneo.yueRy_b;_usez_i%) d`}'gslaxù'
     ¢  0     h       ` 0            `  (0collegtéon=6ğy_r$copd',
   `   ` %( ( °   !   "  `    `     `       d)nd=k'cizdYd&:bQbtmr_enirypt_kdgntity(qdlf/info.fert_id-,'pxmnu':fca|orencrypt_ifelnhTy{elv,in&o*pHong!'rAlNiíe'fmctoö_encr]qt_Hdentity(self.in&/.usub_ncme)})
 ` `   é& nod result:
 0       *0zeuurì sí,g,[DT[DFÁQ\P_VCL^ANT_1¹9999y
 ((   $@+c`jot0r5óu,ts4]*gup('ğ+Re3phnse/) or Nït besult[0U.çev('pzRespoNku&).get 7²epub~Vahte%) \0     ! $  $+r nMX(zesu|t[°U&wed('pyRecôonsu5!.gUt('retwpnvalum'9.gå|¨'cisRgTord-z*`    `     ÷çuero,{elf.SET_EEFEÔMÔ^VALUEOINV_999991y
   ¡!( status=SEsulp[0].Get('pyVmqzol{í''get(7re$ur,^!lue')>Ggp('cisRePo:t')[ U/oet('uòiwebLiceoSeI.').get(§st!Tuó'.3e`f.SUTODEFAULT_RALUE_INT_99¹99=6)

  !     i.¡statt3=½self.ET[DEDAUDT^ÖAlUE[INT_9y99;96 ob`nmt rtatus:
 (     `  ruhurn self.QET[DMFEQLT_\ALUßiLÔ_9)9y)
 (0 (`  staUusList=[]  ` 8"  ib u'ö­£åº°& `n"statE3;J "!   2   " qtatuyNist>apxdjl(&1'+
  "     i& u'É¶å€†%(Éî sTa|wS:
(h  °`$ 0(  statqãLi4.qqpen$'2'-*     "  if u'h½ŒÅ‡º7 hj statu#:
`$    `¨°2  staĞ5gLisT.iøped('3')
%   !   iF t'æ˜€f‰³w 9.({tatus:
b&       2 rt`|u{lmsV,appene(#4g)      "!iv u'æ’¤É”€'0i
 ctap9s:      0(    statusliw|.AQpåndh§='!
  %    ¢Kf"}&ñ€Šé” ' ijst!twS:
0        $  statusLi{t,cğxg>d'6')
      (!iæ u#æ³¨í”€'$in stadus:
    $ !(  ( 3tatôsL`wt.±qtdnD¬')8¨"      èf u'èÿæ³•æœªå¤•ã†'$in!Stetur2
 4 " "!"0   3tat1sNisô®axpent' ')
$       mf0u'¥…œfí¢ä½¿ç¤ˆ' in st`tUs9
 0       $  SpapuS\ist&atpåf$(%9')
  $  ` $if u/ä¸“æ‘„¦œªÅ¦…g' in statvs:J     $ 8! % sta|}sLiwt.gp0enfh##°'-*       ¨iì 5'õäŸ¥' )N rtattó8
 "!4   "   sUetusMiât&append('11')Š & p    if U'é”í¯š' k~1³vasu3:
   ( $ ! ` ÓtetusÄistªa`peÎ`(925)Š       !id W§i¾æ8æ˜ªæªè¯' i. cpaTq3;Z (      "   ctatusL9sT.appeld($57'=
 ¤      if"5'å«¾æœŸæ¢x­‘ç in€s4aôuS:   !` h    (sTa4uwList,aqPenä,&14'+
 "@    !if0u'å»–çøŸô½ö£‘' mn ó|auuC:
   ` ( " ¨a ódqtushqt/app¡nlê'15%)
      ""If u"É€¾ö¸Ÿæœªäµ“æƒ¤' In stadts8
 (  0`    $(st!tuwLasT*apqend '10&-
  $ $  mg u'É„¾æŸæœªå®¡éªŒ§ iî statu÷*J @      "   s4!Ô}sist.ap`dnf('377)
   6 ` (if uä…öä«†/iN status:
  "         gdkv2sLkst.AtP%nf'8§9"     " if`u'æ‰"e™™' i~ rtáDt98
       "   sdituSNisp*aprend('%¹¯)Š        iæ lgt$suaDucJisd:)!  2    0$`return celf.STTGDMBAUlT]VÅÌUEKINt_0(       vetUrî!7;7*jkin(3tatusHist)
 0  dg¦ bqouseFiNA|ScOZf8Selg)z
 !` !   """SpousåFAzalSãore ç”³h«·äºªé…Íe¶çš„õÀŒå›>åˆ†"""
0    !  ypouseI$Nuober }(se\f/il.o.veqqlt.'ut 'diTe)geô)ipouqeIdNymrår+
    %   ~pmu3EĞhoæe }sel".inno.rewõlô.glt('ti|y')/Cd| 'sp.uSePh/.e§)
        sPouSenama  -seld®i:foreRuxu.geq('atq'),fåt)'qp/useName')
  ¡(!  "rEsulTs = se,f.moNgk.5ueryWBy]userÏhd f=7walAxy $golíesi.n=ôd_vecOrd`,fin`="pealLeie#z`f!cTor_gjcr8pt_idenôivy rpo5cLane)<"Car`A`":fucôms_dnëò9py_kdeîtity(CrusdId^uerer)-&phkng :æiãpor^dîcRyPt_{deN|ipy({pïuseXhoná)=)
  ! "" md Fw´ Resulds:
 (          se5uv0salb.CET_DEVÁWÌUWVCLw_éN_99)9¹9
(  $(|  if zdó5l|s[].get8%VaSult%)=?'%3':
$       $   betqrn!welf>SEL/DEBaUÜTYVALUe^INT999Y99)
 ```  0 petu2n(REst4s[8].get('f)~AL_sco2e'-
    dåf __tDReqelt_{ekure({e}æitel^id(;
    0 ° ypeureIdNumcåz €÷glf*ynfO.r¥suèt&eet('eqta'+.ggt(s0ÏuseMlNumveb§)
      ` S`kuS}phOnd 8sel$.ifgo2dsulu/get %dpte&)nge5('qpouwaHîd"!      ! {poqseJame  =sglf.info.ze3ultnget 'datá%).ge4('wpusenQee')` #    drEóumpp < semf.-kngo.query`y_usmr[id(dc,'galux{'l collåctiOn<&tdR%gobd#,di.ds"pealNa-e"*!fa!potuocz{pt\identyd9(spouseNa}u	$"gardYd*>fag´ó_mncry d_idebt)uy¨spuóeMdNu}bdr),"ğxond":bÁgtorOancrypv]identity sq/UseDho.e)}+
"    $  if joT raqults"
   ‚    0 `retqrn$3e,F.SmÔ_DMFÁULT_WCLUE_IFT898q91
    1 $ udR%0wêtReótonse = jcon.lkCds(f!cvkrd5Kviht_ydgndiuyhres}ltsQ].get(%ckn4an4'/))À  `     éf nnt tdRdqorvBespoîse:
  $ (  !    retubn remn.CET_LEFAT_VALU[IFT^99¹1996        For Zw in tdepOrpRdcpknsq.Gut(/ziskWitemsG):C  " !  "$  0if rï7.g%t(7it¥mOad') - ñt2¬id%mhdiz `  " $"      @ 2eturj sEnf.VET_FEF@ULTWVQLU_INT_0
       ´rep4s."Self.SET_DEFEUÌT_VAÄUE_IVQ_0Š
  ``dcf$stgeCeRisJIWem297¶°1p(så`f¨2
       "*"spouseRiskIôuL2?6r ç”±è¯§dºšı…í¡¶çš”è²«äû½è¯õ¿‚åì¿åºä­	¤º­¡˜é£é©í¾ƒÄ¸2©›†Ä¨¯åœ0åŒ¸ ""
       Vevus,!seld.O_udReSelt_spousl(item_yd=297&010)
!   def stousMPaskAÔåm2976222(self):
        """spouseRiskItem2976222 ç”³è¯·äººé…å¶çš„èº«ä»½è¯å‘½ä¸­é«˜é£é™©å…³æ³¨åå•"""
        return self.__tdResult_spouse(item_id=2976222)

    def spouseRiskItem2976256(self):
        """spouseRiskItem2976256 ç”³è¯·äººé…å¶çš„æ‰‹æœºå·å‘½ä¸­é€šä¿¡å°å·åº“"""
        return self.__tdResult_spouse(item_id=2976256)

    def spouseRiskItem2976264(self):
        """spouseRiskItem2976264 ç”³è¯·äººé…å¶çš„æ‰‹æœºå·å‘½ä¸­é«˜é£é™©å…³æ³¨åå•"""
        return self.__tdResult_spouse(item_id=2976264)

    def spouseRiskItem2976386(self):
        """spouseRiskItem2976386 ç”³è¯·äººé…å¶çš„ç¬¬ä¸€è”ç³»äººèº«ä»½è¯å‘½ä¸­æ³•é™¢å¤±ä¿¡åå•-è¿‘äº²"""
        return self.__tdResult_spouse(item_id=2976386)

    def spouseRiskItem2976388(self):
        """spouseRiskItem2976388 ç”³è¯·äººé…å¶çš„ç¬¬ä¸€è”ç³»äººèº«ä»½è¯å‘½ä¸­æ³•é™¢æ‰§è¡Œåå•"""
        return self.__tdResult_spouse(item_id=2976388)

    def spouseRiskItem2976392(self):
        """spouseRiskItem2976392 ç”³è¯·äººé…å¶çš„ç¬¬ä¸€è”ç³»äººèº«ä»½è¯å‘½ä¸­çŠ¯ç½ªé€šç¼‰åå•"""
        return self.__tdResult_spouse(item_id=2976392)

    def spouseRiskItem2976396(self):
        """spouseRiskItem2976396 ç”³è¯·äººé…å¶çš„ç¬¬ä¸€è”ç³»äººèº«ä»½è¯å‘½ä¸­ä¿¡è´·é€¾æœŸåå•"""
        return self.__tdResult_spouse(item_id=2976396)

    def spouseRiskItem2976398(self):
        """spouseRiskItem2976398 ç”³è¯·äººé…å¶çš„ç¬¬ä¸€è”ç³»äººæ‰‹æœºå·å‘½ä¸­ä¿¡è´·é€¾æœŸåå•"""
        return self.__tdResult_spouse(item_id=2976398)

    def spouseRiskItem2976402(self):
        """spouseRiskItem2976402 ç”³è¯·äººé…å¶çš„ç¬¬ä¸€è”ç³»äººæ‰‹æœºå·å‘½ä¸­è™šå‡å·ç æˆ–é€šä¿¡å°å·åº“"""
        return self.__tdResult_spouse(item_id=2976402)

    def spouseRiskItem2976212(self):
        """spouseRiskItem2976212 ç”³è¯·äººé…å¶çš„èº«ä»½è¯å‘½ä¸­æ³•é™¢å¤±ä¿¡é»‘åå•"""
        return self.__tdResult_spouse(item_id=2976212)

    def spouseRiskItem2976214(self):
        """spouseRiskItem2976214 ç”³è¯·äººé…å¶çš„èº«ä»½è¯å‘½ä¸­çŠ¯ç½ªé€šç¼‰åå•"""
        return self.__tdResult_spouse(item_id=2976214)

    def spouseRiskItem2976216(self):
        """spouseRiskItem2976216 ç”³è¯·äººé…å¶çš„èº«ä»½è¯å‘½ä¸­æ³•é™¢æ‰§è¡Œåå•"""
        return self.__tdResult_spouse(item_id=2976216)

    def spouseRiskItem2976220(self):
        """spouseRiskItem2976220 ç”³è¯·äººé…å¶çš„èº«ä»½è¯å‘½ä¸­ä¿¡è´·é€¾æœŸåå•"""
        return self.__tdResult_spouse(item_id=2976220)

    def spouseRiskItem2976224(self):
        """spouseRiskItem2976224 ç”³è¯·äººé…å¶çš„èº«ä»½è¯å‘½ä¸­è½¦è¾†ç§Ÿèµè¿çº¦åå•"""
        return self.__tdResult_spouse(item_id=2976224)

    def spouseRiskItem2976226(self):
        """spouseRiskItem2976226 ç”³è¯·äººé…å¶çš„èº«ä»½è¯å‘½ä¸­æ³•é™¢ç»“æ¡ˆåå•"""
        return self.__tdResult_spouse(item_id=2976226)

    def spouseRiskItem2976254(self):
        """spouseRiskItem2976254 ç”³è¯·äººé…å¶çš„æ‰‹æœºå·å‘½ä¸­è™šå‡å·ç åº“"""
        return self.__tdResult_spouse(item_id=2976254)

    def spouseRiskItem2976258(self):
        """spouseRiskItem2976258 ç”³è¯·äººé…å¶çš„æ‰‹æœºå·å‘½ä¸­è¯ˆéª—éªšæ‰°åº“"""
        return self.__tdResult_spouse(item_id=2976258)

    def spouseRiskItem2976266(self):
        """spouseRiskItem2976266 ç”³è¯·äººé…å¶çš„æ‰‹æœºå·å‘½ä¸­ä¿¡è´·é€¾æœŸåå•"""
        return self.__tdResult_spouse(item_id=2976266)

    def spouseRiskItem2976268(self):
        """spouseRiskItem2976268 ç”³è¯·äººé…å¶çš„æ‰‹æœºå·å‘½ä¸­è½¦è¾†ç§Ÿèµè¿çº¦åå•"""
        return self.__tdResult_spouse(item_id=2976268)

    def spouseRiskItem2976312(self):
        """spouseRiskItem2976312 ç”³è¯·äººé…å¶çš„å•ä½åç§°ç–‘ä¼¼ä¸­ä»‹å…³é”®è¯"""
        return self.__tdResult_spouse(item_id=2976312)

    def spouseRiskItem2976320(self):
        """spouseRiskItem2976320 ç”³è¯·äººé…å¶çš„3ä¸ªæœˆå†…èº«ä»½è¯å…³è”å¤šä¸ªç”³è¯·ä¿¡æ¯"""
        return self.__tdResult_spouse(item_id=2976320)

    def spouseRiskItem2976322(self):
        """spouseRiskItem2976322 ç”³è¯·äººé…å¶çš„3ä¸ªæœˆå†…ç”³è¯·ä¿¡æ¯å…³è”å¤šä¸ªèº«ä»½è¯"""
        return self.__tdResult_spouse(item_id=2976322)

    def spouseRiskItem2976340(self):
        """spouseRiskItem2976340 ç”³è¯·äººé…å¶çš„7å¤©å†…è®¾å¤‡æˆ–èº«ä»½è¯æˆ–æ‰‹æœºå·ç”³è¯·æ¬¡æ•°è¿‡å¤š"""
        return self.__tdResult_spouse(item_id=2976340)

    def spouseRiskItem2976354(self):
        """spouseRiskItem2976354 ç”³è¯·äººé…å¶çš„7å¤©å†…ç”³è¯·äººåœ¨å¤šä¸ªå¹³å°ç”³è¯·å€Ÿæ¬¾"""
        return self.__tdResult_spouse(item_id=2976354)

    def spouseRiskItem2976356(self):
        """spouseRiskItem2976356 ç”³è¯·äººé…å¶çš„1ä¸ªæœˆå†…ç”³è¯·äººåœ¨å¤šä¸ªå¹³å°ç”³è¯·å€Ÿæ¬¾"""
        return self.__tdResult_spouse(item_id=2976356)

    def spouseRiskItem2976372(self):
        """spouseRiskItem2976372 ç”³è¯·äººé…å¶çš„3ä¸ªæœˆå†…ç”³è¯·äººåœ¨å¤šä¸ªå¹³å°è¢«æ”¾æ¬¾_ä¸åŒ…å«æœ¬åˆä½œæ–¹"""
        return self.__tdResult_spouse(item_id=2976372)

    def spouseCredooScore(self):
        """spouseCredooScore å‰æµ·å¾ä¿¡ä¸­ç”³è¯·äººé…å¶çš„ç»¼åˆè¯„åˆ†"""
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
        """spouseLawRiskMsgNum æ±‡æ³•æ˜¯å¦å‘½ä¸­"""
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
                if zx.get("casetopic") not in status_list and zx.get("pctype")==u"è¢«å‘Š":
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
        """spouseLawExecutionState æ±‡æ³•[zhixing]æ¡ˆä»¶çŠ¶æ€"""
        return self.__hf_result_spouse(style='zhixing')

    def spouseLawCaseTopic(self):
        """spouseLawCaseTopic æ±‡æ³•[caipan]æ¶‰æ¡ˆäº‹ç”±"""
        return self.__hf_result_spouse(style='caipan')

    def spouseLawDishonestDetail(self):
        """spouseLawDishonestDetail æ±‡æ³•[shixin]å…·ä½“æƒ…å½¢"""
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
        """spouseLawExecutionTerm æ±‡æ³•[zhixing]æ‰§è¡ŒæœŸé™"""
        return self.__hf_month_money_spouse(style="month")

    def spouseLawExecutionMoney(self):
        """spouseLawExecutionMoney  æ±‡æ³•[zhixing]æ‰§è¡Œæ ‡çš„"""
        return self.__hf_month_money_spouse(style="money")

    def carDealerName(self):
        """carDealerName è¿”å›è½¦è¾†ç»é”€å•†ï¼ˆspï¼‰çš„åç§°"""
        if not self.info.result.get('data').get('dealerName'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('dealerName')

    def carRoomAddressProvince(self):
        """carRoomAddress å–ç”³è¯·äººçš„å±…ä½åœ°å€çœä»½"""
        if not self.info.result.get('data').get('homeProvince'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('homeProvince'))

    def carRoomAddressCity(self):
        """carRoomAddressCity å–ç”³è¯·äººçš„å±…ä½åœ°å€åŸå¸‚"""
        if not self.info.result.get('data').get('homeCity'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('homeCity'))

    def carHouseAddressProvince(self):
        """carHouseAddressProvince å–ç”³è¯·äººçš„æˆ·ç±åœ°å€çœä»½"""
        if not self.info.result.get('data').get('familyProvince'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('familyProvince'))

    def carHouseAddressCity(self):
        """carHouseAddressCity å–ç”³è¯·äººçš„æˆ·ç±åœ°å€åŸå¸‚"""
        if not self.info.result.get('data').get('familyCity'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('familyCity'))

    def carWorkAddressProvince(self):
        """carWorkAddressProvince å–ç”³è¯·äººçš„å·¥ä½œåœ°å€çœä»½"""
        if not self.info.result.get('data').get('workProvince'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('workProvince'))

    def carWorkAddressCity(self):
        """carWorkAddressCity å–ç”³è¯·äººçš„å·¥ä½œåœ°å€åŸå¸‚"""
        if not self.info.result.get('data').get('workCity'):
            return factor_encrypt_identity(self.SET_DEFAULT_VALUE_INT_9999999)
        return factor_encrypt_identity(self.info.result.get('data').get('workCity'))

    def keepAppointmentCreditScorely(self):
        """keepAppointmentCreditScorely å‰æµ·å¾ä¿¡ä¸­å±¥çº¦èƒ½åŠ›è¿™ä¸€é¡¹å¾—åˆ†"""
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
        """rejectCode å¤–éƒ¨æ•°æ®-æ–°ç½‘å¾ä¿¡æ‹’ç»åŸå› ç """
        if not self.info.result.get('data').get('rejectCode'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get('data').get('rejectCode')

    def pbocWhite(self):
        """pbocWhite å¤–éƒ¨æ•°æ®-æ–°ç½‘é“¶è¡Œå¾ä¿¡"""
        if not self.info.result.get('data').get('pbocWhite'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return int(self.info.result.get('data').get('pbocWhite'))

    def lastAuditResult(self):
        """lastAuditResult è½¦è´·ç³»ç»Ÿ-æœ€è¿‘ä¸€æ¬¡å®¡æ ¸ç»“æœ"""
        return self.info.result.get('data').get("lastAuditResult",self.SET_DEFAULT_VALUE_INT_9999999)

    def topFourPhone(self):
        """topFourPhone ç”³è¯·äººæ‰‹æœºå·å‰4ä½"""
        return self.info.phone[:4]

    def spouseTopFourPhone(self):
        """spouseTopFourPhone é…å¶æ‰‹æœºå·å‰4ä½"""
        if not self.info.result.get("data").get('spousePhone'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.info.result.get("data").get('spousePhone')[:4]

    def spouseGeoCurStatus(self):
        """spouseGeoCurStatus é›†å¥¥-ç”³è¯·äººé…å¶-æ‰‹æœºå·å½“å‰çŠ¶æ€"""
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
        """gpsPrice è½¦è´·ç³»ç»Ÿ-Gpsä»·æ ¼"""
        return int(self.info.result.get('data').get("gpsPrice",self.SET_DEFAULT_VALUE_INT_9999999))

    def carPrice(self):
        """carPrice è½¦è´·ç³»ç»Ÿ-è½¦æ¬¾"""
        return int(self.info.result.get('data').get("carPrice",self.SET_DEFAULT_VALUE_INT_9999999))

    def carInsurance(self):
        """carInsurance è½¦è´·ç³»ç»Ÿ-ä¿é™©"""
        return int(self.info.result.get('data').get("carInsurance",self.SET_DEFAULT_VALUE_INT_9999999))

    def carPurchaseTax(self):
        """carPurchaseTax è½¦è´·ç³»ç»Ÿ-è´­ç½®ç¨"""
        return int(self.info.result.get('data').get("carPurchaseTax",self.SET_DEFAULT_VALUE_INT_9999999))

    def applicantNation(self):
        """applicantNation è½¦è´·ç³»ç»Ÿ-æ°‘æ—"""
        return factor_encrypt_identity(self.info.result.get('data').get("applicantNation",self.SET_DEFAULT_VALUE_INT_9999999))

    def carProductType(self):
        """carProductType ç›´æ¥åˆ¤æ–­ç”³è¯·ä»¶æ˜¯å¦å…è®¸è‡ªåŠ¨å®¡æ‰¹é€šè¿‡"""
        return int(self.info.result.get('data').get("carProductType",self.SET_DEFAULT_VALUE_INT_9999999))

    def carRandom(self):
        """carRandom æ ¹æ®å®¢æˆ·çš„èº«ä»½è¯å·åšéšæœºæ•°ï¼Œå¦‚æœå®¢æˆ·è´­ä¹°å¤šå°è½¦ï¼Œè¿”å›åŒä¸€ä¸ªéšæœºæ•°"""
        return hash(str(self.info.cert_id))%2+1

    def carLoanAmount(self):
        """carLoanAmount æ”¾æ¬¾é‡‘é¢"""
        return int(self.info.result.get('data').get("cdwMakeLoanAmount",self.SET_DEFAULT_VALUE_INT_9999999))

    def carZoneCode(self):
        """carZoneCode å¤§åŒºä»£ç """
        code=self.info.result.get('data').get("carZoneCode")
        if not code:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if code=="å†…è’™å¤åŒº" or code=="åŒ—äº¬å¸‚" or code=="å¤©æ´¥å¸‚" or code=="å±±è¥¿çœ" or code=="æ²³åŒ—çœ":
            return 1
        if code=="å‰æ—çœ" or code=="è¾½å®çœ" or code=="é»‘é¾™æ±Ÿçœ":
            return 2
        if code=="ä¸Šæµ·å¸‚" or code=="å®‰å¾½çœ" or code=="å±±ä¸œçœ" or code=="æ±Ÿè‹çœ" or code=="æµ™æ±Ÿçœ":
            return 3
        if code=="å¹¿ä¸œçœ" or code=="å¹¿è¥¿çœ" or code=="æµ·å—çœ" or code=="ç¦å»ºçœ":
            return 4
        if code=="æ±Ÿè¥¿çœ" or code=="æ²³å—çœ" or code=="æ¹–åŒ—çœ" or code=="æ¹–å—çœ":
            return 5
        if code=="äº‘å—çœ" or code=="å››å·çœ" or code=="è´µå·çœ" or code=="é‡åº†å¸‚" or code=="è¥¿è—åŒº":
            return 6
        if code=="å®å¤åŒº" or code=="æ–°ç–†åŒº" or code=="ç”˜è‚ƒçœ" or code=="é™•è¥¿çœ" or code=="é’æµ·çœ":
            return 7
        if code=="é¦™æ¸¯ç‰¹åŒº" or code=="æ¾³é—¨ç‰¹åŒº":
            return 8
        return self.SET_DEFAULT_VALUE_INT_9999999

    def cdwPreRiskLevel(self):
        """cdwPreRiskLevel é¢„å®¡ç­‰çº§"""
        return self.info.result.get('data').get("precallRisklevel", self.SET_DEFAULT_VALUE_INT_9999999)


if __name__ == "__main__":
    serial_no = "1566180648828-A42A7451C0F093DBDAEE5F53F65BFBAB"
    a = CarFactorAuto('T1', serial_no)
    print (a.geoPhoneSelfMatch())