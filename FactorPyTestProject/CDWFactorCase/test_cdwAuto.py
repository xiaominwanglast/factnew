#coding:utf-8
from utils.DoorlsFactor import DoorlsFactor
import pytest
from default import Default
from ProductApi.CarDecisionApiAuto import CarDecisionApiAuto
from CarFactorCollect.CarFactorAuto import CarFactorAuto
from DataForTest.galaxy import *
from utils.MongoUtil import MongoPyUtilPort
import datetime,time
from utils.threeDES import factor_encrypt_identity
class TestcdwAutoFactor(object):
    """自动审批测试"""
    productCode=readCdwConfig('cdwAuto',"productCode")
    sceneCode=readCdwConfig('cdwAuto',"sceneCode")
    certId=readCdwConfig('applicant',"identity")
    phone=readCdwConfig('applicant',"phone")
    userName=readCdwConfig('applicant',"name")

    spouseIdNumber=readCdwConfig('applicant',"identity")
    spousePhone=readCdwConfig('applicant',"phone")
    spouseName=readCdwConfig('applicant',"name")

    serial_no=''
    currentTime=datetime.datetime.now()-datetime.timedelta(hours=8)

    @classmethod
    def setup_class(cls):
        pass

    def teardown_method(self, method):
        print('\n测试用例执行完毕')
        time.sleep(0.5)

    @pytest.fixture()
    def cdwLoanProduct_test1DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'loanProduct':''})
        self.test=CarFactorAuto(env=envopt,serial_no=self.serial_no).cdwLoanProduct()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwLoanProduct')

    @pytest.mark.usefixtures("cdwLoanProduct_test1DataReady")
    def test1_cdwLoanProduct(self):
        """用例1：车贷王中的贷款产品 --类型:接口传参"""
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==Default.SET_DEFAULT_VALUE_STR_9999999

    @pytest.fixture()
    def cdwLoanProduct_test2DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'loanProduct':'10'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwLoanProduct()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwLoanProduct')

    @pytest.mark.usefixtures("cdwLoanProduct_test2DataReady")
    def test2_cdwLoanProduct(self):
        """用例2：车贷王中的贷款产品 --类型:接口传参"""
        print ('车贷访问风控接口传参loanProduct为非空值')
        print(self.serial_no," test:",self.test," dev:",self.dev)
        assert self.test==self.dev

    @pytest.fixture()
    def cdwLoanAmount_test1DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'loanAmount':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwLoanAmount()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwLoanAmount')

    @pytest.mark.usefixtures("cdwLoanAmount_test1DataReady")
    def test3_cdwLoanAmount(self):
        """用例3：车贷融资总额  --类型:接口传参"""
        print ('车贷访问风控接口传参loanAmount为空')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==Default.SET_DEFAULT_VALUE_FLOAT_9999999

    @pytest.fixture()
    def cdwLoanAmount_test2DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'loanAmount':10000000.0})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwLoanAmount()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwLoanAmount')

    @pytest.mark.usefixtures("cdwLoanAmount_test2DataReady")
    def test4_cdwLoanAmount(self):
        """用例4：车贷融资总额 --类型:接口传参"""
        print ('车贷访问风控接口传参loanAmount为非空值')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==float(self.test)

    @pytest.fixture()
    def cdwLoanTerm_test1DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'loanTerm':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwLoanTerm()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwLoanTerm')

    @pytest.mark.usefixtures("cdwLoanTerm_test1DataReady")
    def test5_cdwLoanTerm(self):
        """用例5：贷款期限 --类型:接口传参"""
        print ('车贷访问风控接口传参loanTerm为空')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==Default.SET_DEFAULT_VALUE_INT_9999999

    @pytest.fixture()
    def cdwLoanTerm_test2DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'loanTerm':12})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwLoanTerm()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwLoanTerm')

    @pytest.mark.usefixtures("cdwLoanTerm_test2DataReady")
    def test6_cdwLoanTerm(self):
        """用例6：贷款期限 --类型:接口传参"""
        print ('车贷访问风控接口传参loanTerm为非空值')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==int(self.test)

    @pytest.fixture()
    def cdwVehicleType_test1DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'vehicleType':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwVehicleType()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwVehicleType')

    @pytest.mark.usefixtures("cdwVehicleType_test1DataReady")
    def test7_cdwVehicleType(self):
        """用例7：车辆类型：非能源汽车 --类型:接口传参"""
        print ('车贷访问风控接口传参vehicleType为空')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==Default.SET_DEFAULT_VALUE_STR_9999999

    @pytest.fixture()
    def cdwVehicleType_test2DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'vehicleType':'大众朗逸-280TSI DSG舒适版'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwVehicleType()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwVehicleType')

    @pytest.mark.usefixtures("cdwVehicleType_test2DataReady")
    def test8_cdwVehicleType(self):
        """用例8：车辆类型：非能源汽车 --类型:接口传参"""
        print ('车贷访问风控接口传参vehicleType为非空值')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==self.test

    @pytest.fixture()
    def cdwLenderAge_test1DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwLenderAge()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwLenderAge')

    @pytest.mark.usefixtures("cdwLenderAge_test1DataReady")
    def test9_loanProductApplyStatus(self):
        """用例9：cdwLenderAge 贷款人的年龄 --类型:接口传参"""
        print ('车贷访问风控接口传参vehicleType为空')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==self.test

    @pytest.fixture()
    def cdwRegisterLocationMatchBlacklist_test1DataReady(self,envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='cdw_city_black_record', dataDict={'city': '内蒙古'})
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'registerLocation':'内蒙古'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwRegisterLocationMatchBlacklist()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwRegisterLocationMatchBlacklist')

    @pytest.mark.usefixtures("cdwRegisterLocationMatchBlacklist_test1DataReady")
    def test10_cdwRegisterLocationMatchBlacklist(self):
        """用例10：cdwRegisterLocationMatchBlacklist 最终车辆上牌地区是否命中黑名单  --类型:接口传参"""
        print ('上牌地区未命中黑名单')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==self.test

    @pytest.fixture()
    def cdwRegisterLocationMatchBlacklist_test2DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='cdw_city_black_record', dataList=[{'city': '内蒙古','cityName':'内蒙古','isDelete':0 ,'createTime':self.currentTime}])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'registerLocation': '内蒙古'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwRegisterLocationMatchBlacklist()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwRegisterLocationMatchBlacklist')

    @pytest.mark.usefixtures("cdwRegisterLocationMatchBlacklist_test2DataReady")
    def test11_cdwRegisterLocationMatchBlacklist(self):
        """用例11：cdwRegisterLocationMatchBlacklist 最终车辆上牌地区是否命中黑名单  --类型:接口传参"""
        print('上牌地区命中黑名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwLenderGender_test1DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'gender':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwLenderGender()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwLenderGender')

    @pytest.mark.usefixtures("cdwLenderGender_test1DataReady")
    def test12_cdwLenderGender(self):
        """用例12：贷款人性别 --类型:接口传参"""
        print ('车贷访问风控接口传参gender为空')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==Default.SET_DEFAULT_VALUE_INT_9999999

    @pytest.fixture()
    def cdwLenderGender_test2DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'gender':22})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwLenderGender()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwLenderGender')

    @pytest.mark.usefixtures("cdwLenderGender_test2DataReady")
    def test13_cdwLenderGender(self):
        """用例13：贷款人性别  --类型:接口传参"""
        print ('车贷访问风控接口传参gender为非空值')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==int(self.test)

    @pytest.fixture()
    def cdwMaritalStatus_test1DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'maritalStatus':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwMaritalStatus()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwMaritalStatus')

    @pytest.mark.usefixtures("cdwMaritalStatus_test1DataReady")
    def test14_cdwMaritalStatus(self):
        """用例14：贷款人婚姻状况 --类型:接口传参"""
        print ('车贷访问风控接口传参gender为空')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==Default.SET_DEFAULT_VALUE_INT_9999999

    @pytest.fixture()
    def cdwMaritalStatus_test2DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'maritalStatus':1})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwMaritalStatus()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwMaritalStatus')

    @pytest.mark.usefixtures("cdwMaritalStatus_test2DataReady")
    def test15_cdwMaritalStatus(self):
        """用例15：贷款人婚姻状况 --类型:接口传参"""
        print ('车贷访问风控接口传参gender为非空值')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==int(self.test)

    @pytest.fixture()
    def cdwCzcbDebtScore_test1DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'czcbDebtScore':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbDebtScore()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwCzcbDebtScore')

    @pytest.mark.usefixtures("cdwCzcbDebtScore_test1DataReady")
    def test16_cdwCzcbDebtScore(self):
        """用例16：稠银-个人负债评分 --类型:接口传参"""
        print ('车贷访问风控接口传参czcbDebtScorer为空')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==Default.SET_DEFAULT_VALUE_INT_9999999

    @pytest.fixture()
    def cdwCzcbDebtScore_test2DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'czcbDebtScore':50.0})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbDebtScore()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwCzcbDebtScore')

    @pytest.mark.usefixtures("cdwCzcbDebtScore_test2DataReady")
    def test17_cdwCzcbDebtScore(self):
        """用例17：稠银-个人负债评分 --类型:接口传参"""
        print ('车贷访问风控接口传参czcbDebtScore为非空值')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==float(self.test)

    @pytest.fixture()
    def cdwCzcbGeneralScore_test1DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'czcbGeneralScore':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbGeneralScore()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwCzcbGeneralScore')

    @pytest.mark.usefixtures("cdwCzcbGeneralScore_test1DataReady")
    def test18_cdwCzcbGeneralScore(self):
        """用例18：稠银-个人综合评分 --类型:接口传参"""
        print ('车贷访问风控接口传参czcbDebtScorer为空')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==Default.SET_DEFAULT_VALUE_INT_9999999

    @pytest.fixture()
    def cdwCzcbGeneralScore_test2DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'czcbGeneralScore':50.0})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbGeneralScore()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwCzcbGeneralScore')

    @pytest.mark.usefixtures("cdwCzcbGeneralScore_test2DataReady")
    def test19_cdwCzcbGeneralScore(self):
        """用例19：稠银-个人综合评分 --类型:接口传参"""
        print ('车贷访问风控接口传参czcbDebtScore为非空值')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==float(self.test)

    @pytest.fixture()
    def cdwCzcbOverdueScore_test1DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'czcbOverdueScore':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbOverdueScore()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwCzcbOverdueScore')

    @pytest.mark.usefixtures("cdwCzcbOverdueScore_test1DataReady")
    def test20_cdwCzcbOverdueScore(self):
        """用例20：稠银-个人逾期评分 --类型:接口传参"""
        print ('车贷访问风控接口传参czcbDebtScorer为空')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==Default.SET_DEFAULT_VALUE_INT_9999999

    @pytest.fixture()
    def cdwCzcbOverdueScore_test2DataReady(self,envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'czcbOverdueScore':50.0})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbOverdueScore()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwCzcbOverdueScore')

    @pytest.mark.usefixtures("cdwCzcbOverdueScore_test2DataReady")
    def test21_cdwCzcbOverdueScore(self):
        """用例21：稠银-个人逾期评分 --类型:接口传参"""
        print ('车贷访问风控接口传参czcbDebtScore为非空值')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==float(self.test)

    @pytest.fixture()
    def cdwAgentNameMatchWhitelist_test1DataReady(self,envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='cdw_dealer_white_record', dataList=[{'dealer':'1077','dealerName': '1077','dealerType':'B','isDelete':0 ,'createTime':self.currentTime}])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'agentName':'1077'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwAgentNameMatchWhitelist()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwAgentNameMatchWhitelist')

    @pytest.mark.usefixtures("cdwAgentNameMatchWhitelist_test1DataReady")
    def test22_cdwAgentNameMatchWhitelist(self):
        """用例22：经销商是否命中白名单 --类型:接口传参"""
        print ('车贷访问风控接口传参agentName为B类经销商')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==self.test

    @pytest.fixture()
    def cdwAgentNameMatchWhitelist_test2DataReady(self,envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='cdw_dealer_white_record', dataList=[{'dealer':'1072','dealerName': '1072','dealerType':'A','isDelete':0 ,'createTime':self.currentTime}])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'agentName':'1072'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwAgentNameMatchWhitelist()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwAgentNameMatchWhitelist')

    @pytest.mark.usefixtures("cdwAgentNameMatchWhitelist_test2DataReady")
    def test23_cdwAgentNameMatchWhitelist(self):
        """用例23：经销商是否命中白名单 --类型:接口传参"""
        print ('车贷访问风控接口传参agentName为A类经销商')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==self.test

    @pytest.fixture()
    def cdwAgentNameMatchWhitelist_test3DataReady(self,envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='cdw_dealer_white_record', dataList=[{'dealer':'1047','dealerName': '1047','dealerType':'C','isDelete':0 ,'createTime':self.currentTime}])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'agentName':'1047'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwAgentNameMatchWhitelist()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwAgentNameMatchWhitelist')

    @pytest.mark.usefixtures("cdwAgentNameMatchWhitelist_test3DataReady")
    def test24_cdwAgentNameMatchWhitelist(self):
        """用例24：经销商是否命中白名单 --类型:接口传参"""
        print ('车贷访问风控接口传参agentName为C类经销商')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==self.test

    @pytest.fixture()
    def cdwAgentNameMatchWhitelist_test4DataReady(self,envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='cdw_dealer_white_record', dataList=[{'dealer':'1000','dealerName': '1000','dealerType':'D','isDelete':0 ,'createTime':self.currentTime}])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'agentName':'1000'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwAgentNameMatchWhitelist()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwAgentNameMatchWhitelist')

    @pytest.mark.usefixtures("cdwAgentNameMatchWhitelist_test4DataReady")
    def test25_cdwAgentNameMatchWhitelist(self):
        """用例25：经销商是否命中白名单 --类型:接口传参"""
        print ('车贷访问风控接口传参agentName为t其他类(非A类，B类，C类)经销商')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==self.test

    @pytest.fixture()
    def cdwAgentNameMatchWhitelist_test5DataReady(self,envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteAllData(collection='cdw_dealer_white_record')
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'agentName':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwAgentNameMatchWhitelist()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwAgentNameMatchWhitelist')

    @pytest.mark.usefixtures("cdwAgentNameMatchWhitelist_test5DataReady")
    def test26_cdwAgentNameMatchWhitelist(self):
        """用例26：经销商是否命中白名单 --类型:接口传参"""
        print ('车贷访问风控接口传参agentName为空')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==Default.SET_DEFAULT_VALUE_INT_9999999

    @pytest.fixture()
    def cdwAgentNameMatchWhitelist_test6DataReady(self,envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='cdw_dealer_white_record', dataList=[{'dealer':'1047','dealerName': '1047','dealerType':'C','isDelete':1 ,'createTime':self.currentTime}])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode, sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone, userName=self.userName, test_data={'agentName':'1047'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwAgentNameMatchWhitelist()
        self.dev=DoorlsFactor(env=envopt,serial_no=self.serial_no).get_Factor('cdwAgentNameMatchWhitelist')

    @pytest.mark.usefixtures("cdwAgentNameMatchWhitelist_test6DataReady")
    def test27_cdwAgentNameMatchWhitelist(self):
        """用例27：经销商是否命中白名单 --类型:接口传参"""
        print ('车贷访问风控接口传参agentName为C类经销商,但是已逻辑删除')
        print (self.serial_no," test:",self.test," dev:",self.dev)
        assert self.dev==Default.SET_DEFAULT_VALUE_INT_0

    @pytest.fixture()
    def cdwCzcbDebtRiskResult_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbDebtRiskResult':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbDebtRiskResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbDebtRiskResult')

    @pytest.mark.usefixtures("cdwCzcbDebtRiskResult_test1DataReady")
    def test28_cdwCzcbDebtRiskResult(self):
        """用例28：稠银-个人综合评定结果 --类型:接口传参"""
        print('车贷访问风控接口传参czcbDebtRiskResult为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == Default.SET_DEFAULT_VALUE_STR_9999999

    @pytest.fixture()
    def cdwCzcbDebtRiskResult_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbDebtRiskResult': '建议拒绝'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbDebtRiskResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbDebtRiskResult')

    @pytest.mark.usefixtures("cdwCzcbDebtRiskResult_test2DataReady")
    def test29_cdwCzcbDebtRiskResult(self):
        """用例29：稠银-个人综合评定结果 --类型:接口传参"""
        print('车贷访问风控接口传参czcbDebtRiskResult为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwCzcbOverdueRiskResult_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbOverdueRiskResult':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbOverdueRiskResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbOverdueRiskResult')

    @pytest.mark.usefixtures("cdwCzcbOverdueRiskResult_test1DataReady")
    def test30_cdwCzcbOverdueRiskResult(self):
        """用例30：稠银-个人逾期评定结果 --类型:接口传参"""
        print('车贷访问风控接口传参czcbGeneralRiskResult为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == Default.SET_DEFAULT_VALUE_STR_9999999

    @pytest.fixture()
    def cdwCzcbOverdueRiskResult_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbOverdueRiskResult': '人工复合'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbOverdueRiskResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbOverdueRiskResult')

    @pytest.mark.usefixtures("cdwCzcbOverdueRiskResult_test2DataReady")
    def test31_cdwCzcbOverdueRiskResult(self):
        """用例31：稠银-个人逾期评定结果 --类型:接口传参"""
        print('车贷访问风控接口传参czcbGeneralRiskResult为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwOutOfAuthorizedDistrict_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'outOfAuthorizedDistrict':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwOutOfAuthorizedDistrict()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwOutOfAuthorizedDistrict')

    @pytest.mark.usefixtures("cdwOutOfAuthorizedDistrict_test1DataReady")
    def test32_cdwOutOfAuthorizedDistrict(self):
        """用例32：是否超出授权区域范围 --类型:接口传参"""
        print('车贷访问风控接口传参outOfAuthorizedDistrict为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwOutOfAuthorizedDistrict_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'outOfAuthorizedDistrict': 0})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwOutOfAuthorizedDistrict()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwOutOfAuthorizedDistrict')

    @pytest.mark.usefixtures("cdwOutOfAuthorizedDistrict_test2DataReady")
    def test33_cdwOutOfAuthorizedDistrict(self):
        """用例33：是否超出授权区域范围 --类型:接口传参"""
        print('车贷访问风控接口传参outOfAuthorizedDistrict为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwIdCardAppearCount_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'idCardAppearCount':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwIdCardAppearCount()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwIdCardAppearCount')

    @pytest.mark.usefixtures("cdwIdCardAppearCount_test1DataReady")
    def test34_cdwIdCardAppearCount(self):
        """用例34：车贷系统的身份证号出现次数 --类型:接口传参"""
        print('车贷访问风控接口传参idCardAppearCount为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwIdCardAppearCount_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'idCardAppearCount': 5})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwIdCardAppearCount()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwIdCardAppearCount')

    @pytest.mark.usefixtures("cdwIdCardAppearCount_test2DataReady")
    def test35_cdwIdCardAppearCount(self):
        """用例35：车贷系统的身份证号出现次数 --类型:接口传参"""
        print('车贷访问风控接口传参idCardAppearCount为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwIdCardExpired_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'idCardExpired':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwIdCardExpired()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwIdCardExpired')

    @pytest.mark.usefixtures("cdwIdCardAppearCount_test1DataReady")
    def test36_cdwIdCardExpired(self):
        """用例36：身份证号是否超出有效期 --类型:接口传参"""
        print('车贷访问风控接口传参idCardAppearCount为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwIdCardExpired_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'idCardExpired': 0})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwIdCardExpired()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwIdCardExpired')

    @pytest.mark.usefixtures("cdwIdCardAppearCount_test2DataReady")
    def test37_cdwIdCardExpired(self):
        """用例37：身份证号是否超出有效期 --类型:接口传参"""
        print('车贷访问风控接口传参idCardAppearCount为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwIsLcv_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'isLcv':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwIsLcv()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwIsLcv')

    @pytest.mark.usefixtures("cdwIsLcv_test1DataReady")
    def test38_cdwIsLcv(self):
        """用例38：是否为轻型商用车 --类型:接口传参"""
        print('车贷访问风控接口传参isLcv为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwIsLcv_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'isLcv': 1})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwIsLcv()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwIsLcv')

    @pytest.mark.usefixtures("cdwIsLcv_test2DataReady")
    def test39_cdwIsLcv(self):
        """用例39：是否为轻型商用车 --类型:接口传参"""
        print('车贷访问风控接口传参isLcv为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def pbocInfo_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'pbocInfo':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).pbocInfo()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('pbocInfo')

    @pytest.mark.usefixtures("pbocInfo_test1DataReady")
    def test40_pbocInfo(self):
        """用例40：chouzhou --类型:接口传参"""
        print('车贷访问风控接口传参pbocInfo为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == Default.SET_DEFAULT_VALUE_STR_9999999

    @pytest.fixture()
    def pbocInfo_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'pbocInfo': 'chouzhou'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).pbocInfo()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('pbocInfo')

    @pytest.mark.usefixtures("pbocInfo_test2DataReady")
    def test41_pbocInfo(self):
        """用例41：chouzhou --类型:接口传参"""
        print('车贷访问风控接口传参pbocInfo为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def pbocResult_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'pbocResult':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).pbocResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('pbocResult')

    @pytest.mark.usefixtures("pbocResult_test1DataReady")
    def test42_pbocResult(self):
        """用例42：pbocResult --类型:接口传参"""
        print('车贷访问风控接口传参pbocResult为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == Default.SET_DEFAULT_VALUE_STR_9999999

    @pytest.fixture()
    def pbocResult_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'pbocResult': 'D'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).pbocResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('pbocResult')

    @pytest.mark.usefixtures("pbocResult_test2DataReady")
    def test43_pbocResult(self):
        """用例43：pbocResult --类型:接口传参"""
        print('车贷访问风控接口传参pbocResult为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwIsSpouseIdMatch_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'spouseIdNumber': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwIsSpouseIdMatch()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwIsSpouseIdMatch')

    @pytest.mark.usefixtures("cdwIsSpouseIdMatch_test1DataReady")
    def test44_cdwIsSpouseIdMatch(self):
        """用例44：配偶身份证前6位与用户是否一致 --类型:用户信息"""
        print('车贷访问风控接口传参spouseIdNumber为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwIsSpouseIdMatch_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'spouseIdNumber':str(self.certId)[:6]+"199009012916"})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwIsSpouseIdMatch()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwIsSpouseIdMatch')

    @pytest.mark.usefixtures("cdwIsSpouseIdMatch_test2DataReady")
    def test45_cdwIsSpouseIdMatch(self):
        """用例45：配偶身份证前6位与用户是否一致 --类型:用户信息"""
        print('车贷访问风控接口传参spouseIdNumber前6位预申请人一致')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwIsSpouseIdMatch_test3DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'spouseIdNumber': "391321199009012916"})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwIsSpouseIdMatch()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwIsSpouseIdMatch')

    @pytest.mark.usefixtures("cdwIsSpouseIdMatch_test3DataReady")
    def test46_cdwIsSpouseIdMatch(self):
        """用例46：配偶身份证前6位与用户是否一致 --类型:用户信息"""
        print('车贷访问风控接口传参spouseIdNumber前6位预申请人不一致')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwNoRelationContactCnt_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'noRelationContactCnt': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwNoRelationContactCnt()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwNoRelationContactCnt')

    @pytest.mark.usefixtures("cdwNoRelationContactCnt_test1DataReady")
    def test47_cdwNoRelationContactCnt(self):
        """用例47：关系为0的联系人个数 --类型:接口传参"""
        print('车贷访问风控接口传参noRelationContactCnt为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwNoRelationContactCnt_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'noRelationContactCnt':3})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwNoRelationContactCnt()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwNoRelationContactCnt')

    @pytest.mark.usefixtures("cdwNoRelationContactCnt_test2DataReady")
    def test48_cdwNoRelationContactCnt(self):
        """用例48：关系为0的联系人个数 --类型:接口传参"""
        print('车贷访问风控接口传参noRelationContactCnt为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwNetPrice_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'netPrice': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwNetPrice()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwNetPrice')

    @pytest.mark.usefixtures("cdwNetPrice_test1DataReady")
    def test49_cdwNetPrice(self):
        """用例49：（经销商填写）指导价 --类型:接口传参"""
        print('车贷访问风控接口传参noRelationContactCnt为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwNetPrice_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'netPrice':11000000.0})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwNetPrice()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwNetPrice')

    @pytest.mark.usefixtures("cdwNetPrice_test2DataReady")
    def test50_cdwNoRelationContactCnt(self):
        """用例50：（经销商填写）指导价 --类型:接口传参"""
        print('车贷访问风控接口传参noRelationContactCnt为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == float(self.test)

    @pytest.fixture()
    def cdwCzcbRiskNote_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbRiskNote':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbRiskNote()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbRiskNote')

    @pytest.mark.usefixtures("cdwCzcbRiskNote_test1DataReady")
    def test51_cdwCzcbRiskNote(self):
        """用例51：稠银-稠银征信返回的备注信息 --类型:接口传参"""
        print('车贷访问风控接口传参czcbRiskNote为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwCzcbRiskNote_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbRiskNote': '个人信息记录良好'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbRiskNote()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbRiskNote')

    @pytest.mark.usefixtures("cdwCzcbRiskNote_test2DataReady")
    def test52_cdwCzcbRiskNote(self):
        """用例52：稠银-稠银征信返回的备注信息 --类型:接口传参"""
        print('车贷访问风控接口传参czcbRiskNote为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwCzcbPbocResult_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbGeneralRiskResult':'','czcbDebtRiskResult':'','czcbOverdueRiskResult':'','czcbGeneralScore':-1,'czcbOverdueScore':200})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbPbocResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbPbocResult')

    @pytest.mark.usefixtures("cdwCzcbPbocResult_test1DataReady")
    def test53_cdwCzcbPbocResult(self):
        """用例53：综合稠州银行返回的六个信息做一个综合结论 --类型:接口传参"""
        print('车贷访问风控接口传参czcbGeneralRiskResult为空值、czcbDebtRiskResult为空值、czcbOverdueRiskResult为空值、czcbOverdueScore为200分')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwCzcbPbocResult_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbGeneralRiskResult':'建议拒绝','czcbDebtRiskResult':'','czcbOverdueRiskResult':'','czcbGeneralScore':4,'czcbOverdueScore':900})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbPbocResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbPbocResult')

    @pytest.mark.usefixtures("cdwCzcbPbocResult_test2DataReady")
    def test54_cdwCzcbPbocResult(self):
        """用例54：综合稠州银行返回的六个信息做一个综合结论 --类型:接口传参"""
        print('车贷访问风控接口传参czcbGeneralRiskResult为空值、czcbDebtRiskResult为空值、czcbOverdueRiskResult为空值、czcbOverdueScore为900分')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwCzcbPbocResult_test3DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbGeneralRiskResult':'通过','czcbDebtRiskResult':'通过','czcbOverdueRiskResult':'人工复合','czcbGeneralScore':4,'czcbOverdueScore':200})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbPbocResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbPbocResult')

    @pytest.mark.usefixtures("cdwCzcbPbocResult_test3DataReady")
    def test55_cdwCzcbPbocResult(self):
        """用例55：综合稠州银行返回的六个信息做一个综合结论 --类型:接口传参"""
        print('车贷访问风控接口传参czcbGeneralRiskResult为通过、czcbDebtRiskResult为通过、czcbOverdueRiskResult为人工复合、czcbOverdueScore为200分')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == 'C'

    @pytest.fixture()
    def cdwCzcbPbocResult_test4DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbGeneralRiskResult':'通过','czcbDebtRiskResult':'通过','czcbOverdueRiskResult':'人工复合','czcbGeneralScore':4,'czcbOverdueScore':900})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbPbocResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbPbocResult')

    @pytest.mark.usefixtures("cdwCzcbPbocResult_test4DataReady")
    def test56_cdwCzcbPbocResult(self):
        """用例56：综合稠州银行返回的六个信息做一个综合结论 --类型:接口传参"""
        print('车贷访问风控接口传参czcbGeneralRiskResult为通过、czcbDebtRiskResult为通过、czcbOverdueRiskResult为人工复合、czcbOverdueScore为900分')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def greenChannel_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'greenChannel':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).greenChannel()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('greenChannel')

    @pytest.mark.usefixtures("greenChannel_test1DataReady")
    def test57_greenChannel(self):
        """用例57：车贷绿色通道 --类型:接口传参"""
        print('车贷访问风控接口传参greenChannel为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def greenChannel_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'greenChannel':1})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).greenChannel()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('greenChannel')

    @pytest.mark.usefixtures("greenChannel_test2DataReady")
    def test58_greenChannel(self):
        """用例58：车贷绿色通道 --类型:接口传参"""
        print('车贷访问风控接口传参greenChannel为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def pbocReason_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'pbocReason':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).pbocReason()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('pbocReason')

    @pytest.mark.usefixtures("pbocReason_test1DataReady")
    def test59_pbocReason(self):
        """用例59：众邦征信结果返回是拒绝的原因明细 --类型:接口传参"""
        print('车贷访问风控接口传参pbocReason为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == Default.SET_DEFAULT_VALUE_STR_9999999

    @pytest.fixture()
    def pbocReason_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'pbocReason':'不符合借款要求'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).pbocReason()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('pbocReason')

    @pytest.mark.usefixtures("pbocReason_test2DataReady")
    def test60_pbocReason(self):
        """用例60：众邦征信结果返回是拒绝的原因明细 --类型:接口传参"""
        print('车贷访问风控接口传参pbocReason为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def applicantSpouseType_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'hasSpouse':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).applicantSpouseType()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('applicantSpouseType')

    @pytest.mark.usefixtures("applicantSpouseType_test1DataReady")
    def test61_applicantSpouseType(self):
        """用例61：申请人有没有配偶 --类型:接口传参"""
        print('车贷访问风控接口传参hasSpouse为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def applicantSpouseType_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'hasSpouse':1})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).applicantSpouseType()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('applicantSpouseType')

    @pytest.mark.usefixtures("applicantSpouseType_test1DataReady")
    def test62_applicantSpouseType(self):
        """用例62：申请人有没有配偶 --类型:接口传参"""
        print('车贷访问风控接口传参hasSpouse为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def sponsorType_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'hasGuarantor':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).sponsorType()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('sponsorType')

    @pytest.mark.usefixtures("sponsorType_test1DataReady")
    def test63_sponsorType(self):
        """用例63：是否添加了担保人 --类型:接口传参"""
        print('车贷访问风控接口传参hasGuarantor为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def sponsorType_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'hasGuarantor':1})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).sponsorType()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('sponsorType')

    @pytest.mark.usefixtures("sponsorType_test2DataReady")
    def test64_sponsorType(self):
        """用例64：是否添加了担保人 --类型:接口传参"""
        print('车贷访问风控接口传参hasGuarantor为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carDealerName_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'dealerName': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carDealerName()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carDealerName')

    @pytest.mark.usefixtures("carDealerName_test1DataReady")
    def test65_carDealerName(self):
        """用例65：返回车辆经销商（sp）的名称 --类型:接口传参"""
        print('车贷访问风控接口传参dealerName为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == Default.SET_DEFAULT_VALUE_STR_9999999

    @pytest.fixture()
    def carDealerName_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'dealerName': '奧迪'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carDealerName()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carDealerName')

    @pytest.mark.usefixtures("carDealerName_test2DataReady")
    def test66_carDealerName(self):
        """用例66：返回车辆经销商（sp）的名称 --类型:接口传参"""
        print('车贷访问风控接口传参dealerName为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carRoomAddressProvince_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'homeProvince': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carRoomAddressProvince()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carRoomAddressProvince')

    @pytest.mark.usefixtures("carRoomAddressProvince_test1DataReady")
    def test67_carRoomAddressProvince(self):
        """用例67：取申请人的居住地址省份 --类型:接口传参"""
        print('车贷访问风控接口传参homeProvince为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carRoomAddressProvince_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'homeProvince': '上海'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carRoomAddressProvince()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carRoomAddressProvince')

    @pytest.mark.usefixtures("carRoomAddressProvince_test2DataReady")
    def test68_carRoomAddressProvince(self):
        """用例68：取申请人的居住地址省份 --类型:接口传参"""
        print('车贷访问风控接口传参homeProvince为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carRoomAddressCity_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'homeCity': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carRoomAddressCity()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carRoomAddressCity')

    @pytest.mark.usefixtures("carRoomAddressProvince_test1DataReady")
    def test69_carRoomAddressCity(self):
        """用例69：取申请人的居住地址城市 --类型:接口传参"""
        print('车贷访问风控接口传参homeCity为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carRoomAddressCity_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'homeCity': '上海市'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carRoomAddressCity()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carRoomAddressCity')

    @pytest.mark.usefixtures("carRoomAddressCity_test2DataReady")
    def test70_carRoomAddressCity(self):
        """用例70：取申请人的居住地址城市 --类型:接口传参"""
        print('车贷访问风控接口传参homeCity为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carHouseAddressProvince_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'familyProvince': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carHouseAddressProvince()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carHouseAddressProvince')

    @pytest.mark.usefixtures("carHouseAddressProvince_test1DataReady")
    def test71_carHouseAddressProvince(self):
        """用例71：取申请人的户籍地址省份 --类型:接口传参"""
        print('车贷访问风控接口传参familyProvince为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carHouseAddressProvince_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'familyProvince': '江苏省'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carHouseAddressProvince()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carHouseAddressProvince')

    @pytest.mark.usefixtures("carHouseAddressProvince_test2DataReady")
    def test72_carHouseAddressProvince(self):
        """用例72：取申请人的户籍地址省份 --类型:接口传参"""
        print('车贷访问风控接口传参familyProvince为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carHouseAddressCity_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'familyCity': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carHouseAddressCity()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carHouseAddressCity')

    @pytest.mark.usefixtures("carHouseAddressCity_test1DataReady")
    def test73_carHouseAddressCity(self):
        """用例73：取申请人的户籍地址城市 --类型:接口传参"""
        print('车贷访问风控接口传参familyCity为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carHouseAddressCity_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'familyCity': '宿迁市'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carHouseAddressCity()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carHouseAddressCity')

    @pytest.mark.usefixtures("carHouseAddressCity_test2DataReady")
    def test74_carHouseAddressCity(self):
        """用例74：取申请人的户籍地址城市 --类型:接口传参"""
        print('车贷访问风控接口传参familyCity为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carWorkAddressProvince_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'workProvince': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carWorkAddressProvince()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carWorkAddressProvince')

    @pytest.mark.usefixtures("carWorkAddressProvince_test1DataReady")
    def test75_carWorkAddressProvince(self):
        """用例75：取申请人的工作地址省份 --类型:接口传参"""
        print('车贷访问风控接口传参workProvince为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carWorkAddressProvince_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'workProvince': '上海'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carWorkAddressProvince()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carWorkAddressProvince')

    @pytest.mark.usefixtures("carWorkAddressProvince_test2DataReady")
    def test76_carWorkAddressProvince(self):
        """用例76：取申请人的工作地址省份 --类型:接口传参"""
        print('车贷访问风控接口传参workProvince为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carWorkAddressCity_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'workCity': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carWorkAddressCity()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carWorkAddressCity')

    @pytest.mark.usefixtures("carWorkAddressCity_test1DataReady")
    def test77_carWorkAddressCity(self):
        """用例77：取申请人的工作地址城市 --类型:接口传参"""
        print('车贷访问风控接口传参workCity为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carWorkAddressCity_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'workCity': '上海市'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carWorkAddressCity()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carWorkAddressCity')

    @pytest.mark.usefixtures("carWorkAddressCity_test2DataReady")
    def test78_carWorkAddressCity(self):
        """用例78：取申请人的工作地址城市 --类型:接口传参"""
        print('车贷访问风控接口传参workCity为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def rejectCode_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'rejectCode': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).rejectCode()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('rejectCode')

    @pytest.mark.usefixtures("rejectCode_test1DataReady")
    def test79_rejectCode(self):
        """用例79：外部数据-新网征信拒绝原因码 --类型:接口传参"""
        print('车贷访问风控接口传参rejectCode为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == Default.SET_DEFAULT_VALUE_STR_9999999

    @pytest.fixture()
    def rejectCode_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'rejectCode': 'ED000'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).rejectCode()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('rejectCode')

    @pytest.mark.usefixtures("rejectCode_test2DataReady")
    def test80_rejectCode(self):
        """用例80：外部数据-新网征信拒绝原因码 --类型:接口传参"""
        print('车贷访问风控接口传参rejectCode为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def pbocWhite_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'pbocWhite': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).pbocWhite()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('pbocWhite')

    @pytest.mark.usefixtures("pbocWhite_test1DataReady")
    def test81_pbocWhite(self):
        """用例81：外部数据-新网银行征信 --类型:接口传参"""
        print('车贷访问风控接口传参pbocWhite为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def pbocWhite_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'pbocWhite': '0'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).pbocWhite()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('pbocWhite')

    @pytest.mark.usefixtures("pbocWhite_test2DataReady")
    def test82_pbocWhite(self):
        """用例82：外部数据-新网银行征信 --类型:接口传参"""
        print('车贷访问风控接口传参pbocWhite为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def lastAuditResult_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'lastAuditResult': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).lastAuditResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('lastAuditResult')

    @pytest.mark.usefixtures("lastAuditResult_test1DataReady")
    def test83_lastAuditResult(self):
        """用例83：车贷系统-最近一次审核结果 --类型:接口传参"""
        print('车贷访问风控接口传参lastAuditResult为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == Default.SET_DEFAULT_VALUE_INT_9999999

    @pytest.fixture()
    def lastAuditResult_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'lastAuditResult': '5'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).lastAuditResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('lastAuditResult')

    @pytest.mark.usefixtures("lastAuditResult_test2DataReady")
    def test84_lastAuditResult(self):
        """用例84：车贷系统-最近一次审核结果 --类型:接口传参"""
        print('车贷访问风控接口传参lastAuditResult为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == int(self.test)

    @pytest.fixture()
    def topFourPhone_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).topFourPhone()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('topFourPhone')

    @pytest.mark.usefixtures("topFourPhone_test1DataReady")
    def test85_topFourPhone(self):
        """用例85：申请人手机号前4位 --类型:用户数据"""
        print('车贷访问风控接口传参phone申请人手机号')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseTopFourPhone_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'spousePhone': ''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseTopFourPhone()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseTopFourPhone')

    @pytest.mark.usefixtures("spouseTopFourPhone_test1DataReady")
    def test86_spouseTopFourPhone(self):
        """用例86：配偶手机号前4位  --类型:接口传参"""
        print('车贷访问风控接口传参spousePhone为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == Default.SET_DEFAULT_VALUE_STR_9999999

    @pytest.fixture()
    def spouseTopFourPhone_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName, test_data={'spousePhone': '18209142912'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseTopFourPhone()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseTopFourPhone')

    @pytest.mark.usefixtures("spouseTopFourPhone_test2DataReady")
    def test87_spouseTopFourPhone(self):
        """用例87：配偶手机号前4位 --类型:接口传参"""
        print('车贷访问风控接口传参spousePhone为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def gpsPrice_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'gpsPrice': 200000})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).gpsPrice()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('gpsPrice')

    @pytest.mark.usefixtures("gpsPrice_test1DataReady")
    def test88_gpsPrice(self):
        """用例88：车贷系统-Gps价格 --类型:接口传参"""
        print('车贷访问风控接口传参gpsPrice')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carPrice_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'carPrice': 15000000})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carPrice()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carPrice')

    @pytest.mark.usefixtures("carPrice_test1DataReady")
    def test89_carPrice(self):
        """用例89：车贷系统-车款 --类型:接口传参"""
        print('车贷访问风控接口传参carPrice')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carInsurance_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'carInsurance': 500000})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carInsurance()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carInsurance')

    @pytest.mark.usefixtures("carInsurance_test1DataReady")
    def test90_carInsurance(self):
        """用例90：车贷系统-保险 --类型:接口传参"""
        print('车贷访问风控接口传参carInsurance')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carPurchaseTax_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'carPurchaseTax': 1200000})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carPurchaseTax()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carPurchaseTax')

    @pytest.mark.usefixtures("carPurchaseTax_test1DataReady")
    def test91_carPurchaseTax(self):
        """用例91：车贷系统-购置税 --类型:接口传参"""
        print('车贷访问风控接口传参carInsurance')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def applicantNation_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'applicantNation': '汉族'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).applicantNation()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('applicantNation')

    @pytest.mark.usefixtures("applicantNation_test1DataReady")
    def test92_applicantNation(self):
        """用例92：车贷系统-民族 --类型:接口传参"""
        print('车贷访问风控接口传参applicantNation')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carProductType_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'carProductType': '1'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carProductType()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carProductType')

    @pytest.mark.usefixtures("carProductType_test1DataReady")
    def test93_carProductType(self):
        """用例93：直接判断申请件是否允许自动审批通过 --类型:接口传参"""
        print('车贷访问风控接口传参carProductType')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carRandom_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carRandom()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carRandom')

    @pytest.mark.usefixtures("carRandom_test1DataReady")
    def test94_carRandom(self):
        """用例94：根据客户的身份证号做随机数，如果客户购买多台车，返回同一个随机数 --类型:用户数据"""
        print('根据客户的身份证号做随机数，如果客户购买多台车，返回同一个随机数',str(self.certId))
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carLoanAmount_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'cdwMakeLoanAmount':15000000})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carLoanAmount()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carLoanAmount')

    @pytest.mark.usefixtures("carLoanAmount_test1DataReady")
    def test95_carLoanAmount(self):
        """用例95：放款金额 --类型:接口传参"""
        print('车贷访问风控接口传参cdwMakeLoanAmount')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwPreRiskLevel_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'precallRisklevel':'A'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwPreRiskLevel()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwPreRiskLevel')

    @pytest.mark.usefixtures("cdwPreRiskLevel_test1DataReady")
    def test96_cdwPreRiskLevel(self):
        """用例96：预审等级 --类型:接口传参"""
        print('车贷访问风控接口传参precallRisklevel')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carZoneCode_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'carZoneCode':'内蒙古区'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carZoneCode()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carZoneCode')

    @pytest.mark.usefixtures("carZoneCode_test1DataReady")
    def test97_carZoneCode(self):
        """用例97：预审等级 --类型:接口传参"""
        print('车贷访问风控接口传参carZoneCode')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carZoneCode_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'carZoneCode':'吉林省'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carZoneCode()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carZoneCode')

    @pytest.mark.usefixtures("carZoneCode_test2DataReady")
    def test98_carZoneCode(self):
        """用例98：预审等级 --类型:接口传参"""
        print('车贷访问风控接口传参carZoneCode')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carZoneCode_test3DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'carZoneCode':'上海市'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carZoneCode()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carZoneCode')

    @pytest.mark.usefixtures("carZoneCode_test3DataReady")
    def test99_cdwPreRiskLevel(self):
        """用例99：预审等级 --类型:接口传参"""
        print('车贷访问风控接口传参carZoneCode')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def carZoneCode_test4DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'carZoneCode':'广东省'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).carZoneCode()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('carZoneCode')

    @pytest.mark.usefixtures("carZoneCode_test4DataReady")
    def test100_carZoneCode(self):
        """用例100：自动审批预审等级 --类型:接口传参"""
        print('车贷访问风控接口传参carZoneCode')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def cdwCzcbDebtRiskResult_test1DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbDebtRiskResult':''})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbDebtRiskResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbDebtRiskResult')

    @pytest.mark.usefixtures("cdwCzcbDebtRiskResult_test1DataReady")
    def test101_cdwCzcbDebtRiskResult(self):
        """用例101：稠银-个人综合评定结果 --类型:接口传参"""
        print('车贷访问风控接口传参czcbDebtRiskResult为空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == Default.SET_DEFAULT_VALUE_STR_9999999

    @pytest.fixture()
    def cdwCzcbDebtRiskResult_test2DataReady(self, envopt):
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={'czcbDebtRiskResult': '建议拒绝'})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).cdwCzcbDebtRiskResult()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('cdwCzcbDebtRiskResult')

    @pytest.mark.usefixtures("cdwCzcbDebtRiskResult_test2DataReady")
    def test102_cdwCzcbDebtRiskResult(self):
        """用例102：稠银-个人综合评定结果 --类型:接口传参"""
        print('车贷访问风控接口传参czcbDebtRiskResult为非空值')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def finalScore_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy第三方数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).finalScore()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('finalScore')

    @pytest.mark.usefixtures("finalScore_test1DataReady")
    def test103_finalScore(self):
        """用例103：申请人同盾分 --类型:同盾"""
        print('同盾未准备缓存数据')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def finalScore_test2DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).finalScore()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('finalScore')

    @pytest.mark.usefixtures("finalScore_test2DataReady")
    def test104_finalScore(self):
        """用例104：申请人同盾分 --类型:同盾"""
        print('同盾准备缓存数据-数据在缓存期内')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def finalScore_test3DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_out])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).finalScore()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('finalScore')

    @pytest.mark.usefixtures("finalScore_test3DataReady")
    def test105_finalScore(self):
        """用例105：申请人同盾分 --类型:同盾"""
        print('同盾准备缓存数据-数据在缓存期外-需重新跑同盾')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def riskItem2976222_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).riskItem2976222()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('riskItem2976222')

    @pytest.mark.usefixtures("riskItem2976222_test1DataReady")
    def test106_riskItem2976222(self):
        """用例106：身份证命中高风险关注名单 --类型:同盾"""
        print('身份证命中高风险关注名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def riskItem2976210_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).riskItem2976210()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('riskItem2976210')

    @pytest.mark.usefixtures("riskItem2976210_test1DataReady")
    def test107_riskItem2976210(self):
        """用例107：身份证归宿地位于高风险较为集中地区 --类型:同盾"""
        print('身份证归宿地位于高风险较为集中地区')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def riskItem2976264_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).riskItem2976264()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('riskItem2976264')

    @pytest.mark.usefixtures("riskItem2976264_test1DataReady")
    def test108_riskItem2976264(self):
        """用例108：手机号命中高风险关注名单 --类型:同盾"""
        print('手机号命中高风险关注名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def riskItem2976256_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).riskItem2976256()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('riskItem2976256')

    @pytest.mark.usefixtures("riskItem2976256_test1DataReady")
    def test109_riskItem2976256(self):
        """用例109：机号命中通信小号库 --类型:同盾"""
        print('机号命中通信小号库')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def riskItem2976386_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).riskItem2976386()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('riskItem2976386')

    @pytest.mark.usefixtures("riskItem2976386_test1DataReady")
    def test110_riskItem2976386(self):
        """用例110：第一联系人身份证命中法院失信名单-近亲 --类型:同盾"""
        print('第一联系人身份证命中法院失信名单-近亲')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def riskItem2976388_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).riskItem2976388()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('riskItem2976388')

    @pytest.mark.usefixtures("riskItem2976388_test1DataReady")
    def test111_riskItem2976388(self):
        """用例111：第一联系人身份证命中法院执行名单 --类型:同盾"""
        print('第一联系人身份证命中法院执行名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def riskItem2976392_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).riskItem2976392()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('riskItem2976392')

    @pytest.mark.usefixtures("riskItem2976392_test1DataReady")
    def test112_riskItem2976392(self):
        """用例112：第一联系人身份证命中犯罪通缉名单 --类型:同盾"""
        print('第一联系人身份证命中犯罪通缉名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def riskItem2976396_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).riskItem2976396()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('riskItem2976396')

    @pytest.mark.usefixtures("riskItem2976396_test1DataReady")
    def test113_riskItem2976396(self):
        """用例113：第一联系人身份证命中信贷逾期名单 --类型:同盾"""
        print('第一联系人身份证命中信贷逾期名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def riskItem2976398_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).riskItem2976398()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('riskItem2976398')

    @pytest.mark.usefixtures("riskItem2976398_test1DataReady")
    def test114_riskItem2976398(self):
        """用例114：第一联系人身份证命中信贷逾期名单 --类型:同盾"""
        print('第一联系人身份证命中信贷逾期名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def riskItem2976402_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).riskItem2976402()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('riskItem2976402')

    @pytest.mark.usefixtures("riskItem2976402_test1DataReady")
    def test115_riskItem2976402(self):
        """用例115：第一联系人手机号命中虚假号码或通信小号库 --类型:同盾"""
        print('第一联系人手机号命中虚假号码或通信小号库')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseFinalScore_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseFinalScore()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseFinalScore')

    @pytest.mark.usefixtures("spouseFinalScore_test1DataReady")
    def test116_spouseFinalScore(self):
        """用例116：申请人配偶的同盾分 --类型:同盾"""
        print('申请人配偶的同盾分')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseFinalScore_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseFinalScore()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseFinalScore')

    @pytest.mark.usefixtures("spouseFinalScore_test1DataReady")
    def test117_spouseFinalScore(self):
        """用例117：申请人配偶的同盾分 --类型:同盾"""
        print('申请人配偶的同盾分')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976210_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976210()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976210')

    @pytest.mark.usefixtures("spouseRiskItem2976210_test1DataReady")
    def test118_spouseRiskItem2976210(self):
        """用例118：申请人配偶的身份证归宿地位于高风险较为集中地区 --类型:同盾"""
        print('申请人配偶的身份证归宿地位于高风险较为集中地区')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976222_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976222()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976222')

    @pytest.mark.usefixtures("spouseRiskItem2976222_test1DataReady")
    def test119_spouseRiskItem2976222(self):
        """用例119：申请人配偶的身份证命中高风险关注名单 --类型:同盾"""
        print('申请人配偶的身份证命中高风险关注名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976264_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976264()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976264')

    @pytest.mark.usefixtures("spouseRiskItem2976264_test1DataReady")
    def test120_spouseRiskItem2976264(self):
        """用例120：申请人配偶的手机号命中高风险关注名单 --类型:同盾"""
        print('申请人配偶的手机号命中高风险关注名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976386_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976386()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976386')

    @pytest.mark.usefixtures("spouseRiskItem2976386_test1DataReady")
    def test121_spouseRiskItem2976386(self):
        """用例121：申请人配偶的第一联系人身份证命中法院失信名单-近亲 --类型:同盾"""
        print('申请人配偶的第一联系人身份证命中法院失信名单-近亲')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976388_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976388()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976388')

    @pytest.mark.usefixtures("spouseRiskItem2976388_test1DataReady")
    def test122_spouseRiskItem2976388(self):
        """用例122：申请人配偶的第一联系人身份证命中法院执行名单 --类型:同盾"""
        print('申请人配偶的第一联系人身份证命中法院执行名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976392_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976392()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976392')

    @pytest.mark.usefixtures("spouseRiskItem2976392_test1DataReady")
    def test123_spouseRiskItem2976392(self):
        """用例123：申请人配偶的第一联系人身份证命中犯罪通缉名单 --类型:同盾"""
        print('申请人配偶的第一联系人身份证命中犯罪通缉名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test


    @pytest.fixture()
    def spouseRiskItem2976398_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976398()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976398')

    @pytest.mark.usefixtures("spouseRiskItem2976398_test1DataReady")
    def test124_spouseRiskItem2976398(self):
        """用例124：申请人配偶的第一联系人手机号命中信贷逾期名单 --类型:同盾"""
        print('申请人配偶的第一联系人手机号命中信贷逾期名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976402_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976402()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976402')

    @pytest.mark.usefixtures("spouseRiskItem2976402_test1DataReady")
    def test125_spouseRiskItem2976402(self):
        """用例125：申请人配偶的第一联系人手机号命中虚假号码或通信小号库 --类型:同盾"""
        print('申请人配偶的第一联系人手机号命中虚假号码或通信小号库')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976212_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976212()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976212')

    @pytest.mark.usefixtures("spouseRiskItem2976212_test1DataReady")
    def test126_spouseRiskItem2976212(self):
        """用例126：申请人配偶的身份证命中法院失信黑名单 --类型:同盾"""
        print('申请人配偶的身份证命中法院失信黑名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976214_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976214()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976214')

    @pytest.mark.usefixtures("spouseRiskItem2976214_test1DataReady")
    def test127_spouseRiskItem2976214(self):
        """用例127：申请人配偶的身份证命中犯罪通缉名单 --类型:同盾"""
        print('申请人配偶的身份证命中犯罪通缉名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976216_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976216()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976216')

    @pytest.mark.usefixtures("spouseRiskItem2976216_test1DataReady")
    def test128_spouseRiskItem2976216(self):
        """用例128：申请人配偶的身份证命中法院执行名单 --类型:同盾"""
        print('申请人配偶的身份证命中法院执行名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976220_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976220()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976220')

    @pytest.mark.usefixtures("spouseRiskItem2976220_test1DataReady")
    def test129_spouseRiskItem2976220(self):
        """用例129：申请人配偶的身份证命中信贷逾期名单 --类型:同盾"""
        print('申请人配偶的身份证命中信贷逾期名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976224_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976224()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976224')

    @pytest.mark.usefixtures("spouseRiskItem2976224_test1DataReady")
    def test130_spouseRiskItem2976224(self):
        """用例130：申请人配偶的身份证命中车辆租赁违约名单 --类型:同盾"""
        print('申请人配偶的身份证命中车辆租赁违约名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976226_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976226()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976226')

    @pytest.mark.usefixtures("spouseRiskItem2976226_test1DataReady")
    def test131_spouseRiskItem2976226(self):
        """用例131：申请人配偶的身份证命中法院结案名单 --类型:同盾"""
        print('申请人配偶的身份证命中法院结案名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976254_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976254()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976254')

    @pytest.mark.usefixtures("spouseRiskItem2976254_test1DataReady")
    def test132_spouseRiskItem2976254(self):
        """用例132：申请人配偶的手机号命中虚假号码库 --类型:同盾"""
        print('申请人配偶的手机号命中虚假号码库')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976258_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976258()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976258')

    @pytest.mark.usefixtures("spouseRiskItem2976258_test1DataReady")
    def test133_spouseRiskItem2976258(self):
        """用例133：申请人配偶的手机号命中诈骗骚扰库 --类型:同盾"""
        print('申请人配偶的手机号命中诈骗骚扰库')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976268_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976268()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976268')

    @pytest.mark.usefixtures("spouseRiskItem2976268_test1DataReady")
    def test134_spouseRiskItem2976268(self):
        """用例134：申请人配偶的手机号命中车辆租赁违约名单 --类型:同盾"""
        print('申请人配偶的手机号命中车辆租赁违约名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976312_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976312()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976312')

    @pytest.mark.usefixtures("spouseRiskItem2976312_test1DataReady")
    def test135_spouseRiskItem2976312(self):
        """用例135：申请人配偶的手机号命中信贷逾期名单 --类型:同盾"""
        print('申请人配偶的手机号命中信贷逾期名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976320_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976320()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976320')

    @pytest.mark.usefixtures("spouseRiskItem2976320_test1DataReady")
    def test136_spouseRiskItem2976320(self):
        """用例136：申请人配偶的3个月内身份证关联多个申请信息 --类型:同盾"""
        print('申请人配偶的3个月内身份证关联多个申请信息')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976320_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976320()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976320')

    @pytest.mark.usefixtures("spouseRiskItem2976320_test1DataReady")
    def test136_spouseRiskItem2976320(self):
        """用例136：申请人配偶的3个月内身份证关联多个申请信息 --类型:同盾"""
        print('申请人配偶的3个月内身份证关联多个申请信息')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976322_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976322()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976322')

    @pytest.mark.usefixtures("spouseRiskItem2976322_test1DataReady")
    def test137_spouseRiskItem2976322(self):
        """用例137：申请人配偶的3个月内申请信息关联多个身份证 --类型:同盾"""
        print('申请人配偶的3个月内申请信息关联多个身份证')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976340_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976340()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976340')

    @pytest.mark.usefixtures("spouseRiskItem2976340_test1DataReady")
    def test138_spouseRiskItem2976340(self):
        """用例138：申请人配偶的7天内设备或身份证或手机号申请次数过多 --类型:同盾"""
        print('申请人配偶的7天内设备或身份证或手机号申请次数过多')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976354_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976354()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976354')

    @pytest.mark.usefixtures("spouseRiskItem2976354_test1DataReady")
    def test139_spouseRiskItem2976354(self):
        """用例139：申请人配偶的7天内申请人在多个平台申请借款 --类型:同盾"""
        print('申请人配偶的7天内申请人在多个平台申请借款')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976356_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976356()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976356')

    @pytest.mark.usefixtures("spouseRiskItem2976356_test1DataReady")
    def test140_spouseRiskItem2976356(self):
        """用例140：申请人配偶的1个月内申请人在多个平台申请借款 --类型:同盾"""
        print('申请人配偶的1个月内申请人在多个平台申请借款')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976372_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976372()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976372')

    @pytest.mark.usefixtures("spouseRiskItem2976372_test1DataReady")
    def test141_spouseRiskItem2976372(self):
        """用例141：申请人配偶的3个月内申请人在多个平台被放款_不包含本合作方 --类型:同盾"""
        print('申请人配偶的3个月内申请人在多个平台被放款_不包含本合作方')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976256_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976256()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976256')

    @pytest.mark.usefixtures("spouseRiskItem2976256_test1DataReady")
    def test142_spouseRiskItem2976256(self):
        """用例142：申请人配偶的手机号命中通信小号库 --类型:同盾"""
        print('申请人配偶的手机号命中通信小号库')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976396_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976396()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976396')

    @pytest.mark.usefixtures("spouseRiskItem2976396_test1DataReady")
    def test143_spouseRiskItem2976396(self):
        """用例143：申请人配偶的第一联系人身份证命中犯罪通缉名单 --类型:同盾"""
        print('申请人配偶的第一联系人身份证命中犯罪通缉名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def spouseRiskItem2976266_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='td_record', dataDict={'cardId': factor_encrypt_identity(self.spouseIdNumber)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='td_record', dataList=[td_record_in])
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.spouseIdNumber, phone=self.spousePhone,userName=self.spouseName,test_data={})
        time.sleep(1)#等待galaxy数据落库
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).spouseRiskItem2976266()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('spouseRiskItem2976266')

    @pytest.mark.usefixtures("spouseRiskItem2976266_test1DataReady")
    def test144_spouseRiskItem2976266(self):
        """用例144：申请人配偶的手机号命中信贷逾期名单 --类型:同盾"""
        print('申请人配偶的手机号命中信贷逾期名单')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def geoPhoneEntDuration_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='geo_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='geo_record', dataList=[geo_record_in])
        time.sleep(1)#等待galaxy数据落库
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).geoPhoneEntDuration()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('geoPhoneEntDuration')

    @pytest.mark.usefixtures("geoPhoneEntDuration_test1DataReady")
    def test145_geoPhoneEntDuration(self):
        """用例145：手机在网时间 --类型:集奥"""
        print('申请人手机在网时间')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def geoPhoneSelfMatch_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='geo_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='geo_record', dataList=[geo_record_in])
        time.sleep(1)#等待galaxy数据落库
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).geoPhoneSelfMatch()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('geoPhoneSelfMatch')

    @pytest.mark.usefixtures("geoPhoneSelfMatch_test1DataReady")
    def test146_geoPhoneSelfMatch(self):
        """用例146：手机为本人实名认证 --类型:集奥"""
        print('手机为本人实名认证')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test

    @pytest.fixture()
    def geoCurStatus_test1DataReady(self, envopt):
        MongoPyUtilPort(env=envopt, db='galaxy').deleteData(collection='geo_record', dataDict={'cardId': factor_encrypt_identity(self.certId)})
        MongoPyUtilPort(env=envopt, db='galaxy').insertData(collection='geo_record', dataList=[geo_record_in])
        time.sleep(1)#等待galaxy数据落库
        self.serial_no = CarDecisionApiAuto(env=envopt, productId=self.productCode,sceneId=self.sceneCode).makeDecision(certId=self.certId, phone=self.phone,userName=self.userName,test_data={})
        self.test = CarFactorAuto(env=envopt, serial_no=self.serial_no).geoCurStatus()
        self.dev = DoorlsFactor(env=envopt, serial_no=self.serial_no).get_Factor('geoCurStatus')

    @pytest.mark.usefixtures("geoCurStatus_test1DataReady")
    def test147_geoCurStatus(self):
        """用例147：集奥当前状态 --类型:集奥"""
        print('集奥当前状态')
        print(self.serial_no, " test:", self.test, " dev:", self.dev)
        assert self.dev == self.test




