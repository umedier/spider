import json
import os


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
