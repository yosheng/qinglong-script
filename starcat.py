import hashlib
import json
import time
import os

import requests

import sendNotify


class StarCatSign:
    def __init__(self):
        self.authorization = os.environ.get('STARCAT_AUTH', '')
        self.base_url = "http://www.starcatzx.com/starcat/public/index.php"
        self.version = "3.7.4"
        self.platform = "android"

    def encrypt(self, param_string):
        try:
            md5 = hashlib.md5()
            md5.update(param_string.encode('utf-8'))
            array_of_byte = md5.digest()
            string_builder = []
            for b in array_of_byte:
                str_hex = format(b & 0xFF, '02x')
                string_builder.append(str_hex)
            return ''.join(string_builder)
        except Exception as e:
            print(f'加密过程发生错误: {str(e)}')
            return ""

    def get_headers(self):
        current_time_stamp = int(time.time())
        string_builder = self.authorization
        string_builder += str(current_time_stamp)
        string_builder += "StarCat20180803"

        encrypted_string = self.encrypt(string_builder)

        return {
            "authorization": self.authorization,
            "time": str(current_time_stamp),
            "version": self.version,
            "SecretKey": encrypted_string,
            "platform": self.platform,
            "Host": "www.starcatzx.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.11.0"
        }

    def sign_in(self):
        try:
            url = f"{self.base_url}?s=index%2Fuser%2Fsignin"
            response = requests.get(url, headers=self.get_headers())
            return json.loads(response.text)
        except Exception as e:
            print(f'签到过程发生错误: {str(e)}')
            return None

    def get_user_info(self):
        try:
            url = f"{self.base_url}?s=index%2Fuser%2Fuserinfo"
            response = requests.get(url, headers=self.get_headers())
            return json.loads(response.text)
        except Exception as e:
            print(f'获取用户信息发生错误: {str(e)}')
            return None


def main():
    if 'STARCAT_AUTH' not in os.environ:
        print('未设置STARCAT_AUTH环境变量')
        return

    starcat = StarCatSign()

    try:
        # 执行签到
        sign_result = starcat.sign_in()
        print(f'签到结果: {sign_result}')

        # 获取用户信息
        user_info = starcat.get_user_info()

        # 准备通知内容
        notification_content = []

        if sign_result:
            notification_content.append(f"签到状态: {sign_result.get('message', '未知')}")

        if user_info and 'data' in user_info:
            catcoins = user_info['data'].get('catcoins', '未知')
            notification_content.append(f"当前Catcoins: {catcoins}")

        # 发送通知
        content = '\n'.join(notification_content)
        print('==================================')
        print(content)
        sendNotify.send(title="占星喵签到", content=content)

    except Exception as e:
        error_msg = f'运行过程发生错误: {str(e)}'
        print(error_msg)
        try:
            sendNotify.send(title="占星喵签到异常", content=error_msg)
        except:
            print('发送通知失败')


if __name__ == '__main__':
    main()