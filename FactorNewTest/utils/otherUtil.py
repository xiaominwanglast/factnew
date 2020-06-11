#coding:utf-8
import re
import requests
import datetime
from dateutil.relativedelta import relativedelta
import calendar
from math import sin,cos,asin,radians,sqrt

def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371.393  # 地球平均半径，单位为公里
    return c * r * 1000

def getPlaceFromGeo(lng,lat):
    url = "http://api.map.baidu.com/geocoder/v2/?location=%s,%s&output=json&pois=1&ak=FYtp2nUySbF0uhoGHwA2DNE0" % (lat, lng)
    r = requests.get(url)
    if r.status_code!=200:
        return {}
    return r.json()

def return_strfYmd_date(date):
    return datetime.datetime.strptime(date.strftime('%Y-%m-%d'),'%Y-%m-%d')

def phoneValid(phone):
    phone = str(phone).replace(' ', '').replace('-', '')
    pattern = re.compile(r'^((17911)|(12593)|(17951)|(86)|(086)|(\+86)|(\(\+86\)))?(((13[0-9]{1})|(15[0-9]{1})|(18[0,5-9]{1}))+\d{8})$')
    if pattern.match(phone):
        if len(phone) > 11:
            return phone[-11:]
        else:
            return phone
    else:
        return None

def phoneClear(phone):
    phone=str(phone).replace('-','').replace(' ','').replace('\t','').replace('\r','').replace('\n','').replace('\r\n','').replace(' ','')
    if len(phone)==11:
        return str(phone)
    if len(phone)>11 and phone.startswith('+'):
        return phone[3:]
    if len(phone)>11 and phone.startswith('86'):
        return phone[2:]
    if len(phone)>11 and (phone.startswith('17951') or phone.startswith('12593')):
        return phone[5:]
    return

def phone_clean_new(phone):
    data=re.match("^(1[3456789](\d{9}))$",str(phone))
    if data:
        return phone
    else:
        return

def phone_clean(phone):
    data=re.match("^(1[34578](\\d{9}))$",str(phone))
    if data:
        return phone
    else:
        return

def phoneClean(phone):
    phone = str(phone).replace(' ', '').replace('-', '')
    pattern = re.compile(r'^((17911)|(12593)|(17951)|(86)|(086)|(\+86)|(\(\+86\)))?(((13[0-9]{1})|(15[0-9]{1})|(18[0,5-9]{1}))+\d{8})$')
    if pattern.match(phone):
        if len(phone) > 11:
            return phone[-11:]
        else:
            return phone
    else:
        return phone[-11:]

def calmonths(d1, d2):
    date_list = []
    begin_date = d1
    end_date = d2
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m")
        date_list.append(date_str)
        begin_date = add_months(begin_date,1)
    return len(date_list)-1

def add_months(dt,months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)

def calmonths_rhzx(d1, d2):
    date_list = []
    begin_date = d1
    end_date = d2
    while begin_date < end_date:
        date_str = begin_date.strftime("%Y%m")
        date_list.append(date_str)
        begin_date = add_months_rhzx(begin_date,1)
    return len(date_list)

def add_months_rhzx(dt,months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def getXmonthDate(eventTime,month):
    dateCollect=eventTime+datetime.timedelta(hours=8)
    date0=str(dateCollect)[0:10]+" "+"00:00:00"
    date= datetime.datetime.strptime(date0,"%Y-%m-%d %H:%M:%S")
    dateDelta=date+relativedelta(months=month)
    return dateDelta

def sxjPhoneVaild(phone):
    if not phone:
        return
    if isinstance(phone,int):
        phone=str(phone)
    pattern = re.compile(r'^\s?(\d{5})?(0?)(1(3|4|5|6|7|8|9)(\d{9}))(\D|$)')
    if pattern.match(phone):
        if len(phone) > 11:
            return phone[-11:]
        else:
            return phone
    else:
        return None
def phone_cleanV2(phone):
    data=re.match("^(1[34578](\\d{9}))$",str(phone))
    if data:
        return phone
    else:
        return

if __name__ == '__main__':
    # phone = '15090658127'
    # phone=phoneClear(phone)
    # print phone_clean_new(phone)
    a=getPlaceFromGeo(114.112,22.664).get("result").get("addressComponent")
    print a.get("province")
    print a.get("city")