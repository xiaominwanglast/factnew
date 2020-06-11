# -*- coding: UTF-8 -*-
from utils.DoorlsFactor import DoorlsFactor
from FrameRunner.RunnerInit import NewRunnerInit

class NewRunnerByFactor(NewRunnerInit):
    def __init__(self, env, serial_no=''):
        super(NewRunnerByFactor,self).__init__(env, serial_no)

    def self_Factors(self,factor,print_type='print'):
        class_name = self.Get_class(factor)
        if not class_name:
            return
        factor_qa = eval("self.{0}.{1}()".format(class_name, factor))
        if print_type == 'print':
            print factor, ":", factor_qa
        else:
            return factor_qa

    def dev_Factors(self,factor,print_type='print'):
        factor_dev = DoorlsFactor(self.env, serial_no).get_Factor(factor)
        if print_type == 'print':
            print factor, ":", factor_dev
        else:
            return factor_dev

    def compare_Factors(self,factor,print_type='print'):
        factor_qa = self.self_Factors(factor, print_type='noprint')
        factor_dev = self.dev_Factors(factor, print_type='noprint')
        if print_type == 'print':
            print factor, ":", factor_qa, "|| ", factor_dev

    def Get_Factor(self,print_type='print',list_type='new'):
        if print_type == 'print':
            print "-- customerId:", self.info.customer_id, "userId:", self.info.user_id, " --"
        test_list = eval("self." + list_type + "_list")
        for factor in test_list:
            self.compare_Factors(factor=factor)

if __name__ == '__main__':
    env = 'T1'

    serial_no_list = ['5bd28c91004f9e736cbbdca3']

    for serial_no in serial_no_list:
        test = NewRunnerByFactor(env, serial_no)
        test.Get_Factor(list_type='new')