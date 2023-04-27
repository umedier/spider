import json
import os
import mysql


wechat_spider_json_file = "wechat_spider_data.json"

# 获取当前json文件内容，计算已爬取的页数
if os.path.exists(wechat_spider_json_file):
    with open(wechat_spider_json_file, "r") as file:
        wechat_app_msg_list = json.load(file)


# i = len(wechat_app_msg_list)
# print("之前已抓取{}页文章,将从下一页开始抓取".format(i))

with mysql.SQLManager() as db:
    for item in wechat_app_msg_list:
        for row in item['app_msg_list']:
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
                db.conn.rollback()
                print(e)
