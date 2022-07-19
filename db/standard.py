from typing import Tuple, Optional
from logger.logger import infoLogger, errLogger
from db.conn import get_db, close_db


def standard_query(sql: str, params: Tuple) -> Optional[Tuple[Tuple]]:
    """
    一个标准的查询过程，包含了数据库连接的打开和关闭。如果查询失败则返回None. 空的2维元组代表查询成功但数据库里没有相应数据。
    使用了parameter binding。

    :param sql: str
    :param params: Tuple
    :return: Optional[Tuple[Tuple]]
    """
    infoLogger.log(sql)
    if len(params) > 0:
        infoLogger.log(params)

    r = None
    try:
        connection, cursor = get_db()
    except Exception as e:
        raise e

    try:
        if len(params) == 0:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)
        r = cursor.fetchall()
    except Exception as e:
        errLogger.log(sql)
        errLogger.log(e, enable_traceback=True, line_below=True)
        # 在这里不return，因为一定要尝试关闭连接

    try:
        close_db(connection, cursor)
    except Exception as e:
        raise e

    return r


def standard_update(sql: str, params: Tuple) -> bool:
    """
    一个标准的插入/更新过程，包含了数据库连接的打开和关闭。假如成功则返回True.
    使用了parameter binding。

    :param sql: str
    :param params: Tuple
    :return: bool
    """
    infoLogger.log(sql)
    if len(params) > 0:
        infoLogger.log(params)

    try:
        connection, cursor = get_db()
    except Exception as e:
        raise e

    r = True
    try:
        if len(params) == 0:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)
        connection.commit()
    except Exception as e:
        errLogger.log(sql)
        errLogger.log(e, enable_traceback=True, line_below=True)
        r = False
        connection.rollback()
        # 在这里不return，因为一定要尝试关闭连接

    try:
        close_db(connection, cursor)
    except Exception as e:
        raise e

    return r
