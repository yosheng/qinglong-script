import sendNotify
import os
import requests
import time


def do_lottery(user_id, cookie, ut):
    params = {
        'user_id': user_id,
        'ut': ut,
        'product_id': 3
    }

    headers = {
        'Cookie': cookie
    }

    try:
        # 抽奖主页信息
        url = 'https://m.baletu.com/Lotteryapi/index'
        res = requests.post(url, params=params, headers=headers)
        if res.status_code == 200:
            data = res.json()
            print(f'抽奖主页信息:{data}')

        # 执行任务
        url = 'https://m.baletu.com/UserPoints/doExchange'
        res = requests.post(url, params=params, headers=headers)
        if res.status_code == 200:
            data = res.json()
            print(f'任务结果:{data}')

        # 购买抽奖次数
        url = 'https://m.baletu.com/Lotteryapi/buyLotteryCnt'
        res = requests.post(url, params=params, headers=headers)
        if res.status_code == 200:
            data = res.json()
            print(f'购买结果:{data}')

        # 获取今日可用抽奖次数
        url = 'https://m.baletu.com/Lotteryapi/getTodayLastCnt'
        res = requests.post(url, params=params, headers=headers)
        lottery_results = []

        if res.status_code == 200:
            data = res.json()
            lottery_count = int(data['result']['today_last_cnt'])
            print(f'可用抽奖次数:{lottery_count}')

            # 执行抽奖
            while lottery_count > 0:
                url = 'https://m.baletu.com/Lotteryapi/doLottery'
                res = requests.post(url, params=params, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    result = data["result"]
                    lottery_results.append(result["goods_name"])
                    print(f'本次抽奖结果:{result["goods_name"]} 返回参数:{data}')
                else:
                    print('抽奖请求异常')
                lottery_count -= 1
                time.sleep(1)  # 添加延迟，避免请求过快

        return lottery_results

    except Exception as e:
        print(f'抽奖过程发生异常: {str(e)}')
        return []


def main():
    user_id = ''
    cookie = ''
    ut = ''

    # 优先使用环境变量
    if 'BALATU_COOKIE' in os.environ:
        cookie = os.environ.get("BALATU_COOKIE")
        user_id = os.environ.get("BALATU_USERID")
        ut = os.environ.get("BALATU_UT")
    else:
        print('未检测到环境变量，使用本地配置')

    if not all([user_id, cookie, ut]):
        print('缺少必要的登录信息')
        return

    try:
        lottery_results = do_lottery(user_id, cookie, ut)

        # 生成通知内容
        if lottery_results:
            content = "抽奖完成!\n获得奖品: " + ", ".join(lottery_results)
        else:
            content = "抽奖完成，但未获得奖品"

        print('==================================')
        sendNotify.send(title="巴乐兔抽奖", content=content)

    except Exception as e:
        print(f'运行异常: {str(e)}')
        try:
            sendNotify.send(title="巴乐兔抽奖异常", content=f"发生错误: {str(e)}")
        except:
            print('发送通知失败')


if __name__ == '__main__':
    main()