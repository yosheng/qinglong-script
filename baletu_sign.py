import sendNotify
import os

import requests


def main(userid, cookie, ut):
    url = 'https://api.baletu.com/App401/UserSignIn/SignInList'

    params = {'user_id': userid, 'ut': ut, 'product_id': 3}

    headers = {
        'Cookie': cookie
    }

    res = requests.post(url, params=params, headers=headers)
    if res.status_code == 200:
        data = res.json()
        print(f'签到结果:{data["result"]}')


if __name__ == '__main__':
    user_id = 1002301111
    cookie = ""
    ut = ''
    if 'BALATU_COOKIE' in os.environ:
        cookie = os.environ.get("BALATU_COOKIE")
        user_id = os.environ.get("BALATU_USERID")
        ut = os.environ.get("BALATU_UT")
        main(user_id, cookie, ut)
    else:
        print('不存在青龙变量，本地运行')
        if user_id == '' or cookie == '' or ut == '':
            print('缺乏登入用户信息')
            exit()
        else:
            try:
                main(user_id, cookie, ut)
            except Exception as e:
                print(e)
    try:
        print('==================================')
        sendNotify.send(title="巴乐兔", content="签到完成!")  # 发送通知
    except Exception as e:
        print(e)
