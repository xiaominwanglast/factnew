#coding:utf-8
import time
import string
import random
class CarDecisionProperty(object):
    def __init__(self):
        self.applyId = self.get_applyId
        self.applyTime = self.get_applyTime
        self.loanProduct = self.get_loanProduct
        self.loanAmount = self.get_loanAmount
        self.loanTerm = self.get_loanTerm
        self.vehicleType = self.get_vehicleType
        self.age = self.get_age
        self.gender = self.get_gender
        self.maritalStatus = self.get_maritalStatus
        self.czcbGeneralScore = self.get_czcbGeneralScore
        self.czcbDebtScore = self.get_czcbDebtScore
        self.czcbOverdueScore = self.get_czcbOverdueScore
        self.bankcardNo = self.get_bankcardNo
        self.registerLocation = self.get_registerLocation
        self.agentName = self.get_agentName
        self.czcbGeneralRiskResult=self.get_RiskResult
        self.czcbDebtRiskResult=self.get_RiskResult
        self.czcbOverdueRiskResult=self.get_RiskResult
        self.czcbRiskNote=self.get_czcbRiskNote
        self.outOfAuthorizedDistrict=self.get_outOfAuthorizedDistrict
        self.idCardAppearCount=self.get_idCardAppearCount
        self.idCardExpired=self.get_idCardExpired
        self.isLcv =self.get_isLcv
        self.pbocResult=self.get_pbocResult
        self.pbocInfo=self.get_pbocInfo
        self.guarantorIdNumber=self.get_guarantorIdNumber
        self.spouseIdNumber=self.get_spouseIdNumber
        self.noRelationContactCnt=self.get_noRelationContactCnt
        self.netPrice=self.get_netPrice
        self.guarantorPhone=self.get_guarantorPhone
        self.greenChannel=self.get_greenChannel
        self.pbocReason=self.get_pbocReason
        self.hasSpouse=self.get_hasSpouse
        self.hasGuarantor=self.get_hasGuarantor
        self.spousePhone=self.get_spousePhone
        self.spouseName=self.get_spouseName
        self.guarantorName=self.get_guarantorName
        self.familyProvince=self.get_familyProvince
        self.familyCity=self.get_familyCity
        self.homeProvince=self.get_homeProvince
        self.homeCity=self.get_homeCity
        self.workProvince=self.get_workProvince
        self.workCity=self.get_workCity
        self.dealerName=self.get_dealerName
        self.rejectCode=self.get_rejectCode
        self.pbocWhite=self.get_pbocWhite
        self.applicantNation=self.get_applicantNation
        self.lastAuditResult=self.get_lastAuditResult
        self.gpsPrice=self.get_gpsPrice
        self.carPrice=self.get_carPrice
        self.carInsurance=self.get_carInsurance
        self.carPurchaseTax=self.get_carPurchaseTax
        self.carProductType=self.get_carProductType
        self.cdwMakeLoanAmount=self.get_cdwMakeLoanAmount
        self.carZoneCode=self.get_carZoneCode
        self.precallRisklevel=self.get_precallRisklevel
        self.carPurchase=self.get_carPurchase
        self.bankPhone = self.get_bankPhone
        self.colleagueContact = self.get_colleagueContact
        self.friendContact = self.get_friendContact
        self.relativeContact = self.get_relativeContact
        self.firstApplyTime = self.get_firstApplyTime
        self.livingAddress = self.get_livingAddress
        self.residenceAddress = self.get_residenceAddress
        self.unitAddress = self.get_unitAddress
        self.unitName = self.get_unitName

    @property
    def get_bankPhone(self):
        return 17621145005

    @property
    def get_colleagueContact(self):
        return 17621145006

    @property
    def get_friendContact(self):
        return 17621145007

    @property
    def get_relativeContact(self):
        return 17621145008

    @property
    def get_firstApplyTime(self):
        return int(int(round(time.time() * 1000)))

    @property
    def get_livingAddress(self):
        return "上海上海市浦东新区康新公路300号"

    @property
    def get_residenceAddress(self):
        return "江苏省南京市华东发展大道200号"

    @property
    def get_unitAddress(self):
        return "上海上海市张江科技园区环科路5550号"

    @property
    def get_unitName(self):
        return "上海二三四五金融科技有限公司"

    @property
    def get_carPurchase(self):
        return random.choice(['0','1','2','3'])

    @property
    def get_precallRisklevel(self):
        return random.choice(['A','B'])

    @property
    def get_carZoneCode(self):
        return random.choice(["重庆市","四川省","贵州省","云南省","西藏区","陕西省","甘肃省","青海省","宁夏区","新疆区","江西省","河南省","湖北省","湖南省","福建省",\
                              "广东省","广西区","海南省","江苏省","浙江省","安徽省","山东省","上海市","北京市","天津市","河北省","山西省","内蒙古区","辽宁省","吉林省",\
                              "黑龙江省","香港特区","澳门特区"])

    @property
    def get_cdwMakeLoanAmount(self):
        return random.randint(3000000,10000000)

    @property
    def get_carProductType(self):
        return random.choice([1,2])

    @property
    def get_carPurchaseTax(self):
        return random.choice([20000,20000.0,20000.00])

    @property
    def get_carInsurance(self):
        return random.choice([2000,2000.0,2000.00])

    @property
    def get_carPrice(self):
        return random.choice([200000,200000.0,200000.00])

    @property
    def get_gpsPrice(self):
        return random.choice([1000,1000.0,1000.00])

    @property
    def get_lastAuditResult(self):
        return random.choice([1,2,3,4,5])

    @property
    def get_applicantNation(self):
        return random.choice(["汉族","满族","壮族","维吾尔族"])

    @property
    def get_pbocWhite(self):
        return random.choice([0,1])

    @property
    def get_rejectCode(self):
        return random.choice(['太穷','太傻','太天真'])

    @property
    def get_hasSpouse(self):
        return 0
        # return random.choice([0,1])

    @property
    def get_hasGuarantor(self):
        return random.choice([0,1])

    @property
    def get_spousePhone(self):
        return '13995066188'
        # return '183'+''.join(random.sample(string.digits, 8))

    @property
    def get_spouseName(self):
        return '张新年'

    @property
    def get_spouseIdNumber(self):
        return '640211197510256032'
        # return str(time.time())[:8]+ ''.join(random.sample(string.digits, 10))

    @property
    def get_guarantorName(self):
        return '王担保'


    @property
    def get_guarantorIdNumber(self):
        # return random.randint(10000,99999)
        return 431022197807031977

    @property
    def get_guarantorPhone(self):
        return 18301924915
        # return random.choice(['12','13','14','15','16','17','18'])+''.join(random.sample(string.digits, 9))


    @property
    def get_familyProvince(self):
        return random.choice(['江苏省','江西省'])

    @property
    def get_familyCity(self):
        return random.choice(['宿迁','苏州'])

    @property
    def get_homeProvince(self):
        return random.choice(["湖南省","湖北省"])

    @property
    def get_homeCity(self):
        return random.choice(["长沙","岳阳"])

    @property
    def get_workProvince(self):
        return random.choice(['上海','北京'])

    @property
    def get_workCity(self):
        return random.choice(['上海市','北京市'])

    @property
    def get_dealerName(self):
        return random.choice(['奥迪A6经销商','宝马x6经销商','买不起经销商'])

    @property
    def get_pbocReason(self):
        return random.choice(['信用不足','人格不行','高富帅','白富美'])

    @property
    def get_greenChannel(self):
        return random.randint(0,2)


    @property
    def get_netPrice(self):
        return random.randint(100000, 299999)

    @property
    def get_noRelationContactCnt(self):
        return random.randint(0,10)


    @property
    def get_pbocResult(self):
        return random.choice(['A', 'B' ,'C' ,'D'])

    @property
    def get_pbocInfo(self):
        return random.choice(['chouzhou','zhongbang',''])

    @property
    def get_salt(self):
        return "cpo8%osM"

    @property
    def get_RiskResult(self):
        return random.choice(['人工复合','通过','建议拒绝','直接拒绝'])

    @property
    def get_applyId(self):
        return str(int(time.time())) + str(random.randint(1000, 5000))

    @property
    def get_applyTime(self):
        return int(int(round(time.time() * 1000)))

    @property
    def get_loanProduct(self):
        return '2345_' + str(random.randint(1000, 5000))

    @property
    def get_loanAmount(self):
        return round(random.uniform(1000000, 20000000), 2)

    @property
    def get_loanTerm(self):
        return random.choice([12, 24, 36])

    @property
    def get_vehicleType(self):
        return str(random.randint(0, 5))

    @property
    def get_age(self):
        return random.randint(18, 50)

    @property
    def get_gender(self):
        return random.choice([0, 1])

    @property
    def get_maritalStatus(self):
        return random.choice([0, 1])

    @property
    def get_czcbGeneralScore(self):
        return round(random.uniform(100, 999), random.randint(1, 3))

    @property
    def get_czcbDebtScore(self):
        return round(random.uniform(100, 999), random.randint(1, 3))

    @property
    def get_czcbOverdueScore(self):
        return round(random.uniform(100, 999), random.randint(1, 3))

    @property
    def get_bankcardNo(self):
        return str(62284800383516) + str(random.randint(10000, 99999))

    @property
    def get_registerLocation(self):
        return str(random.randint(100000, 500000))

    @property
    def get_agentName(self):
        return str(random.randint(1000, 5000))

    @property
    def get_czcbRiskNote(self):
        return random.choice(['很好','很差','穷B','完美'])

    @property
    def get_outOfAuthorizedDistrict(self):
        return random.choice([0, 1])

    @property
    def get_idCardAppearCount(self):
        return random.randint(5, 20)

    @property
    def get_idCardExpired(self):
        return random.choice([0, 1])

    @property
    def get_isLcv(self):
        return random.choice([0, 1])