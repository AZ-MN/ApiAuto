"""
@FileName  test.py
@Auther    百里
@description  ... 
"""

import time


def get_random_num():
    id = str(int(time.time()))
    print(id)  # 需要将结果打印出来，不然dos命令调用后，结果为空


if __name__ == '__main__':
    get_random_num()
