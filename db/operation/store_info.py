from typing import Tuple


class StoreBasicInfo:
    """
    门店基础信息。

    Attributes:
        store_id: 客户唯一识别码
        apply_date: 申请日期
        store_type: 渠道类型
        store_name: 门店名称
        store_status: 门店状态
        province: 省/直辖市名称
        city: 城市名称
        district: 市内行政区名称
        detailed_location: 门店地址
        salesman: 门店销售
        p1_id: 1p经销商代码
        p1_name: 1p经销商名称
        p2_id: 2p经销商代码
        p2_name: 2p经销商名称
        area: 面积
        tables: 桌数
        booth: 包厢/卡座
        average_consumption: 人均消费
    """

    def __init__(self, store_id: str, apply_date: str, store_type: str, store_name: str, store_status: str,
                 province: str, city: str, district: str, detailed_location: str, salesman: str,
                 p1_id: str, p1_name: str, p2_id: str, p2_name: str,
                 area: str, tables: int, booth: int, average_consumption: int, data_id: int = -1):
        """
        门店基础信息。

        :param store_id: 客户唯一识别码
        :param apply_date: 申请日期
        :param store_type: 渠道类型
        :param store_name: 门店名称
        :param store_status: 门店状态
        :param province: 省/直辖市名称
        :param city: 城市名称
        :param district: 市内行政区名称
        :param detailed_location: 门店地址
        :param salesman: 门店销售
        :param p1_id: 1p经销商代码
        :param p1_name: 1p经销商名称
        :param p2_id: 2p经销商代码
        :param p2_name: 2p经销商名称
        :param area: 面积
        :param tables: 桌数
        :param booth: 包厢/卡座
        :param average_consumption: 人均消费
        :param data_id: 这条记录在数据库里的id，通常不用, 默认-1
        """
        self.store_id = store_id
        self.apply_date = apply_date
        self.store_type = store_type
        self.store_name = store_name
        self.store_status = store_status
        self.province = province
        self.city = city
        self.district = district
        self.detailed_location = detailed_location
        self.salesman = salesman
        self.p1_id = p1_id
        self.p1_name = p1_name
        self.p2_id = p2_id
        self.p2_name = p2_name
        self.area = area
        self.tables = tables
        self.booth = booth
        self.average_consumption = average_consumption
        self.data_id = data_id

    def generate_tuple(self) -> Tuple:
        """
        返回一个用于插入新记录的有序元组。
        （客户唯一识别码,申请日期,渠道类型,门店名称,门店状态,省/直辖市名称,城市名称,市内行政区名称,门店地址,
        门店销售,1p经销商代码,1p经销商名称,2p经销商代码,2p经销商名称,面积,桌数,包厢/卡座,人均消费）

        :return: Tuple
        """
        return (self.store_id, self.apply_date, self.store_type, self.store_name, self.store_status,
                self.province, self.city, self.district, self.detailed_location, self.salesman,
                self.p1_id, self.p1_name, self.p2_id, self.p2_name,
                self.area, self.tables, self.booth, self.average_consumption)