# coding:utf-8
import datetime
from utils.otherUtil import *
from FrameRunner.FactorInit import NewFactorInit
from utils.TestInit import factor_encrypt_identity, factor_decrypt_identity

class SkynetRotaFactor(NewFactorInit):
    def __init__(self, env, serial_no):
        super(SkynetRotaFactor, self).__init__(env, serial_no)

    def __hitFreezeList(self, productId):
        mysql = "select * from rota_freeze where cert_id='{0}' and product_id={1} and freeze_expires>='{2}' and is_deleted=0".format(
            factor_encrypt_identity(int(self.info.cert_id)),
            productId, datetime.datetime.now())
        result = self.mysql.queryone_by_customer_id_sxj(db='skynet_rota', sql=mysql)
        if not result:
            return 0
        return 1

    def hitFreezeListLjd(self):
        """IsDjLjd 判断用户是否命中立即贷冻结名单"""
        return self.__hitFreezeList(productId=self.ljd_product_id)

    def hitFreezeListSxj(self):
        """IsDjSxj 判断用户是否命中随心借冻结名单"""
        return self.__hitFreezeList(productId=self.sxj_product_id)

    def hitFreezeListKdw(self):
        """IsDjKdw 判断用户是否命中卡贷王冻结名单"""
        return self.__hitFreezeList(productId=self.kdw_product_id)

    def hitFreezeListDkw(self):
        """IsDjDkw 判断用户是否命中贷款王冻结名单"""
        return self.__hitFreezeList(productId=self.rota_dkw_product_id)

    def hitFreezeListJkd(self):
        """IsDjJkd 判断用户是否命中即刻贷冻结名单"""
        return self.__hitFreezeList(productId=self.rota_jkd_product_id)

    def contactsPhoneHitFrozenPhoneCnt(self):
        """contactsPhoneHitFrozenPhoneCnt 申请人的联系人手机号命中冻结客户手机号个数  产品：全产品"""
        count = self.SET_DEFAULT_VALUE_INT_0
        if self.info.relativeContact:
            sql = "select * from rota_freeze where is_deleted=0 and encryption_phone='%s'" % factor_encrypt_identity(self.info.relativeContact)
            status_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
            if status_result:
                count += 1
        if self.info.colleagueContact:
            sql = "select * from rota_freeze where is_deleted=0 and encryption_phone='%s'" % factor_encrypt_identity(self.info.colleagueContact)
            status_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
            if status_result:
                count += 1
        if self.info.friendContact:
            sql = "select * from rota_freeze where is_deleted=0 and encryption_phone='%s'" % factor_encrypt_identity(self.info.friendContact)
            status_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
            if status_result:
                count += 1
        return count

    def phoneHitFrozenCertIdCnt(self):
        """phoneHitFrozenCertIdCnt 申请人手机号命中冻结客户手机号个数"""
        sql = "select * from rota_freeze where is_deleted=0 and encryption_phone='%s'" % factor_encrypt_identity(self.info.phone)
        rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        if not rota_result:
            return self.SET_DEFAULT_VALUE_INT_0
        cardIds = []
        for card in rota_result:
            if card.get('cert_id'):
                cardIds.append(factor_decrypt_identity(card.get('cert_id')))
        return len(list(set(cardIds)))

    def idcardHitFrozenIdcard(self):
        """idcardHitFrozenIdcard 申请人身份证号命中冻结客户身份证号"""
        sql = "select * from rota_freeze where is_deleted=0 and cert_id='%s'" % factor_encrypt_identity(
            self.info.cert_id)
        rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        if not rota_result:
            return self.SET_DEFAULT_VALUE_INT_0
        return self.SET_DEFAULT_VALUE_INT_1

    def __hitFraud(self, device_type):
        devices = []
        count = 0
        result = self.mongo.query_all_by_userId_inXdays(db='lake', collection='s_user_mobile_device_info_{0}'.format(
            int(self.info.user_id) % 4),
                                                        find={'user_id': self.info.user_id}, serial_no=self.serial_no,
                                                        start_days=1, end_days=0)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if device_type == 'imei':
            for d in result[:20]:
                if d.get('imei'):
                    devices.append(d.get('imei'))
            if not devices:
                return self.SET_DEFAULT_VALUE_INT_9999999
            if len(list(set(devices))) > 5:
                return self.SET_DEFAULT_VALUE_INT_9999997
            for imei in list(set(devices)):
                sql = "select * from rota_fraud where imei='%s' and is_deleted=0" % imei
                rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
                if rota_result:
                    count += 1
            return count
        elif device_type == 'idfa':
            for d in result[:20]:
                if d.get('idfa'):
                    devices.append(d.get('idfa'))
            if not devices:
                return self.SET_DEFAULT_VALUE_INT_9999999
            if len(list(set(devices))) > 5:
                return self.SET_DEFAULT_VALUE_INT_9999997
            for idfa in list(set(devices)):
                sql = "select * from rota_fraud where idfa='%s' and is_deleted=0" % idfa
                rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
                if rota_result:
                    count += 1
            return count
        elif device_type == 'imsi':
            for d in result[:20]:
                if d.get('imsi'):
                    devices.append(d.get('imsi'))
            if not devices:
                return self.SET_DEFAULT_VALUE_INT_9999999
            if len(list(set(devices))) > 5:
                return self.SET_DEFAULT_VALUE_INT_9999997
            for imsi in list(set(devices)):
                sql = "select * from rota_fraud where imsi='%s' and is_deleted=0" % imsi
                rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
                if rota_result:
                    count += 1
            return count
        elif device_type == 'android_id':
            for d in result[:20]:
                if d.get('android_id'):
                    devices.append(d.get('android_id'))
            if not devices:
                return self.SET_DEFAULT_VALUE_INT_9999999
            if len(list(set(devices))) > 5:
                return self.SET_DEFAULT_VALUE_INT_9999997
            for android_id in list(set(devices)):
                sql = "select * from rota_fraud where android_id='%s' and is_deleted=0" % android_id
                rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
                if rota_result:
                    count += 1
            return count
        elif device_type == "mac":
            for d in result[:20]:
                if d.get('mac'):
                    devices.append(d.get('mac'))
            if not devices:
                return self.SET_DEFAULT_VALUE_INT_9999999
            if len(list(set(devices))) > 5:
                return self.SET_DEFAULT_VALUE_INT_9999997
            for mac in list(set(devices)):
                sql = "select * from rota_fraud where mac='%s' and is_deleted=0" % mac
                rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
                if rota_result:
                    count += 1
            return count
        else:
            return self.SET_DEFAULT_VALUE_INT_9999999

    def hitFraudImsiCnt(self):
        """hitFraudImsiCnt 申请人imsi命中欺诈客户imsi的个数"""
        return self.__hitFraud(device_type='imsi')

    def hitFraudIdfaCnt(self):
        """hitFraudIdfaCnt 申请人idfa命中欺诈客户idfa的个数"""
        return self.__hitFraud(device_type='idfa')

    def hitFraudImeiCnt(self):
        """hitFraudImeiCnt 申请人imei命中欺诈客户imei的个数"""
        return self.__hitFraud(device_type='imei')

    def hitFraudAndroididCnt(self):
        """hitFraudAndroididCnt 申请人androidid命中欺诈客户androidid的个数"""
        return self.__hitFraud(device_type='android_id')

    def hitFraudMacCnt(self):
        """hitFraudMacCnt 申请人mac命中欺诈客户mac的个数 """
        return self.__hitFraud(device_type='mac')

    def __hitFraudMore(self, deviceList):
        device0 = deviceList[0]
        device1 = deviceList[1]
        device_all = []
        devices = []
        count = 0
        result = self.mongo.query_all_by_userId_inXdays(db='lake', collection='s_user_mobile_device_info_{0}'.format(
            int(self.info.user_id) % 4),
                                                        find={'user_id': self.info.user_id}, serial_no=self.serial_no,
                                                        start_days=1, end_days=0)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        for dev in result[:20]:
            if dev.get(device0) and dev.get(device1):
                device_all.append(dev)
        if not device_all:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if device0 == 'mac' and device1 == 'imei':
            for d in result[:20]:
                if d.get('mac') and d.get('imei') and [d.get('mac', ''), d.get('imei', '')] not in devices:
                    devices.append([d.get('mac'), d.get('imei')])
            if not devices:
                return self.SET_DEFAULT_VALUE_INT_9999999
            if len(devices) > 5:
                return self.SET_DEFAULT_VALUE_INT_9999997
            for dev in devices:
                sql = "select * from rota_fraud where mac='%s' and imei='%s' and is_deleted=0" % (dev[0], dev[1])
                rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
                if rota_result:
                    count += 1
            return count
        elif device0 == 'imei' and device1 == 'android_id':
            for d in result[:20]:
                if d.get('imei') and d.get('android_id') and [d.get('imei', ''),
                                                              d.get('android_id', '')] not in devices:
                    devices.append([d.get('imei'), d.get('android_id')])
            if not devices:
                return self.SET_DEFAULT_VALUE_INT_9999999
            if len(devices) > 5:
                return self.SET_DEFAULT_VALUE_INT_9999997
            for dev in devices:
                sql = "select * from rota_fraud where imei='%s' and android_id='%s' and is_deleted=0" % (dev[0], dev[1])
                rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
                if rota_result:
                    count += 1
            return count
        else:
            return self.SET_DEFAULT_VALUE_INT_9999999

    def hitFraudImeiAndroididCnt(self):
        """hitFraudImeiAndroididCnt 申请人imei+androidid命中欺诈客户imei+androidid的个数 """
        return self.__hitFraudMore(deviceList=["imei", "android_id"])

    def hitFraudMacImeiCnt(self):
        """hitFraudMacImeiCnt 申请人mac+imei命中欺诈客户mac+imei的个数"""
        return self.__hitFraudMore(deviceList=["mac", "imei"])

    def __HitBadPhone(self, phone):
        sql = "select * from rota_bad where phone='%s' and is_deleted=0" % phone
        rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        if rota_result:
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def phoneHitBadPhone(self):
        """phoneHitBadPhone 申请人手机号命中不良手机号"""
        return self.__HitBadPhone(phone=self.info.phone)

    def relaPhoneHitBadPhone(self):
        """relaPhoneHitBadPhone 申请人的亲属联系人手机号是否命中不良手机号"""
        if self.info.relativeContact:
            return self.__HitBadPhone(phone=self.info.relativeContact)
        return self.SET_DEFAULT_VALUE_INT_9999999

    def friendPhoneHitBadPhone(self):
        """riendPhoneHitBadPhone 申请人的朋友联系人手机号是否命中不良手机号"""
        if self.info.friendContact:
            return self.__HitBadPhone(phone=self.info.friendContact)
        return self.SET_DEFAULT_VALUE_INT_9999999

    def colleaguePhoneHitBadPhone(self):
        """colleaguePhoneHitBadPhone 申请人的同事联系人手机号是否命中不良手机号"""
        if self.info.colleagueContact:
            return self.__HitBadPhone(phone=self.info.colleagueContact)
        return self.SET_DEFAULT_VALUE_INT_9999999

    def idcardHitFraudIdcard(self):
        """idcardHitFraudIdcard 申请人身份证号命中欺诈客户身份证号"""
        sql = "select * from rota_fraud where cert_id='%s' and is_deleted=0" % factor_encrypt_identity(
            self.info.cert_id)
        rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        if rota_result:
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def phoneHitFraudPhoneCnt(self):
        """phoneHitFraudPhoneCnt 申请人手机号命中欺诈客户手机号个数"""
        phoneList = []
        sql = "select * from rota_fraud where phone='%s' and is_deleted=0" % self.info.phone
        rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        if rota_result:
            for fra in rota_result:
                phoneList.append(factor_decrypt_identity(fra.get('cert_id')))
            return len(list(set(phoneList)))
        return self.SET_DEFAULT_VALUE_INT_0

    def contactsPhoneHitFraudPhoneCnt(self):
        """contactsPhoneHitFraudPhoneCnt 申请人的联系人手机号命中欺诈客户手机号个数"""
        count = 0
        if self.info.relativeContact:
            sql = "select * from rota_fraud where phone='%s' and is_deleted=0" % self.info.relativeContact
            rota_relative_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
            if rota_relative_result:
                count += 1
        if self.info.friendContact:
            sql = "select * from rota_fraud where phone='%s' and is_deleted=0" % self.info.friendContact
            rota_friend_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
            if rota_friend_result:
                count += 1
        if self.info.colleagueContact:
            sql = "select * from rota_fraud where phone='%s' and is_deleted=0" % self.info.colleagueContact
            rota_colleague_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
            if rota_colleague_result:
                count += 1
        return count

    def __HitFraudContactsCnt(self, phone):
        carId = []
        sql = "select * from rota_fraud where relative_phone='%s' and is_deleted=0" % phone
        rota_relative_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        for fraud in rota_relative_result:
            carId.append(fraud.get('cert_id'))
        sql = "select * from rota_fraud where friend_phone='%s' and is_deleted=0" % phone
        rota_friend_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        for fraud in rota_friend_result:
            carId.append(fraud.get('cert_id'))
        sql = "select * from rota_fraud where colleague_phone='%s' and is_deleted=0" % phone
        rota_colleague_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        for fraud in rota_colleague_result:
            carId.append(fraud.get('cert_id'))
        return len(list(set(carId)))

    def phoneHitFraudContactsCertIdCnt(self):
        """phoneHitFraudContactsCertIdCnt 申请人手机号命中欺诈客户联系人手机号个数"""
        return self.__HitFraudContactsCnt(phone=self.info.phone)

    def relaPhoneHitFraudContactsCertIdCnt(self):
        """relaPhoneHitFraudContactsCertIdCnt 申请人的亲属联系人手机号命中欺诈客户联系人手机号个数"""
        return self.__HitFraudContactsCnt(phone=self.info.relativeContact)

    def friendPhoneHitFraudContactsCertIdCnt(self):
        """friendPhoneHitFraudContactsCertIdCnt 申请人的朋友联系人手机号命中欺诈客户联系人手机号个数"""
        return self.__HitFraudContactsCnt(phone=self.info.friendContact)

    def colleaguePhoneHitFraudContactsCertIdCnt(self):
        """colleaguePhoneHitFraudContactsCertIdCnt 申请人的同事联系人手机号命中欺诈客户联系人手机号个数"""
        return self.__HitFraudContactsCnt(phone=self.info.colleagueContact)

    def devicenoHitFraudMaxCertIdCnt(self):
        """devicenoHitFraudMaxCertIdCnt 申请人的设备号命中欺诈客户设备号的个数"""
        devices = []
        device_no = []
        result = self.mongo.query_all_by_userId_inXdays(db='lake', collection='s_user_mobile_device_info_{0}'.format(
            int(self.info.user_id) % 4),
                                                        find={'user_id': self.info.user_id}, serial_no=self.serial_no,
                                                        start_days=1, end_days=0)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        for dev in result[:100]:
            if dev.get('device_no') and dev.get('device_no') not in devices:
                devices.append(dev.get('device_no'))
        for dev in devices:
            cardId = []
            sql = "select * from rota_fraud where device_no='%s' and is_deleted=0" % dev
            rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
            for rota in rota_result:
                if rota.get('cert_id') and rota.get('cert_id') not in cardId:
                    cardId.append(rota.get('cert_id'))
            device_no.append(len(cardId))
        return max(device_no)

    def callMax5HitFraudContactsPhoneCnt(self):
        """callMax5HitFraudContactsPhoneCnt 申请人通话记录次数最多的5个人命中欺诈客户联系人手机号个数"""
        phoneMax5 = self.mongo.query_phone_max5_beforeEvenTime_inXdays(db='lake',
                                                                       collection="s_user_mobile_contact_action_{0}".format(
                                                                           int(self.info.user_id) % 4),
                                                                       find={"user_id": int(self.info.user_id)},
                                                                       serial_no=self.serial_no, days=180)
        count = 0
        if phoneMax5 == 'No DATA':
            return self.SET_DEFAULT_VALUE_INT_0
        for phone_ in phoneMax5:
            cardList = self.__HitFraudContactsCnt(phone_)
            if cardList >= 1:
                count += 1
        return count

    def callMax5HitFraudPhoneCnt(self):
        """callMax5HitFraudPhoneCnt 申请人通话记录次数最多的5个人命中欺诈客户手机号个数"""
        phoneMax5 = self.mongo.query_phone_max5_beforeEvenTime_inXdays(db='lake',
                                                                       collection="s_user_mobile_contact_action_{0}".format(
                                                                           int(self.user_id) % 4),
                                                                       find={"user_id": int(self.user_id)},
                                                                       serial_no=self.serial_no, days=180)
        count = 0
        if phoneMax5 == 'No DATA':
            return self.SET_DEFAULT_VALUE_INT_0
        for phone_ in phoneMax5:
            sql = "select * from rota_fraud where phone='%s' and is_deleted=0" % phone_
            rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
            if rota_result:
                count += 1
        return count

    def certIdHitOverdueCertId(self):
        """certIdHitOverdueCertId  申请人身份证号命中逾期客户身份证号  产品：全产品"""
        mysql = "select cert_id from rota_overdue where cert_id='{0}' and is_deleted=0".format(
            factor_encrypt_identity(self.info.cert_id))
        result = self.mysql.queryone_by_customer_id_sxj(db='skynet_rota', sql=mysql)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_0
        return self.SET_DEFAULT_VALUE_INT_1

    def phoneHitOverdueCertIdCnt(self):
        """phoneHitOverdueCertIdCnt 申请人手机号命中逾期客户手机号的身份证号数  产品：全产品"""
        mysql_cert_id = "select count(distinct(cert_id)) as certcnt from rota_overdue where phone='{0}' and is_deleted=0".format(
            self.info.phone)
        result_mysql_cert_id = self.mysql.queryone_by_customer_id_sxj(db='skynet_rota', sql=mysql_cert_id)
        if not result_mysql_cert_id:
            return self.SET_DEFAULT_VALUE_INT_0
        return result_mysql_cert_id.get('certcnt')

    def phoneHitOverdueContactsCertIdCnt(self):
        """phoneHitOverdueContactsCertIdCnt 申请人手机号命中逾期客户联系人手机号个数  产品：全产品"""
        cn_list = []
        mysql = "select * from rota_overdue where relative_phone='{0}' or friend_phone='{0}' or colleague_phone='{0}'  and is_deleted=0".format(
            self.info.phone)
        result = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=mysql)
        for row in result:
            cn_list.append(factor_decrypt_identity(row.get('cert_id')))
        return len(list(set(cn_list)))

    def contactsPhoneHitOverduePhoneCnt(self):
        """ contactsPhoneHitOverduePhoneCnt 申请人的联系人手机号命中逾期客户手机号个数  产品：全产品"""
        if not self.info.colleagueContact:
            contacts = (self.info.relativeContact, self.info.friendContact)
        else:
            contacts = (self.info.relativeContact, self.info.friendContact, self.info.colleagueContact)
        count = 0
        for phone in contacts:
            mysql_overdue = "select * from rota_overdue where phone ='{0}' and is_deleted=0".format(phone)
            result = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=mysql_overdue)
            if result:
                count = count + 1
        return count

    def __HitOverdueContactsCnt(self, phone):
        carId = []
        sql = "select * from rota_overdue where relative_phone='%s' and is_deleted=0" % phone
        rota_relative_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        for fraud in rota_relative_result:
            carId.append(fraud.get('cert_id'))
        sql = "select * from rota_overdue where friend_phone='%s' and is_deleted=0" % phone
        rota_friend_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        for fraud in rota_friend_result:
            carId.append(fraud.get('cert_id'))
        sql = "select * from rota_overdue where colleague_phone='%s' and is_deleted=0" % phone
        rota_colleague_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        for fraud in rota_colleague_result:
            carId.append(fraud.get('cert_id'))
        return len(list(set(carId)))

    def relaPhoneHitOverdueContactsCertIdCnt(self):
        """relaPhoneHitOverdueContactsCertIdCnt 申请人的亲属联系人手机号命中逾期客户联系人手机号个数 产品：全产品"""
        if not self.info.relativeContact:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.__HitOverdueContactsCnt(self.info.relativeContact)

    def friendPhoneHitOverdueContactsCertIdCnt(self):
        """friendPhoneHitOverdueContactsCertIdCnt 申请人的朋友联系人手机号命中逾期客户联系人手机号个数 产品：全产品"""
        if not self.info.friendContact:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.__HitOverdueContactsCnt(self.info.friendContact)

    def colleaguePhoneHitOverdueContactsCertIdCnt(self):
        """colleaguePhoneHitOverdueContactsCertIdCnt 申请人的同事联系人手机号命中逾期客户联系人手机号个数 产品：全产品"""
        if not self.info.colleagueContact:
            return self.SET_DEFAULT_VALUE_INT_9999999
        return self.__HitOverdueContactsCnt(self.info.colleagueContact)

    def devicenoHitOverdueMaxCertIdCnt(self):
        """devicenoHitOverdueMaxCertIdCnt  申请人的设备号命中逾期客户设备号的个数  产品：全产品"""
        result = self.mongo.query_all_by_userId_inXdays(db='lake', collection='s_user_mobile_device_info_{0}'.format(
            int(self.info.user_id) % 4),
                                                        find={'user_id': self.info.user_id}, serial_no=self.serial_no,
                                                        start_days=1, end_days=0)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        devices = []
        for data in result[:20]:
            if data.get('device_no') and data.get('device_no') not in devices:
                devices.append(data.get('device_no'))
        if len(devices) > 5:
            return self.SET_DEFAULT_VALUE_INT_9999997
        count = []
        for device_no in devices:
            cardId = []
            device_mysql = "select cert_id  from  rota_overdue where device_no='{0}' and is_deleted=0".format(device_no)
            result = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=device_mysql)
            for card in result:
                cardId.append(factor_decrypt_identity(card.get('cert_id')))
            count.append(len(cardId))
        return max(count)

    def callMax5HitOverduePhoneCnt(self):
        """callMax5HitOverduePhoneCnt 申请人通话记录次数最多的5个人命中逾期客户手机号个数 产品：全产品"""
        data = self.mongo.query_phone_max5_beforeEvenTime_inXdays('lake', "s_user_mobile_contact_action_{0}".format(
            int(self.user_id) % 4), {"user_id": int(self.user_id)}, self.serial_no, 180)
        if data == 'No DATA':
            return self.SET_DEFAULT_VALUE_INT_0
        count = 0
        for phone in data:
            mysql_overdue = "select distinct(cert_id) as cert_id from rota_overdue where phone ='{0}' and is_deleted=0".format(
                phone)
            result = self.mysql.queryone_by_customer_id_sxj(db='skynet_rota', sql=mysql_overdue)
            if result:
                count = count + 1
        return count

    def callMax5HitOverdueContactsPhoneCnt(self):
        """callMax5HitOverdueContactsPhoneCnt 申请人通话记录次数最多的5个人命中逾期客户联系人手机号个数  产品：全产品"""
        data = self.mongo.query_phone_max5_beforeEvenTime_inXdays('lake',
                                                                  "s_user_mobile_contact_action_{0}".format(
                                                                      int(self.user_id) % 4),
                                                                  {"user_id": int(self.user_id)},
                                                                  self.serial_no,
                                                                  180)
        if data == 'No DATA':
            return self.SET_DEFAULT_VALUE_INT_0
        count = 0
        for phone in data:
            mysql_overdue = "select distinct(cert_id) as cert_id from rota_overdue where friend_phone ='{0}' or colleague_phone='{0}' or relative_phone='{0}' and is_deleted=0".format(
                phone)
            result = self.mysql.queryone_by_customer_id_sxj(db='skynet_rota', sql=mysql_overdue)
            if result:
                count = count + 1
        return count

    def __hitBlackDeviceMore(self, deviceList):
        result = self.mongo.query_all_by_userId_inXdays(db='lake', collection='s_user_mobile_device_info_{0}'.format(
            int(self.info.user_id) % 4),
                                                        find={'user_id': self.info.user_id}, serial_no=self.serial_no,
                                                        start_days=1, end_days=0)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        devices = []
        device1 = deviceList[0]
        device2 = deviceList[1]
        for row in result[0:20]:
            if row.get(device1) and row.get(device2) and [row.get(device1), row.get(device2)] not in devices:
                devices.append([row.get(device1), row.get(device2)])
        if not devices:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if len(devices) > 5:
            return self.SET_DEFAULT_VALUE_INT_9999997
        count = 0
        for de in devices:
            sql_mi = 'SELECT * FROM rota_device WHERE {0}="{1}" AND {2}="{3}" AND is_deleted=0;'.format(device1, de[0],
                                                                                                        device2, de[1])
            result = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=sql_mi)
            if result:
                count = count + 1
        return count

    def hitBlackDeviceMacImeiCnt(self):
        """hitBlackDeviceMacImeiCnt 申请人mac+imei命中设备名单mac+imei的个数 产品：全产品"""
        return self.__hitBlackDeviceMore(deviceList=["mac", "imei"])

    def hitBlackDeviceImeiAndroididCnt(self):
        """hitBlackDeviceImeiAndroididCnt 申请人imei+androidid命中设备名单imei+androidid的个数  产品：全产品"""
        return self.__hitBlackDeviceMore(deviceList=["imei", "android_id"])

    def __hitBlackDevice(self, device):
        result = self.mongo.query_all_by_userId_inXdays(db='lake', collection='s_user_mobile_device_info_{0}'.format(
            int(self.info.user_id) % 4),
                                                        find={'user_id': self.info.user_id}, serial_no=self.serial_no,
                                                        start_days=1, end_days=0)
        if not result:
            return self.SET_DEFAULT_VALUE_INT_9999999
        device_list = []
        for row in result[:20]:
            if row.get(device) and row.get(device) not in device_list:
                device_list.append(row.get(device))
        if not device_list:
            return self.SET_DEFAULT_VALUE_INT_9999999
        if len(device_list) > 5:
            return self.SET_DEFAULT_VALUE_INT_9999997
        count = 0
        for de in device_list:
            sql_mac = 'SELECT * FROM rota_device WHERE {0}="{1}" AND is_deleted=0;'.format(device, de)
            result = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=sql_mac)
            if result:
                count = count + 1
        return count

    def hitBlackDeviceMacCnt(self):
        """hitBlackDeviceMacCnt 申请人mac命中设备名单mac的个数   产品：全产品"""
        return self.__hitBlackDevice(device='mac')

    def hitBlackDeviceAndroididCnt(self):
        """hitBlackDeviceAndroididCnt 申请人androidid命中设备名单androidid的个数  产品：全产品"""
        return self.__hitBlackDevice(device='android_id')

    def hitBlackDeviceImeiCnt(self):
        """hitBlackDeviceImeiCnt 申请人imei命中设备名单imei的个数   产品：全产品"""
        return self.__hitBlackDevice(device='imei')

    def hitBlackDeviceIdfaCnt(self):
        """hitBlackDeviceIdfaCnt 申请人idfa命中设备名单idfa的个数   产品：全产品"""
        return self.__hitBlackDevice(device='idfa')

    def maxContactPhoneCallCnt(self):
        """maxContactPhoneCallCnt 与坏账客户通话的最大次数 """
        max_count = []
        # skynet_rota 通话黑名单 rota_contact_1 rota_contact_2 立即贷的通话黑名单 rota_contact_meta 管控走的1或者2 rota_dkw_contact 贷款王黑名单
        sql = 'select `table_name` from rota_contact_meta where status=1'
        status_result = self.mysql.queryone_by_customer_id_sxj('skynet_rota', sql)
        sql_ljd = "select callcnt from  %s  where contact_phone='%s'" % (status_result['table_name'], self.info.phone)
        ljd_result = self.mysql.queryall_by_table_new_only('skynet_rota', sql_ljd)
        if ljd_result:
            for unit in ljd_result:
                max_count.append(unit['callcnt'])
        sql_dkw = "select callcnt from rota_dkw_contact where contact_phone='%s'" % self.info.phone
        dkw_result = self.mysql.queryall_by_table_new_only('skynet_rota', sql_dkw)
        if dkw_result:
            for unit in dkw_result:
                max_count.append(unit['callcnt'])
        if not max_count:
            return 0
        return max(max_count)

    def phoneHitBlackCallListMaxTime(self):
        """phoneHitBlackCallListMaxTime 申请人手机号命中通话记录黑名单手机号，该号码与对应坏账客户的通话时长  产品：全产品"""
        max_count = []
        # skynet_rota 通话黑名单 rota_contact_1 rota_contact_2 立即贷的通话黑名单 rota_contact_meta 管控走的1或者2 rota_dkw_contact 贷款王黑名单
        sql = 'select `table_name` from rota_contact_meta where status=1'
        status_result = self.mysql.queryone_by_customer_id_sxj('skynet_rota', sql)
        sql_ljd = "select * from %s where contact_phone='%s'" % (status_result['table_name'], self.info.phone)
        ljd_result = self.mysql.queryall_by_table_new_only('skynet_rota', sql_ljd)
        if ljd_result:
            for unit in ljd_result:
                if unit['callduration']:
                    max_count.append(unit['callduration'])
        sql_dkw = "select * from rota_dkw_contact where contact_phone='%s'" % self.info.phone
        dkw_result = self.mysql.queryall_by_table_new_only('skynet_rota', sql_dkw)
        if dkw_result:
            for unit in dkw_result:
                max_count.append(unit['callduration'])
        if not max_count:
            return self.SET_DEFAULT_VALUE_INT_0
        return max(max_count)

    @staticmethod
    def __getRiskGrade(code):
        if code == "0":
            return 10
        if code == "1":
            return 11
        if code == "2":
            return 12
        if code == "3":
            return 13
        if code == "4":
            return 14
        if code == "5":
            return 15
        return code

    def __contactHitBadContactPhone(self, contact):
        sql = "select * from rota_general_list where is_deleted=0 and number_value='%s'" % contact
        result = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=sql)
        if result and result[0].get("number_type") == "1001":
            if not result[0].get("risk_grade"):
                return self.SET_DEFAULT_VALUE_INT_9999996
            return self.__getRiskGrade(result[0].get("risk_grade"))
        if result and result[0].get("number_type") != "1001":
            return 9
        if not result:
            return 0

    def contact1HitBadContactPhone(self):
        """contact1HitBadContactPhone 客户直系亲属手机号命中不良联系人号码"""
        if not self.info.relativeContact:
            return -1
        return self.__contactHitBadContactPhone(self.info.relativeContact)

    def contact2HitBadContactPhone(self):
        """contact2HitBadContactPhone 客户朋友手机号命中不良联系人号码"""
        if not self.info.friendContact:
            return -1
        return self.__contactHitBadContactPhone(self.info.friendContact)

    def contact3HitBadContactPhone(self):
        """contact3HitBadContactPhone 客户同事手机号命中不良联系人号码"""
        if not self.info.colleagueContact:
            return -1
        return self.__contactHitBadContactPhone(self.info.colleagueContact)

    def userPhoneHitBadContactPhone(self):
        """userPhoneHitBadContactPhone 客户注册号码手机号命中不良联系人号码"""
        if not self.info.phone:
            return -1
        return self.__contactHitBadContactPhone(self.info.phone)

    def homeAddressHitRiskAddress(self):
        """homeAddressHitRiskAddress 客户居住地址命中风险地址"""
        if not self.info.homeAddress:
            return self.SET_DEFAULT_VALUE_INT_9999999
        sql = "select * from rota_address_list where is_deleted=0 and address_name='%s'" % self.info.homeAddress
        result = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=sql)
        if not result:
            return 0
        grade_all = []
        home_new_grade = []
        units_new_grade = []
        home_address = [address.get("risk_grade") for address in result if address.get("address_type") == "home_address"]
        units_address = [address.get("risk_grade") for address in result if address.get("address_type") == "units_address"]
        if not home_address and not units_address:
            return 9
        for grade in home_address:
            if not grade:
                home_new_grade.append(str(self.SET_DEFAULT_VALUE_INT_9999996))
                continue
            home_new_grade.append(str(self.__getRiskGrade(grade)))
        for grade in units_address:
            if not grade:
                units_new_grade.append(str(self.SET_DEFAULT_VALUE_INT_9999996))
                continue
            if grade in ["0","1","2","3","4","5"]:
                units_new_grade.append(str(self.__getRiskGrade(grade)+10))
            else:
                units_new_grade.append(str(self.__getRiskGrade(grade)))
        grade_all.extend(home_new_grade)
        grade_all.extend(units_new_grade)
        if not grade_all:
            return 0
        grade_all.sort()
        return ','.join(grade_all)

    def unitsAddressHitRiskAddress(self):
        """unitsAddressHitRiskAddress 客户单位地址命中风险地址"""
        if not self.info.unitsAddress:
            return self.SET_DEFAULT_VALUE_INT_9999999
        sql = "select * from rota_address_list where is_deleted=0 and address_name='%s'" % self.info.unitsAddress
        result = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=sql)
        if not result:
            return 0
        grade_all = []
        home_new_grade = []
        units_new_grade = []
        home_address = [address.get("risk_grade") for address in result if address.get("address_type") == "home_address"]
        units_address = [address.get("risk_grade") for address in result if address.get("address_type") == "units_address"]
        if not home_address and not units_address:
            return 9
        for grade in home_address:
            if not grade:
                home_new_grade.append(str(self.SET_DEFAULT_VALUE_INT_9999996))
                continue
            if grade in ["0", "1", "2", "3", "4", "5"]:
                home_new_grade.append(str(self.__getRiskGrade(grade)+10))
            else:
                home_new_grade.append(str(self.__getRiskGrade(grade)))
        for grade in units_address:
            if not grade:
                units_new_grade.append(str(self.SET_DEFAULT_VALUE_INT_9999996))
                continue
            units_new_grade.append(str(self.__getRiskGrade(grade)))
        grade_all.extend(home_new_grade)
        grade_all.extend(units_new_grade)
        if not grade_all:
            return 0
        grade_all.sort()
        return ','.join(grade_all)

    def unitsNameHitRiskName(self):
        """unitsNameHitRiskName 客户单位名称命中风险单位名称"""
        if not self.info.unitsName:
            return self.SET_DEFAULT_VALUE_INT_9999999
        sql = "select * from rota_company_list where is_deleted=0 and company_name='%s'" % self.info.unitsName
        result = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=sql)
        if not result:
            return 0
        if not result[0].get("risk_grade"):
            return self.SET_DEFAULT_VALUE_INT_9999996
        return self.__getRiskGrade(result[0].get("risk_grade"))

    def __get_device_info(self, deviceType):
        result = self.mongo.query_all_by_userId_inXdays(db='lake', collection='s_user_mobile_device_info_{0}'.format(
            int(self.info.user_id) % 4),
                                                        find={'user_id': self.info.user_id}, serial_no=self.serial_no,
                                                        start_days=30, end_days=0)
        if not result:
            return -1
        lakeList = []
        for data in result:
            if data.get(deviceType):
                lakeList.extend(data.get(deviceType).split(','))
        deviceList = list(set(lakeList))
        if not deviceList:
            return -1
        riskGradeList = []
        riskGradeList_9 = []
        if deviceType=="network_env":
            deviceType="networkenv"
        for T in deviceList:
            sql = "select * from rota_general_list where is_deleted=0 and number_value='%s' and number_type='%s'" % (T, deviceType)
            deviceTResult = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=sql)
            deviceTList = [d.get("risk_grade") for d in deviceTResult]
            for grade in deviceTList:
                if not grade:
                    riskGradeList.append(str(self.SET_DEFAULT_VALUE_INT_9999996))
                    continue
                riskGradeList.append(str(self.__getRiskGrade(grade)))
        for T in deviceList:
            sql="select * from rota_general_list where is_deleted=0 and number_value='%s' and number_type !='%s'" % (T, deviceType)
            deviceTResult = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=sql)
            deviceTList_9 = [d.get("risk_grade") for d in deviceTResult]
            for grade in deviceTList_9:
                if not grade:
                    riskGradeList_9.append(str(self.SET_DEFAULT_VALUE_INT_9999996))
                    continue
                riskGradeList_9.append(str(self.__getRiskGrade(grade)))
        if not riskGradeList and not riskGradeList_9:
            return 0
        if not riskGradeList and riskGradeList_9:
            return 9
        riskGradeList.sort()
        return ','.join(riskGradeList)

    def qqHitRiskQqWeixin(self):
        """QqHitRiskQqWeixin 客户QQ命中风险QQ"""
        return self.__get_device_info(deviceType='qq')

    def idfaHitRiskIdfa(self):
        """idfaHitRiskIdfa 客户idfa命中风险idfa"""
        return self.__get_device_info(deviceType='idfa')

    def imsiHitRiskImsi(self):
        """imsiHitRiskImsi 客户imsi命中风险imsi"""
        return self.__get_device_info(deviceType='imsi')

    def imeiHitRiskImei(self):
        """imeiHitRiskImei 客户imei命中风险imei"""
        return self.__get_device_info(deviceType='imei')

    def networkenvHitRiskNetworkenv(self):
        """networkenvHitRiskNetworkenv 客户networkenv命中风险networkenv"""
        return self.__get_device_info(deviceType='network_env')

    def ipHitRiskIp(self):
        """ipHitRiskIp 客户ip命中风险ip"""
        return self.__get_device_info(deviceType='ip')

    def __riskGradeList(self,contactList,contactType):
        riskGradeList = []
        riskGradeList_9 = []
        cleanContactList=[]
        for contact in contactList:
            if phoneClear(contact):
                if phone_clean(phoneClear(contact)):
                    if phone_clean(phoneClear(contact)) not in cleanContactList:
                        cleanContactList.append(phone_clean(phoneClear(contact)))
        for contact in cleanContactList:
            sql = "select * from rota_general_list where is_deleted=0 and number_value='%s' and number_type='%s'" % (contact,contactType)
            result = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=sql)
            gradeList = [d.get("risk_grade") for d in result]
            for grade in gradeList:
                if not grade:
                    riskGradeList.append(str(self.SET_DEFAULT_VALUE_INT_9999996))
                    continue
                riskGradeList.append(str(self.__getRiskGrade(grade)))
        for contact in cleanContactList:
            sql = "select * from rota_general_list where is_deleted=0 and number_value='%s' and number_type !='%s'" % (contact,contactType)
            result = self.mysql.queryall_by_customer_id(db='skynet_rota', sql=sql)
            deviceTList_9 = [d.get("risk_grade") for d in result]
            for grade in deviceTList_9:
                if not grade:
                    riskGradeList_9.append(str(self.SET_DEFAULT_VALUE_INT_9999996))
                    continue
                riskGradeList_9.append(str(self.__getRiskGrade(grade)))
        riskGradeList.sort()
        return riskGradeList,riskGradeList_9

    def contactSrcHitBadContactSrcPhone(self):
        """contactSrcHitBadContactSrcPhone 客户通讯录手机号命中不良通讯录号码"""
        result = self.mongo.query_contact_list_beforeEvenTime_inXdays(db='lake',
                                                                      collection="s_user_mobile_contact_{0}".format(
                                                                          int(self.user_id) % 4),
                                                                      find={"user_id": int(self.user_id)},
                                                                      serial_no=self.serial_no, days=30, clean=False)
        if result == 'No DATA':
            return -1
        riskGradeList, riskGradeList_9 = self.__riskGradeList(result,contactType='1002')
        if not riskGradeList and not riskGradeList_9:
            return 0
        if not riskGradeList and riskGradeList_9:
            return 9
        return ','.join(riskGradeList)

    def contactActionHitBadContactActionPhone(self):
        """contactActionHitBadContactActionPhone 客户通话记录手机号命中不良通话记录号码"""
        result = self.mongo.query_contact_action_list_beforeEvenTime_inXdays(db='lake',
                                                                             collection="s_user_mobile_contact_action_{0}".format(int(self.user_id) % 4),
                                                                             find={"user_id": int(self.user_id)},
                                                                             serial_no=self.serial_no, days=30)
        if result == 'No DATA':
            return -1
        contactActionList = []
        for ac in result:
            if ac.get("callNumber"):
                contactActionList.append(ac.get("callNumber"))
        riskGradeList, riskGradeList_9 = self.__riskGradeList(contactActionList,contactType='1003')
        if not riskGradeList and not riskGradeList_9:
            return 0
        if not riskGradeList and riskGradeList_9:
            return 9
        return ','.join(riskGradeList)

    def contactSmsHitBadContactSmsPhone(self):
        """contactSmsHitBadContactSmsPhone 客户短信手机号命中不良短信号码"""
        result = self.mongo.query_sms_list_beforeEvenTime_inXdays(db='lake',
                                                                  collection="s_user_mobile_sms_list_{0}".format(int(self.user_id) % 4),
                                                                  find={"user_id": int(self.user_id)},
                                                                  serial_no=self.serial_no, days=30)
        if result == 'No DATA':
            return -1
        smsList = []
        for ac in result:
            if ac.get("phoneNum"):
                smsList.append(ac.get("phoneNum"))
        riskGradeList, riskGradeList_9 = self.__riskGradeList(smsList,contactType='1004')
        if not riskGradeList and not riskGradeList_9:
            return 0
        if not riskGradeList and riskGradeList_9:
            return 9
        return ','.join(riskGradeList)

    def __chech_own_black_by_phone(self,phone):
        results = self.mongo.queryall_by_userId(db='galaxy',collection="own_black_record",find={"phone": str(phone)})
        return len(results)

    def relaDirectRelationBlacklist(self):
        """relaDirectRelationBlacklist	直系亲属手机号码是否命中内部黑名单"""
        relative_contact=self.info.result.get('data').get('relativeContact')
        if not relative_contact:
            return -9999999
        if self.__chech_own_black_by_phone(relative_contact)==0:
            return 0
        else:
            return 1

    def relaOtherRelationBlacklist(self):
        """relaOtherRelationBlacklist	其他联系人手机号码是否命内部黑名单"""
        colleague_contact=self.info.result.get('data').get('friendContact')
        if not colleague_contact:
            return -9999999
        if self.__chech_own_black_by_phone(colleague_contact) == 0:
            return 0
        else:
            return 1

    def __HitRotaFreeze(self, hitType='',hitData=''):
        if hitType=='encryption_phone':
            sql = "select * from rota_freeze where encryption_phone='%s' and is_deleted=0" % hitData
        else:
            sql = "select * from rota_freeze where cert_id='%s' and is_deleted=0" % hitData
        rota_result = self.mysql.queryall_by_customer_id('skynet_rota', sql)
        if rota_result:
            return self.SET_DEFAULT_VALUE_INT_1
        return self.SET_DEFAULT_VALUE_INT_0

    def idcardHitFrozenIdcardNew(self):
        """idcardHitFrozenIdcardNew 身份证号命中冻结名单  --产品:2345借款"""
        return self.__HitRotaFreeze(hitType='cert_id',hitData=factor_encrypt_identity(self.info.cert_id))

    def phoneHitFrozenPhone(self):
        """phoneHitFrozenPhone 手机号命中冻结名单  --产品:2345借款"""
        return self.__HitRotaFreeze(hitType='encryption_phone',hitData=factor_encrypt_identity(self.info.phone))

if __name__ == "__main__":
    serial_no = "1539829754839-CFCBDC32E3D337900430D64C8CC53469"
    a = SkynetRotaFactor('T2', serial_no)
    print a.contactSrcHitBadContactSrcPhone()