# flask
import flask.wrappers
from flask import (
    Blueprint, request
)
from flask_cors import CORS

# log
from logger.logger import infoLogger, errLogger
from util.request_hander.common import verify_auth_token

from util.request_hander.store_record import __extract_store_record
from util.response_handler import (
    response_success, response_failure
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
    插入一个新的门店合同。

    :return: flask.wrappers.Response:
    """
    try:
        infoLogger.log("/store/new_store_record 开始")
        new_record = __extract_store_record(request.get_json())
        print(new_record.generate_tuple())
        infoLogger.log(request.get_json())
        success = store_sql.insert_store_contract(new_record)
        infoLogger.log("/store/new_store_record success: " + str(success), line_below=True)
        return __quick_response(success)
    except Exception as e:
        __log_err(e, request)
        return response_failure()
