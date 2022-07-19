# 用于生成flask response
import flask.wrappers
from flask import make_response, jsonify

key_result = "结果"

value_success = "成功！"
value_failure = "发生错误！"


def response_success() -> flask.wrappers.Response:
    """
    回复一个标准的‘成功’信息。

    :return:
    """
    return make_response(jsonify({key_result: value_success}))


def response_failure() -> flask.wrappers.Response:
    """
    回复一个标准的‘失败’信息。

    :return:
    """
    return make_response(jsonify({key_result: value_failure}))


def response_with_msg(msg: str) -> flask.wrappers.Response:
    """
    回复一个带有自定义消息的信息。

    :param msg: str
    :return:
    """
    return make_response(jsonify({key_result: msg}))
