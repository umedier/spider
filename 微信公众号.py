

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
import mysql

with open("wechat.yaml", "r") as file:
    file_data = file.read()
config = yaml.safe_load(file_data)

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "cookie": config['cookie'],
    "user-agent": config['user-agent'],
}
url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
# SELECT COUNT(DISTINCT(appmsgid)) FROM `wechat`
begin = 880
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

# 代表页数
with mysql.SQLManager() as db:
    while True:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        resp = requests.get(url, params=params, headers=headers)

        # 抓取失败，退出
        if resp.json()['base_resp']['ret'] == 200013:
            print("触发微信机制，抓取失败")
            break

        # 抓取完成，结束
        if len(resp.json()['app_msg_list']) == 0:
            print("已抓取完所有文章")
            break

        # 信息打印
        for row in resp.json()['app_msg_list']:
            count_sql = "SELECT * FROM wechat WHERE aid = '%s'" % (row['aid'])
            try:
                db.cursor.execute(count_sql)
                results = db.cursor.fetchone()
                if results is None:
                    insert_sql = '''INSERT INTO `spiders`.`wechat` (aid, album_id, appmsg_album_infos, appmsgid, checking, copyright_type, cover, create_time, digest, has_red_packet_cover, is_pay_subscribe, item_show_type, itemidx, link, media_duration, mediaapi_publish_status, tagid, title, update_time) VALUES( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
                        row['aid'], row['album_id'], json.dumps(row['appmsg_album_infos']), row['appmsgid'], row['checking'], row['copyright_type'], row['cover'], row['create_time'], row['digest'], row['has_red_packet_cover'], row['is_pay_subscribe'], row['item_show_type'], row['itemidx'], row['link'], row['media_duration'], row['mediaapi_publish_status'], row['tagid'], row['title'], row['update_time'])
                    db.cursor.execute(insert_sql)
                    db.conn.commit()
            except Exception as e:
                print(e)
                break

        # 循环下一页
        params['begin'] += 5
        print(params['begin'])

        # 随机等待几秒，避免被微信识别到
        num = random.randint(120, 360)
        print("---------------%s" % num)
        time.sleep(num)
