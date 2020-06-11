# coding:utf-8
import logging
from utils import logger_config  # 导入自定义的logging配置

logger = logging.getLogger(__file__)  # 生成logger实例

class LogUtil:

    @classmethod
    def printlog(cls,req,resp):
        logging.info("【请求报文】"+str(req))
        logging.info("【响应报文】"+str(resp))
