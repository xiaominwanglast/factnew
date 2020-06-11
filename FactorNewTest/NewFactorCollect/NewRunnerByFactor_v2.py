# -*- coding: UTF-8 -*-
from utils.DoorlsFactor import DoorlsFactor
from FrameRunner.RunnerInit import NewRunnerInit
from FactList.NewFactorList import *

class NewRunnerByFactor(NewRunnerInit):
    def __init__(self, env, serial_no=''):
        super(NewRunnerByFactor, self).__init__(env, serial_no)
        self.test_list = Test_mx_1224

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

    def dev_Factors_v2(self, factor, print_type='print'):
        factor_dev = DoorlsFactor(self.env, serial_no).get_Factor_v2(factor)
        if print_type == 'print':
            print factor, ":", factor_dev
        else:
            return factor_dev

    def Get_Factor(self, list_type='test'):
        print "--", "customerId:", self.info.customer_id, "userId:", self.info.user_id, " --"
        print u'因子名：',u'测试脚本值 ||',u'风控v1值 ||',u'风控v2值'
        test_list = eval("self." + list_type + "_list")
        for factor in test_list:
            factor_qa = self.self_Factors(factor, print_type='no_print')
            factor_dev = self.dev_Factors(factor, print_type='no_print')
            factor_dev_v2 = self.dev_Factors_v2(factor, print_type='no_print')
            try:
                if str(factor_dev_v2) == str(factor_dev):
                    print factor, ":", factor_qa, "|| ", factor_dev , "|| ",factor_dev_v2
                else:
                    print '\033[1;31m%s\033[0m' % factor, ":", '\033[1;31m%s\033[0m' % factor_qa, "|| ", '\033[1;31m%s\033[0m' % factor_dev, "|| ", '\033[1;31m%s\033[0m' % factor_dev_v2
            except:
                print factor, ": ", factor_qa, "|| ", factor_dev, "|| ",factor_dev_v2

if __name__ == '__main__':
    env = 'T1'
    serial_no_list = ['1547012552243-A1DCCFAEE85DF235F5D9894D43BBBCD7']
    for serial_no in serial_no_list:
        test = NewRunnerByFactor(env, serial_no)
        test.Get_Factor(list_type='test')