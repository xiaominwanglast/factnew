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
        return long(int(round(time.time() * 1000)))

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