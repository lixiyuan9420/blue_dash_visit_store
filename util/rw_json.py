from json import load
from typing import Dict


def read_json(filename: str) -> Dict:
    """
    读取一个JSON文件并返回相应的结构体。

    :param filename: str
    :return: Dict
    """
    with open(filename, 'r', encoding="UTF-8") as f:
        return load(f)
