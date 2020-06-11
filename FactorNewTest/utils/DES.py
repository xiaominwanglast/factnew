#coding:utf-8
import StringIO
import base64
import gzip
import json
class Des(object):
    def unGzip(self,str_data):
        """
        :param str_data: 需要解压的内容
        :return: 解压后的内容
        """
        bs_data = base64.b64decode(str_data)
        compressed_stream = StringIO.StringIO(bs_data)
        gzip_per = gzip.GzipFile(mode='rb', fileobj=compressed_stream)
        return gzip_per.read()

    def Gzip(self,str_data):
        """
        :param str_data: 需要压缩的内容
        :return: 压缩后的内容
        """
        buf = StringIO.StringIO()
        f = gzip.GzipFile(mode='wb', fileobj=buf)
        try:
            f.write(str_data)
        finally:
            f.close()
        return base64.b64encode(buf.getvalue())

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