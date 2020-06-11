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

        self.mysql_skynet_fact_material_connection = pymysql.connect(
                                                            host=SETTING[env]['MYSQL']['skynet_fact_material']['host'],
                                                            user=SETTING[env]['MYSQL']['skynet_fact_material']['user'],
                                                            password=SETTING[env]['MYSQL']['skynet_fact_material']['password'],
                                                            db=SETTING[env]['MYSQL']['skynet_fact_material']['db'],
                                                            charset=SETTING[env]['MYSQL']['skynet_fact_material']['charset'],
                                                            port=SETTING[env]['MYSQL']['skynet_fact_material']['port'],
                                                            cursorclass=pymysql.cursors.DictCursor)
        self.mysql_skynet_fact_material_cursor = self.mysql_skynet_fact_material_connection.cursor()

        self.mysql_skynet_connection = pymysql.connect(
                                                           host=SETTING[env]['MYSQL']['skynet']['host'],
                                                           user=SETTING[env]['MYSQL']['skynet']['user'],
                                                           password=SETTING[env]['MYSQL']['skynet']['password'],
                                                           db=SETTING[env]['MYSQL']['skynet']['db'],
                                                           charset=SETTING[env]['MYSQL']['skynet']['charset'],
                                                           port=SETTING[env]['MYSQL']['skynet']['port'],
                                                           cursorclass=pymysql.cursors.DictCursor)
        self.mysql_skynet_cursor = self.mysql_skynet_connection.cursor()

        self.mysql_skynet_rota_connection = pymysql.connect(host=SETTING[env]['MYSQL']['skynet_rota']['host'],
                                                            user=SETTING[env]['MYSQL']['skynet_rota']['user'],
                                                            password=SETTING[env]['MYSQL']['skynet_rota']['password'],
                                                            db=SETTING[env]['MYSQL']['skynet_rota']['db'],
                                                            charset=SETTING[env]['MYSQL']['skynet_rota']['charset'],
                                                            port=SETTING[env]['MYSQL']['skynet_rota']['port'],
                                                            cursorclass=pymysql.cursors.DictCursor)
        self.mysql_skynet_rota_cursor = self.mysql_skynet_rota_connection.cursor()

        self.mysql_pms_product_register_connection = pymysql.connect(
                                                            host=SETTING[env]['MYSQL']['pms_product_register']['host'],
                                                            user=SETTING[env]['MYSQL']['pms_product_register']['user'],
                                                            password=SETTING[env]['MYSQL']['pms_product_register']['password'],
                                                            db=SETTING[env]['MYSQL']['pms_product_register']['db'],
                                                            charset=SETTING[env]['MYSQL']['pms_product_register']['charset'],
                                                            port=SETTING[env]['MYSQL']['pms_product_register']['port'],
                                                            cursorclass=pymysql.cursors.DictCursor)
        self.mysql_pms_product_register_cursor = self.mysql_pms_product_register_connection.cursor()

        self.mysql_skynet_credit_line_connection = pymysql.connect(
                                                            host=SETTING[env]['MYSQL']['skynet_credit_line']['host'],
                                                            user=SETTING[env]['MYSQL']['skynet_credit_line']['user'],
                                                            password=SETTING[env]['MYSQL']['skynet_credit_line']['password'],
                                                            db=SETTING[env]['MYSQL']['skynet_credit_line']['db'],
                                                            charset=SETTING[env]['MYSQL']['skynet_credit_line']['charset'],
                                                            port=SETTING[env]['MYSQL']['skynet_credit_line']['port'],
                                                            cursorclass=pymysql.cursors.DictCursor)
        self.mysql_skynet_credit_line_cursor = self.mysql_skynet_credit_line_connection.cursor()

        self.mysql_collection_connection  = pymysql.connect(
                                                    host=SETTING[env]['MYSQL']['collection']['host'],
                                                    user=SETTING[env]['MYSQL']['collection']['user'],
                                                    password=SETTING[env]['MYSQL']['collection']['password'],
                                                    db=SETTING[env]['MYSQL']['collection']['db'],
                                                    charset=SETTING[env]['MYSQL']['collection']['charset'],
                                                    port=SETTING[env]['MYSQL']['collection']['port'],
                                                    cursorclass=pymysql.cursors.DictCursor)
        self.mysql_collection_cursor = self.mysql_collection_connection.cursor()

        self.mysql_pms_account_register_connection = pymysql.connect(
                                                    host=SETTING[env]['MYSQL']['pms_account_register']['host'],
                                                    user=SETTING[env]['MYSQL']['pms_account_register']['user'],
                                                    password=SETTING[env]['MYSQL']['pms_account_register']['password'],
                                                    db=SETTING[env]['MYSQL']['pms_account_register']['db'],
                                                    charset=SETTING[env]['MYSQL']['pms_account_register']['charset'],
                                                    port=SETTING[env]['MYSQL']['pms_account_register']['port'],
                                                    cursorclass=pymysql.cursors.DictCursor)

        self.mysql_pms_account_register_cursor = self.mysql_pms_account_register_connection.cursor()

        self.mysql_bpa_connection = pymysql.connect(
                                                    host=SETTING[env]['MYSQL']['bpa']['host'],
                                                    user=SETTING[env]['MYSQL']['bpa']['user'],
                                                    password=SETTING[env]['MYSQL']['bpa']['password'],
                                                    db=SETTING[env]['MYSQL']['bpa']['db'],
                                                    charset=SETTING[env]['MYSQL']['bpa']['charset'],
                                                    port=SETTING[env]['MYSQL']['bpa']['port'],
                                                    cursorclass=pymysql.cursors.DictCursor)
        self.mysql_bpa_cursor = self.mysql_bpa_connection.cursor()

        self.mysql_skynet_embrace = pymysql.connect(
                                                    host=SETTING[env]['MYSQL']['skynet_embrace']['host'],
                                                    user=SETTING[env]['MYSQL']['skynet_embrace']['user'],
                                                    password=SETTING[env]['MYSQL']['skynet_embrace']['password'],
                                                    db=SETTING[env]['MYSQL']['skynet_embrace']['db'],
                                                    charset=SETTING[env]['MYSQL']['skynet_embrace']['charset'],
                                                    port=SETTING[env]['MYSQL']['skynet_embrace']['port'],
                                                    cursorclass=pymysql.cursors.DictCursor)
        self.mysql_skynet_embrace_cursor = self.mysql_skynet_embrace.cursor()

        self.mysql_skynet_merchant = pymysql.connect(
                                                    host=SETTING[env]['MYSQL']['skynet_merchant']['host'],
                                                    user=SETTING[env]['MYSQL']['skynet_merchant']['user'],
                                                    password=SETTING[env]['MYSQL']['skynet_merchant']['password'],
                                                    db=SETTING[env]['MYSQL']['skynet_merchant']['db'],
                                                    charset=SETTING[env]['MYSQL']['skynet_merchant']['charset'],
                                                    port=SETTING[env]['MYSQL']['skynet_merchant']['port'],
                                                    cursorclass=pymysql.cursors.DictCursor)
        self.mysql_skynet_merchant_cursor = self.mysql_skynet_merchant.cursor()


        self.mysql_skynet_embrace_connection = pymysql.connect(
                                                    host=SETTING[env]['MYSQL']['skynet_embrace']['host'],
                                                    user=SETTING[env]['MYSQL']['skynet_embrace']['user'],
                                                    password=SETTING[env]['MYSQL']['skynet_embrace']['password'],
                                                    db=SETTING[env]['MYSQL']['skynet_embrace']['db'],
                                                    charset=SETTING[env]['MYSQL']['skynet_embrace']['charset'],
                                                    port=SETTING[env]['MYSQL']['skynet_embrace']['port'],
                                                    cursorclass=pymysql.cursors.DictCursor)
        self.mysql_skynet_embrace_cursor = self.mysql_skynet_embrace_connection.cursor()

        self.mysql_skynet_merchant_connection = pymysql.connect(
                                                    host=SETTING[env]['MYSQL']['skynet_merchant']['host'],
                                                    user=SETTING[env]['MYSQL']['skynet_merchant']['user'],
                                                    password=SETTING[env]['MYSQL']['skynet_merchant']['password'],
                                                    db=SETTING[env]['MYSQL']['skynet_merchant']['db'],
                                                    charset=SETTING[env]['MYSQL']['skynet_merchant']['charset'],
                                                    port=SETTING[env]['MYSQL']['skynet_merchant']['port'],
                                                    cursorclass=pymysql.cursors.DictCursor)
        self.mysql_skynet_merchant_cursor = self.mysql_skynet_merchant_connection.cursor()



        # self.mysql_zu_che_connection = pymysql.connect(
        #                                             host=SETTING[env]['MYSQL']['zu_che']['host'],
        #                                             user=SETTING[env]['MYSQL']['zu_che']['user'],
        #                                             password=SETTING[env]['MYSQL']['zu_che']['password'],
        #                                             db=SETTING[env]['MYSQL']['zu_che']['db'],
        #                                             charset=SETTING[env]['MYSQL']['zu_che']['charset'],
        #                                             port=SETTING[env]['MYSQL']['zu_che']['port'],
        #                                             cursorclass=pymysql.cursors.DictCursor)
        # self.mysql_zu_che_cursor = self.mysql_zu_che_connection.cursor()

        # self.mysql_auto_loan_entry_test_connection = pymysql.connect(
        #                                                   host=SETTING['newCDW']['auto_loan_entry_test']['host'],
        #                                                   user=SETTING['newCDW']['auto_loan_entry_test']['user'],
        #                                                   password=SETTING['newCDW']['auto_loan_entry_test']['password'],
        #                                                   db=SETTING['newCDW']['auto_loan_entry_test']['db'],
        #                                                   charset=SETTING['newCDW']['auto_loan_entry_test']['charset'],
        #                                                   port=SETTING['newCDW']['auto_loan_entry_test']['port'],
        #                                                   cursorclass=pymysql.cursors.DictCursor)
        # self.mysql_auto_loan_entry_test_cursor = self.mysql_auto_loan_entry_test_connection.cursor()

        # self.mysql_auto_loan_intserv_connection = pymysql.connect(
        #                                                   host=SETTING['newCDW']['auto_loan_intserv_test']['host'],
        #                                                   user=SETTING['newCDW']['auto_loan_intserv_test']['user'],
        #                                                   password=SETTING['newCDW']['auto_loan_intserv_test']['password'],
        #                                                   db=SETTING['newCDW']['auto_loan_intserv_test']['db'],
        #                                                   charset=SETTING['newCDW']['auto_loan_intserv_test']['charset'],
        #                                                   port=SETTING['newCDW']['auto_loan_intserv_test']['port'],
        #                                                   cursorclass=pymysql.cursors.DictCursor)
        # self.mysql_auto_loan_intserv_cursor = self.mysql_auto_loan_intserv_connection.cursor()

    def __del__(self):
        self.mysql_customer_center_connection.close()
        self.mysql_customer_center_cursor.close()

        self.mysql_loan_center_connection.close()
        self.mysql_loan_center_cursor.close()

        self.mysql_apply_center_connection.close()
        self.mysql_apply_center_cursor.close()

        self.mysql_xinyongjin_connection.close()
        self.mysql_xinyongjin_cursor.close()

        self.mysql_skynet_fact_material_connection.close()
        self.mysql_skynet_fact_material_cursor.close()

        self.mysql_skynet_connection.close()
        self.mysql_skynet_cursor.close()

        self.mysql_skynet_rota_connection.close()
        self.mysql_skynet_rota_cursor.close()

        self.mysql_pms_product_register_connection.close()
        self.mysql_pms_product_register_cursor.close()

        self.mysql_skynet_credit_line_connection.close()
        self.mysql_skynet_credit_line_cursor.close()

        self.mysql_collection_connection.close()
        self.mysql_collection_cursor.close()

        self.mysql_bpa_connection.close()
        self.mysql_bpa_cursor.close()

        # self.mysql_zu_che_connection.close()
        # self.mysql_zu_che_cursor.close()

        # self.mysql_auto_loan_entry_test_connection.close()
        # self.mysql_auto_loan_entry_test_cursor.close()

        # self.mysql_auto_loan_intserv_connection.close()
        # self.mysql_auto_loan_intserv_cursor.close()

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
        table_id = int(customid) % 20
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

    def insertIntoData(self, db,sql):
        cursor= eval("self.mysql_{0}_cursor".format(db))
        connection=eval("self.mysql_{0}".format(db))
        cursor.execute(sql)
        connection.commit()



class MysqlPyUntil:
    def __init__(self, env,db):
        """
        :param env: 环境
        :param db:  数据库
        """
        self.env = env
        self.db=db
        self.mysql_connection = pymysql.connect(
                                              host=SETTING[env]['MYSQL'][self.db]['host'],
                                              user=SETTING[env]['MYSQL'][self.db]['user'],
                                              password=SETTING[env]['MYSQL'][self.db]['password'],
                                              db=SETTING[env]['MYSQL'][self.db]['db'],
                                              charset=SETTING[env]['MYSQL'][self.db]['charset'],
                                              port=SETTING[env]['MYSQL'][self.db]['port'],
                                              cursorclass=pymysql.cursors.DictCursor )
        self.mysql_cursor = self.mysql_connection.cursor()

    def __del__(self):
        """
        数据库游标断开，数据库链接断开
        :return:
        """
        self.mysql_cursor.close()
        self.mysql_connection.close()

    #新增数据
    #INSERT INTO table_name ( field1, field2,...fieldN ) VALUES (value1, value2,...valueN);
    def insertIntoData(self, sql):
        self.mysql_cursor.execute(sql)
        self.mysql_connection.commit()

    #查询数据单条(最新一条)
    def queryNewOne(self,sql):
        self.mysql_cursor.execute(sql)
        result = self.mysql_cursor.fetchone()
        return result

    #查询数据全部
    def queryAll(self, sql):
        self.mysql_cursor.execute(sql)
        result = self.mysql_cursor.fetchall()
        return result

    # 分表查询
    def queryall_by_table(self, sql):
        resultall = []
        for i in range(20):
            self.mysql_cursor.execute(sql.format(i))
            result = self.mysql_cursor.fetchall()
            resultall += result
        return resultall

    #更新数据
    #UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = 'boy'
    def updateData(self, sql):
        self.mysql_cursor.execute(sql)
        self.mysql_connection.commit()

    #删除数据
    #DELETE FROM EMPLOYEE WHERE AGE > 20"
    def deleteData(self, sql):
        self.mysql_cursor.execute(sql)
        self.mysql_connection.commit()
