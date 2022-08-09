# create table `门店拜访记录` (
#         id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
#         `是否预约` varchar(5),
#         `预约日期` Date,
#         `销售编号` varchar(20),
#         `拜访目的` varchar(20),
#         `门店` varchar(60),
#         `经销商` varchar(60),
#         `门店经销商名称` varchar(60),
#         `门店/经销商联系人名称` varchar(20),
#         `门店/经销商电话` varchar(60),
#         `门店/经销商地址` varchar(100),
#         `拜访日期` Date,
#         `拜访结果` varchar(255),
#         `下次拜访日期` Date,
#         `部门` varchar(20),
#         `成员` varchar(20)
#     );
from typing import Tuple

from pymysql import Date


class StoreRecord:
    """
    拜访记录

    Attributes:
        is_book:是否预约
        book_time:预约日期
        sale_id:销售编号
        goal:拜访目的
        store:门店
        sales:经销商
        store_name:门店/经销商名称
        store_phone_name:门店/经销商联系人名称
        store_phone:门店/经销商电话
        store_address:门店/经销商地址
        time:拜访日期
        result:拜访结果
        next_time:下次拜访日期
        part:部门
        sale_name:成员

    """

    def __init__(self, is_book: str, book_time: Date, sale_id: str, goal: str,
                 store: str, sales: str, store_name: str, store_phone_name: str, store_phone: str,
                 store_address: str, time: Date, result: str, next_time: Date, part: str, sale_name: str,
                 data_id: int = -1):
        """

        :param is_book: 是否预约
        :param book_time: 预约日期
        :param sale_id: 销售编号
        :param goal: 拜访目的
        :param store: 门店
        :param sales: 经销商
        :param store_name: 门店/经销商名称
        :param store_phone_name: 门店/经销商联系人名称
        :param store_phone: 门店/经销商电话
        :param store_address: 门店/经销商地址
        :param time: 拜访日期
        :param result: 拜访结果
        :param next_time: 下次拜访日期
        :param part: 部门
        :param sale_name: 成员
        :param data_id: 这条记录在数据库里的id，通常不用, 默认-1

        """
        self.is_book = is_book
        self.book_time = book_time
        self.sale_id = sale_id
        self.goal = goal
        self.store = store
        self.sales = sales
        self.store_name = store_name
        self.store_phone_name = store_phone_name
        self.store_phone = store_phone
        self.store_address = store_address
        self.time = time
        self.result = result
        self.next_time = next_time
        self.part = part
        self.sale_name = sale_name
        self.data_id = data_id

    def generate_tuple(self) -> Tuple:
        """

        :return:
        """
        return (self.is_book, self.book_time, self.sale_id, self.goal, self.store, self.sales, self.store_name,
                self.store_phone_name,
                self.store_phone, self.store_address, self.time, self.result, self.next_time, self.part, self.sale_name)
