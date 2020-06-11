#coding:utf-8
import hashlib
import io
import base64
import gzip
import json

from Crypto.Hash import SHA1
from Crypto.Signature import pkcs1_15
from pyDes import des, CBC, PAD_PKCS5
from Crypto.PublicKey import RSA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


class Des(object):
    def unGzip(self,str_data):
        """
        :param str_data: 需要解压的内容
        :return: 解压后的内容
        """
        bs_data = base64.b64decode(str_data)
        compressed_stream = io.BytesIO(bs_data)
        gzip_per = gzip.GzipFile(mode='rb', fileobj=compressed_stream)
        return gzip_per.read()

    def Gzip(self,str_data):
        """
        :param str_data: 需要压缩的内容
        :return: 压缩后的内容
        """
        buf = io.StringIO()
        f = gzip.GzipFile(mode='wb', fileobj=buf)
        try:
            f.write(str_data)
        finally:
            f.close()
        return base64.b64encode(buf.getvalue())

#风控输出加签
    def get_sign(self,data,secret_key):
        list = []
        for i in data.keys():
            list.append(i)
            new = sorted(list, key=lambda i: i[0])
        sign_str = ""
        for i in new:
            sign_str = sign_str + i + "=" + data.get(i) + "&"
        sign_str = sign_str[0:-1] + "&secretKey=" + secret_key
        print(sign_str)
        m = hashlib.md5()
        m.update(sign_str.encode('utf-8'))
        print(m.hexdigest())
        return m.hexdigest()

    def get_md5(self,str):
        m = hashlib.md5()
        m.update(str.encode('utf-8'))
        #print(m.hexdigest())
        return m.hexdigest()


    def rsa_sign(self,private_key,content):
        # 读取私钥信息用于加签
        private_key = RSA.importKey(private_key) ## open("my_private_rsa_key.pem").read()
        #print ("con---:"+content)
        hash_obj = SHA1.new(content)
        # print(pkcs1_15.new(private_key).can_sign())  #check wheather object of pkcs1_15 can be signed
        # base64编码打印可视化

        signature = base64.b64encode(pkcs1_15.new(private_key).sign(hash_obj))
        sign_str=str(signature,'utf-8') #转换为字符串
        print (sign_str)
        return sign_str

    def rsa_signverify(self,publickey,message,signature):
        # 读取公钥信息用于验签
        public_key = RSA.importKey(publickey)
        # message做“哈希”处理，RSA签名这么要求的
        hash_obj = SHA1.new(message)
        try:
            # 因为签名被base64编码，所以这里先解码，再验签
            pkcs1_15.new(public_key).verify(hash_obj, base64.b64decode(signature))
            print('The signature is valid.')
            return True
        except (ValueError, TypeError):
            print('The signature is error.')
            return False

    def RSAencript(self,key,content):
        rsakey = RSA.importKey(key)  # 导入读取到的公钥
        cipher = PKCS1_v1_5.new(rsakey)  # 生成对象
        cipher_text = base64.b64encode(cipher.encrypt(
            content.encode(encoding="utf-8")))  # 通过生成的对象加密message明文，注意，在python3中加密的数据必须是bytes类型的数据，不能是str类型的数据
        print(cipher_text)
        cipher_text = str(cipher_text, 'utf-8')  # 转换为字符串
        return cipher_text

    def RSAdecript(self,key,content):
        rsakey = RSA.importKey(key)
        cipher = PKCS1_v1_5.new(rsakey)
        cipher_text = cipher.decrypt(base64.b64decode(content), "ERROR")
        print (cipher_text)
        return cipher_text

if __name__=="__main__":
    fs=open('1.txt','r')
    data=fs.read()
    fs.close()
    # gzip1= Des().Gzip(data)
    # print gzip1
    json_1=json.loads(Des().unGzip(data))
    with open('db', 'wt') as f:
        f.write(json.dumps(json_1,sort_keys=True, indent=2))
    f.close()
    # print json.dumps(json_1,sort_keys=True, indent=2)