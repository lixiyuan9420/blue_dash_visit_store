# flask
import flask.wrappers
from flask import (
    Blueprint, request
)
from flask_cors import CORS

# log
from logger.logger import infoLogger, errLogger
from util.request_hander.common import verify_auth_token

from util.request_hander.store_record import __extract_store_record, extract_store_is_exist
from util.response_handler import (
    response_success, response_failure, response_with_msg
)

# db operation
from db.operation import store_sql

# service

# 创建一个蓝图
bp = Blueprint('biz_logic', __name__)
# 允许跨域请求
cors = CORS(bp)


def __log_err(e: Exception, req: request):
    """
    在发生错误时将错误写入日志中。

    :param e: Exception
    :param req: request
    :return: None
    """
    errLogger.log("request:")
    errLogger.log(req)
    errLogger.log(e, enable_traceback=True, line_below=True)
    infoLogger.log("发生错误", line_below=True)


def __quick_response(success: bool) -> flask.wrappers.Response:
    """
    回复最简单的成功或失败。

    :param success: bool
    :return: flask.wrappers.Response:
    """
    if success:
        return response_success()
    else:
        return response_failure()


@bp.route("/mock_verification", methods=["POST"])
def mock_verification() -> flask.wrappers.Response:
    """
    一个虚假的路径，用来模拟身份验证。

    :return: flask.wrappers.Response
    """
    try:
        infoLogger.log("/mock_verification 开始")
        verify_auth_token(request.get_json())
        response = response_success()
        infoLogger.log("/mock_verification 完成", line_below=True)
        return response
    except Exception as e:
        __log_err(e, request)
        return response_failure()


# for sending new data

@bp.route("/store/new_store_record", methods=["POST"])
def new_store_contract() -> flask.wrappers.Response:
    """
    插入一个新的门店拜访记录。

    :return: flask.wrappers.Response:
    """
    try:
        infoLogger.log("/store/new_store_record 开始")
        new_record = __extract_store_record(request.get_json())
        infoLogger.log(request.get_json())
        success = store_sql.insert_store_contract(new_record)
        infoLogger.log("/store/new_store_record success: " + str(success), line_below=True)
        return __quick_response(success)
    except Exception as e:
        __log_err(e, request)
        return response_failure()


@bp.route("/store/query_is_exist", methods=["POST"])
def query_is_exist_api() -> flask.wrappers.Response:
    """
    插入一个新的门店合同。

    :return: flask.wrappers.Response:
    """
    try:
        infoLogger.log("/store/query_is_exist 开始")
        record = extract_store_is_exist(request.get_json())
        infoLogger.log(record)
        infoLogger.log("/store/query_is_exist success: " + str(record), line_below=True)
        if record == 0:
            return response_with_msg("没有归属任何销售")
        elif record > 0:
            return response_with_msg("有销售正在跟进")
        elif record == -1:
            return response_with_msg("地址错误请检查地址")
    except Exception as e:
        __log_err(e, request)
        return response_failure()
