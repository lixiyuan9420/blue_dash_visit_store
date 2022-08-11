from typing import Tuple, List

from db.operation.store import StoreRecord
from db.standard import standard_update, standard_query

insertion_store_record = "insert into 门店拜访记录(是否预约,预约日期,销售编号,拜访目的,`门店`,`经销商`,`门店经销商名称`,`门店/经销商联系人名称`," \
                         "`门店/经销商电话`,`门店/经销商地址`,拜访日期,拜访结果,下次拜访日期,部门,成员) " \
                         "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
query_store_record_prefix = "select * from 门店拜访记录"
condition_query_store_record = "where to_days(预约日期)=to_days(now()) and 是否预约='是';"
condition_query_store_record_1 = "where to_days(下次拜访日期) = to_days(now());"
condition_query_store_record_yesterday = "where to_days(now())-to_days(预约日期)=1"
condition_query_store_record_yesterday_1 = "where to_days(now())-to_days(下次拜访日期)=1"
condition_query_store_record_two_day = "where to_days(now())-to_days(预约日期) = 2"
condition_query_store_record_two_day_1 = "where to_days(now())-to_days(下次拜访日期)=2"
condition_query_is_exist_store = "where 门店 = %s and 经销商 = %s and 成员 = %s"


def insert_store_contract(store_record: StoreRecord) -> bool:
    """
    将一条新的门店拜访插入数据库中。会返回是否成功。
    :param store_record: StoreRecord 门店拜访记录
    :return: bool
    """
    sql = insertion_store_record
    return standard_update(sql, store_record.generate_tuple())


def __query_store_record(condition: str, params: Tuple = ()) -> List[StoreRecord]:
    """
    根据条件查询门店拜访记录(去重)
    :param condition:
    :param params:
    :return:
    """
    r = []
    sql = query_store_record_prefix + " " + condition
    tuples = standard_query(sql, params)
    if tuples is None:
        raise ValueError("standard_query() returns None")
    for the_tuple in tuples:
        r.append(StoreRecord(*the_tuple[1:], data_id=the_tuple[0]))
    return r


def query_store_record() -> List[StoreRecord]:
    """
    查询某销售的本周的门店拜访记录
    :param name:销售名字
    :return:列表
    """
    return __query_store_record(condition_query_store_record, ())


def __query_store_record_1(condition: str, params: Tuple = ()) -> List[StoreRecord]:
    """
    根据条件查询门店拜访记录(去重)
    :param condition:
    :param params:
    :return:
    """
    r = []
    sql = query_store_record_prefix + " " + condition
    tuples = standard_query(sql, params)
    if tuples is None:
        raise ValueError("standard_query() returns None")
    for the_tuple in tuples:
        r.append(StoreRecord(*the_tuple[1:], data_id=the_tuple[0]))
    return r


def query_store_record_1() -> List[StoreRecord]:
    """
    查询某销售的本周的门店拜访记录(去重)
    :param name:销售名字
    :return:列表
    """
    return __query_store_record(condition_query_store_record_1, ())


def __query_store_record_yesterday(condition: str, params: Tuple = ()) -> List[StoreRecord]:
    """
    根据条件查询门店拜访记录(去重)
    :param condition:
    :param params:
    :return:
    """
    r = []
    sql = query_store_record_prefix + " " + condition
    tuples = standard_query(sql, params)
    if tuples is None:
        raise ValueError("standard_query() returns None")
    for the_tuple in tuples:
        r.append(StoreRecord(*the_tuple[1:], data_id=the_tuple[0]))
    return r


def query_store_record_yesterday() -> List[StoreRecord]:
    """
    查询某销售的本周的门店拜访记录
    :param name:销售名字
    :return:列表
    """
    return __query_store_record(condition_query_store_record_yesterday, ())


def __query_store_record_yesterday_1(condition: str, params: Tuple = ()) -> List[StoreRecord]:
    """
    根据条件查询门店拜访记录(去重)
    :param condition:
    :param params:
    :return:
    """
    r = []
    sql = query_store_record_prefix + " " + condition
    tuples = standard_query(sql, params)
    if tuples is None:
        raise ValueError("standard_query() returns None")
    for the_tuple in tuples:
        r.append(StoreRecord(*the_tuple[1:], data_id=the_tuple[0]))
    return r


def query_store_record_yesterday_1() -> List[StoreRecord]:
    """
    查询某销售的本周的门店拜访记录(去重)
    :param name:销售名字
    :return:列表
    """
    return __query_store_record(condition_query_store_record_yesterday_1, ())


def __query_store_record_two_day(condition: str, params: Tuple = ()) -> List[StoreRecord]:
    """
    根据条件查询门店拜访记录(去重)
    :param condition:
    :param params:
    :return:
    """
    r = []
    sql = query_store_record_prefix + " " + condition
    tuples = standard_query(sql, params)
    if tuples is None:
        raise ValueError("standard_query() returns None")
    for the_tuple in tuples:
        r.append(StoreRecord(*the_tuple[1:], data_id=the_tuple[0]))
    return r


def query_store_record_two_day() -> List[StoreRecord]:
    """
    查询某销售的本周的门店拜访记录
    :param name:销售名字
    :return:列表
    """
    return __query_store_record(condition_query_store_record_yesterday, ())


def __query_store_record_two_day_1(condition: str, params: Tuple = ()) -> List[StoreRecord]:
    """
    根据条件查询门店拜访记录(去重)
    :param condition:
    :param params:
    :return:
    """
    r = []
    sql = query_store_record_prefix + " " + condition
    tuples = standard_query(sql, params)
    if tuples is None:
        raise ValueError("standard_query() returns None")
    for the_tuple in tuples:
        r.append(StoreRecord(*the_tuple[1:], data_id=the_tuple[0]))
    return r


def query_store_record_two_day_1() -> List[StoreRecord]:
    """
    查询某销售的本周的门店拜访记录(去重)
    :param name:销售名字
    :return:列表
    """
    return __query_store_record(condition_query_store_record_yesterday_1, ())


def query_is_exist(store,sale,name):
     """
     查询是否存在
     :return:
     """
     return  __query_is_exist(condition_query_is_exist_store,(store,sale,name))


def __query_is_exist(condition:str,params :Tuple = ()) -> List[StoreRecord]:
    """
    查询是否存在
    :param condition:
    :param params:
    :return:
    """
    r = []
    sql = query_store_record_prefix + " " + condition
    tuples = standard_query(sql, params)
    if tuples is None:
        raise ValueError("standard_query() returns None")
    for the_tuple in tuples:
        r.append(StoreRecord(*the_tuple[1:], data_id=the_tuple[0]))
    return r
