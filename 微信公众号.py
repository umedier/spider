

'''
登录
搜索
文章列表
    https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=5&fakeid=MzIyMDMxOTIyOQ==&type=9&query=&token=1559984897&lang=zh_CN&f=json&ajax=1
    https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=50&count=5&fakeid=MzIyMDMxOTIyOQ==&type=9&query=%E8%8A%AF%E7%89%87&token=1559984897&lang=zh_CN&f=json&ajax=1
    https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=1&fakeid=MzIyMDMxOTIyOQ==&type=9&query=&token=1559984897&lang=zh_CN&f=json&ajax=1
    https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=1&fakeid=MzIyMDMxOTIyOQ&type=9&query=&token=1559984897&lang=zh_CN&f=json&ajax=1
'''


import yaml
import requests
import time
import datetime
import json
import os
import random

with open("wechat.yaml", "r") as file:
    file_data = file.read()
config = yaml.safe_load(file_data)
# headers = {
#     "cookie": config['cookie'],
#     "user-agent": config['user-agent'],
# }

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": config['user-agent'],
    "cookie": "appmsglist_action_3232843256=card; ua_id=WOBLP8jp3HexYZgvAAAAACfYO1hxtNJryk4RdPjevH4=; wxuin=81301713657027; mm_lang=zh_CN; pgv_pvid=2853491328; RK=NSWkFnn9dT; ptcz=b7e1727801ea73e978afc9076c3383bc3362442bf572faad47caac84c34ee6bd; rewardsn=; wxtokenkey=777; wwapp.vid=; wwapp.cst=; wwapp.deviceid=; sig=h010c2848ccef67ebaec85b7c712ac3d58f5529d4b3048923bc15227b08d46bc3548a45650eef9ffef3; _clck=0|1|fb0|0; uuid=2fdf1bfac39df91c4a3d87204865bb41; rand_info=CAESIJErN5pChAh0lIrICe9GK+7PDAdBsRm1ougjka6EkFbo; slave_bizuin=3232843256; data_bizuin=3247840771; bizuin=3232843256; data_ticket=SIvEHMfuDKIyFSUX6G8NDyGFyGNwUcT4zOXpbSAYnDX7O8fYoI9yYf8joBCGWkWJ; slave_sid=TXNOWWxBdVE5OFNrZl9Vcl93QXdHb2FBd0FTekZHaFFVQVZwR0xpSFRpUFh2dUhJMTJqeHpJaEpiaG13eTQ4Y3UzSXlWWXoyRG0xeGRpMHJzOW1QUFJZM0VEal9WcURiNTM5Tjc0ZTRndE01d2VqR3hVbFp4RWEycmdOMmFOcFRWcm9XZ00yYWR1RVZJbHYw; slave_user=gh_1d846312aa47; xid=189e10cf57c00867dc5a4abdeb37c329"
}
url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
begin = 0
count = 5
params = {
    'action': 'list_ex',
    'begin': begin,
    'count': count,
    'fakeid': config['fakeid'],
    'type': 9,
    'query': '',
    'token': config['token'],
    'lang': 'zh_CN',
    'f': 'json',
    'ajax': 1,
}


# 结果文件设置
wechat_spider_json_file = "wechat_spider_data.json"

# 获取当前json文件内容，计算已爬取的页数
if os.path.exists(wechat_spider_json_file):
    with open(wechat_spider_json_file, "r") as file:
        wechat_app_msg_list = json.load(file)
        # print("之前已抓取{}页文章,将从下一页开始抓取".format(1+len(wechat_app_msg_list))
else:
    wechat_app_msg_list = []


i = len(wechat_app_msg_list)
print("之前已抓取{}页文章,将从下一页开始抓取".format(i))

while True:
    init = i * int(count)
    params["begin"] = str(init)

    # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    resp = requests.get(url, params=params, headers=headers)

    # 抓取失败，退出
    if resp.json()['base_resp']['ret'] == 200013:
        print("触发微信机制，抓取失败，当前抓取第{0}页，每页{1}篇".format((i+1), count))
        break

    # 抓取完成，结束
    if len(resp.json()['app_msg_list']) == 0:
        print("已抓取完所有文章，共抓取{0}篇".format((i+1)*int(count)))
        break

    # 抓取成功，json格式保存返回的接口信息
    wechat_app_msg_list.append(resp.json())
    print("抓取第{0}页成功，每页{1}篇, 共抓取了{2}篇".format((i+1), count, (i+1)*int(count)))

    # 信息打印
    for item in resp.json()['app_msg_list']:
        # 随机等待几秒，避免被微信识别到
        num = random.randint(0, 2)
        time.sleep(num)
        print(item['title'])

    # 循环下一页
    i += 1
    # if i == 1:
    #     break

with open(wechat_spider_json_file, "w") as file:
    json.dump(wechat_app_msg_list, file, indent=2, ensure_ascii=False)

# 46 / 69 / 90  16:51 18:06
