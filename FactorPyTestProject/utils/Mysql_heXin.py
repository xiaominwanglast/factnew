#coding:utf-8
import pymysql.cursors
from utils.Setting import *

class Mysql_heXin:
    def __init__(self, env,bill=0):
        self.bill="hexin_bill_"+str(bill)
        self.env = env
        self.mysql_hexin_bill_connection = pymysql.connect(
                                                            host=SETTING[env]['MYSQL']['hexin_bill']['host'],
                                                            user=SETTING[env]['MYSQL']['hexin_bill']['user'],
                                                            password=SETTING[env]['MYSQL']['hexin_bill']['password'],
                                                            db=self.bill,
                                                            charset=SETTING[env]['MYSQL']['hexin_bill']['charset'],
                                                            port=SETTING[env]['MYSQL']['hexin_bill']['port'],
                                                            cursorclass=pymysql.cursors.DictCursor)

    def __del__(self):
        self.mysql_hexin_bill_connection.close()
        self.mysql_hexin_bill_connection.cursor().close()

    def queryone_by_id(self, sql):
        cursor = self.mysql_hexin_bill_connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

    def queryall_by_id(self, sql):
        cursor = self.mysql_hexin_bill_connection.cursor()
        cursor.execute(sql)
        resultall = cursor.fetchall()
        return resultall

if __name__=='__main__':
    print (Mysql_heXin('T2',3).queryall_by_id(sql="select * from loan_info where user_id='112386703' and prod_id=10002"))