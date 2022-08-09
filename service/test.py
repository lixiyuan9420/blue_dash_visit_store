from datetime import datetime

import requests
import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_apscheduler import APScheduler

import biz_logic
import config


def get(url: str, **kwargs):
    r = requests.get(
        url,
        cookies=kwargs.get("cookies", {}),
        params=kwargs.get("params", {}),
        headers=dict(kwargs.get("headers", {}), **{"Connection": "close"}),
        json=kwargs.get("json", {}),
    )
    return r


def post(url: str, **kwargs):
    r = requests.post(
        url,
        cookies=kwargs.get("cookies", {}),
        params=kwargs.get("params", {}),
        headers=dict(kwargs.get("headers", {}), **{"Connection": "close"}),
        json=kwargs.get("json", {}),
    )
    return r


def get_tenant_header():
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal/"
    # 开放平台机器人应用凭证，用于开通访问服务台权限
    body = {
        "app_id": "cli_a207337a17f9100e",
        "app_secret": "oXmHsL2k1z36Z4eHZkaijgAXzcdUuj4w"
    }
    # 把 服务台ID:服务台Token 转换为base64，填写到 X-Lark-Helpdesk-Authorization，用于指定访问哪个服务台
    # 在线base64编码  https://base64.us  https://tool.oschina.net/encrypt?type=3
    return {
        "Authorization": "Bearer %s"
                         % post(url, json=body).json()["tenant_access_token"],
        "X-Lark-Helpdesk-Authorization": "Njk4OTgwNTM1ODU1ODQ3ODM1NTpodC1lYjk1Y2ZlYi03ZGM1LTY1ZGUtMTUzOS1iMzZmOTk3MmM3ZjA=",
    }


tenant_header = get_tenant_header()


def get_ticket(id):
    url = "https://open.feishu.cn/open-apis/helpdesk/v1/tickets/%s" % id
    res = get(url, headers=tenant_header)
    try:
        info = res.json()["data"]["ticket"]
        return info
    except:
        print(id, res)
        return get_ticket(id)


scheduler = APScheduler(scheduler=BackgroundScheduler(timezone='Asia/Shanghai'))



app = Flask(__name__)

# 加载初始化设置
app.config.from_object(config)

# 登记蓝图，于是这个app可以作为一个web server生效
app.register_blueprint(biz_logic.bp)

def pr():
    print(1)
# 自动运行这个app
if __name__ == '__main__':
    book_time = '2022-8-9'
    book_year = 0000,
    book_month = 00
    book_day = 00
    if book_time != '0001-01-01':
        book_year = datetime.strptime(book_time, '%Y-%m-%d').year
        book_month = datetime.strptime(book_time, '%Y-%m-%d').month
        book_day = datetime.strptime(book_time, '%Y-%m-%d').day
    scheduler.add_job(func=pr, id=str(book_time),
                      trigger='date', run_date=datetime(book_year, book_month, book_day,
                                                        10, 29, 0))
    scheduler.init_app(app=app)
    scheduler.start()
    app.run(host='0.0.0.0',port=3393)



