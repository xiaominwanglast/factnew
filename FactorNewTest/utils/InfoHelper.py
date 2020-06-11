# -*- coding: utf-8 -*-
from utils.MongoUtil import MongoUntil
from utils.MysqlUtil import MysqlUntil
from datetime import timedelta
import re
from TestInit import factor_decrypt_identity


class InfoHelper(object):
    def __init__(self, env, serial_no, mongdb='skynet'):
        self.env = env
        self.mysql = MysqlUntil(env=self.env)
        self.mongo = MongoUntil(self.env)
        result = self.mongo.query_by_user_id(mongdb, "skynet_user_info", {"serial_no": serial_no})
        if not result:
            return
        self.result = result[0]
        self.customer_id = self.result.get('customer_id')
        self.user_id = self.result.get('user_id')
        self.user_name = factor_decrypt_identity(self.result.get('encryption_user_name'))
        self.event_time = self.result.get('event_time')
        self.cert_id = factor_decrypt_identity(self.result.get('encryption_cert_id'))
        self.phone = factor_decrypt_identity(self.result.get('encryption_phone'))
        self.create_time = self.result.get('create_time')
        if self.result.get('event_time'):
            self.event_time_add8h = self.result.get('event_time') + timedelta(hours=8)
        self.product_code = self.result.get('product_code')
        self.scene_code = self.result.get('scene_code')
        if self.result.get('data',{}):
            self.old_user_id = self.result.get('data',{}).get('oldUserId')
            self.colleagueContact = self.result.get('data', {}).get('colleagueContact')
            self.relativeContact = self.result.get('data', {}).get('relativeContact')
            self.friendContact = self.result.get('data', {}).get('friendContact')
            self.homeAddress = self.result.get('data', {}).get('homeAddress')
            self.unitsName =self.result.get('data', {}).get('unitsName')
            self.unitsAddress=self.result.get('data',{}).get('unitsAddress')


    def get_mobile_location(self, phone, locatin_type='city'):
        sql = "select * from dict_mobile_location where mobile = '%s';" % str(phone)[:7]
        result = self.mysql.queryall_by_customer_id('skynet', sql)
        if len(result) > 0:
            if locatin_type == 'city':
                return result[0]['city']
            if locatin_type == 'province':
                return result[0]['province']
        else:
            return False

    def get_mobile_location_list(self, phone_list, locatin_type='city'):
        phone_location = []
        for phone in phone_list:
            phon_location = self.get_mobile_location(phone, locatin_type=locatin_type)
            if phon_location:
                phone_location.append(phon_location)
        return list(set(phone_location))

    def get_mobile_location_list_not_dict(self, phone_list):
        phone_location = []
        if len(phone_list) == 0:
            return []
        for phone in phone_list:
            phon_location = self.get_mobile_location(phone)
            if phon_location:
                phone_location.append(phon_location)
        return phone_location

    def get_mobilephone_one_after_cleaned(self, phone):
        if not phone and not isinstance(phone, str):
            return False
        phone = phone.replace('-', '').replace(' ', '').replace("\t", "").replace("\r", "").replace("\n", "").replace(
            "\r\n", "")
        if len(phone) > 11 and phone[:1] == "+":
            phone = phone[3:]
        if len(phone) > 11 and phone[:2] == "86":
            phone = phone[2:]
        if len(phone) > 11 and (phone[:5] == "17951" or phone[:5] == "12593"):
            phone = phone[5:]
        try:
            int(phone)
        except:
            return False
        if re.match("^(1[34578](\\d{9}))$", str(phone)):
            return phone
        else:
            return False

    def get_phone_one_after_cleaned(self, phone):
        phone_clean = self.get_mobilephone_one_after_cleaned(phone)
        if phone_clean:
            return phone_clean
        else:
            return phone

    def get_mobilephone_one_after_cleaned_by_oldRule(self, phone):
        if re.match("^((86)|(086)|(\+86)|(\(\+86\)))?(((13[0-9]{1})|(15[0-9]{1})|(18[0,5-9]{1}))+\d{8})$", str(phone)):
            return phone


    def get_mobilephone_list_after_cleaned_not_dict(self, phone_list):
        contact_mobilephone_list = []
        if not phone_list:
            return []
        for i in range(0, len(phone_list)):
            if self.get_mobilephone_one_after_cleaned(phone_list[i]):
                contact_mobilephone_list.append(self.get_mobilephone_one_after_cleaned(phone_list[i]))
        return contact_mobilephone_list

    def get_phonelist_dic(self, phonelist):
        dict_list = []
        for row in phonelist:
            if row not in dict_list:
                dict_list.append(row)
        return dict_list

    def get_mobilephone_list_after_cleaned_dict(self, phone_list):
        contact_mobilephone_list = self.get_mobilephone_list_after_cleaned_not_dict(phone_list)
        return self.get_phonelist_dic(contact_mobilephone_list)

    def get_mobilephone_list_by_contacts(self, contacts):
        contact_list = []
        for sub_contact in contacts:
            for i in range(1, 4):
                if sub_contact.get("phone" + str(i)):
                    contact_list.append(str(sub_contact.get("phone" + str(i))))
        return contact_list

    def get_mobilephone_list_by_contacts_dict_by_NameAndPhone(self, contacts, type='phone'):
        contact_list = []
        name_list = []
        list = []
        for sub_contact in contacts:
            for i in range(1, 4):
                if sub_contact.get("phone" + str(i)):
                    if (sub_contact.get("phone" + str(i)) + sub_contact.get('name')) not in list:
                        contact_list.append(str(sub_contact.get("phone" + str(i))))
                        name_list.append(sub_contact.get('name'))
                        list.append(sub_contact.get("phone" + str(i)) + sub_contact.get('name'))
        if type == 'phone':
            return contact_list
        if type == 'name':
            return name_list

    def get_mobilephone_list_by_contacts_dict_by_NameAndCleanedPhone(self, contacts, type='phone'):
        contact_list = []
        name_list = []
        list = []
        for sub_contact in contacts:
            for i in range(1, 4):
                phone_num = sub_contact.get("phone" + str(i))
                phone_num = self.get_phone_one_after_cleaned(phone_num)
                if phone_num:
                    if not sub_contact.get('name'):
                        name = ''
                    else:
                        name = sub_contact.get('name')
                    if (phone_num + name) not in list:
                        contact_list.append(str(phone_num))
                        name_list.append(name)
                        list.append(phone_num + name)
        if type == 'phone':
            return contact_list
        if type == 'name':
            return name_list

    def compare_lists(self, list1, list2):
        count = 0
        for l1 in list1:
            for l2 in list2:
                if str(l1) == str(l2):
                    count += 1
        return count, len(list1), len(list2)


if __name__ == "__main__":
    Info = InfoHelper(env='T1', serial_no='5aa0db4ac71f8d76fbc632bb')
    print Info.get_phone_one_after_cleaned('1110')

