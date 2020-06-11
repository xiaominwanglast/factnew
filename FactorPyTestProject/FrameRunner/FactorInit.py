#coding:utf-8
from utils.InfoHelper import InfoHelper
from utils.MysqlUtil import MysqlUntil
from utils.MongoUtil import MongoUntil

class FactorInit(object):
    def __init__(self, env, serial_no):
        self.env = env
        self.serial_no = serial_no
        self.info = InfoHelper(env=self.env, serial_no=self.serial_no)
        self.mysql = MysqlUntil(env=self.env)
        self.mongo = MongoUntil(env=self.env)

        #TODO 立即贷产品编号为10002
        #TODO 随心借产品编号为102
        #TODO 卡带王产品编号为101
        #TODO 即刻贷产品编号10002(老产品)
        #TODO 贷款王茶品编号很多，名单库使用100(老产品)
        #TODO 2345借款产品编号108
        #TODO 畅借款产品编号109
        #TODO 好借款产品编号110
        #TODO 黄金屋产品编号111

        self.jyj_product_id=111
        self.gd_product_id=110
        self.ql_product_id=109
        self.ljd_product_id=10002
        self.sxj_product_id=102
        self.kdw_product_id=101
        self.JK_product_id=108
        self.rota_jkd_product_id=10002
        self.rota_dkw_product_id=100

        #TODO 立即贷产品code为 vip_loan
        #TODO 随心借产品code为 sxj_loan
        #TODO 卡带王产品code为 kdw_loan
        #TODO 好借款产品code为 gd_loan
        #TODO 2345借款产品code为 jk_loan
        #TODO 畅借款产品code为 ql_loan
        #TODO 黄金屋产品code为 hjd_loan

        self.gd_product_code="gd_loan"
        self.ljd_product_code="vip_loan"
        self.sxj_product_code="sxj_loan"
        self.kdw_product_code="kdw_loan"
        self.JK_product_code='jk_loan'
        self.QL_product_code='ql_loan'
        self.jyj_product_code='hjw_loan'

        #TODO -9999999:风控可接受的不可抗异常，比如：调用外部黑名单超时，设置因子为self.SET_DEFAULT_VALUE_INT_9999999，这样风控可以决定是过还是拒，而不是卡件；
        #TODO -9999998:分母为零的情况；
        #TODO -9999997:性能取舍，如：根据用户设备号获取同设备号用户的逾期情况时，同设备号匹配到的用户过多，无法在要求时间内计算出结果，评估影响后，当匹配到用户数大于999时，直接设置因子值为-9999997
        #TODO -9999996:脏数据，如：1、用户的身份证号为空（而根据业务逻辑身份证号本不应该为空）；2、外部数据调用时返回的分数字段为空（本不应该为空的）
        #TODO -9999995:客观上不满足因子计算条件，如：用户登录间隔，但是用户只登陆了一次；
        #TODO -8888888:程序无法处理的异常，未知异常等，发生这些异常卡件，如：数据库查询失败、远程接口调用失败；
        self.SET_DEFAULT_VALUE_INT_9999999=-9999999
        self.SET_DEFAULT_VALUE_INT_9999998=-9999998
        self.SET_DEFAULT_VALUE_INT_9999997=-9999997
        self.SET_DEFAULT_VALUE_INT_9999996=-9999996
        self.SET_DEFAULT_VALUE_INT_9999995=-9999995
        self.SET_DEFAULT_VALUE_INT_8888888=-8888888

        #TODO 针对异常值为小数时的数据
        self.SET_DEFAULT_VALUE_FLOAT_9999998=-9999998.0
        self.SET_DEFAULT_VALUE_FLOAT_9999997=-9999997.0
        self.SET_DEFAULT_VALUE_FLOAT_9999996=-9999996.0
        self.SET_DEFAULT_VALUE_FLOAT_9999995=-9999995.0
        self.SET_DEFAULT_VALUE_FLOAT_9999999=-9999999.0

        #TODO 针对时间的异常值(元年-8H)
        self.SET_DEFAULT_VALUE_STRING_DATETIME="0000-12-29 16:00:00"

        #TODO 针对数据取0或分数取0.0,数据取1
        self.SET_DEFAULT_VALUE_INT_0=0
        self.SET_DEFAULT_VALUE_FLOAT_0=0.0
        self.SET_DEFAULT_VALUE_INT_1=1


class CarFactorInit(FactorInit):
    def __init__(self, env, serial_no):
        super(CarFactorInit,self).__init__(env, serial_no)

class NewFactorInit(FactorInit):
    def __init__(self, env, serial_no):
        super(NewFactorInit,self).__init__(env, serial_no)
        self.user_id = self.info.result.get("user_id")
        self.customer_id = self.info.result.get("customer_id")
        self.ljd_customer_id = self.get_ljd_customer_id
        self.sxj_customer_id = self.get_sxj_customer_id
        self.kdw_customer_id = self.get_kdw_customer_id
        self.ql_customer_id=self.get_ql_customer_id
        self.jk_customer_id=self.get_jk_customer_id
        self.gd_customer_id=self.get_gd_customer_id
        self.jyj_customer_id=self.get_jyj_customer_id

    @property
    def get_ljd_customer_id(self):
        sql = "SELECT * FROM user where id = %s" % (self.info.user_id,)
        result = self.mysql.queryone_by_customer_id('customer_center', sql)
        return result['custId_behalf']

    @property
    def get_sxj_customer_id(self):
        sql= "SELECT * FROM customer where user_id=%s and prod_id=%s"%(self.info.user_id,102)
        result= self.mysql.queryone_by_customer_id('customer_center', sql)
        if result:
            return result.get('id')
        else:
            return False
    @property
    def get_kdw_customer_id(self):
        sql= "SELECT * FROM customer where user_id=%s and prod_id=%s"%(self.info.user_id,101)
        result= self.mysql.queryone_by_customer_id('customer_center', sql)
        if result:
            return result.get('id')
        else:
            return False
    @property
    def get_ql_customer_id(self):
        sql= "SELECT * FROM customer where user_id=%s and prod_id=%s"%(self.info.user_id,109)
        result= self.mysql.queryone_by_customer_id('customer_center', sql)
        if result:
            return result.get('id')
        else:
            return False
    @property
    def get_jk_customer_id(self):
        sql= "SELECT * FROM customer where user_id=%s and prod_id=%s"%(self.info.user_id,108)
        result= self.mysql.queryone_by_customer_id('customer_center', sql)
        if result:
            return result.get('id')
        else:
            return False
    @property
    def get_gd_customer_id(self):
        sql= "SELECT * FROM customer where user_id=%s and prod_id=%s"%(self.info.user_id,110)
        result= self.mysql.queryone_by_customer_id('customer_center', sql)
        if result:
            return result.get('id')
        else:
            return False
    @property
    def get_jyj_customer_id(self):
        sql= "SELECT * FROM customer where user_id=%s and prod_id=%s"%(self.info.user_id,111)
        result= self.mysql.queryone_by_customer_id('customer_center', sql)
        if result:
            return result.get('id')
        else:
            return False