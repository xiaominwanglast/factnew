#coding:utf-8
import pytest,json
from default import Default
from DataForTest.galaxy import *
from utils.DES import Des
from utils.MongoUtil import  MongoPyUtil
from utils.MysqlUtil import MysqlPyUntil
from utils.threeDES import factor_decrypt_identity,factor_encrypt_identity

class TestScoreFactor(object):
    """自动审批测试"""
    certId=readCdwConfig('applicant',"identity")
    phone=readCdwConfig('applicant',"phone")
    userName=readCdwConfig('applicant',"name")

    currentTime = datetime.datetime.now()
    @classmethod
    def setup_class(cls):
        pass

    @pytest.fixture()
    def DataReady(self, envopt):
        MySqlData=MysqlPyUntil(env=envopt, db='skynet_embrace').queryNewOne(sql="SELECT * FROM skynet_factor_tmp WHERE delete_flag=0 ORDER BY id limit 1;")
        self.user_id = MySqlData.get('user_id')
        self.old_user_id = MySqlData.get('old_user_id')
        self.userinfo_name_score=MySqlData.get('userinfo_name_score')
        self.userinfo_identity_score=MySqlData.get('userinfo_identity_score')
        self.userinfo_phone_registion=MySqlData.get('userinfo_phone_registion')
        self.ocr_result = MySqlData.get('ocr_result')
        self.live_body_result = MySqlData.get('live_body_result')
        self.face_match_result = MySqlData.get('face_match_result')
        self.identity_match_result = MySqlData.get('identity_match_result')
        self.user_home_adress = MySqlData.get('user_home_adress')
        self.user_home_city = MySqlData.get('user_home_city')
        self.user_home_province = MySqlData.get('user_home_province')
        self.user_units_city = MySqlData.get('user_units_city')
        self.user_units_province = MySqlData.get('user_units_province')
        self.user_units_adress = MySqlData.get('user_units_adress')
        self.user_units_name = MySqlData.get('user_units_name')
        self.colleague_phone = MySqlData.get('colleague_phone')
        self.friend_phone = MySqlData.get('friend_phone')
        self.relatives_phone = MySqlData.get('relatives_phone')
        self.is_bind_card = MySqlData.get('is_bind_card')
        self.is_exist_credit_email = MySqlData.get('is_exist_credit_email')
        self.is_exist_zhengxin = MySqlData.get('is_exist_zhengxin')
        self.is_exist_taobao = MySqlData.get('is_exist_taobao')
        self.is_exist_alipay = MySqlData.get('is_exist_alipay')
        self.credit_is_itsself = MySqlData.get('credit_is_itsself')
        self.mxUserPhoneInTimeDays = MySqlData.get('mxUserPhoneInTimeDays')
        self.mxIsExistCarrier = MySqlData.get('mxIsExistCarrier')
        self.refuse_drools_sum = MySqlData.get('refuse_drools_sum')
        self.drools_count = MySqlData.get('drools_count')
        self.bjBlacklist = MySqlData.get('bjBlacklist')
        self.tdbbBlacklistResult = MySqlData.get('tdbbBlacklistResult')
        self.tdBlacklistResult = MySqlData.get('tdBlacklistResult')
        self.riskLevelScore = MySqlData.get('riskLevelScore')
        self.creditScore = MySqlData.get('creditScore')
        self.zfbCertified = MySqlData.get('zfbCertified')
        self.userinfoPhoneRegistionOld = MySqlData.get('userinfoPhoneRegistionOld','')
        self.deviceroot_num = MySqlData.get('deviceroot_num')

        self.MongoData=MongoPyUtil(env=envopt, db='skynet-feature').queryNewOne(collection='skynet_fact_info', find={'userinfoPhoneRegistionScore':self.userinfo_phone_registion})
        if self.MongoData:
            self.MongoDataOne=self.MongoData[0]
        else:
            self.MongoDataOne={}


    @pytest.fixture()
    def DataReadyV2(self, envopt):
        MySqlData=MysqlPyUntil(env=envopt, db='skynet_embrace').queryNewOne(sql="SELECT * FROM skynet_factor_tmp_v2 WHERE delete_flag=0 ORDER BY id limit 1;")
        self.user_id_v2 = MySqlData.get('user_id')
        self.userinfo_name_score_v2=MySqlData.get('userinfo_name_score')
        self.userinfo_identity_score_v2=MySqlData.get('userinfo_identity_score')
        self.userinfo_phone_registion_v2=MySqlData.get('userinfo_phone_registion')
        self.ocr_result_v2 = MySqlData.get('ocr_result')
        self.colleague_phone_v2  = MySqlData.get('colleague_phone')
        self.friend_phone_v2  = MySqlData.get('friend_phone')
        self.relatives_phone_v2  = MySqlData.get('relatives_phone')
        self.old_credit_num_score = MySqlData.get('old_credit_num_score')
        self.new_credit_num_score = MySqlData.get('new_credit_num_score')
        self.night_cnt_drools_xj_score= MySqlData.get('night_cnt_drools_xj_score')
        self.cnt_drools_xj_score = MySqlData.get('cnt_drools_xj_score')
        self.applist_score = MySqlData.get('applist_score')
        self.decision_result_score = MySqlData.get('decision_result_score')
        self.artificial_result_score = MySqlData.get('artificial_result_score')
        self.model_fraud_score = MySqlData.get('model_fraud_score')
        self.fraud_result_score = MySqlData.get('fraud_result_score')
        self.model_result_score = MySqlData.get('model_result_score')
        self.mo_refuse_apply_credit_number = MySqlData.get('mo_refuse_apply_credit_number')
        self.mo_refuse_apply_re_pre_borrow_number = MySqlData.get('mo_refuse_apply_re_pre_borrow_number')
        self.apply_credit_number = MySqlData.get('apply_credit_number')
        self.apply_re_pre_borrow_number = MySqlData.get('apply_re_pre_borrow_number')
        self.fr_refuse_apply_credit_number = MySqlData.get('fr_refuse_apply_credit_number')
        self.fr_refuse_apply_re_pre_borrow_number = MySqlData.get('fr_refuse_apply_re_pre_borrow_number')
        self.refuse_apply_re_pre_borrow_number = MySqlData.get('refuse_apply_re_pre_borrow_number')
        self.refuse_apply_credit_number = MySqlData.get('refuse_apply_credit_number')
        self.rto_refuse_drools_xj_score = MySqlData.get('rto_refuse_drools_xj_score')
        self.enter_ma_number_score = MySqlData.get('enter_ma_number_score')
        self.apply_re_pre_borrow_number_cache = MySqlData.get('apply_re_pre_borrow_number_cache')
        self.pre_borrow_cnt_drools_xj_score = MySqlData.get('pre_borrow_cnt_drools_xj_score')

        self.MongoDataV2=MongoPyUtil(env=envopt, db='skynet-feature').queryNewOne(collection='skynet_fact_info_v2', find={'userinfoPhoneRegistionScore':self.userinfo_phone_registion_v2})
        if self.MongoDataV2:
            self.MongoDataOneV2=self.MongoDataV2[0]
        else:
            self.MongoDataOneV2={}



    @pytest.mark.usefixtures("DataReady")
    def test1_userinfoIdentityScore(self):
        """用例1：申请人身份证号码 --类型:评分"""
        print ('风控评分输出-申请人身份证号码')
        print ('skynet_embrace/skynet_factor_tmp:'+str(self.userinfo_identity_score)+' || '+'skynet-feature/skynet_fact_info:'+str(self.MongoDataOne.get('userinfoIdentityScore')))
        assert self.userinfo_identity_score==self.MongoDataOne.get('userinfoIdentityScore')

    @pytest.mark.usefixtures("DataReady")
    def test2_userinfoNameScore(self):
        """用例2：用户姓名 --类型:评分"""
        print ('风控评分输出-用户姓名')
        print ('skynet_embrace/skynet_factor_tmp:'+str(self.userinfo_name_score)+' || '+'skynet-feature/skynet_fact_info:'+str(self.MongoDataOne.get('userinfoNameScore')))
        assert self.userinfo_name_score==self.MongoDataOne.get('userinfoNameScore')

    @pytest.mark.usefixtures("DataReady")
    def test3_userinfoPhoneRegistionScore(self):
        """用例3：注册手机号 --类型:评分"""
        print ('风控评分输出-注册手机号')
        print ('skynet_embrace/skynet_factor_tmp:'+str()+' || '+'skynet-feature/skynet_fact_info' )

    @pytest.mark.usefixtures("DataReady")
    def test4_userinfoPhoneRegistionOld(self):
        """用例4：历史注册手机号 --类型:评分"""
        print ('风控评分输出-历史注册手机号')
        print ('skynet_embrace/skynet_factor_tmp:'+str(self.userinfoPhoneRegistionOld)+' || '+'skynet-feature/skynet_fact_info:'+str(self.MongoDataOne.get('userinfoPhoneRegistionOld')))
        assert self.userinfoPhoneRegistionOld==self.MongoDataOne.get('userinfoPhoneRegistionOld')

    @pytest.mark.usefixtures("DataReady")
    def test5_liveBodyResultScore(self):
        """用例5：活体检测结果 --类型:评分"""
        print ('风控评分输出-活体检测结果')
        print ('skynet_embrace/skynet_factor_tmp:'+str(self.live_body_result)+' || '+'skynet-feature/skynet_fact_info:'+str(self.MongoDataOne.get('liveBodyResultScore')))
        if str(self.live_body_result)=='-1':
            self.live_body_result=Default.SET_DEFAULT_VALUE_INT_9999999
        assert self.live_body_result==self.MongoDataOne.get('liveBodyResultScore')

    @pytest.mark.usefixtures("DataReady")
    def test6_faceMatchResultScore(self):
        """用例6：人脸比对结果 --类型:评分"""
        print ('风控评分输出-人脸比对结果')
        print ('skynet_embrace/skynet_factor_tmp:'+str(self.face_match_result)+' || '+'skynet-feature/skynet_fact_info:'+str(self.MongoDataOne.get('faceMatchResultScore')))
        if str(self.face_match_result)=='-1':
            self.face_match_result=Default.SET_DEFAULT_VALUE_INT_9999999
        assert self.face_match_result==self.MongoDataOne.get('faceMatchResultScore')

    @pytest.mark.usefixtures("DataReady")
    def test7_identityMatchResultScore(self):
        """用例7：身份匹配结果 --类型:评分"""
        print ('风控评分输出-身份匹配结果')
        print ('skynet_embrace/skynet_factor_tmp:'+str(self.identity_match_result)+' || '+'skynet-feature/skynet_fact_info:'+str(self.MongoDataOne.get('identityMatchResultScore')))
        if str(self.identity_match_result)=='-1':
            self.identity_match_result=Default.SET_DEFAULT_VALUE_INT_9999999
        assert self.identity_match_result==self.MongoDataOne.get('identityMatchResultScore')

    @pytest.mark.usefixtures("DataReady")
    def test8_deviceRootNumScore(self):
        """用例8：客户申请时的手机设备已经越狱次数之和 --类型:评分"""
        print ('风控评分输出-客户申请时的手机设备已经越狱次数之和')
        print ('skynet_embrace/skynet_factor_tmp:'+str(self.deviceroot_num)+' || '+'skynet-feature/skynet_fact_info:'+str(self.MongoDataOne.get('deviceRootNumScore')))
        if not self.deviceroot_num:
            self.deviceroot_num=Default.SET_DEFAULT_VALUE_INT_9999999
        assert self.deviceroot_num==self.MongoDataOne.get('deviceRootNumScore')

    @pytest.mark.usefixtures("DataReady")
    def test9_userinfoHomeScore(self):
        """用例9：居住信息完整度 --类型:评分"""
        print ('风控评分输出-居住信息完整度')
        print ('skynet_embrace/skynet_factor_tmp:'+str(self.user_home_adress)+str(self.user_home_city)+str(self.user_home_province))
        count=0
        if self.user_home_adress:
            count+=1
        if self.user_home_city:
            count+=1
        if self.user_home_province:
            count+=1
        assert round(float(count)/3,4)==self.MongoDataOne.get('userinfoHomeScore')

    @pytest.mark.usefixtures("DataReady")
    def test10_unitsScore(self):
        """用例10：单位信息完整度 --类型:评分"""
        print ('风控评分输出-单位信息完整度')
        count=0
        if self.user_units_city:
            count+=1
        if self.user_units_province:
            count+=1
        if self.user_units_adress:
            count+=1
        if self.user_units_name:
            count+=1
        assert round(float(count)/4,4)==self.MongoDataOne.get('unitsScore')

    @pytest.mark.usefixtures("DataReady")
    def test11_phoneHomeUnitsCityScore(self,envopt):
        """用例11：手机号注册城市和其他三址是否一致 --类型:评分"""
        print ('风控评分输出-手机号注册城市和其他三址是否一致')
        if not self.userinfo_phone_registion or (not self.user_home_city and not self.user_units_city and not self.userinfo_identity_score):
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999995
        else:
            phoneRegistionCity=MysqlPyUntil(env=envopt, db='skynet').queryNewOne(sql="SELECT city FROM dict_mobile_location where mobile='%s' limit 1;"%factor_decrypt_identity(self.userinfo_phone_registion)[:7])
            RegistionCity= (phoneRegistionCity.get('city',"").replace("市",""))
            identityScoreCity=MysqlPyUntil(env=envopt, db='skynet').queryNewOne(sql="SELECT city FROM dict_idcard_location where code='%s' limit 1;"%factor_decrypt_identity(self.userinfo_identity_score)[:6])
            ScoreCity =identityScoreCity.get('city',"").replace("市","")
            homeCity=self.user_home_city.replace("市","")
            unitsCity=self.user_units_city.replace("市","")
            if RegistionCity==ScoreCity or RegistionCity==homeCity or RegistionCity==unitsCity:
                factorResult=Default.SET_DEFAULT_VALUE_INT_1
            else:
                factorResult=Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult==self.MongoDataOne.get('phoneHomeUnitsCityScore')

    @pytest.mark.usefixtures("DataReady")
    def test12_homeUnitsCityScore(self):
        """用例12：居住城市和工作城市是否一致 --类型:评分"""
        print ('风控评分输出-居住城市和工作城市是否一致')
        if not self.user_units_city or not self.user_home_city:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999995
        else:
            if self.user_units_city.replace("市","")==self.user_home_city.replace("市",""):
                factorResult=Default.SET_DEFAULT_VALUE_INT_1
            else:
                factorResult=Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult==self.MongoDataOne.get('homeUnitsCityScore')

    @pytest.mark.usefixtures("DataReady")
    def test13_relateDisphoneCntScore(self):
        """用例13：不同的联系人个数 --类型:评分"""
        print ('风控评分输出-不同的联系人个数')
        contact=[self.colleague_phone,self.friend_phone,self.relatives_phone]
        factorResult=len(list(set(contact)))
        assert factorResult==self.MongoDataOne.get('relateDisphoneCntScore')

    @pytest.mark.usefixtures("DataReady")
    def test14_relaOverdueDaysScore(self,envopt):
        """用例14：联系人-历史借款最大逾期天数 --类型:评分"""
        print ('风控评分输出-联系人-历史借款最大逾期天数')
        relativesPhoneData=MysqlPyUntil(env=envopt, db='skynet_embrace').queryNewOne(sql="SELECT * FROM skynet_factor_tmp WHERE userinfo_phone_registion='%s' and delete_flag=0 limit 1;"%self.relatives_phone)
        friendPhoneData=MysqlPyUntil(env=envopt, db='skynet_embrace').queryNewOne(sql="SELECT * FROM skynet_factor_tmp WHERE userinfo_phone_registion='%s' and delete_flag=0 limit 1;"%self.friend_phone)
        colleaguePhoneData=MysqlPyUntil(env=envopt, db='skynet_embrace').queryNewOne(sql="SELECT * FROM skynet_factor_tmp WHERE userinfo_phone_registion='%s' and delete_flag=0 limit 1;"%self.colleague_phone)
        newUserId=[]
        oldUserId=[]
        if relativesPhoneData:
            newUserId.append(relativesPhoneData.get('user_id'))
            if relativesPhoneData.get("old_user_id"):
                oldUserId.append(relativesPhoneData.get("old_user_id"))
        if friendPhoneData:
            newUserId.append(friendPhoneData.get('user_id'))
            if friendPhoneData.get("old_user_id"):
                oldUserId.append(friendPhoneData.get("old_user_id"))
        if colleaguePhoneData:
            newUserId.append(colleaguePhoneData.get('user_id'))
            if colleaguePhoneData.get("old_user_id"):
                oldUserId.append(colleaguePhoneData.get("old_user_id"))
        mongoResult=[]
        mysqlResult=[]
        for u in newUserId:
            mongoResultU=MongoPyUtil(env=envopt,db='skynet-feature').queryAll(collection='skynet_loan_info',find={"user_id":u})
            mongoResult=mongoResultU+mongoResult
        if oldUserId:
            oldUserIdStr=','.join(oldUserId)
            mysqlResult=MysqlPyUntil(env=envopt,db='skynet_fact_material').queryAll(sql="select * from all_fin_rownumber where user_id in (%s) "%oldUserIdStr)
        newOverdue=[(i.get('settle_date',self.currentTime)- i.get('repay_date')).days for i in mongoResult ]
        oldOverdue=[]
        for r in mysqlResult:
            if r.get('real_repayment_date')==None:
                real_repayment_date=self.currentTime.date()
            else:
                real_repayment_date=r.get('real_repayment_date')
            oldOverdue.append((real_repayment_date-r.get('next_pay_date')).days)
        if newOverdue and oldOverdue:
            maxOverdue=[max(newOverdue),max(oldOverdue),0]
        elif newOverdue and not oldOverdue:
            maxOverdue = [max(newOverdue), 0]
        elif not newOverdue and oldOverdue:
            maxOverdue = [max(oldOverdue), 0]
        else:
            maxOverdue =[0]
        assert max(maxOverdue)==self.MongoDataOne.get('relaOverdueDaysScore')

    @pytest.mark.usefixtures("DataReady")
    def test15_contactsPhoneHitFraudPhoneCntScore(self,envopt):
        """用例15：申请人的联系人手机号命中欺诈客户手机号个数 --类型:评分"""
        print ('风控评分输出-申请人的联系人手机号命中欺诈客户手机号个数')
        count=0
        for phone in [self.colleague_phone,self.friend_phone,self.relatives_phone]:
            if phone:
                mysqlResult=MysqlPyUntil(env=envopt,db='skynet_rota').queryAll(sql="select * from rota_fraud where phone='%s' and is_deleted=0"%phone)
                if mysqlResult:
                    count+=1
        assert count ==  self.MongoDataOne.get('contactsPhoneHitFraudPhoneCntScore')

    @pytest.mark.usefixtures("DataReady")
    def test16_hitBjblackScore(self):
        """用例16：命中冰鉴黑名单 --类型:评分"""
        print ('风控评分输出-命中冰鉴黑名单')
        print ('skynet_embrace/skynet_factor_tmp:'+str(self.bjBlacklist)+' || '+'skynet-feature/skynet_fact_info:'+str(self.MongoDataOne.get('hitBjblackScore')))
        if not self.bjBlacklist and self.bjBlacklist!=0:
            self.bjBlacklist=Default.SET_DEFAULT_VALUE_INT_9999999
        assert self.bjBlacklist==self.MongoDataOne.get('hitBjblackScore')

    @pytest.mark.usefixtures("DataReady")
    def test17_hitTdblackScore(self):
        """用例17：命中同盾黑名单 --类型:评分"""
        print ('风控评分输出-命中同盾黑名单')
        factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        if self.tdbbBlacklistResult or self.tdBlacklistResult:
            factorResult=1
        if self.tdbbBlacklistResult==0 or self.tdBlacklistResult==0:
            factorResult=0
        assert factorResult==self.MongoDataOne.get('hitTdblackScore')

    @pytest.mark.usefixtures("DataReady")
    def test18_zfbtaobaoAuthorizationScore(self):
        """用例18：支付宝或淘宝是否曾经授权 --类型:评分"""
        print ('风控评分输出-支付宝或淘宝是否曾经授权')
        factorResult=Default.SET_DEFAULT_VALUE_INT_0
        if self.is_exist_taobao==1 or self.is_exist_alipay==1:
            factorResult=1
        assert factorResult==self.MongoDataOne.get('zfbtaobaoAuthorizationScore')

    @pytest.mark.usefixtures("DataReady")
    def test19_zfbCertifiedScore(self):
        """用例19：支付宝是否实名认证 --类型:评分"""
        print ('风控评分输出-支付宝是否实名认证')
        factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        assert factorResult==self.MongoDataOne.get('zfbCertifiedScore')

    @pytest.mark.usefixtures("DataReady")
    def test20_creditIsItsselfScore(self):
        """用例20：账单是否是本人 --类型:评分"""
        print ('风控评分输出-账单是否是本人')
        print ('skynet_embrace/skynet_factor_tmp:'+str(self.credit_is_itsself)+' || '+'skynet-feature/skynet_fact_info:'+str(self.MongoDataOne.get('creditIsItsselfScore')))
        assert self.credit_is_itsself==self.MongoDataOne.get('creditIsItsselfScore')

    @pytest.mark.usefixtures("DataReady")
    def test21_mxUserPhoneInTimeDaysScore (self):
        """用例21：手机号入网天数 --类型:评分"""
        print ('风控评分输出-手机号入网天数')
        print ('skynet_embrace/skynet_factor_tmp:' + str(self.mxUserPhoneInTimeDays))
        assert self.mxUserPhoneInTimeDays==self.MongoDataOne.get('mxUserPhoneInTimeDaysScore')

    @pytest.mark.usefixtures("DataReady")
    def test22_mxIsExistCarrierScore(self):
        """用例22：是否抓取到运营商数据 --类型:评分"""
        print('风控评分输出-是否抓取到运营商数据')
        print('skynet_embrace/skynet_factor_tmp:' + str(self.mxIsExistCarrier))
        assert self.mxIsExistCarrier == self.MongoDataOne.get('mxIsExistCarrierScore')

    @pytest.mark.usefixtures("DataReady")
    def test23_isExistCreditReportScore(self):
        """用例23：是否有魔蝎征信报告 --类型:评分"""
        print('风控评分输出-是否有魔蝎征信报告')
        print('skynet_embrace/skynet_factor_tmp:' + str(self.is_exist_zhengxin))
        assert self.is_exist_zhengxin == self.MongoDataOne.get('isExistCreditReportScore')

    @pytest.mark.usefixtures("DataReady")
    def test24_isExistCreditScore(self):
        """用例24：是否有邮箱信用卡账单 --类型:评分"""
        print('风控评分输出-是否有邮箱信用卡账单')
        print('skynet_embrace/skynet_factor_tmp:' + str(self.is_exist_credit_email))
        assert self.is_exist_credit_email == self.MongoDataOne.get('isExistCreditScore')

    @pytest.mark.usefixtures("DataReady")
    def test25_bankScore(self):
        """用例25：是否绑定过银行卡 --类型:评分"""
        print('风控评分输出-是否绑定过银行卡')
        print('skynet_embrace/skynet_factor_tmp:' + str(self.is_bind_card))
        assert self.is_bind_card == self.MongoDataOne.get('bankScore')

    @pytest.mark.usefixtures("DataReady")
    def test26_hitInnerBlackScore(self,envopt):
        """用例26：命中内部名单的类型 --类型:评分"""
        print('风控评分输出-命中内部名单的类型')
        factorResult=Default.SET_DEFAULT_VALUE_INT_0
        phoneResult=[]
        badPhoneResult=[]
        fraudResult=[]
        phoneResult1=MysqlPyUntil(env=envopt, db='skynet_rota').queryAll(sql="select * from rota_overdue where cert_id='%s' and is_deleted=0" % self.userinfo_identity_score)
        oldPhone = self.userinfoPhoneRegistionOld.split(',')
        for p in oldPhone:
            if p:
                if MysqlPyUntil(env=envopt, db='skynet_rota').queryAll(sql="select * from rota_overdue where phone='%s' and is_deleted=0" %p):
                    phoneResult.append(MysqlPyUntil(env=envopt, db='skynet_rota').queryAll(sql="select * from rota_overdue where phone='%s' and is_deleted=0" %p))
        if phoneResult or phoneResult1:
            factorResult=3
        else:
            for p in oldPhone:
                if p:
                    if MysqlPyUntil(env=envopt, db='skynet_rota').queryAll(sql="select * from rota_bad where phone='%s' and is_deleted=0" %p):
                        badPhoneResult.append(MysqlPyUntil(env=envopt, db='skynet_rota').queryAll(sql="select * from rota_bad where phone='%s' and is_deleted=0" %p))
            if badPhoneResult:
                factorResult=2
            else:
                fraudResult1=MysqlPyUntil(env=envopt, db='skynet_rota').queryAll(sql="select * from rota_fraud where cert_id='%s' and is_deleted=0" % self.userinfo_identity_score)
                for p in oldPhone:
                    if p:
                        if MysqlPyUntil(env=envopt, db='skynet_rota').queryAll(sql="select * from rota_fraud where phone='%s' and is_deleted=0" % p):
                            fraudResult.append(MysqlPyUntil(env=envopt, db='skynet_rota').queryAll(sql="select * from rota_fraud where phone='%s' and is_deleted=0" % p))
                if fraudResult or fraudResult1:
                    factorResult=1
        assert factorResult == self.MongoDataOne.get('hitInnerBlackScore')

    @pytest.mark.usefixtures("DataReady")
    def test27_overduePctScore(self,envopt):
        """用例27：逾期次数占比 --类型:评分"""
        print('风控评分输出-逾期次数占比')
        mongoResult=MongoPyUtil(env=envopt,db='skynet-feature').queryAll(collection='skynet_loan_info',find={"user_id":self.user_id})
        mysqlResult=MysqlPyUntil(env=envopt,db='skynet_fact_material').queryAll(sql="select * from all_fin_rownumber where user_id='%s'"%self.old_user_id)
        newOverdue=[i for i in mongoResult if i.get('settle_date',self.currentTime-datetime.timedelta(hours=8))>i.get('repay_date') ]
        oldOverdue=[]
        for r in mysqlResult:
            if r.get('real_repayment_date')==None:
                real_repayment_date=self.currentTime.date()
            else:
                real_repayment_date=r.get('real_repayment_date')
            if real_repayment_date>r.get('next_pay_date'):
                 oldOverdue.append(r)
        if not mongoResult and not mysqlResult:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult=round(float(len(oldOverdue)+len(newOverdue))/(len(mongoResult)+len(mysqlResult)),4)
        assert factorResult==self.MongoDataOne.get('overduePctScore')

    @pytest.mark.usefixtures("DataReady")
    def test28_allMaxOverdueDaysPamthScore(self,envopt):
        """用例28：所有借款历史最大逾期天数 --类型:评分"""
        print('风控评分输出-所有借款历史最大逾期天数')
        mongoResult=MongoPyUtil(env=envopt,db='skynet-feature').queryAll(collection='skynet_loan_info',find={"user_id":self.user_id})
        mysqlResult=MysqlPyUntil(env=envopt,db='skynet_fact_material').queryAll(sql="select * from all_fin_rownumber where user_id='%s'"%self.old_user_id)
        newOverdue=[(i.get('settle_date',self.currentTime)- i.get('repay_date')).days for i in mongoResult ]
        oldOverdue=[]
        for r in mysqlResult:
            if r.get('real_repayment_date')==None:
                real_repayment_date=self.currentTime.date()
            else:
                real_repayment_date=r.get('real_repayment_date')
            oldOverdue.append((real_repayment_date-r.get('next_pay_date')).days)
        maxOverdue=[max(newOverdue),max(oldOverdue),0]
        assert max(maxOverdue)==self.MongoDataOne.get('allMaxOverdueDaysPamthScore')

    @pytest.mark.usefixtures("DataReady")
    def test29_currentOverdueStatusPamthScore(self,envopt):
        """用例29：当前逾期状态 --类型:评分"""
        print('风控评分输出-当前逾期状态')
        mongoResult=MongoPyUtil(env=envopt,db='skynet-feature').queryAll(collection='skynet_loan_info',find={"user_id":self.user_id})
        mysqlResult=MysqlPyUntil(env=envopt,db='skynet_fact_material').queryAll(sql="select * from all_fin_rownumber where user_id='%s'"%self.old_user_id)
        newOverdue=[i for i in mongoResult if not i.get('settle_date') ]
        oldOverdue=[]
        for r in mysqlResult:
            if r.get('real_repayment_date')==None:
                 oldOverdue.append(r)

        if not mongoResult and not mysqlResult:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            if newOverdue or oldOverdue:
                factorResult=Default.SET_DEFAULT_VALUE_INT_1
            else:
                factorResult=Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult==self.MongoDataOne.get('currentOverdueStatusPamthScore')

    @pytest.mark.usefixtures("DataReady")
    def test30_creditScore(self):
        """用例30：客户最近一次申请时的授信额度 --类型:评分"""
        print('风控评分输出-客户最近一次申请时的授信额度')
        print('skynet_embrace/skynet_factor_tmp:' + str(self.creditScore))
        assert self.creditScore == self.MongoDataOne.get('creditScore')

    @pytest.mark.usefixtures("DataReady")
    def test31_riskLevelScore(self):
        """用例31：客户最近一次申请时的风控评级 --类型:评分"""
        print('风控评分输出-客户最近一次申请时的风控评级')
        print('skynet_embrace/skynet_factor_tmp:' + str(self.riskLevelScore))
        assert self.riskLevelScore == self.MongoDataOne.get('riskLevelScore')

    @pytest.mark.usefixtures("DataReady")
    def test32_rtoRefuseOfDroolsXjScore(self):
        """用例32：2345借款平台下产品调用drools被拒绝比例（不包含缓存） --类型:评分"""
        print('风控评分输出-2345借款平台下产品调用drools被拒绝比例（不包含缓存）')
        if not self.drools_count:
            factorResult =Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult=round(float(self.refuse_drools_sum)/self.drools_count,4)
        assert factorResult==self.MongoDataOne.get('rtoRefuseOfDroolsXjScore')

    @pytest.mark.usefixtures("DataReady")
    def test33_relatePhoneHitBadPhonecntScore(self,envopt):
        """用例33：申请人的联系人手机号命中不良手机号的个数 --类型:评分"""
        print('风控评分输出-申请人的联系人手机号命中不良手机号的个数')
        count=0
        for phone in [self.colleague_phone,self.friend_phone,self.relatives_phone]:
            if phone:
                mysqlResult=MysqlPyUntil(env=envopt,db='skynet_rota').queryAll(sql="select * from rota_bad where phone='%s' and is_deleted=0"%phone)
                if mysqlResult:
                    count+=1
        assert count ==  self.MongoDataOne.get('relatePhoneHitBadPhonecntScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test34_relaRelationBlacklistScore(self,envopt):
        """用例34：联系人手机号码命内部黑名单的个数 --类型:评分"""
        print ("联系人手机号码命内部黑名单的个数")
        count=0
        for phone in [self.friend_phone_v2,self.relatives_phone_v2,self.colleague_phone_v2]:
            mongoResult=MongoPyUtil(env=envopt,db='galaxy').queryNewOne(collection='own_black_record',find={"phone":phone})
            if mongoResult:
                count+=1
        assert count == self.MongoDataOneV2.get('relaRelationBlacklistScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test35_userinfoAgeScore(self):
        """用例35：用户年龄 --类型:评分"""
        print ("用户年龄")
        if not self.userinfo_identity_score_v2:
            factorResult = Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult = int(self.currentTime.strftime('%Y')) - int(self.userinfo_identity_score_v2[6:10])
        assert factorResult==self.MongoDataOneV2.get('relaRelationBlacklistScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test36_ocrresultScore(self):
        """用例36：Ocr结果 --类型:评分"""
        if not self.ocr_result_v2 and self.ocr_result_v2!=0:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        elif self.ocr_result_v2==-1:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult=self.ocr_result_v2
        assert factorResult==self.MongoDataOneV2.get('ocrresultScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test37_relatephoneCntScore(self):
        """用例37：联系人个数
         --类型:评分"""
        print ("联系人个数")
        count=0
        if self.relatives_phone_v2:
            count+=1
        if self.colleague_phone_v2:
            count+=1
        if self.friend_phone_v2:
            count+=1
        assert count==self.MongoDataOneV2.get('relatephoneCntScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test38_contactsPhoneHitOverduePhoneCntScore(self,envopt):
        """用例38：申请人的联系人手机号命中逾期客户手机号个数 --类型:评分"""
        print ("申请人的联系人手机号命中逾期客户手机号个数")
        contacts = (self.relatives_phone_v2, self.colleague_phone_v2, self.friend_phone_v2)
        count = 0
        for p in contacts:
            if p!='':
                result = MysqlPyUntil(env=envopt,db='skynet_rota').queryAll(sql="select * from rota_overdue where phone ='{0}' and is_deleted=0".format(p))
                if result:
                    count = count + 1
        assert count==self.MongoDataOneV2.get('contactsPhoneHitOverduePhoneCntScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test39_userinfoCreditcardAgeScore(self,envopt):
        """用例39：人行征信-最早卡龄 --类型:评分"""
        print ("人行征信-最早卡龄")
        mongoResult = MongoPyUtil(env=envopt, db='galaxy').queryAll(collection='mx_zhengxin_report',find={"user_id": self.user_id_v2})
        if not mongoResult:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            create_time=mongoResult[-1].get("create_time")
            response=(str(mongoResult[-1].get("response"),encoding='utf-8'))
            responseJson=json.loads(response)
            creditCardRecordDetailAnalyzes=responseJson.get("creditCardRecordDetailAnalyzes")
            if not creditCardRecordDetailAnalyzes:
                factorResult = Default.SET_DEFAULT_VALUE_INT_9999999
            else:
                minCreditCardData=min([datetime.datetime.strptime(i.get("grant_date") , "%Y-%m-%d") for i in creditCardRecordDetailAnalyzes])
                factorResult=(create_time.year - minCreditCardData.year) * 12 + (create_time.month - minCreditCardData.month)
                if create_time.day>minCreditCardData.day:
                    factorResult=factorResult+1
        assert factorResult==self.MongoDataOneV2.get('userinfoCreditcardAgeScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test40_userinfoLoanAgeScore(self,envopt):
        """用例40：人行征信-最早贷龄 --类型:评分"""
        print ("人行征信-最早贷龄")
        mongoResult = MongoPyUtil(env=envopt, db='galaxy').queryAll(collection='mx_zhengxin_report',find={"user_id": self.user_id_v2})
        if not mongoResult:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            create_time=mongoResult[-1].get("create_time")
            response=(str(mongoResult[-1].get("response"),encoding='utf-8'))
            responseJson=json.loads(response)
            otherLoanRecordDetailAnalyzes=responseJson.get("otherLoanRecordDetailAnalyzes")
            housingLoanRecordDetailAnalyzes=responseJson.get("housingLoanRecordDetailAnalyzes")
            if not otherLoanRecordDetailAnalyzes and not housingLoanRecordDetailAnalyzes:
                factorResult = Default.SET_DEFAULT_VALUE_INT_9999999
            else:
                otherLoanData=[datetime.datetime.strptime(i.get("grant_date") , "%Y-%m-%d") for i in otherLoanRecordDetailAnalyzes]
                housingLoanData=[datetime.datetime.strptime(i.get("grant_date") , "%Y-%m-%d") for i in housingLoanRecordDetailAnalyzes]
                minLoanDate=min(otherLoanData+housingLoanData)
                factorResult=(create_time.year - minLoanDate.year) * 12 + (create_time.month - minLoanDate.month)
        assert factorResult==self.MongoDataOneV2.get('userinfoLoanAgeScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test41_creditOverdue3mCntScore(self,envopt):
        """用例41：逾期超过90天的月数 --类型:评分"""
        print ("逾期超过90天的月数")
        mongoResult = MongoPyUtil(env=envopt, db='galaxy').queryAll(collection='mx_zhengxin_report',find={"user_id": self.user_id_v2})
        if not mongoResult:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            response=(str(mongoResult[-1].get("response"),encoding='utf-8'))
            responseJson=json.loads(response)
            creditCardRecordDetailAnalyzes = responseJson.get("creditCardRecordDetailAnalyzes")
            otherLoanRecordDetailAnalyzes=responseJson.get("otherLoanRecordDetailAnalyzes")
            housingLoanRecordDetailAnalyzes=responseJson.get("housingLoanRecordDetailAnalyzes")
            if not creditCardRecordDetailAnalyzes and not otherLoanRecordDetailAnalyzes and not housingLoanRecordDetailAnalyzes:
                factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
            else:
                otherLoanData=[i.get("nintydays_overdue_month") for i in otherLoanRecordDetailAnalyzes if i.get("nintydays_overdue_month")]
                housingLoanData=[i.get("nintydays_overdue_month") for i in housingLoanRecordDetailAnalyzes if i.get("nintydays_overdue_month")]
                creditCardData=[i.get("nintydays_overdue_month") for i in creditCardRecordDetailAnalyzes if i.get("nintydays_overdue_month")]
                factorResult=sum(otherLoanData+housingLoanData+creditCardData)
        assert factorResult==self.MongoDataOneV2.get('creditOverdue3mCntScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test42_creditOverdueCurrentOrgCntScore(self,envopt):
        """用例42：用户当前逾期机构数 --类型:评分"""
        print ("用户当前逾期机构数")
        mongoResult = MongoPyUtil(env=envopt, db='galaxy').queryAll(collection='mx_zhengxin_report',find={"user_id": self.user_id_v2})
        if not mongoResult:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            response=(str(mongoResult[-1].get("response"),encoding='utf-8'))
            responseJson=json.loads(response)
            creditCardRecordDetailAnalyzes = responseJson.get("creditCardRecordDetailAnalyzes")
            otherLoanRecordDetailAnalyzes=responseJson.get("otherLoanRecordDetailAnalyzes")
            housingLoanRecordDetailAnalyzes=responseJson.get("housingLoanRecordDetailAnalyzes")
            if not creditCardRecordDetailAnalyzes and not otherLoanRecordDetailAnalyzes and not housingLoanRecordDetailAnalyzes:
                factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
            else:
                otherLoanData=[i for i in otherLoanRecordDetailAnalyzes if float(i.get('overdue_amount'))!=0.0 ]
                housingLoanData=[i for i in housingLoanRecordDetailAnalyzes if float(i.get('overdue_amount'))!=0.0 ]
                creditCardData=[i for i in creditCardRecordDetailAnalyzes if float(i.get('overdue_amount'))!=0.0 ]
                factorResult=len(otherLoanData+housingLoanData+creditCardData)
        assert factorResult==self.MongoDataOneV2.get('creditOverdue3mCntScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test43_creditPaymentAmountScore(self,envopt):
        """用例43：用户当前负债额 --类型:评分"""
        print ("用户当前负债额")
        mongoResult = MongoPyUtil(env=envopt, db='galaxy').queryAll(collection='mx_zhengxin_report',find={"user_id": self.user_id_v2})
        if not mongoResult:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            response=(str(mongoResult[-1].get("response"),encoding='utf-8'))
            responseJson=json.loads(response)
            creditCardRecordDetailAnalyzes = responseJson.get("creditCardRecordDetailAnalyzes")
            otherLoanRecordDetailAnalyzes=responseJson.get("otherLoanRecordDetailAnalyzes")
            housingLoanRecordDetailAnalyzes=responseJson.get("housingLoanRecordDetailAnalyzes")
            if not creditCardRecordDetailAnalyzes and not otherLoanRecordDetailAnalyzes and not housingLoanRecordDetailAnalyzes:
                factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
            else:
                otherLoanData=[(datetime.datetime.strptime(i.get("expiration_date") , "%Y-%m-%d"), datetime.datetime.strptime(i.get("grant_date") , "%Y-%m-%d"),i.get("loan_amount")) for i in otherLoanRecordDetailAnalyzes if i.get('expiration_date') and i.get('grant_date')]
                housingLoanData=[(datetime.datetime.strptime(i.get("expiration_date") , "%Y-%m-%d"), datetime.datetime.strptime(i.get("grant_date") , "%Y-%m-%d"),i.get("loan_amount")) for i in housingLoanRecordDetailAnalyzes if i.get('expiration_date') and i.get('grant_date')]
                creditCardData=[i.get('used_credit_line') for i in creditCardRecordDetailAnalyzes]
                otherLoan=[round(float(i[2])/(int((i[0]-i[1]).days/30)),2) for i in otherLoanData]
                housingLoan=[round(float(i[2])/(int((i[0]-i[1]).days/30)),2) for i in housingLoanData]
                factorResult=str(round(sum(creditCardData)+sum(otherLoan)+sum(housingLoan),2))
        assert factorResult==self.MongoDataOneV2.get('creditPaymentAmountScore')

    @pytest.mark.usefixtures("DataReady")
    @pytest.mark.usefixtures("DataReadyV2")
    def test44_meanOverdueDaysScore(self,envopt):
        """用例44：平均逾期天数 --类型:评分"""
        print ("平均逾期天数")
        mongoResult = MongoPyUtil(env=envopt, db='skynet-feature').queryAll(collection='skynet_loan_info',find={"user_id": self.user_id_v2})
        mysqlResult = MysqlPyUntil(env=envopt, db='skynet_fact_material').queryAll(sql="select * from all_fin_rownumber where user_id =%s" % self.old_user_id)
        borrowCnt=len(mongoResult)+len(mysqlResult)
        Overdue = [(i.get('settle_date', self.currentTime-datetime.timedelta(hours=8)) - i.get('repay_date')).days for i in mongoResult if (i.get('settle_date', self.currentTime) - i.get('repay_date')).days>0]
        for r in mysqlResult:
            if r.get('real_repayment_date')==None:
                real_repayment_date=self.currentTime.date()
            else:
                real_repayment_date=r.get('real_repayment_date')
            if (real_repayment_date-r.get('next_pay_date')).days>0:
                Overdue.append((real_repayment_date-r.get('next_pay_date')).days)
        if borrowCnt==0:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult=round(float(sum(Overdue))/borrowCnt,4)
        print (borrowCnt,sum(Overdue))
        assert factorResult==self.MongoDataOneV2.get('meanOverdueDaysScore')

    @pytest.mark.usefixtures("DataReady")
    @pytest.mark.usefixtures("DataReadyV2")
    def test45_histDealNumXjScore(self,envopt):
        """用例45：客户在我司历史累计成交次数（不包含车贷和卡贷王） --类型:评分"""
        print ("客户在我司历史累计成交次数（不包含车贷和卡贷王）")
        mongoResult = MongoPyUtil(env=envopt, db='skynet-feature').queryAll(collection='skynet_loan_info',find={"user_id": self.user_id_v2})
        mysqlResult = MysqlPyUntil(env=envopt, db='skynet_fact_material').queryAll(sql="select * from all_fin_rownumber where user_id =%s" % self.old_user_id)
        mongoResultNotKdw=[i for i in mongoResult if i.get('product_id')not in (101,200)]
        mysqlResultDkw=[i for i in mysqlResult if i.get('bank_type')!=10002]
        mysqlResultJkd=[i for i in mysqlResult if i.get('bank_type')==10002 or i.get('bank_type')==10001]
        count=0
        if mysqlResultDkw:
            count+=1
        if mysqlResultJkd:
            count+=1
        count=count+len(mongoResultNotKdw)
        assert count == self.MongoDataOneV2.get('histDealNumXjScore')

    @pytest.mark.usefixtures("DataReady")
    @pytest.mark.usefixtures("DataReadyV2")
    def test46_histDealAmtXjScore(self, envopt):
        """用例46：客户在我司历史累计成交金额（不包含车贷和卡贷王） --类型:评分"""
        print("客户在我司历史累计成交金额（不包含车贷和卡贷王）")
        mongoResult = MongoPyUtil(env=envopt, db='skynet-feature').queryAll(collection='skynet_loan_info',find={"user_id": self.user_id_v2})
        mysqlResult = MysqlPyUntil(env=envopt, db='skynet_fact_material').queryAll(sql="select * from all_fin_rownumber where user_id =%s" % self.old_user_id)
        mongoResultNotKdw=[float(i.get("total_principal")) for i in mongoResult if i.get('product_id')not in (101,200)]
        mysqlResult=[float(i.get('amount')) for i in mysqlResult]
        if not mongoResultNotKdw and not mysqlResult:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult=sum(mongoResultNotKdw)+sum(mysqlResult)
        assert factorResult == self.MongoDataOneV2.get('histDealAmtXjScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test47_creditNumScore(self):
        """用例47：开户产品数 --类型:评分"""
        print("开户产品数")
        oldProduct=[]
        newProduct=[]
        if self.old_credit_num_score:
            oldProduct=self.old_credit_num_score.split(',')
        if self.new_credit_num_score:
            newProduct=self.new_credit_num_score.split(',')
        factorResult=len(oldProduct)+len(newProduct)
        assert factorResult== self.MongoDataOneV2.get('creditNumScore')

    @pytest.mark.usefixtures("DataReady")
    @pytest.mark.usefixtures("DataReadyV2")
    def test48_dealProductTypePamthScore(self,envopt):
        """用例48：历史成交产品 --类型:评分"""
        print("历史成交产品")
        mongoResult = MongoPyUtil(env=envopt, db='skynet-feature').queryAll(collection='skynet_loan_info',find={"user_id": self.user_id_v2})
        mysqlResult = MysqlPyUntil(env=envopt, db='skynet_fact_material').queryAll(sql="select * from all_fin_rownumber where user_id =%s" % self.old_user_id)
        mongoResultNotCDW=[i.get("product_id") for i in mongoResult if i.get('product_id') not in (200,101)]
        mysqlResultDkw=[i for i in mysqlResult if i.get('bank_type')!=10002]
        mysqlResultJkd=[i for i in mysqlResult if i.get('bank_type')==10002 or i.get('bank_type')==10001]
        productCount=0
        if mysqlResultDkw:
            productCount+=1
        if mysqlResultJkd:
            productCount+=1
        productCount=productCount+len(list(set(mongoResultNotCDW)))
        if not productCount:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult=productCount
        assert factorResult == self.MongoDataOneV2.get('dealProductTypePamthScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test49_nightCntOfDroolsXjScore(self):
        """用例49：风控夜间决策拒绝比例 --类型:评分"""
        print ("风控夜间决策拒绝比例")
        if not self.night_cnt_drools_xj_score:
            factorResult = Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult = self.night_cnt_drools_xj_score
        assert factorResult == self.MongoDataOneV2.get('nightCntOfDroolsXjScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test50_cntOfDroolsXjScore(self):
        """用例50：跑drools的次数(去缓存) --类型:评分"""
        print ("跑drools的次数(去缓存)")
        if not self.cnt_drools_xj_score:
            factorResult = Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult = self.cnt_drools_xj_score
        assert factorResult == self.MongoDataOneV2.get('cntOfDroolsXjScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test51_applistScore(self):
        """用例51：客户最近一次申请时的applistScore（20190315之前--包含20190315） --类型:评分"""
        print ("客户最近一次申请时的applistScore（20190315之前--包含20190315）")
        assert float(self.applist_score) == self.MongoDataOneV2.get('applistScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test52_decisionresultScore(self):
        """用例52：客户最近一次申请的最终决策结果（20190315之前--包含20190315） --类型:评分"""
        print ("客户最近一次申请的最终决策结果（20190315之前--包含20190315）")
        assert self.decision_result_score == self.MongoDataOneV2.get('decisionresultScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test53_artificialresultScore(self):
        """用例53：客户最近一次申请的人工审批结果（20190315之前--包含20190315） --类型:评分"""
        print ("客户最近一次申请的人工审批结果（20190315之前--包含20190315）")
        assert self.artificial_result_score == self.MongoDataOneV2.get('artificialresultScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test54_modelFraudScore(self):
        """用例54：客户最近一次申请的模型和反欺诈审批结果（20190315之前--包含20190315） --类型:评分"""
        print ("客户最近一次申请的模型和反欺诈审批结果（20190315之前--包含20190315）")
        assert self.model_fraud_score == self.MongoDataOneV2.get('modelFraudScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test55_fraudresultScore(self):
        """用例55：客户最近一次申请的反欺诈审批结果（20190315之前--包含20190315） --类型:评分"""
        print ("客户最近一次申请的反欺诈审批结果（20190315之前--包含20190315）")
        assert self.fraud_result_score == self.MongoDataOneV2.get('fraudresultScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test56_modelresultScore(self):
        """用例56：客户最近一次申请的模型审批结果（20190315之前--包含20190315） --类型:评分"""
        print ("客户最近一次申请的模型审批结果（20190315之前--包含20190315）")
        assert self.model_result_score == self.MongoDataOneV2.get('modelresultScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test57_modelresultpctScore(self):
        """用例57：模型拒绝比例 --类型:评分"""
        print ("模型拒绝比例")
        if self.apply_credit_number + self.apply_re_pre_borrow_number==0:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult=round(float(self.mo_refuse_apply_credit_number+self.mo_refuse_apply_re_pre_borrow_number)/(self.apply_credit_number+self.apply_re_pre_borrow_number),4)
        assert factorResult == float(self.MongoDataOneV2.get('modelresultpctScore'))

    @pytest.mark.usefixtures("DataReadyV2")
    def test58_fraudresultpctScore(self):
        """用例58：反欺诈拒绝比例 --类型:评分"""
        print ("反欺诈拒绝比例")
        if self.apply_credit_number + self.apply_re_pre_borrow_number==0:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult = round(float(self.fr_refuse_apply_credit_number + self.fr_refuse_apply_re_pre_borrow_number) / (self.apply_credit_number + self.apply_re_pre_borrow_number), 4)
        assert factorResult == self.MongoDataOneV2.get('modelresultpctScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test59_modelfraudRejectcntRefuseScore(self):
        """用例59：模型和反欺诈拒绝比例 --类型:评分"""
        print ("模型和反欺诈拒绝比例")
        if self.apply_credit_number + self.apply_re_pre_borrow_number==0:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            factorResult = round(float(self.refuse_apply_re_pre_borrow_number + self.refuse_apply_credit_number) / (self.apply_credit_number + self.apply_re_pre_borrow_number_cache), 4)
        assert factorResult == float(self.MongoDataOneV2.get('modelfraudRejectcntRefuseScore'))

    @pytest.mark.usefixtures("DataReadyV2")
    def test60_rtoRefuseOfDroolsXjHiScore(self):
        """用例60：2345借款平台下产品调用drools被拒绝比例（包含缓存） --类型:评分"""
        print ("2345借款平台下产品调用drools被拒绝比例（包含缓存）")
        assert self.rto_refuse_drools_xj_score == self.MongoDataOneV2.get('rtoRefuseOfDroolsXjHiScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test61_enterNumberScore(self):
        """用例61：2345借款平台下产品调用drools被拒绝比例（包含缓存） --类型:评分"""
        print ("2345借款平台下产品调用drools被拒绝比例（包含缓存）")
        assert self.enter_ma_number_score == self.MongoDataOneV2.get('enterNumberScore')


    @pytest.mark.usefixtures("DataReadyV2")
    def test62_preBorrowCntOfDroolsXjScore(self):
        """用例62：2345借款平台调用drools预借环节次数（包含缓存） --类型:评分"""
        print ("2345借款平台调用drools预借环节次数（包含缓存）")
        assert self.pre_borrow_cnt_drools_xj_score == self.MongoDataOneV2.get('preBorrowCntOfDroolsXjScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test63_tbRegisterMonthScore(self,envopt):
        """用例63：淘宝用户注册的时间距今的月份数 --类型:评分"""
        print ("淘宝用户注册的时间距今的月份数")
        mongoData=MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_taobao_userinfo', find={'user_id':self.user_id_v2})
        if not mongoData or not mongoData[0].get("register_time"):
            factorResult = Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            year = (mongoData[0].get("create_time").year-mongoData[0].get("register_time").year)
            month= (mongoData[0].get("create_time").month-mongoData[0].get("register_time").month)
            day= (mongoData[0].get("create_time").day-mongoData[0].get("register_time").day)
            if day<0:
                factorResult=year*12+month-1
            else:
                factorResult=year*12+month+1
        assert factorResult==self.MongoDataOneV2.get('tbRegisterMonthScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test64_zfbRegisterMonthScore(self,envopt):
        """用例64：支付宝用户注册的时间距今的月份数 --类型:评分"""
        print ("支付宝用户注册的时间距今的月份数")
        mongoData=MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_alipay_bills_data', find={'user_id':self.user_id_v2})
        if not mongoData:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            response=json.loads((mongoData[0].get("response")).decode('utf-8'))
            register_time=datetime.datetime.strptime(response.get("userinfo").get("register_time")[:19].replace("T",' '), "%Y-%m-%d %H:%M:%S")
            year = (mongoData[0].get("create_time").year-register_time.year)
            month= (mongoData[0].get("create_time").month-register_time.month)
            day= (mongoData[0].get("create_time").day-register_time.day)
            if day<0:
                factorResult=year*12+month-1
            else:
                factorResult=year*12+month+1
        assert factorResult == self.MongoDataOneV2.get('zfbRegisterMonthScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test65_tbPhoneNumberAgreementScore(self,envopt):
        """用例65：淘宝绑定账号的手机号与注册客户手机号是否一致 --类型:评分"""
        print ("淘宝绑定账号的手机号与注册客户手机号是否一致")
        mongoData = MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_taobao_userinfo',find={'user_id': self.user_id_v2})
        if not mongoData:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            phone_number = factor_decrypt_identity(mongoData[0].get("phone_number"))
            if phone_number[:3]==factor_decrypt_identity(self.userinfo_phone_registion_v2)[:3] and phone_number[-2:]==factor_decrypt_identity(self.userinfo_phone_registion_v2)[-2:]:
                factorResult=Default.SET_DEFAULT_VALUE_INT_1
            else:
                factorResult=Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult == self.MongoDataOneV2.get('zfbPhoneNumberAgreementScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test66_zfbPhoneNumberAgreementScore(self,envopt):
        """用例66：支付宝绑定账号的手机号与注册客户手机号是否一致 --类型:评分"""
        print ("支付宝绑定账号的手机号与注册客户手机号是否一致")
        mongoData = MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_alipay_bills_data',find={'user_id': self.user_id_v2})
        if not mongoData:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            response = json.loads((mongoData[0].get("response")).decode('utf-8'))
            phone_number = response.get("userinfo").get("phone_number")
            print (phone_number)
            print (factor_decrypt_identity(self.userinfo_phone_registion_v2))
            if phone_number[:3]==factor_decrypt_identity(self.userinfo_phone_registion_v2)[:3] and phone_number[-2:]==factor_decrypt_identity(self.userinfo_phone_registion_v2)[-2:]:
                factorResult=Default.SET_DEFAULT_VALUE_INT_1
            else:
                factorResult=Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult == self.MongoDataOneV2.get('zfbPhoneNumberAgreementScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test67_publicFundScore(self,envopt):
        """用例67：是否有公积金记录 --类型:评分"""
        print ("是否有公积金记录")
        mongoData=MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_fund_bill', find={'user_id':self.user_id_v2})
        if mongoData:
            factorResult=Default.SET_DEFAULT_VALUE_INT_1
        else:
            factorResult=Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult == self.MongoDataOneV2.get('publicFundScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test68_socialInsuranceScore(self,envopt):
        """用例68：是否有社保记录 --类型:评分"""
        print ("是否有社保记录")
        mongoBillData = MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_security_bill',find={'user_id': self.user_id_v2})
        mongoReportData = MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_security_report',find={'user_id': self.user_id_v2})
        if mongoBillData or mongoReportData:
            factorResult=Default.SET_DEFAULT_VALUE_INT_1
        else:
            factorResult=Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult == self.MongoDataOneV2.get('socialInsuranceScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test69_mxUserinfoIdAuthenticateIdSameScore(self,envopt):
        """用例69：注册身份证号与客户授权手机号对应的实名身份证号是否一致 --类型:评分"""
        print ("注册身份证号与客户授权手机号对应的实名身份证号是否一致")
        mongoData = MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_carrier_basic_message',find={'user_id': self.user_id_v2})
        if not mongoData:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            name=factor_decrypt_identity(mongoData[0].get('name')).replace('*','')
            idcard=factor_decrypt_identity(mongoData[0].get("idcard"))
            mysqlIdcard=factor_decrypt_identity(self.userinfo_identity_score_v2)
            idcardNoXing=[]
            count=0
            for i in idcard:
                if i=='*':
                    idcardNoXing.append(mysqlIdcard[count])
                else:
                    idcardNoXing.append(i)
                count+=1
            idcardNoXingStr=''.join(idcardNoXing)
            if name==factor_decrypt_identity(self.userinfo_name_score_v2) and idcardNoXingStr== mysqlIdcard:
                factorResult=Default.SET_DEFAULT_VALUE_INT_1
            else:
                factorResult=Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult == self.MongoDataOneV2.get('mxUserinfoIdAuthenticateIdSameScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test70_zfbIdCardNumberAgreementScore(self,envopt):
        """用例70：支付宝用户身份证号码与注册客户身份证号码是否一致 --类型:评分"""
        print ("支付宝用户身份证号码与注册客户身份证号码是否一致")
        mongoData = MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_alipay_bills_data',find={'user_id': self.user_id_v2})
        if not mongoData:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            response = json.loads((mongoData[0].get("response")).decode('utf-8'))
            idcard_number = response.get("userinfo").get("idcard_number")
            if idcard_number[0]==factor_decrypt_identity(self.userinfo_identity_score_v2)[0] and idcard_number[-1]==factor_decrypt_identity(self.userinfo_identity_score_v2)[-1]:
                factorResult=Default.SET_DEFAULT_VALUE_INT_1
            else:
                factorResult=Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult == self.MongoDataOneV2.get('zfbIdCardNumberAgreementScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test71_tbNameAgreementScore(self,envopt):
        """用例71：淘宝用户姓名与注册客户姓名是否一致 --类型:评分"""
        print ("淘宝用户姓名与注册客户姓名是否一致")
        mongoData = MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_taobao_userinfo',find={'user_id': self.user_id_v2})
        if not mongoData:
            factorResult= Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            real_name=mongoData[0].get("real_name")
            if real_name == factor_decrypt_identity(self.userinfo_name_score_v2):
                factorResult=Default.SET_DEFAULT_VALUE_INT_1
            else:
                factorResult=Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult == self.MongoDataOneV2.get('tbNameAgreementScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test72_zfbNameAgreementScore(self,envopt):
        """用例72：支付宝用户姓名与注册客户姓名是否一致 --类型:评分"""
        print ("支付宝用户姓名与注册客户姓名是否一致")
        mongoData = MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_alipay_bills_data',find={'user_id': self.user_id_v2})
        if not mongoData:
            factorResult=Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            response = json.loads((mongoData[0].get("response")).decode('utf-8'))
            user_name = response.get("userinfo").get("user_name")
            if user_name == factor_decrypt_identity(self.userinfo_name_score_v2):
                factorResult = Default.SET_DEFAULT_VALUE_INT_1
            else:
                factorResult = Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult == self.MongoDataOneV2.get('zfbNameAgreementScore')

    @pytest.mark.usefixtures("DataReadyV2")
    def test73_mxUserinfoPhoneAuthenticatePhSameScore(self,envopt):
        """用例73：注册手机号与客户授权手机号是否一致 --类型:评分"""
        print ("注册手机号与客户授权手机号是否一致")
        mongoData = MongoPyUtil(env=envopt, db='galaxy').queryNewOne(collection='mx_carrier_basic_message',find={'user_id': self.user_id_v2})
        if not mongoData:
            factorResult = Default.SET_DEFAULT_VALUE_INT_9999999
        else:
            mobile = factor_decrypt_identity(mongoData[0].get("mobile"))
            phone = factor_decrypt_identity(self.userinfo_phone_registion_v2)
            if mobile==phone:
                factorResult = Default.SET_DEFAULT_VALUE_INT_1
            else:
                factorResult = Default.SET_DEFAULT_VALUE_INT_0
        assert factorResult == self.MongoDataOneV2.get('mxUserinfoPhoneAuthenticatePhSameScore')