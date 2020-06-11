# -*- coding: UTF-8 -*-
from utils.MongoUtil import MongoUntil
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
                time.sleep(2)
            else:
                for l in range(1,3):
                    FactorValue=drools_data[0].get('facts').get(Factor,'createFactor')
                    if FactorValue=='createFactor':
                        time.sleep(1)
                    else:
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

if __name__=="__main__":
    env='T1'
    serial_no = '1563758015905-2002030CDE9A98CAEAFBBBDD5AE1DC49'
    test=DoorlsFactor(env,serial_no)
    print (test.get_Factor('geoPhoneEntDuration'))
    # test.testDemo()