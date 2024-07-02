import logging

from models.ConfigRegion import ConfigRegion

# 创建一个logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# 创建一个文件处理器，用于写入日志到文件
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# 创建一个控制台处理器，用于输出日志到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 定义日志输出格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 将处理器添加到logger中
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# config_region=ConfigRegion("高新区","632","919",7,2,3,4,5)
config_region=ConfigRegion("锦江区","989","813",6,1,2,3,4)
# config_region=ConfigRegion("青羊区","873","954",6,1,2,3,4)
