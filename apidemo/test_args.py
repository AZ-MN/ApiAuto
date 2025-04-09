import argparse


def get_random_num():
    # 获取jmeter传入的值，然后赋值给变量ticket，变量即可为Python调用
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--ticket", help="这是ticket")
    args = parser.parse_args()
    ticket = args.ticket
    # print('你输入的值：{}'.format(ticket))
    result = "new_value:" + str(ticket) + "123"
    print(result)  # 需要将结果打印出来，不然dos命令调用后，结果为空


if __name__ == '__main__':
    get_random_num()
