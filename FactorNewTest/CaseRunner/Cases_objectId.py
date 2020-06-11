#coding:utf-8
import  datetime
from bson.objectid import ObjectId
import time

# gen_time=datetime.datetime.strptime("2019-02-20 16:16:01", "%Y-%m-%d %H:%M:%S")



gen_time = datetime.datetime(2018,10,12,16,0,0)
dummy_id = ObjectId.from_datetime(gen_time)
print dummy_id
strid=ObjectId("5a7ce4800000000000000000")
# strid1=ObjectId("5be12a204f9e73448c64045d")
print time.localtime(time.mktime(strid.generation_time.timetuple()))
# print time.localtime(time.mktime(strid1.generation_time.timetuple()))
# print time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(1534004099))

print ObjectId("5c7639cb913bc9404d383cfc")>ObjectId("5c6d7d410000000000000000")