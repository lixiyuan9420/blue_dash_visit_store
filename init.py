from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler

scheduler = APScheduler(scheduler=BackgroundScheduler(timezone='Asia/Shanghai'))
