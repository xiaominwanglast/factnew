import hashlib
from utils.DES import *
import requests


SECRET_KEY = "sisrwaofn3m4snwyllxnvo6d"
#host="kmopenapi.2345.com"
host="testkmapi.2345.com"


#host="172.17.0.31:10106"
data = {
	"sign": "2a41558e04a3c8570cc9e232d51fcb49",
	"signType": "MD5",
	"data": {
		"requestTime": "1218196800000",
		"merchantCode": "jhf_test",
		"applyNo": "140000199708095458",
		"name": "王晓敏",
		"mobile": "17621145335", #18301924915
		"certId": "450321199710141258" #321321199109012916
	}
}
data.pop("sign")
print(data)
sign=Des().get_sign(data['data'],secret_key=SECRET_KEY)
data['sign']=sign
url="https://%s/skynet-embrace/risk/creditScore" % host
print (url)
r=requests.post(url=url,json=data)

print (r.status_code)
print (r.json())



# 叶松林
# 36072619950104439X
# 刘科
# 371202198912104916
# 宁倩娟
# 142727199701271041
# 吴浩杰
# 410325199603176058