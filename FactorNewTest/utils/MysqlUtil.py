# -*- coding: UTF-8 -*-
import pymysql.cursors

from utils.Setting import *


class MysqlUntil:
    def __init__(self, env):
        self.env = env
        self.mysql_facade_center_connection = pymysql.connect(
                                                          host=SETTING[env]['MYSQL']['facade_center']['host'],
                                                          user=SETTING[env]['MYSQL']['facade_center']['user'],
                                                          password=SETTING[env]['MYSQL']['facade_center'][
                                                              'password'],
                                                          db=SETTING[env]['MYSQL']['facade_center']['db'],
                                                          charset=SETTING[env]['MYSQL']['facade_center']['charset'],
                                                          port=SETTING[env]['MYSQL']['facade_center']['port'],
                                                          cursorclass=pymysql.cursors.DictCursor)
        self.mysql_facade_center_cursor = self.mysql_facade_center_connection.cursor()

        self.mysql_customer_center_connection = pymysql.connect(
                                                            host=SETTING[env]['MYSQL']['customer_center']['host'],
                                                            user=SETTING[env]['MYSQL']['customer_center']['user'],
                                                            password=SETTING[env]['MYSQL']['customer_center'][
                                                                'password'],
                                                            db=SETTING[env]['MYSQL']['customer_center']['db'],
                                                            charset=SETTING[env]['MYSQL']['customer_center'][
                                                                'charset'],
                                                            port=SETTING[env]['MYSQL']['customer_center']['port'],
                                                            cursorclass=pymysql.cursors.DictCursor)
        self.mysql_customer_center_cursor = self.mysql_customer_center_connection.cursor()

        self.mysql_loan_center_connection = pymysql.connect(host=SETTING[env]['MYSQL']['loan_center']['host'],
                                                            user=SETTING[env]['MYSQL']['loan_center']['user'],
                                                            password=SETTING[env]['MYSQL']['loan_center']['password'],
                                                            db=SETTING[env]['MYSQL']['loan_center']['db'],
                                                            charset=SETTING[env]['MYSQL']['loan_center']['charset'],
                                                            port=SETTING[env]['MYSQL']['loan_center']['port'],
                                                            cursorclass=pymysql.cursors.DictCursor)
        self.mysql_loan_center_cursor = self.mysql_loan_center_connection.cursor()

        self.mysql_apply_center_connection = pymysql.connect(host=SETTING[env]['MYSQL']['apply_center']['host'],
                                                             user=SETTING[env]['MYSQL']['apply_center']['user'],
                                                             password=SETTING[env]['MYSQL']['apply_center']['password'],
                                                             db=SETTING[env]['MYSQL']['apply_center']['db'],
                                                             charset=SETTING[env]['MYSQL']['apply_center']['charset'],
                                                             port=SETTING[env]['MYSQL']['apply_center']['port'],
                                                             cursorclass=pymysql.cursors.DictCursor)
        self.mysql_apply_center_cursor = self.mysql_apply_center_connection.cursor()

        self.mysql_xinyongjin_connection = pymysql.connect(host=SETTING[env]['MYSQL']['xinyongjin']['host'],
                                                           user=SETTING[env]['MYSQL']['xinyongjin']['user'],
                                                           password=SETTING[env]['MYSQL']['xinyongjin']['password'],
                                                           db=SETTING[env]['MYSQL']['xinyongjin']['db'],
                                                           charset=SETTING[env]['MYSQL']['xinyongjin']['charset'],
                                                           port=SETTING[env]['MYSQL']['xinyongjin']['port'],
                                                           cursorclass=pymysql.cursors.DictCursor)
        self.mysql_xinyongjin_cursor = self.mysql_xinyongjin_connection.cursor()


    def __del__(self):
        self.mysql_customer_center_connection.close()
        self.mysql_customer_center_cursor.close()

        self.mysql_loan_center_connection.close()
        self.mysql_loan_center_cursor.close()

        self.mysql_apply_center_connection.close()
        self.mysql_apply_center_cursor.close()

        self.mysql_xinyongjin_connection.close()
        self.mysql_xinyongjin_cursor.close()

    def queryone_by_customer_id(self, db, sql):
        cursor = eval("self.mysql_{0}_cursor".format(db))
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

    def queryall_by_customer_id(self, db, sql):
        cursor = eval("self.mysql_{0}_cursor".format(db))
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def queryall_by_table(self, db, sql):
        cursor = eval("self.mysql_{0}_cursor".format(db))
        resultall = []
        if '{0}' in sql:
            for i in range(20):
                cursor.execute(sql.format(i))
                result = cursor.fetchall()
                resultall += result
        else:
            cursor.execute(sql)
            resultall = cursor.fetchall()
        return resultall

    def queryall_by_table_new(self, db, sql):
        cursor = eval("self.mysql_{0}_cursor".format(db))
        resultall = []
        cursor.execute(sql)
        result = cursor.fetchall()
        resultall += result
        return resultall

    def queryone_table(self, db, sql, customid):
        cursor = eval("self.mysql_{0}_cursor".format(db))
        table_id = long(customid) % 20
        cursor.execute(sql.format(table_id))
        result = cursor.fetchall()
        return result

    def queryone_by_customer_id_sxj(self, db, sql):
        cursor = eval("self.mysql_{0}_cursor".format(db))
        cursor.execute(sql)
        result = cursor.fetchone()
        return result

    def queryall_by_table_new_only(self, db, sql):
        cursor = eval("self.mysql_{0}_cursor".format(db))
        resultall = []
        if '{0}' in sql:
            for i in range(20):
                cursor.execute(sql.format(i))
                result = cursor.fetchall()
                resultall += result
        else:
            cursor.execute(sql)
            resultall = cursor.fetchall()
        return resultall