#coding:utf-8
from utils.InfoHelper import InfoHelper
from NewFactorCollect.SkynetRotaFactor.SkynetRotaFactor import SkynetRotaFactor
from NewFactorCollect.ThirdFactor.ThirdFactor import ThirdFactor
from NewFactorCollect.CreditLineFactor.CreditLineFactor import CreditLineFactor
from NewFactorCollect.LakeFactor.LakeFactor import LakeFactor
from NewFactorCollect.DroolsFactor.DroolsFactor import DroolsFactor
from NewFactorCollect.MXFactor.MXFactor import MXFactor
from NewFactorCollect.MXFactor.MXFactorV2 import MXFactorV2
from NewFactorCollect.BaseFactor.BaseFactor import BaseFactor
from NewFactorCollect.MachineLearning.MachineLearning import MachineLearning
from CarFactorCollect.CarFactorAuto import CarFactorAuto
from CarFactorCollect.CarFactor import CarFactor
from utils.MongoUtil import MongoUntil
import sys
class RunnerInit(object):
    def __init__(self,env,serial_no):
        """
        :param env: 环境
        :param serial_no: 序列号
        """
        self.env = env
        self.serial_no = serial_no
        self.info = InfoHelper(env=self.env, serial_no=self.serial_no)
        if "product_code" in self.info.__dict__.keys() and self.info.product_code !="CDW":
            self.decision_status_check()

    def decision_status_check(self):
        user_info_result = MongoUntil(self.env).query_by_user_id(db='skynet', collection="skynet_user_info",find={"serial_no": self.serial_no})
        if user_info_result and user_info_result[0].get("scene_code")=="collection":
            return
        decision_result=MongoUntil(self.env).query_by_user_id(db='skynet', collection="skynet_decision_result",find={"serial_no": self.serial_no})
        if not decision_result:
            print ('make decision Failure! please check door!')
            sys.exit()
        if decision_result[0].get('status') in ("SUCCESS","MA_WAITING"):
            if decision_result[0].get('mock'):
                print ("make decision mock true! Please change mock value to false!")
                sys.exit()
            if decision_result[0].get('product_code')!='jk_loan' and decision_result[0].get("main_rules").get("freeze_list_rule").get("result")==1:
                print ("make decision freezed ! Please remove cerd_id from rota_freeze and take care of redis!")
                sys.exit()
        else:
            print ("make decision Failure or Waiting! Please check!")
            sys.exit()

class NewRunnerInit(RunnerInit):
    def __init__(self,env,serial_no):
        super(NewRunnerInit,self).__init__(env,serial_no)
        self.Rota = SkynetRotaFactor(env, serial_no)
        self.Third = ThirdFactor(env, serial_no)
        self.Credit = CreditLineFactor(env, serial_no)
        self.Lake = LakeFactor(env, serial_no)
        self.Drools = DroolsFactor(env, serial_no)
        self.MX =   MXFactor(env, serial_no)
        self.MXV2 = MXFactorV2(env ,serial_no)
        self.Base =BaseFactor(env,serial_no)
        self.Machine=MachineLearning(env,serial_no)

        self.FactorDict={}
        self.get_factor_class_dict("Rota", self.Rota)
        self.get_factor_class_dict("Third", self.Third)
        self.get_factor_class_dict("Credit", self.Credit)
        self.get_factor_class_dict("Lake", self.Lake)
        self.get_factor_class_dict("Drools", self.Drools)
        # self.get_factor_class_dict("MX", self.MX)
        self.get_factor_class_dict("MXV2", self.MXV2)
        self.get_factor_class_dict("Base", self.Base)
        self.get_factor_class_dict("Machine", self.Machine)


    def get_factor_class_dict(self,FactorClassName,FactorClass):
        for FactorFunc in dir(FactorClass):
            if not FactorFunc.startswith('_') and not FactorFunc.startswith('__') and not FactorFunc.startswith('SET_DEFAULT_VALUE') \
                    and "_customer_id" not in FactorFunc and "_product_id" not in FactorFunc and FactorFunc not in ["env","mysql","serial_no","info","mongo"]:
                self.FactorDict[FactorFunc]=FactorClassName
        return self.FactorDict


class CarRunnerInit(RunnerInit):
    def __init__(self,env,serial_no):
        super(CarRunnerInit,self).__init__(env,serial_no)
        self.Car = CarFactor(env, serial_no)
        self.CarAuto = CarFactorAuto(env, serial_no)

        self.FactorDict={}
        self.get_factor_class_dict("Car", self.Car)
        self.get_factor_class_dict("CarAuto", self.CarAuto)

    def get_factor_class_dict(self,FactorClassName,FactorClass):
        for FactorFunc in dir(FactorClass):
            if not FactorFunc.startswith('_') and not FactorFunc.startswith('__') and not FactorFunc.startswith('SET_DEFAULT_VALUE') \
                    and "_customer_id" not in FactorFunc and "_product_id" not in FactorFunc and FactorFunc not in ["env","mysql","serial_no","info","mongo"]:
                self.FactorDict[FactorFunc]=FactorClassName
        return self.FactorDict
