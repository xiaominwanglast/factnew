#coding:utf-8
import time
import json
import string
import random
class NewDecisionProperty(object):
    def __init__(self):
        self.bankCard=self.get_bankCard
        self.channedId=self.get_channedId
        self.unitsPhone=self.get_unitsPhone
        self.unitsName=self.get_unitsName
        self.unitsProvince=self.get_Province
        self.unitsCity=self.get_City
        self.unitsDistrict=self.get_District
        self.unitsAddress=self.get_Address
        self.homeProvince=self.get_Province
        self.homeCity=self.get_City
        self.homeDistrict=self.get_District
        self.homeAddress=self.get_Address
        self.relativeContact=self.get_contact
        self.colleagueContact=self.get_contact
        self.friendContact=self.get_contact
        self.creditLine=self.get_creditLine
        self.borrowCount=0
        self.oldUserId=self.get_oldUserId
        self.applyId = self.get_applyId
        self.applyTime = self.get_applyTime
        self.repaymentTime=self.get_repaymentTime
        self.orderId = self.get_orderId
        self.billId = self.get_billId
        self.extraDataStatus=1
        self.previousSerialNo=self.get_previousSerialNo
        self.extraData=self.get_extraData
        self.applyStatusId=self.get_applyStatusId
        self.terminalType=self.get_terminalType
        self.channelCode=self.get_channelCode
        self.warrantFileUrl=self.get_warrantFileUrl
        self.periods=self.get_periods

    @property
    def get_periods(self):
        return random.choice(['3','6','9','12'])

    @property
    def get_warrantFileUrl(self):
        return "group1/M01/3E/19/rBAAjlxzhheAWTT3AAC5U0qNB6k808.png"

    @property
    def get_channelCode(self):
        #第三方渠道code：银码头:ljd-yinmatouapi_cpc_zbc  大王贷:ljd-xinlangdwd_cpl_qck
        return
    @property
    def get_terminalType(self):
        #第三方固定渠道，目前定义是ljd_3rd
        return
    @property
    def get_applyStatusId(self):
        return str(random.randint(1,10))
    @property
    def get_extraData(self):
        return ','.join(random.sample(['1','3','5','6','10','11','15'], 2))
    @property
    def get_previousSerialNo(self):
        return str(time.time()*1000)+ ''.join(random.sample(string.ascii_letters + string.digits, 32))
    @property
    def get_bankCard(self):
        return json.dumps([{"bankName":"中国银行","bankcard":"62284800383516"+str(random.randint(10000,99999)),"reservedPhone":"183"+str(random.randint(10000000,99999999))}])
    @property
    def get_channedId(self):
        return str(random.randint(100,900))
    @property
    def get_unitsPhone(self):
        return "021"+str(random.randint(10000000,99999999))
    @property
    def get_unitsName(self):
        return u"二三四五"+str(random.randint(1000,9999))
    @property
    def get_Province(self):
        return random.choice([
            u'北京市',u'天津市',u'上海市',u'重庆市',u'河北省',u'山西省',u'辽宁省',u'吉林省',u'黑龙江省',u'江苏省',u'浙江省',
            u'安徽省',u'福建省',u'江西省',u'山东省',u'河南省',u'湖北省',u'湖南省',u'广东省',u'海南省',u'四川省',u'贵州省',u'云南省',u'陕西省',
            u'甘肃省',u'青海省',u'台湾省',u'内蒙古自治区',u'广西壮族自治区',u'西藏自治区',u'宁夏回族自治区',u'新疆维吾尔自治区',u'香港特别行政区',u'澳门特别行政区'
            ])
    @property
    def get_City(self):
        return random.choice([
            u'南京',u'徐州',u'连云港',u'宿迁',u'淮安',u'扬州',u'盐城',u'南通',u'泰州',u'苏州',u'常州',u'无锡',u'镇江'
        ])
    @property
    def get_District(self):
        return random.choice([
            u'玄武区',u'秦淮区',u'鼓楼区',u'建邺区',u'栖霞区',u'雨花台区',u'浦口区',u'江宁区',u'六合区',u'溧水区',u'高淳区'
        ])
    @property
    def get_Address(self):
        return random.choice([
            U'秀沿路',u'秀铺路',u'杜甫路',u'伽利略路',u'华夏东路',u'罗山西路',u'金科路',u'环科路',u'环桥路',u'上南路',u'御桥路'
        ])
    @property
    def get_creditLine(self):
        return random.randint(100000,500000)
    @property
    def get_oldUserId(self):
        return random.randint(1000000,2000000)
    @property
    def get_contact(self):
        return "183"+str(random.randint(10000000,99999999))
    @property
    def get_applyId(self):
        return str(int(time.time())) + str(random.randint(100000, 500000))
    @property
    def get_applyTime(self):
        return long(int(round(time.time() * 1000)))
    @property
    def get_repaymentTime(self):
        return int(time.time()*1000)
    @property
    def get_orderId(self):
        return "67997073531"+str(random.randint(100000,999999))
    @property
    def get_billId(self):
        return "67997073531"+str(random.randint(100000,999999))