from db.operation.store import StoreRecord
from db.standard import standard_update

insertion_store_record = "insert into 门店拜访记录(是否预约,预约日期,销售编号,拜访目的,`门店`,`经销商`,`门店经销商名称`,`门店/经销商联系人名称`," \
                         "`门店/经销商电话`,`门店/经销商地址`,拜访日期,拜访结果,下次拜访日期,部门,成员) " \
                         "values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


def insert_store_contract(store_record: StoreRecord) -> bool:
    """
    将一条新的门店拜访插入数据库中。会返回是否成功。

    :param store_record: StoreRecord 门店拜访记录
    :return: bool
    """
    sql = insertion_store_record
    return standard_update(sql, store_record.generate_tuple())