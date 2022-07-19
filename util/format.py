# 用于各种原始数据格式之间的转换（主要是字符串转为其他类型，和其他类型转为字符串）
from typing import Tuple, Dict


def extract_ym(formatted_date: str) -> Tuple[int, int]:
    """
    从形如‘2022-06-09 00:00:00’的日期字符串中提取年，月。如果字符串不符合格式则会出错！

    :param formatted_date: str
    :return: Tuple[int, int]
    """
    r = [0, 0]
    idx = 0
    s = ""
    for c in formatted_date:
        if "0" <= c <= "9":
            s += c
        else:
            r[idx] = int(s)
            idx += 1
            if idx == len(r):
                break
    return r[0], r[1]


def ym_to_str(year: int, month: int, sep: str = "-", add_zero: bool = True) -> str:
    """
    将年月日转换成形如‘2022-06-09’的形式。

    :param year: 年
    :param month: 月
    :param sep: 连接符合，默认为'-'
    :param add_zero: 是否在一位整数前添加0，默认为True
    :return: str
    """
    r = str(year) + sep
    if month < 10:
        if add_zero:
            r = r + "0"
    return r + str(month)


def extract_ym_from_int(year_month: int) -> Tuple[int, int]:
    """
    从形如202206的整数中抽取出年份2022和月份6.

    :param year_month: int
    :return: int
    """
    return year_month // 100, year_month % 100


def ym_to_int(year: int, month: int) -> int:
    """
    e.g., 将年份2022和月份6合并成整数202206.

    :param year: int
    :param month: int
    :return: int
    """
    return year * 100 + month


def combine_dict(d1: Dict[str, int], d2: Dict[str, int]) -> Dict[str, int]:
    """
    相加两个字典中可以相加的部分。比如，{"a": 1, "b": 2} 和 {"a": 3, "c": 6} 的结果是 {"a": 4, "b": 2, "c": 6}.

    它改变第一个字典，并返回改变后的第一个字典。

    :param d1: Dict[str, int]
    :param d2: Dict[str, int]
    :return: Dict[str, int]
    """
    for s, n in d2.items():
        if s in d1:
            d1[s] += n
        else:
            d1[s] = n
    return d1
