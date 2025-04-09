import argparse
import base64
import rsa


# 通过公钥加密
def rsa_jiami():
    # 接收cmd命令里面的参数
    parse = argparse.ArgumentParser()
    parse.add_argument("-t", "--ticket", action="append")
    args = parse.parse_args()
    ticket = args.ticket
    # print("ticket:%s" % ticket)
    # 导入公钥
    public_key_str = ("-----BEGIN RSA PUBLIC KEY-----\nMIGJAoGBALO7UPE26anTGHND2Q54zYYPusDx+tbO1Yia7zoxpZediw"
                      "+Baea7aFZC\nJ+ZvWd5ZBTopuWvb8hNkY24eBHcXN0pU32WjsH9REp1kXhxbndnw+u3diaoUFqVc\n66xl"
                      "+LXEo1Y9oDWfkGCir2JnN0aieUiPlHDLhmc+LII/ZDspITKDAgMBAAE=\n-----END RSA PUBLIC KEY-----")
    pubkey = rsa.PublicKey.load_pkcs1(public_key_str.encode())
    # 加密用户名
    username_str = rsa.encrypt(str(ticket[0]).encode("utf-8"), pubkey)
    # 把二进制转化成字符串格式
    username_miwen = base64.b64encode(username_str).decode("utf-8")
    print(username_miwen)
    print("###")
    # 加密密码
    password_str = rsa.encrypt(str(ticket[1]).encode("utf-8"), pubkey)
    # 把二进制转化成字符串格式
    password_miwen = base64.b64encode(password_str).decode("utf-8")
    print(password_miwen)


if __name__ == '__main__':
    rsa_jiami()
