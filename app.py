from datetime import datetime


import config
from flask import Flask
import biz_logic

# 创建一个Flask app对象
from init import scheduler
from util.request_hander.store_record import send_message_book, send_message_total

app = Flask(__name__)

# 加载初始化设置
app.config.from_object(config)

# 登记蓝图，于是这个app可以作为一个web server生效
app.register_blueprint(biz_logic.bp)

# 自动运行这个app
if __name__ == '__main__':
    scheduler.add_job(func=send_message_total,id='1', trigger='interval',days = 1,start_date = '2022-08-18 09:00:00')
    scheduler.init_app(app=app)
    scheduler.start()
    app.run(host='0.0.0.0',port=3392)
