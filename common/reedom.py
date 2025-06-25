import random
import time
from datetime import datetime

# 生成1-99的随机数
num = random.randint(1, 99)
# 格式化为两位数，个位数补零
posNo = f"{num:02d}"
print(posNo)  # 示例输出：05 或 42


# 获取当前时间戳（10位，秒级）
timestamp = int(time.time())
print(timestamp)  # 示例输出：1719391234

# "%Y%m%d%H%M%m%S%f" 年月日时分秒毫秒
# 生成10位时间字段（格式：YYYYMMDDHH）
serialNumber = datetime.now().strftime("%d%m%M%m%S")
print(serialNumber)  # 示例输出：2024062716（2024年6月27日16时）
