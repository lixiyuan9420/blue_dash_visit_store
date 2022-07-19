from typing import List

from db.operation.store import StoreRecord


def __extract_store_record(data_json) -> StoreRecord:
    data = data_json["门店拜访记录"]
    is_book = data["是否预约"]
    book_time = data["预约日期"]
    sale_id = data["销售编号"]
    goal = data["拜访目的"]
    store = data["`门店/经销商`"]
    store_name = data["`门店/经销商名称`"]
    store_phone_name = data["`门店/经销商联系人名称`"]
    store_phone = data["`门店/经销商电话`"]
    store_address = data["`门店/经销商地址`"]
    time = data["拜访日期"]
    result = data["拜访结果"]
    next_time = data["下次拜访日期"]
    part = data["部门"]
    sale_name = data["成员"]
    return StoreRecord(is_book,book_time,sale_id,goal,store,store_name,
                       store_phone_name,store_phone,store_address,time,result,
                       next_time,part,sale_name)