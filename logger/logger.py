import logging
import traceback
import os
from typing import Optional
from datetime import datetime

# 设置2个可供其他包引用的logger类，分别用作不同的用途并写入不同的文件
# 是否打开日志；默认为是（在测试期间可以为否，其他时间都应该为是）
turn_on_logging = True

# 分界线，用于区分日志的不同部分
line_mark = "------------------------------------------------------------------------"
log_file_size = 204800    # in bytes = 200 kb
log_file_appendix = ".log"


def __random_log_name(old_name: str) -> str:
    """
    根据当前时间重命名日志文件，必须保证旧文件名是形如 ../../log.log 的形式，即最后四个字符必须是 .log

    :param old_name: str
    :return: str
    """
    cur = str(datetime.utcnow()).replace(":", "-")
    try:
        return old_name[:-4] + cur + log_file_appendix
    except Exception as e:
        print(e)
        return cur + log_file_appendix


def create_new_log_file(filename: str):
    """
    重命名日志文件，并创建一个新的（这个会在.log()时自动发生，因此不在这里完成）。

    :param filename: str
    :return: None
    """
    new_log_name = __random_log_name(filename)
    os.rename(filename, new_log_name)


def file_too_big(filename: str) -> bool:
    """
    检查当前日志文件是否过大

    :param filename: str
    :return: bool
    """
    try:
        size = os.path.getsize(filename)
    except OSError:
        size = 0

    if size > log_file_size:    # 文件过大
        return True
    return False


class __Logger:
    """
    自定义的日志类。
    """

    def __init__(self, logger_name: str, log_level: int, output_file: str):
        """
        自定义的日志类。

        :param logger_name: str 这个logger的名称，必须唯一
        :param log_level: int 日志等级（如logging.INFO）
        :param output_file: str 输出日志文件的路径
        """
        the_logger = logging.getLogger(logger_name)
        the_logger.setLevel(log_level)
        self.logger = the_logger
        self.default_level = log_level
        self.output_file = output_file
        self.__refresh_handler()
        self.active = True

    def turn_off(self):
        """
        暂时停止写入日志，但不会关闭日志文件。

        :return: None
        """
        self.active = False

    def turn_on(self):
        """
        开始写入日志。

        :return: None
        """
        self.active = True

    def __get_handler(self) -> logging.FileHandler:
        """
        返回一个自动配置的handler对象

        :return: logging.FileHandler
        """
        the_handler = logging.FileHandler(self.output_file, encoding="UTF-8")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        the_handler.setFormatter(formatter)
        return the_handler

    def __remove_handler(self) -> None:
        """
        自动清除handler对象
        """
        self.logger.removeHandler(self.handler)
        self.handler.close()

    def __refresh_handler(self) -> None:
        """
        重置handler
        """
        self.handler = self.__get_handler()
        self.logger.addHandler(self.handler)

    def log(self, msg, level: Optional[int] = None, enable_traceback: bool = False, line_below: bool = False):
        """
        记录日志。

        :param msg: Any
        :param level: int 默认为None，即使用日志类本身的级别。可以手动指定。
        :param enable_traceback: bool 是否显示traceback
        :param line_below: bool 是否在结尾处添加一条分界线
        :return: None
        """
        if self.active:
            if file_too_big(self.output_file):
                # 清空旧log
                self.__remove_handler()
                create_new_log_file(self.output_file)
                self.__refresh_handler()
            if level is None:
                level = self.default_level
            if enable_traceback:
                self.logger.log(level, traceback.format_exc())
            if turn_on_logging:
                self.logger.log(level, msg)
            if line_below:
                self.logger.log(level, line_mark)


# 清除根logger的handle使得我们的自定义logger可以正常运行
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# 两个用来给其他包引用的单例
infoLogger = __Logger("info_12345", logging.INFO, "log_info.log")
errLogger = __Logger("err_12345", logging.ERROR, "log_err.log")
bonusCalculationLog = __Logger("bonus_cal_12345", logging.INFO, "log_bonus_cal.log")
