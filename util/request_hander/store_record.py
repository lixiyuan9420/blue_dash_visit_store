import json

import jieba
import pandas as pd
import requests
from gensim import corpora, models, similarities

from config import APP_ID, APP_SECRET, emails
from db.operation.store import StoreRecord
from db.operation.store_sql import query_store_record_1, query_store_record, query_store_record_yesterday, \
    query_store_record_yesterday_1, query_store_record_two_day, query_store_record_two_day_1, \
    query_is_exist_by_store, query_is_exist_by_sale, query_is_exist_by_people, \
    query_is_exist_by_address, query_is_exist_by_phone, query_is_exist, query_is_exist_by_ip
from logger.logger import infoLogger, errLogger


def confirm_add(address):
    para = {'key': '2f6d8c027b74979f34de9b25a4540c0d',  # 高德Key
            'keywords': address}  # 地址参数
    url = 'https://restapi.amap.com/v3/place/text?parameters'  # 高德地图地理编码API服务地址
    result = requests.get(url, para)  # GET方式请求
    result = result.json()

    return result


def extract_store_is_exist(data_json):
    # {
    #
    #     "查询归属": {
    #
    #         "成员": "xxx",
    #         "门店": "xxx",
    #         "经销商": "xxx"
    #     },
    #
    #     "token": "this_is_a_token"
    #
    # }
    data = data_json["查询归属"]
    member = data["成员"]
    store = data["门店"]
    sale = data["经销商"]
    store_people = data["门店联系人"]
    sale_people = data["经销商联系人"]
    store_phone = data["门店电话"]
    sale_phone = data["经销商电话"]
    store_address = data["门店地址"]
    sale_address = data["经销商地址"]
    store_is_exist = query_is_exist_by_store(store,member)
    sale_is_exist = query_is_exist_by_sale(sale,member)
    # sale_is_exist = []
    store_people_is_exist = query_is_exist_by_people(store_people)
    sale_people_is_exist = query_is_exist_by_people(sale_people)
    store_address_is_exist = query_is_exist_by_address(store_address,member)
    sale_address_is_exist = query_is_exist_by_address(sale_address,member)
    exist = 0
    if store_address is not None:
        result = confirm_add(store_address)
        store_ip_is_exist = query_is_exist_by_ip(str(result['pois'][0]['location']),member)
        print(len(store_ip_is_exist))
        if len(store_ip_is_exist) > 0:
                exist = exist + len(store_ip_is_exist)
        elif len(store_ip_is_exist) == 0:
            exist = exist + 0
    if sale_address is not None:
        result = confirm_add(sale_address)
        sale_ip_is_exist = query_is_exist_by_ip(str(result['pois'][0]['location']),member)
        print(len(sale_ip_is_exist))
        if len(sale_ip_is_exist) > 0:
                exist = exist + len(sale_ip_is_exist)
        elif len(sale_ip_is_exist) == 0:
            exist = exist + 0
    store_phone_is_exist = query_is_exist_by_phone(store_phone)
    sale_phone_is_exist = query_is_exist_by_phone(sale_phone)
    is_exist = 0
    if len(store_is_exist) + len(sale_is_exist) + len(store_address_is_exist) + len(sale_address_is_exist) + exist > 0:
        is_exist = len(store_is_exist) + len(sale_is_exist) + len(store_address_is_exist) + len(sale_address_is_exist)+exist
    return is_exist


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
    ip = ""
    if store_address != 'null':
        ip = str(confirm_add(store_address)['pois'][0]['location'])
        # print("ip = "+str(ip))
    if store_address == 'null':
        ip = "null"
    # infoLogger.log("store   开始添加定时任务")
    # if book_time != '0001-01-01':
    #     infoLogger.log("添加任务  预约拜访时间"+str(book_time))
    #     book_year = datetime.strptime(book_time, '%Y-%m-%d %H:%M').year
    #     book_month = datetime.strptime(book_time, '%Y-%m-%d %H:%M').month
    #     book_day = datetime.strptime(book_time, '%Y-%m-%d %H:%M').day
    # scheduler.add_job(func=send_message_book, id=str(book_time)+str(sale_name),
    #                   trigger='date', run_date=datetime(book_year, book_month, book_day,13, 0, 0),timezone='Asia/Shanghai')
    # infoLogger.log("添加" + str(book_time) + "任务已完成")
    # if next_time != '0001-01-01':
    #     infoLogger.log("添加任务  下一次拜访时间"+str(next_time))
    #     book_year = datetime.strptime(next_time, '%Y-%m-%d %H:%M').year
    #     book_month = datetime.strptime(next_time, '%Y-%m-%d %H:%M').month
    #     book_day = datetime.strptime(next_time, '%Y-%m-%d %H:%M').day
    #     scheduler.add_job(func=send_message_book, id=str(next_time)+str(sale_name),
    #                       trigger='date', run_date=datetime(book_year, book_month, book_day,13, 22, 0),timezone='Asia/Shanghai')
    #     infoLogger.log("添加"+str(next_time)+"任务已完成")
    return StoreRecord(is_book, book_time, sale_id, goal, store, sales, store_name,
                       store_phone_name, store_phone, store_address, time, result,
                       next_time, part, sale_name, ip)


def send_message_total():
    send_message_book()
    send_message_book_second()
    send_message_book_third()


def send_message_book():
    try:
        infoLogger.log("发送预约任务开始执行")
        store_books = query_store_record()
        stores = query_store_record_1()
        for store_book in store_books:
            for email in emails:
                if email.get('name') == store_book.sale_name:
                    user_email = email.get('email')
                    user_name = email.get('name')
                    chat_id = get_chatId()
                    user_id = get_userid(user_email)
                    send_messages(user_id, chat_id, user_email, user_name, store_book)
        for store in stores:
            for email in emails:
                if email.get('name') == store.sale_name:
                    user_email = email.get('email')
                    user_name = email.get('name')
                    chat_id = get_chatId()
                    user_id = get_userid(user_email)
                    send_messages(user_id, chat_id, user_email, user_name, store)
        infoLogger.log("发送预约任务执行成功")
    except:
        errLogger.log("发送预约任务执行失败")


def send_message_book_second():
    """
    提前两天发送消息
    :return:
    """
    try:
        infoLogger.log("发送提前一天任务开始执行")
        store_books = query_store_record_yesterday()
        stores = query_store_record_yesterday_1()
        for store_book in store_books:
            for email in emails:
                if email.get('name') == store_book.sale_name:
                    user_email = email.get('email')
                    user_name = email.get('name')
                    chat_id = get_chatId()
                    user_id = get_userid(user_email)
                    send_messages_yesterday(user_id, chat_id, user_email, user_name, store_book)
        for store in stores:
            for email in emails:
                if email.get('name') == store.sale_name:
                    user_email = email.get('email')
                    user_name = email.get('name')
                    chat_id = get_chatId()
                    user_id = get_userid(user_email)
                    send_messages_yesterday(user_id, chat_id, user_email, user_name, store)
        infoLogger.log("发送提前一天拜访任务执行成功")
    except:
        errLogger.log("发送提前一天拜访任务执行失败")


def send_message_book_third():
    """
    提前两天发送消息
    :return:
    """
    try:
        infoLogger.log("发送提前两天拜访任务开始执行")
        store_books = query_store_record_two_day()
        stores = query_store_record_two_day_1()
        for store_book in store_books:
            for email in emails:
                if email.get('name') == store_book.sale_name:
                    user_email = email.get('email')
                    user_name = email.get('name')
                    chat_id = get_chatId()
                    user_id = get_userid(user_email)
                    send_messages_two_day(user_id, chat_id, user_email, user_name, store_book)
        for store in stores:
            for email in emails:
                if email.get('name') == store.sale_name:
                    user_email = email.get('email')
                    user_name = email.get('name')
                    chat_id = get_chatId()
                    user_id = get_userid(user_email)
                    send_messages_two_day(user_id, chat_id, user_email, user_name, store)
        infoLogger.log("发送提前两天拜访任务执行成功")
    except:
        errLogger.log("发送提前两天拜访任务执行失败")


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


def send_messages(userID, chatID, email, name, store):
    try:
        infoLogger.log("__month_send_messages 发送预约消息开始" + name)
        if store.store_name == "null":
            store.store_name = ""
        if store.store == "null":
            store.store = ""
        if store.sales == "null":
            store.sales = ""
        data1 = {
            "chat_id": chatID,
            "user_id": userID,
            "msg_type": "text",
            "content": {
                "text": str(name) + "，早上好！您预约今天拜访" + str(store.store_name) + str(store.store) + str(store.sales) +
                        "门店，拜访目的为" + str(store.goal) + "，请准时到访。"
            }
        }
        token = get_token()
        headers_group = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        url_mess = "https://open.feishu.cn/open-apis/message/v4/send/"
        requests.post(url_mess, json=data1, headers=headers_group)
        infoLogger.log("__month_send_messages" + str(name) + " 发送预约消息成功")
    except:
        errLogger.log("send_messages  发送消息失败")


def send_messages_yesterday(userID, chatID, email, name, store):
    try:
        infoLogger.log("__month_send_messages 发送提前一天消息开始" + name)
        if store.store_name == "null":
            store.store_name = ""
        if store.store == "null":
            store.store = ""
        if store.sales == "null":
            store.sales = ""
        data1 = {
            "chat_id": chatID,
            "user_id": userID,
            "msg_type": "text",
            "content": {
                "text": str(name) + "，早上好！您预约明天拜访" + str(store.store_name) + str(store.store) + str(store.sales) +
                        "门店，拜访目的为" + str(store.goal) + "，请准时到访。"
            }
        }
        token = get_token()
        headers_group = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        url_mess = "https://open.feishu.cn/open-apis/message/v4/send/"
        requests.post(url_mess, json=data1, headers=headers_group)
        infoLogger.log("__month_send_messages" + str(name) + " 发送提前一天消息成功")
    except:
        errLogger.log("send_messages  发送提前一天消息失败")


def send_messages_two_day(userID, chatID, email, name, store):
    try:
        infoLogger.log("__month_send_messages 发送提前两天消息开始" + name)
        if store.store_name == "null":
            store.store_name = ""
        if store.store == "null":
            store.store = ""
        if store.sales == "null":
            store.sales = ""
        data1 = {
            "chat_id": chatID,
            "user_id": userID,
            "msg_type": "text",
            "content": {
                "text": str(name) + "，早上好！您预约后天拜访" + str(store.store_name) + str(store.store) + str(store.sales) +
                        "门店，拜访目的为" + str(store.goal) + "，请准时到访。"
            }
        }
        token = get_token()
        headers_group = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
        url_mess = "https://open.feishu.cn/open-apis/message/v4/send/"
        requests.post(url_mess, json=data1, headers=headers_group)
        infoLogger.log("__month_send_messages" + str(name) + " 发送提前两天消息成功")
    except:
        errLogger.log("send_messages  发送提前两天消息失败")


def confirm_address(address):
    if address is not None:
        data = query_is_exist()
        data.insert(0,'user')
        print(data)
        find = [address]
        find.insert(0,'name')
        print(find)
            # 遍历该列表
        with open("mdjcxx.csv", 'r+', encoding='gbk') as users:
            users.truncate()
            for i in data:
                print(i)
                # 以append的方式不断写入到csv文件中
                # 写入文件时增加换行符，保证每个元素位于一行
                users.write(str(i) + '\n')
        with open("new.csv", 'r+', encoding='gbk') as names:
            names.truncate()
            for i in find:
                print(i)
                # 写入文件时增加换行符，保证每个元素位于一行
                names.write(str(i) + '\n')
        data = pd.read_csv(r"mdjcxx.csv",encoding='gbk')
        find = pd.read_csv(r"new.csv",encoding='gbk')
        data_split_word = data.user.apply(jieba.lcut)
        dictionary = corpora.Dictionary(data_split_word.values)
        data_corpus = data_split_word.apply(dictionary.doc2bow)
        trantab = str.maketrans("0123456789", "零一二三四五六七八九")
        find_corpus = find.name.apply(
            lambda x: dictionary.doc2bow(jieba.lcut(x.translate(trantab))))

        tfidf = models.TfidfModel(data_corpus.to_list())
        index = similarities.SparseMatrixSimilarity(
                tfidf[data_corpus], num_features=len(dictionary))
        result = []
        for corpus in find_corpus.values:
            sim = pd.Series(index[corpus])
            print(sim.nlargest(1).values)
            if sim.nlargest(1).values >= 0.75:
                result.append(data.user[sim.nlargest(1).index].values)
            else:
                continue
        result = pd.DataFrame(result)
            # result.rename(columns=lambda i: f"匹配{i + 1}", inplace=True)
        result = pd.concat([result], axis=1)
        result.head(30)
        print(result)
        return result
    else:
        return None
