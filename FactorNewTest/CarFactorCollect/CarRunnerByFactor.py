# -*- coding: UTF-8 -*-
from FrameRunner.RunnerInit import CarRunnerInit
from utils.DoorlsFactor import DoorlsFactor
from FactList.CarFactorList import *

class CarRunnerByFactor(CarRunnerInit):
    def __init__(self, env, serial_no=''):
        super(CarRunnerByFactor, self).__init__(env, serial_no)
        self.test_list = carAuto_0306_list

    def self_Factors(self, factor, print_type='print'):
        if factor not in self.FactorDict.keys():
            return
        factor_qa = eval("self.{0}.{1}()".format(self.FactorDict[factor], factor))
        if print_type == 'print':
            print factor, ":", factor_qa
        else:
            return factor_qa

    def dev_Factors(self, factor, print_type='print'):
        factor_dev = DoorlsFactor(self.env, serial_no).get_Factor(factor)
        if print_type == 'print':
            print factor, ":", factor_dev
        else:
            return factor_dev

    def Get_Factor(self, list_type='test'):
        print "--", "customerId:", self.info.customer_id, "userId:", self.info.user_id, " --"
        test_list = eval("self." + list_type + "_list")
        for factor in test_list:
            factor_qa = self.self_Factors(factor, print_type='no_print')
            factor_dev = self.dev_Factors(factor, print_type='no_print')
            try:
                if str(factor_qa) == str(factor_dev):
                    print factor, ":", factor_qa, "|| ", factor_dev
                else:
                    print '\033[1;31m%s\033[0m' % factor, ":", '\033[1;31m%s\033[0m' % factor_qa, "|| ", '\033[1;31m%s\033[0m' % factor_dev
            except:
                print factor, ": ", factor_qa, "|| ", factor_dev

if __name__ == '__main__':
    env = 'T3'
    serial_no_list = ['1552272652793-A702DF6A6A65706CE253577D09FCBD65']
    for serial_no in serial_no_list:
        test = CarRunnerByFactor(env, serial_no)
        test.Get_Factor(list_type='test')