from datetime import datetime


import config
from flask import Flask
import biz_logic

# 创建一个Flask app对象
from init import scheduler
from util.request_hander.store_record import send_message_book

app = Flask(__name__)

# 加载初始化设置
app.config.from_object(config)

# 登记蓝图，于是这个app可以作为一个web server生效
app.register_blueprint(biz_logic.bp)

def add_book_time(book_time,book_year,book_month,book_day):
    scheduler.add_job(func=send_message_book, id=str(book_time),
                      trigger='date', run_date=datetime(book_year, book_month, book_day,
                                                        15, 38, 0))

# 自动运行这个app
if __name__ == '__main__':
    scheduler.init_app(app=app)
    scheduler.start()
    app.run(host='0.0.0.0',port=3392)
