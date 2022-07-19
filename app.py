import config
from flask import Flask
import biz_logic

# 创建一个Flask app对象
app = Flask(__name__)

# 加载初始化设置
app.config.from_object(config)

# 登记蓝图，于是这个app可以作为一个web server生效
app.register_blueprint(biz_logic.bp)

# 自动运行这个app
if __name__ == '__main__':
    app.run()
