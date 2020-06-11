import hashlib
from utils.DES import *
import requests


SECRET_KEY = "AEE7790037EBF4E2B5DFACC26079055C"
host="kmopenapi.2345.com"
#host="testkmapi.2345.com"



def invoke(url):
	data = {
		"sign": "2a41558e04a3c8570cc9e232d51fcb49",
		"signType": "MD5",
		"data": {
			"requestTime": "1218196800000",
			"merchantCode": "2345test",
			"applyNo": "140000199708095458",
			"name": "王晓敏",
			"mobile": "17621145335", #18301924915
			"certId": "310112198912244913" #321321199109012916
		}
	}
	data.pop("sign")
	print(data)
	sign=Des().get_sign(data['data'],secret_key=SECRET_KEY)
	data['sign']=sign
	url=url
	print (url)
	r=requests.post(url=url,json=data)

	print (r.status_code)
	print (r.json())


if __name__=='__main__':
	url="https://%s/skynet-embrace/risk/creditScore" % host
	invoke(url)  # 1.0
	url = "https://%s/skynet-embrace/risk/1.5/creditScore" % host
	invoke(url)   # 1.5


# 叶松林
# 36072619950104439X
# 刘科
# 371202198912104916
# 宁倩娟
# 142727199701271041
# 吴浩杰
# 410325199603176058