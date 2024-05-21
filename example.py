"""快速开始的实例 """

import time

from src.pynonjishokei.main import scan_input_string

START_TIME = time.perf_counter()
print(scan_input_string(""))
END_TIME = time.perf_counter()
print(f"耗时:{round((END_TIME - START_TIME) * 1000, 3)}毫秒")
