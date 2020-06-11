#coding:utf-8
import pymysql.cursors
from localSetting import SETTING
class MysqlUntil:
    def __init__(self, env):
        self.env = env
        self.mysql_online_skynet_check_connection = pymysql.connect(
                                                          host=SETTING[env]['MYSQL']['online_skynet_check']['host'],
                                                          user=SETTING[env]['MYSQL']['online_skynet_check']['user'],
                                                          password=SETTING[env]['MYSQL']['online_skynet_check']['password'],
                                                          db=SETTING[env]['MYSQL']['online_skynet_check']['db'],
                                                          charset=SETTING[env]['MYSQL']['online_skynet_check']['charset'],
                                                          port=SETTING[env]['MYSQL']['online_skynet_check']['port'],
                                                          cursorclass=pymysql.cursors.DictCursor)
        self.mysql_online_skynet_check_cursor = self.mysql_online_skynet_check_connection.cursor()

    def __del__(self):
        self.mysql_online_skynet_check_connection.close()
        self.mysql_online_skynet_check_cursor.close()


    def insert_skynet_data(self,product_code,time_over,scene_code,decision_000_count,decision_001_count,decision_002_count):
        decision_pass_rate=str(round(float(decision_002_count)/(decision_000_count+decision_001_count+decision_002_count),4))
        decision_refuse_rate=str(round(float(decision_000_count)/(decision_000_count+decision_001_count+decision_002_count),4))
        sql="insert into skynet_decision values (DEFAULT ,'{0}','{1}','{2}',{3},{4},{5},'{6}','{7}',DEFAULT )".format(product_code,time_over,scene_code,decision_000_count,decision_001_count,decision_002_count,decision_pass_rate,decision_refuse_rate)
        self.mysql_online_skynet_check_cursor.execute(sql)
        self.mysql_online_skynet_check_connection.commit()

    def insert_lake_data(self):
        """TODO 后期再写"""
        pass


    def insert_galaxy_data(self):
        """TODO 后期再写"""
        pass

if __name__=="__main__":
    MysqlUntil(env='local').insert_skynet_data(product_code='vip',time_over='[2019/03/11 16:20:00]-[2019/03/11 16:30:00]',
                                               scene_code='credit',decision_000_count=40,decision_001_count=10,decision_002_count=90)
