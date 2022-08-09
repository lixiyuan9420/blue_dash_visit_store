import json
from datetime import datetime

import requests

from config import APP_ID, APP_SECRET, emails
from db.operation.store import StoreRecord
from init import scheduler
from logger.logger import infoLogger, errLogger



def __extract_store_record(data_json) -> StoreRecord:
    """

    :param data_json:
    :return:
    """
    data = data_json["门店拜访记录"]
    is_book = data["是否预约"]
    book_time = data["预约日期"]
    sale_id = data["销售编号"]
    goal = data["拜访目的"]
    store = data["`门店`"]
    sales = data["`经销商`"]
    store_name = data["`门店/经销商名称`"]
    store_phone_name = data["`门店/经销商联系人名称`"]
    store_phone = data["`门店/经销商电话`"]
    store_address = data["`门店/经销商地址`"]
    time = data["拜访日期"]
    result = data["拜访结果"]
    next_time = data["下次拜访日期"]
    part = data["部门"]
    sale_name = data["成员"]
    if book_time == 'null':
        book_time = '0001-01-01'
    if time == 'null':
        time = '0001-01-01'
    if next_time == 'null':
        next_time = '0001-01-01'
    infoLogger.log("store   开始添加定时任务")
    print("开始添加定时任务"+str(book_time)+str(next_time))
    if book_time != '0001-01-01':
        infoLogger.log("添加任务  预约拜访时间"+str(book_time))
        print(222)
        book_year = datetime.strptime(book_time, '%Y-%m-%d').year
        print(book_year)
        book_month = datetime.strptime(book_time, '%Y-%m-%d').month
        print(book_month)
        book_day = datetime.strptime(book_time, '%Y-%m-%d').day
        print(book_day)
        print(book_year,book_month,book_day)
        scheduler.add_job(func=send_message_book, id=str(book_time),
                          trigger='date', run_date=datetime(book_year, book_month, book_day,16, 45, 0))
        print(111)
        infoLogger.log("添加" + str(book_time) + "任务已完成")
    if next_time != '0001-01-01':
        print(222)
        infoLogger.log("添加任务  下一次拜访时间"+str(next_time))
        book_year = datetime.strptime(next_time, '%Y-%m-%d').year
        book_month = datetime.strptime(next_time, '%Y-%m-%d').month
        book_day = datetime.strptime(next_time, '%Y-%m-%d').day
        print(next_time,book_month,book_day)
        scheduler.add_job(func=send_message_book, id=str(next_time),
                          trigger='date', run_date=datetime(book_year, book_month, book_day, 16,45, 0))
        print(111)
        infoLogger.log("添加"+str(next_time)+"任务已完成")
    return StoreRecord(is_book, book_time, sale_id, goal, store, sales, store_name,
                       store_phone_name, store_phone, store_address, time, result,
                       next_time, part, sale_name)


def send_message_book():
    try:
        infoLogger.log("发送预约任务开始执行")
        print("发送预约任务开始执行")
        for email in emails:
            user_email = email.get('email')
            user_name = email.get('name')
            chat_id = get_chatId()
            user_id = get_userid(user_email)
            send_messages(user_id, chat_id,user_email,user_name)
    except:
        errLogger.log("发送预约任务执行失败")


def get_chatId():
    try:
        infoLogger.log("____get_chatId 开始")
        token = get_token()
        headers_group = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        url_group = "https://open.feishu.cn/open-apis/chat/v4/list?"
        res_group = requests.get(url_group, headers=headers_group)
        chatId = ""
        if res_group.status_code == 200:
            chatId = ((json.loads(res_group.text)).get('data').get('groups'))[0].get('chat_id')
        infoLogger.log("____get_chatId 结束")
        return chatId
    except:
        print('请求失败1')
        return None


def get_userid(email):
    """
    根据邮箱get用户id
    :param email:
    :return:
    """
    try:
        infoLogger.log("____get_userid 开始" + email)
        token = get_token()
        headers_group = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        url = "https://open.feishu.cn/open-apis/user/v1/batch_get_id?emails=%s" % email
        # userurl = "https://open.feishu.cn/open-apis/user/v1/batch_get_id?mobiles=%s" % mobiles
        res_data = requests.get(url=url, headers=headers_group)
        userid = json.loads(res_data.text)['data']['email_users'][email][0]['user_id']
        infoLogger.log("____get_userid 结束" + userid)
        return userid
    except:
        errLogger.log('请求失败userid')


def get_token():
    data = {"app_id": APP_ID, "app_secret": APP_SECRET}
    headers = {"Content-Type": "application/json"}
    url_token = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    global token
    try:
        infoLogger.log("____get_token 开始")
        res = requests.post(url_token, json=data, headers=headers)
        if res.status_code == 200:
            token = (json.loads(res.text)).get('tenant_access_token')
        return token
    except:
        errLogger.log('请求失败token')


def send_messages(userID, chatID, email, name):
    try:
        infoLogger.log("__month_send_messages 开始" + name)
        data1 = {
            "chat_id": chatID,
            "user_id": userID,
            "msg_type": "text",
            "content": {
                "text": "预约内容"
            }
        }
        token = get_token()
        headers_group = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        url_mess = "https://open.feishu.cn/open-apis/message/v4/send/"
        requests.post(url_mess, json=data1, headers=headers_group)
        infoLogger.log("__month_send_messages"+str(name)+" 发送周报成功")
    except:
        errLogger.log("send_messages  发送消息失败")
