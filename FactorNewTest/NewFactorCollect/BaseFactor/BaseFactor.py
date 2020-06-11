# coding:utf-8
from FrameRunner.FactorInit import NewFactorInit
from utils.TestInit import factor_decrypt_identity
from utils.otherUtil import *

class BaseFactor(NewFactorInit):
    def __init__(self, env, serial_no):
        super(BaseFactor, self).__init__(env, serial_no)

    def idcardProvince(self):
        """idcardProvince 申请人身份证号省份"""
        hit = ""
        result1 = self.mysql.queryall_by_customer_id(db='customer_center',
                                                               sql="select identity_card from customer_identiy_%s where customer_id='%s' and delete_flag=0" % (
                                                               self.info.customer_id % 20, self.info.customer_id))

        if not result1:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            idCard = factor_decrypt_identity(result1[0].get('identity_card'))
            proList = ["省","市","特别行政区","壮族自治区","回族自治区","维吾尔自治区","自治区"]
            idCard = str(idCard)[:6]
            result = self.mysql.queryall_by_customer_id(db='skynet',sql="select province from dict_idcard_location where code = %s" % (idCard))
            if not result:
                return self.SET_DEFAULT_VALUE_INT_9999999
            else:
                province = result[0].get('province')
                province = province.encode('utf-8')
                for i in proList:
                    if i in province:
                        hit = i
                        break
                proLen = len(hit)
                if proLen == 0 :
                    return province
                else:
                    return str(province)[:-proLen]

    def idcardCity(self):
        """idcardCity 申请人身份证号市"""
        result1 = self.mysql.queryall_by_customer_id(db='customer_center',
                                                               sql="select identity_card from customer_identiy_%s where customer_id='%s' and delete_flag=0" % (
                                                                   self.info.customer_id % 20, self.info.customer_id))
        if not result1:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            idCard = factor_decrypt_identity(result1[0].get('identity_card'))
            proList = ["地区","市","回族自治州","彝族自治州","藏族自治州","土家族苗族自治州","哈尼族彝族自治州","傣族自治州","藏族羌族自治州","苗族侗族自治州","布依族苗族自治州","哈萨克自治州","柯尔克孜自治州","朝鲜族自治州","蒙古族藏族自治州","蒙古自治州","白族自治州","傣族景颇族自治州","傈僳族自治州","壮族苗族自治州"]
            idCard = str(idCard)[:6]
            result = self.mysql.queryall_by_customer_id(db='skynet',
                                                                  sql="select city from dict_idcard_location where code = %s" % (
                                                                      idCard))
            if not result:
                return self.SET_DEFAULT_VALUE_INT_9999999
            else:
                city = result[0].get('city')
                city = city.encode('utf-8')
                hit=''
                for i in proList:
                    if i in city:
                        hit =i
                        break
                proLen = len(hit)
                if proLen == 0:
                    cityResult = city
                else:
                    cityResult =  str(city)[:-proLen]
                if cityResult == "滁县" :
                    cityResult = "滁州"
                elif cityResult == "乌兰察布" :
                    cityResult = "乌兰察布市"
                elif cityResult == "宿县":
                    cityResult = "宿州"
                return cityResult

    def phoneCity(self):
        """phoneCity 手机号码归属地（指注册手机号）"""
        hit = ""
        result1 = self.mysql.queryall_by_customer_id(db='customer_center',
                                                               sql="select mobilephone from `user` where id='%s' and delete_flag=0" % (self.info.user_id))

        if not result1:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            mobile = result1[0].get('mobilephone')
            proList = ["地区", "市", "回族自治州", "彝族自治州", "藏族自治州", "土家族苗族自治州", "哈尼族彝族自治州", "傣族自治州", "藏族羌族自治州", "苗族侗族自治州",
                       "布依族苗族自治州", "哈萨克自治州", "柯尔克孜自治州", "朝鲜族自治州", "蒙古族藏族自治州", "蒙古自治州", "白族自治州", "傣族景颇族自治州", "傈僳族自治州",
                       "壮族苗族自治州"]
            mobile = str(mobile)[:7]
            result = self.mysql.queryall_by_customer_id(db='skynet',
                                                                  sql="select city from dict_mobile_location where mobile = %s" % (
                                                                      mobile))
            if not result:
                return self.SET_DEFAULT_VALUE_INT_9999999
            else:
                city = result[0].get('city')
                city = city.encode('utf-8')
                for i in proList:
                    if i in city:
                        hit = i
                        break
                proLen = len(hit)
                if proLen == 0:
                    cityResult = city
                else:
                    cityResult = str(city)[:-proLen]
                if cityResult == "滁县":
                    cityResult = "滁州"
                if cityResult == "乌兰察布":
                    cityResult = "乌兰察布市"
                if cityResult == "宿县":
                    cityResult = "宿州"
                return cityResult

    def gpsCity(self):
        """gpsCity 最新gps定位城市"""
        hit = ""
        proList = ["地区", "市", "回族自治州", "彝族自治州", "藏族自治州", "土家族苗族自治州", "哈尼族彝族自治州", "傣族自治州", "藏族羌族自治州", "苗族侗族自治州",
                   "布依族苗族自治州", "哈萨克自治州", "柯尔克孜自治州", "朝鲜族自治州", "蒙古族藏族自治州", "蒙古自治州", "白族自治州", "傣族景颇族自治州", "傈僳族自治州",
                   "壮族苗族自治州"]
        data = self.mysql.query_by_user_id('lake', "s_user_mobile_basic_info",
                                           {"user_id": int(self.info.user_id)})
        if len(data) <= 0:
            return self.SET_DEFAULT_VALUE_INT_9999999
        lng = data[0]['lng']
        lat = data[0]['lat']
        url = "http://api.map.baidu.com/geocoder/v2/?location=%s,%s&output=json&pois=1&ak=FYtp2nUySbF0uhoGHwA2DNE0" % (
        lat, lng)
        r = requests.get(url)
        if r.json().get('result') and r.json().get('result').get('addressComponent') and r.json().get('result').get(
                'addressComponent').get('city'):
            city = r.json()['result']['addressComponent']['city']
            if city != "" or city != None:
                cityResult = city
                cityResult = cityResult.encode("utf-8")

                for i in proList:
                    if i in cityResult:
                        hit = i
                        break
                proLen = len(hit)
                if proLen == 0:
                    cityResult = cityResult
                else:
                    cityResult = str(cityResult)[:-proLen]
                if cityResult == "滁县":
                    cityResult = "滁州"
                if cityResult == "乌兰察布":
                    cityResult = "乌兰察布市"
                if cityResult == "宿县":
                    cityResult = "宿州"
                return cityResult
            else:
                return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            return self.SET_DEFAULT_VALUE_INT_9999999

    def idcardValidDays(self):
        """idcardValidDays 身份证有效天数"""
        result1 = self.mysql.queryall_by_customer_id(db='customer_center',
                                                               sql="select ocr_validDate from ocr_log_%s where customer_id='%s'" % (
                                                                   self.info.customer_id % 20, self.info.customer_id))
        if not result1:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            dateResult = result1[0].get('ocr_validDate')
            dateResult = dateResult.replace(".",'').encode("utf-8")


            if not dateResult or'期' in dateResult:
                return self.SET_DEFAULT_VALUE_INT_9999999
            dateResult = str(dateResult)[-8:]
            dateResult = datetime.datetime.strptime(dateResult,"%Y%m%d")
            dataNow = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'),'%Y-%m-%d')
            return (dateResult-dataNow).days

    def identityDigit(self):
        """identityDigit 身份证号位数"""
        result1 = self.mysql.queryall_by_customer_id(db='customer_center',
                                                               sql="select identity_card from customer_identiy_%s where customer_id='%s' and delete_flag=0" % (
                                                                   self.info.customer_id % 20, self.info.customer_id))
        if not result1:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            idCard = factor_decrypt_identity(result1[0].get('identity_card'))
            return len(idCard)

    def relativesPhone(self):
        """relativesPhone 亲属手机号"""
        result1 = self.mysql.queryall_by_customer_id(db='customer_center',
                                                               sql="select contact_mobilephone from customer_contacts_%s where customer_id='%s' and contact_type=1 and delete_flag=0" % (
                                                                   self.info.customer_id % 20, self.info.customer_id))
        if not result1:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            phoneNumber = result1[0].get("contact_mobilephone")
            phoneNumber = phone_clean_new(phoneNumber)
            if phoneNumber:
                return phoneNumber
            else:
                return self.SET_DEFAULT_VALUE_INT_9999999

    def friendPhone(self):
        """colleaguePhone 同事/朋友手机号"""
        result1 = self.mysql.queryall_by_customer_id(db='customer_center',
                                                               sql="select contact_mobilephone from customer_contacts_%s where customer_id='%s' and contact_type=2 and delete_flag=0" % (
                                                                   self.info.customer_id % 20, self.info.customer_id))
        if not result1:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            phoneNumber = result1[0].get("contact_mobilephone")
            phoneNumber = phone_clean_new(phoneNumber)
            if phoneNumber:
                return phoneNumber
            else:
                return self.SET_DEFAULT_VALUE_INT_9999999

    def customerPhone(self):
        """customerPhone 客户手机号"""
        result1 = self.mysql.queryall_by_customer_id(db='customer_center',
                                                               sql="select mobilephone from `user` where id='%s' and delete_flag=0" % (
                                                                   self.info.user_id))
        if not result1:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            phoneNumber = result1[0].get("mobilephone")
            phoneNumber = phone_clean_new(phoneNumber)
            if phoneNumber:
                return phoneNumber
            else:
                return self.SET_DEFAULT_VALUE_INT_9999999

    def callTimeZeroRate(self):
        """callTimeZeroRate 通话时间为0占比"""
        callList=self.mongo.query_contact_action_list_beforeEvenTime_inXdays(db='lake',
                                                                     collection="s_user_mobile_contact_action_{0}".format(int(self.user_id) % 4),
                                                                     find={"user_id": int(self.user_id)},serial_no=self.serial_no,days=30)
        count=0
        sum=0
        if callList=="No DATA":
            return self.SET_DEFAULT_VALUE_INT_9999995
        for call in callList:
            if (return_strfYmd_date(self.info.event_time_add8h)-return_strfYmd_date(call.get("callTime"))).days<=6:
                if call.get('callDuration')==0:
                    print call
                    count+=1
                sum+=1
        if sum==0:
            return self.SET_DEFAULT_VALUE_INT_9999998
        return int(round(float(count)/sum*100,0))

    def userinfoWorkDistrict(self):
        """userinfoWorkDistrict 单位地址区县"""
        sql="select * from work_info_%s where customer_id=%s and delete_flag=0"%(self.info.customer_id%20,self.info.customer_id)
        result=self.mysql.queryone_by_customer_id(db='customer_center',sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999996
        if not result.get("units_district_name"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return result.get("units_district_name")

    def userinfoHomeCounty(self):
        """userinfoHomeDistrict 居住地址区县"""
        sql="select * from home_info_%s where customer_id=%s and delete_flag=0"%(self.info.customer_id%20,self.info.customer_id)
        result=self.mysql.queryone_by_customer_id(db='customer_center',sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999996
        if not result.get("home_district_msg"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return result.get("home_district_msg")

    def gpsDistrict(self):
        """GpsDistrict gps地址区县"""
        data = self.mongo.query_by_user_id('lake', "s_user_mobile_device_info_%s"%str(self.info.user_id%4),
                                           {"user_id": int(self.info.user_id)})
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999996
        lng = data[0].get('location').split(',')[1]
        lat = data[0].get('location').split(',')[0]
        if not lng or not lat:
            return self.SET_DEFAULT_VALUE_INT_9999996
        geoResult=getPlaceFromGeo(lng,lat)
        if not geoResult or not geoResult.get("result") or not geoResult.get("result").get("addressComponent") or not geoResult.get("result").get("addressComponent").get("district"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return  geoResult.get("result").get("addressComponent").get("district")

    def unitsName(self):
        """unitsName 单位名称"""
        sql = "select * from work_info_%s where customer_id=%s and delete_flag=0" % (self.info.customer_id % 20, self.info.customer_id)
        result = self.mysql.queryone_by_customer_id(db='customer_center', sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result.get("units_name"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return result.get("units_name")

    def unitsAddress(self):
        """unitsAddress 单位地址"""
        sql = "select * from work_info_%s where customer_id=%s and delete_flag=0" % (self.info.customer_id % 20, self.info.customer_id)
        result = self.mysql.queryone_by_customer_id(db='customer_center', sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result.get("units_address"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return result.get("units_address")

    def homeAddress(self):
        """homeAddress 居住地址"""
        sql = "select * from home_info_%s where customer_id=%s and delete_flag=0" % (self.info.customer_id % 20, self.info.customer_id)
        result = self.mysql.queryone_by_customer_id(db='customer_center', sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result.get("home_address"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return result.get("home_address")

    def unitsNameBeStudent(self):
        """unitsNameBeStudent 单位名称是否命中疑似学生关键字"""
        regexp_name=u"学院|大学|高等专科学校|职业技术学院|职业学院|职业学校|技术学院|技术学校|技师学院"
        not_regexp_name=u"小学|附属|中学|幼儿|医院|食堂|小吃|超市|公司|舞蹈|美甲|少儿|奶茶"
        sql = "select * from work_info_%s where customer_id=%s and delete_flag=0" % (self.info.customer_id % 20, self.info.customer_id)
        result = self.mysql.queryone_by_customer_id(db='customer_center', sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result.get("units_name"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for reg in regexp_name.split("|"):
            for not_reg in not_regexp_name.split("|"):
                if re.findall(reg,result.get("units_name")) and not re.findall(not_reg,result.get("units_name")):
                    return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def unitsAddressBeStudent(self):
        """unitsAddressBeStudent 单位地址是否命中疑似学生关键字"""
        regexp_name=u"学院|大学|高等专科学校|职业技术学院|职业学院|职业学校|技术学院|技术学校|技师学院"
        not_regexp_name=u"大学路|学院路|小学|附属|中学|幼儿|医院|食堂|小吃|超市|公司|舞蹈|美甲|少儿|奶茶"
        sql = "select * from work_info_%s where customer_id=%s and delete_flag=0" % (self.info.customer_id % 20, self.info.customer_id)
        result = self.mysql.queryone_by_customer_id(db='customer_center', sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result.get("units_address"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for reg in regexp_name.split("|"):
            for not_reg in not_regexp_name.split("|"):
                if re.findall(reg,result.get("units_address")) and not re.findall(not_reg,result.get("units_address")):
                    return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def homeAddressBeStudent(self):
        """homeAddressBeStudent 居住地址是否命中疑似学生关键字"""
        regexp_name=u"学院|大学|高等专科学校|职业技术学院|职业学院|职业学校|技术学院|技术学校|技师学院"
        not_regexp_name=u"大学路|学院路|小学|附属|中学|幼儿|医院|食堂|小吃|超市|公司|舞蹈|美甲|少儿|奶茶"
        sql = "select * from home_info_%s where customer_id=%s and delete_flag=0" % (
        self.info.customer_id % 20, self.info.customer_id)
        result = self.mysql.queryone_by_customer_id(db='customer_center', sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not result.get("home_address"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        for reg in regexp_name.split("|"):
            for not_reg in not_regexp_name.split("|"):
                if re.findall(reg,result.get("home_address")) and not re.findall(not_reg,result.get("home_address")):
                    return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def device_type(self):
        """device_type　设备类型"""
        return self.deviceType()

    def deviceType(self):
        """deviceType 设备类型"""
        results = self.mongo.query_by_user_id(db='lake',
                                              collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return results[0].get("device_type",self.SET_DEFAULT_VALUE_INT_9999999)

    def deviceCapacity(self):
        """deviceCapacity 磁盘容量G"""
        results = self.mongo.query_by_user_id(db='lake',
                                              collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        if not results[0].get("capacity"):
            return self.SET_DEFAULT_VALUE_FLOAT_9999996
        capacity=results[0].get("capacity").replace(" ","").lower()
        if capacity[-4:] == 'byte' and len(capacity) > 4:
            return round(float(capacity[:-4]) / 1024 / 1024 / 1024,4)
        return self.SET_DEFAULT_VALUE_FLOAT_9999996

    def device_capacity(self):
        """device_capacity 磁盘容量G"""
        results = self.mongo.query_by_user_id(db='lake',
                                              collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get("capacity"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        capacity=results[0].get("capacity").replace(" ","").lower()
        if capacity[-4:] == 'byte' and len(capacity) > 4:
            return int(round(float(capacity[:-4]) / 1024 / 1024 / 1024,0))
        return self.SET_DEFAULT_VALUE_INT_9999996

    def deviceModel(self):
        """deviceModel android机型"""
        results = self.mongo.query_by_user_id(db='lake',
                                              collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get("model"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        model = results[0].get('model').replace(' ', '').lower()
        model = re.sub(u"[\s,\u00A0,\u3000,\u2028,\u2029]", '', model)
        return model

    def device_model(self):
        """device_model android机型"""
        return self.deviceModel()

    def device_screen_size(self):
        """device_screen_size """
        results = self.mongo.query_by_user_id(db='lake',
                                              collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get('screen'):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return int(results[0].get('screen').split('*')[0])*int(results[0].get('screen').split('*')[1])

    def deviceImei(self):
        """deviceImei 设备imei"""
        results = self.mongo.query_by_user_id(db='lake',
                                              collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get("imei"):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return results[0].get("imei",self.SET_DEFAULT_VALUE_INT_9999999)
    def deviceImsi(self):
        """deviceImsi 设备imsi"""
        results = self.mongo.query_by_user_id(db='lake',
                                              collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return results[0].get("imsi",self.SET_DEFAULT_VALUE_INT_9999999)

    def deviceIfa(self):
        """deviceIfa 设备ifa"""
        results = self.mongo.query_by_user_id(db='lake',
                                              collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return results[0].get("idfa",self.SET_DEFAULT_VALUE_INT_9999999)

    def deviceManufacture(self):
        """deviceManufacture 设备制造商"""
        results = self.mongo.query_by_user_id(db='lake',
                                              collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get("manfacture"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return results[0].get("manfacture").upper()

    def deviceMemory(self):
        """deviceMemory """
        results = self.mongo.query_by_user_id(db='lake',
                                              collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        if not results[0].get("memory"):
            return self.SET_DEFAULT_VALUE_FLOAT_9999996
        memory=results[0].get("memory").replace(' ','').lower()
        if memory[-2:].lower() == 'kb' and len(memory) > 2:
            return round(float(memory[:-2]) / 1024 / 1024 , 4)
        if memory[-4:].lower()== 'byte' and len(memory) > 4:
            return round(float(memory[:-4]) / 1024 / 1024 / 1024, 4)
        return self.SET_DEFAULT_VALUE_FLOAT_9999999

    def deviceModelCleanAfter(self):
        """deviceModelCleanAfter """
        results = self.mongo.query_by_user_id(db='lake',
                                              collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)})
        if not results:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if not results[0].get("model"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        model=results[0].get("model").replace(' ','').lower()
        model=re.sub(u"[\s,\u00A0,\u3000,\u2028,\u2029]",'',model)
        for str_ in ("(",u"（",u"）",")",",",u"，"):
            find_line=model.find(str_)
            if find_line!=-1:
                model=model[:find_line]
        return model

    def appEdition(self):
        """appEdition app版本号"""
        device_results = self.mongo.query_by_user_id(db='lake',
                                                     collection="s_user_mobile_device_info_{0}".format(int(self.info.user_id) % 4),
                                                     find={"customer_id": int(self.info.customer_id)})
        if not device_results or not device_results[0].get('app_version'):
            return self.SET_DEFAULT_VALUE_INT_9999999
        return device_results[0].get('app_version')

    def appVersion(self):
        """appVersion app版本"""
        return self.appEdition()

    def identityCheckType(self):
        """identityCheckType 身份校验类型"""
        sql="select * from customer_ocr_provider_{0} where (provider='FACE_ID' or provider='WZ') and customer_id={1}".format(self.info.customer_id%20,self.info.customer_id)
        result=self.mysql.queryall_by_table_new_only(db='customer_center',sql=sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999996
        if len(result)!=2:
            return self.SET_DEFAULT_VALUE_INT_9999996
        if len(result)==2:
            OCR=[]
            OCR.append(result[0].get("provider"))
            OCR.append(result[1].get("provider"))
            if len(list(set(OCR)))!=1:
                return self.SET_DEFAULT_VALUE_INT_9999995
            if list(set(OCR))[0] not in ["FACE_ID","WZ"]:
                return self.SET_DEFAULT_VALUE_INT_9999995
        if result[0].get("provider")=='FACE_ID':
            return 2
        elif result[0].get("provider")=='WZ':
            return 1


    def hourlyArtificialApplyNumber(self):
        """hourlyArtificialApplyNumber 每小时进入人工的客户数"""
        results = self.mongo.query_all_by_userId_inOneHour(db='skynet',
                                                         collection="skynet_decision_result",
                                                         find={"data.decisionResult":"001"},
                                                         serial_no=self.serial_no)
        count=0
        for row in results:
            if row.get("product_code") in ("vip_loan","sxj_loan","kdw_loan"):
                count+=1
        return count

    def applicationCnt(self):
        """applicationCnt 当天申请开户量"""
        customerId=[]
        data=self.mongo.query_all_by_userId_inXdays(db='skynet',
                                                    collection='skynet_decision_result',
                                                    serial_no=self.serial_no,
                                                    find={"scene_code" : "credit"},
                                                    start_time='00:00:00',
                                                    start_days=0,
                                                    end_days=1,
                                                    end_time='00:00:00')
        for unit in data:
            customerId.append(unit['customer_id'])
        if not customerId:
            return 0
        return len(list(set(customerId)))

    def currentProductApplicationCnt(self):
        """currentProductApplicationCnt 当前产品当天申请开户量"""
        customerId=[]
        data=self.mongo.query_all_by_userId_inXdays(db='skynet',
                                                    collection='skynet_decision_result',
                                                    serial_no=self.serial_no,
                                                    find={"product_code": self.info.product_code,"scene_code" : "credit"},
                                                    start_time='00:00:00',
                                                    start_days=0,
                                                    end_days=1,
                                                    end_time='00:00:00')
        for unit in data:
            customerId.append(unit['customer_id'])
        if not customerId:
            return 0
        return len(list(set(customerId)))

    def __userinfoUnitsnameApplication(self, day):
        units_name = self.info.result.get('data').get('unitsName')
        if not units_name:
            return self.SET_DEFAULT_VALUE_INT_9999999
        sql = "SELECT * from s_user_product_audit where job_unit='%s' and create_at<='%s' and create_at>='%s'" % (units_name, self.info.event_time_add8h.strftime("%Y-%m-%d %H:%M:%S"), day)
        result = self.mysql.queryall_by_table('xinyongjin', sql)
        id_nos_old = list(set([str(data['id_no']) for data in result]))
        result = self.mongo.query_by_user_id("skynet", "skynet_user_apply_info",
                                             {"units_name": units_name,
                                              "product_code": "vip_loan",
                                              "create_time": {"$gte": datetime.datetime.strptime(day,"%Y-%m-%d %H:%M:%S") - datetime.timedelta(hours=8)}})

        id_nos_new = list(set([str(data['cert_id']) for data in result]))
        id_nos = list(set(id_nos_old + id_nos_new))
        return len(id_nos)

    def userinfoUnitsnameApplicationCnt(self):
        """userinfoUnitsnameApplicationCnt 同一单位名称对应的申请人数 """
        day = (self.info.event_time_add8h - datetime.timedelta(days=179)).strftime("%Y-%m-%d %H:%M:%S")
        return self.__userinfoUnitsnameApplication(day)

    def userinfoUnitsnameApplication1daysCnt(self):
        """userinfoUnitsnameApplication1daysCnt 同一单位名称近1天对应的申请人数"""
        day = (self.info.event_time_add8h - datetime.timedelta(seconds=24 * 60 * 60)).strftime("%Y-%m-%d %H:%M:%S")
        return self.__userinfoUnitsnameApplication(day)

    def userinfoUnitsnameApplication7daysCnt(self):
        """userinfoUnitsnameApplication7daysCnt 同一单位名称近7天对应的申请人数"""
        day = (self.info.event_time_add8h - datetime.timedelta(days=6)).strftime("%Y-%m-%d 00:00:00")
        return self.__userinfoUnitsnameApplication(day)

    def userinfoUnitsnameApplication15daysCnt(self):
        """userinfoUnitsnameApplication15daysCnt 同一单位名称近15天对应的申请人数"""
        day = (self.info.event_time_add8h - datetime.timedelta(days=14)).strftime("%Y-%m-%d 00:00:00")
        return self.__userinfoUnitsnameApplication(day)

    def registrationChannel(self):
        """registrationChannel 注册渠道  --银码头，大王贷"""
        sql="SELECT app_id,channel_code FROM pms_product_register_{0} WHERE user_id={1};".format(int(self.info.user_id%64),self.info.user_id)
        result=self.mysql.queryone_by_customer_id("pms_product_register",sql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999995
        if result['channel_code']=='ljd-yinmatouapi_cpc_zbc':
            return 2
        if result['channel_code'] == 'ljd-xinlangdwd_cpl_qck':
            return 5
        if result['channel_code'] == 'ljd-qunajieapi_cpj_lj':
            return 6
        if result['channel_code'] == 'ljd-hqwyapi_cpl_lj':
            return 7
        elif result['app_id']=="10002":
            return 1
        elif result['app_id']=="102":
            return 3
        elif result['app_id']=="101":
            return 4
        return self.SET_DEFAULT_VALUE_INT_9999995

    def currentChannel(self):
        """currentChannel 当前进件渠道渠道  --银码头，大王贷"""
        result = self.mongo.query_by_user_id('skynet', "skynet_user_info", {"serial_no": self.serial_no})
        if not result:
            return
        result = result[0]
        channel_code = result.get('channel_code',self.SET_DEFAULT_VALUE_INT_9999999)
        if not channel_code:
            return self.SET_DEFAULT_VALUE_INT_0
        if channel_code=="ljd-yinmatouapi_cpc_zbc":
            return 1
        if channel_code=="ljd-xinlangdwd_cpl_qck":
            return 2
        if channel_code=="ljd-qunajieapi_cpj_lj":
            return 3
        if channel_code=="ljd-hqwyapi_cpl_lj":
            return 4
        return 0


    def days7LogIntervalAvg(self):
        """days7LogIntervalAvg	近7天平均登录间隔(天)"""
        login_day_list=[]
        sql="select min(create_at) as create_at from customer where id ='%s';"%(self.info.customer_id)
        customer_result=self.mysql.queryall_by_customer_id('customer_center', sql)
        if not customer_result:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        regist_date =  customer_result[0].get('create_at')
        if not regist_date:
            regist_days_sub =6
        else:
            regist_days_sub= (return_strfYmd_date(self.info.event_time)-return_strfYmd_date(regist_date)).days
        sub_days=min(regist_days_sub,6)
        device_results = self.mongo.query_all_by_userId_inXdays(db='lake',
                                                                collection="s_user_mobile_device_info_{0}".format(
                                                                    int(self.info.user_id) % 4),
                                                                find={"user_id": int(
                                                                    self.info.user_id)},
                                                                serial_no=self.serial_no, start_days=sub_days,
                                                                start_time='00:00:00', end_days=1)
        device_results_all = self.mongo.query_all_by_userId_inXdays(db='lake',
                                                                collection="s_user_mobile_device_info_{0}".format(
                                                                    int(self.info.user_id) % 4),
                                                                find={"user_id": int(
                                                                    self.info.user_id)},
                                                                serial_no=self.serial_no, start_days=3000,
                                                                start_time='00:00:00', end_days=1)
        start_day = str(self.info.event_time + datetime.timedelta(hours=8) - datetime.timedelta(days=6))[0:10] + ' ' + "00:00:00"
        start_date = datetime.datetime.strptime(start_day, "%Y-%m-%d %H:%M:%S") - datetime.timedelta(hours=8)
        if not regist_date and device_results_all and not device_results:
            login_day_list.append(start_date)
        elif  not regist_date and len(device_results_all)>len(device_results):
            login_day_list.append(start_date)
        elif not regist_date and device_results:
            login_day_list.append(device_results[0].get('create_at'))
        elif not regist_date and not device_results:
            return self.SET_DEFAULT_VALUE_FLOAT_9999999
        elif (return_strfYmd_date(self.info.event_time)-return_strfYmd_date(regist_date)).days >6:
            login_day_list.append(start_date)
        else:
            login_day_list.append(regist_date)
        if device_results:
            for row in device_results:
                login_day_list.append(row.get('create_at'))
        login_day_list.append(self.info.event_time)
        login_day_list.sort()
        date_sub_list=[]
        for i in range(1,len(login_day_list)):
            date_sub_list.append( (return_strfYmd_date(login_day_list[i])-return_strfYmd_date(login_day_list[i-1])).days)
        return  round(float(sum(date_sub_list))/len(date_sub_list),4)

    def days30DayLogCnt(self):
        """days30DayLogCnt	近30天白天登录次数"""
        days30DayLogCnt=0
        device_results = self.mongo.query_all_by_userId_inXdays(db='lake',
                                                                collection="s_user_mobile_device_info_{0}".format(
                                                                    int(self.info.user_id) % 4),
                                                                find={"user_id": int(self.info.user_id)},
                                                                serial_no=self.serial_no, start_days=29,
                                                                start_time='00:00:00', end_days=1000)
        if not device_results or len(device_results)==0:
            return -9999999
        for row in device_results:
            device_time_hour=(row.get('create_at')+ datetime.timedelta(hours=8)).hour
            if device_time_hour>=6 and device_time_hour<=17:
                days30DayLogCnt+=1
        return days30DayLogCnt

    def days30LogProvMax(self):
        """days30LogProvMax 近30个自然天登录最多的省份(去省)"""
        provice_sort = [u'台湾', u'香港', u'澳门', u'西藏', u'新疆', u'宁夏', u'江西', u'广东', u'广西', u'福建', u'云南', u'青海', u'湖北',u'甘肃',
                        u'吉林', u'四川', u'海南', u'河北', u'辽宁', u'湖南', u'重庆', u'陕西', u'浙江', u'上海', u'黑龙江', u'江苏', u'河南',u'山西', u'贵州']
        data = self.mongo.query_all_by_userId_inXdays(db='lake',
                                                      collection="s_user_mobile_device_info_{0}".format(
                                                          int(self.info.user_id) % 4),
                                                      serial_no=self.serial_no,
                                                      find={"user_id": int(self.info.user_id)},
                                                      start_days=29,
                                                      start_time="00:00:00",
                                                      end_days=0)
        if not data:
            return self.SET_DEFAULT_VALUE_INT_9999999
        location = []
        province_list = []
        province_dict = {}
        for unit in data:
            location.append(unit['location'])
        for locat in location:
            lng = locat.split(',')[1]
            lat = locat.split(',')[0]
            geoResult = getPlaceFromGeo(lng, lat)
            if geoResult.get('result') and geoResult.get('result').get('addressComponent') and geoResult.get('result').get('addressComponent').get('city'):
                province = geoResult['result']['addressComponent']['province']
                if province != "" or province:
                    province_list.append(province.replace(u'市', '').replace(u'省', ''))


        for i in province_list:
            province_dict[i] = province_list.count(i)

        sort_province = sorted(province_dict.items(), key=lambda item: item[1])
        sort_province_max = []

        for i in sort_province:
            if sort_province[-1][1] == i[1]:
                sort_province_max.append(i)

        for i in provice_sort:
            for j in sort_province_max:
                if i == j[0]:
                    return j[0]

    def __get_contact_action_in_30days_lengthInXdays(self,days=0):
        total_call_inXdays_list=[]
        total_call_inXdays_call_time_list=[]
        results=self.mongo.query_all_by_userId_inXdays(db='lake',
                                              collection="s_user_mobile_contact_action_{0}".format(int(self.info.user_id) % 4),
                                              find={"user_id": int(self.info.user_id)},serial_no=self.serial_no,start_days=30, end_days=1,end_time="00:00:00")
        if days >0:
            start_date = self.info.event_time - datetime.timedelta(days=days) + datetime.timedelta(hours=8)
            end_date = self.info.event_time + datetime.timedelta(hours=8)
        for row in results:
            for subrow in row.get('actions'):
                if days >0 and (subrow.get('callTime')<start_date or subrow.get('callTime')>end_date):
                    break
                if subrow.get('callTime') not in total_call_inXdays_call_time_list:
                    total_call_inXdays_list.append(subrow)
                    total_call_inXdays_call_time_list.append(subrow.get('callTime'))
        return total_call_inXdays_list

    def total_timespan_60(self):
        """total_timespan_60 通话跨度60天及以上的号码数量(取到的数据至申请日全部数据去重）（取到通话记录，匹配不到通话跨度60天及以上的号码数据, 记为0）"""
        total_call_in30days_list = self.__get_contact_action_in_30days_lengthInXdays()
        if len(total_call_in30days_list)==0:
            return -9999999
        cnt=0
        #获取去重的电话号码
        phone_list=[]
        for row in total_call_in30days_list:
            row_phone=self.info.get_phone_one_after_cleaned(str(row.get('callNumber')))
            if  row_phone not in phone_list:
                phone_list.append(row_phone)
        for phone in phone_list:
            #获取每个号码的通话时间点
            phone_time=[]
            for row in total_call_in30days_list:
                row_phone = self.info.get_phone_one_after_cleaned(str(row.get('callNumber')))
                if row_phone==phone:
                    phone_time.append(row.get('callTime'))
            if (max(phone_time) - min(phone_time)).days >= 60:
                cnt = cnt + 1
        return cnt

    def hitReduceList(self):
        """hitReduceList 是否击中降额名单   --全产品"""
        sql="SELECT user_id FROM `skynet_fact_material`.`skynet_user_need_reduce` WHERE user_id='%s'AND delete_flag=0 ;" % (self.info.user_id)
        result=self.mysql.queryall_by_customer_id('skynet_fact_material',sql)
        if not result:
            return 0
        return 1

    def user_age_by_year(self):
        """age 年龄"""
        if len(self.info.cert_id)!=18:
            return self.SET_DEFAULT_VALUE_INT_9999999
        else:
            return int(self.info.create_time.strftime('%Y'))-int(self.info.cert_id[6:10])

    def isCreditCardUser(self):
        """isCreditCardUser 申请人是否为信用卡客户  --产品：2345借款"""
        if self.info.result.get("data").get("creditCard"):
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0


if __name__ == "__main__":
    serial_no = "1547454773000-A0A205790B32A41A0512920109FFA7C0"
    a = BaseFactor('T1', serial_no)
    print a.hitReduceList()
