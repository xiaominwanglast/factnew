#coding:utf-8
import configparser

def readCdwConfig(part,chid):
    config = configparser.ConfigParser()
    config.read("cdwConfig.ini", encoding="utf-8")
    return config.get(part, chid)


