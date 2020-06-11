# -*- coding: UTF-8 -*-
from utils.MongoUtil import MongoUntil
from FactList.NewFactorList import *
import time
import datetime
class DoorlsFactor(object):
    def __init__(self,env,serial_no):
        """
        :param env: 环境
        :param serial_no: 序列号
        """
        self.mongo = MongoUntil(env)
        self.serial_no=serial_no

    def get_Factor(self,Factor):
        """
        :param Factor: 因子名字
        :return: 无因子值时返回 None
        """
        for t in range(1,10):
            drools_data = self.mongo.query_by_user_id(db='skynet', collection="skynet_e_factor_result",find={"serial_no": self.serial_no})
            if not drools_data:
                time.sleep(3)
            else:
                FactorValue=drools_data[0].get('facts').get(Factor)
                if not FactorValue:
                    return FactorValue
                try:
                    if type(FactorValue)==datetime.datetime:
                        return FactorValue+datetime.timedelta(hours=8)
                    if "," not in str(FactorValue):
                        return FactorValue
                    if "," in str(FactorValue):
                        FactorEveryList=str(FactorValue).split(",")
                        FactorEveryList.sort()
                        return ",".join(FactorEveryList)
                except Exception as e:
                    return FactorValue
                return FactorValue
        return False

    def get_Factor_v2(self,Factor):
        """
        :param Factor: 因子名字
        :return: 无因子值时返回 None
        """
        for t in range(1,10):
            drools_data = self.mongo.query_by_user_id(db='skynet', collection="skynet_e_factor_result_v2",find={"serial_no": self.serial_no})
            if not drools_data:
                time.sleep(3)
            else:
                FactorValue=drools_data[0].get('facts').get(Factor)
                if not FactorValue:
                    return FactorValue
                try:
                    if type(FactorValue)==datetime.datetime:
                        return FactorValue+datetime.timedelta(hours=8)
                    if "," not in str(FactorValue):
                        return FactorValue
                    if "," in str(FactorValue):
                        FactorEveryList=str(FactorValue).split(",")
                        FactorEveryList.sort()
                        return ",".join(FactorEveryList)
                except Exception as e:
                    return FactorValue
                return FactorValue
        return False

    def testDemo(self):
        # result =self.mongo.query_by_user_id(db='skynet',collection='skynet_e_factor_result_v2',find={"serial_no": self.serial_no})
        # if not result:
        #     return
        # test_list= result[0].get("facts").keys()
        print 'serial_no:'+serial_no
        print u'借还款因子名: '+u'V1值'+' || '+u'V2值'
        test_list=Test_bill_1120+Test_bill_1120_cdw+Test_bill_cdw
        for factor in test_list:
            factor_qa = test.get_Factor(factor)
            factor_dev = test.get_Factor_v2(factor)
            if not factor_qa or not factor_dev:
                continue
            try:
                if str(factor_qa) == str(factor_dev):
                    print factor, ":", factor_qa, "|| ", factor_dev
                else:
                    print '\033[1;31m%s\033[0m' % factor, ":", '\033[1;31m%s\033[0m' % factor_qa, "|| ", '\033[1;31m%s\033[0m' % factor_dev
            except:
                print factor, ": ", factor_qa, "|| ", factor_dev


if __name__=="__main__":
    env='T1'
    serial_no = '1552443969819-3A8559F7594F9B1697F765653F88FF3C'
    test=DoorlsFactor(env,serial_no)
    print test.get_Factor('newBigLastOverdueAmt')
    # test.testDemo()
