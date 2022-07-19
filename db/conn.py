# 从连接池获取连接与返还连接
from db.pool import Pool
from logger.logger import infoLogger


def get_db():
    """
    从连接池获得一个数据库连接和它的cursor对象。不要忘记使用close_db()！

    :return: 数据库连接
    """
    connection = Pool.connection()
    cursor = connection.cursor()
    infoLogger.log("get_db() 打开数据库连接")
    return connection, cursor


def close_db(connection, cursor) -> None:
    """
    将当前的数据库连接还给连接池。

    :param connection: 数据库连接
    :param cursor: 该数据库的cursor对象
    :return: None
    """
    cursor.close()
    connection.close()
    infoLogger.log("close_db() 返还数据库连接")
