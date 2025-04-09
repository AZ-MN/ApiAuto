import argparse
import base64
import rsa


# 通过公钥加密
def rsa_encrypt():
    try:
        # 接收命令行参数
        parser = argparse.ArgumentParser(description="RSA 加密工具")
        parser.add_argument("-t", "--ticket", nargs=2, required=True,
                            help="用户名和密码列表，格式为 [username, password]")
        args = parser.parse_args()
        username, password = args.ticket

        # 导入公钥
        public_key_str = (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            "MIGJAoGBALO7UPE26anTGHND2Q54zYYPusDx+tbO1Yia7zoxpZediw+Baea7aFZC\n"
            "J+ZvWd5ZBTopuWvb8hNkY24eBHcXN0pU32WjsH9REp1kXhxbndnw+u3diaoUFqVc\n"
            "66xl+LXEo1Y9oDWfkGCir2JnN0aieUiPlHDLhmc+LII/ZDspITKDAgMBAAE=\n"
            "-----END RSA PUBLIC KEY-----"
        )
        pubkey = rsa.PublicKey.load_pkcs1(public_key_str.encode())

        # 加密用户名
        encrypted_username = rsa.encrypt(username.encode("utf-8"), pubkey)
        username_ciphertext = base64.b64encode(encrypted_username).decode("utf-8")

        # 加密密码
        encrypted_password = rsa.encrypt(password.encode("utf-8"), pubkey)
        password_ciphertext = base64.b64encode(encrypted_password).decode("utf-8")

        # 输出结果
        print(username_ciphertext)
        print("###")
        print(password_ciphertext)

    except Exception as e:
        print(f"加密过程中发生错误: {e}")


if __name__ == '__main__':
    rsa_encrypt()
