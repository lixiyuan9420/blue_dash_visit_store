import pymysql
from dbutils.pooled_db import PooledDB


# 一些常量
mysql_username = "bluedash"
mysql_host_name = "localhost"
mysql_host_password = "BLUEYOUUP"
mysql_port_number = 3306
mysql_database_name_1 = "总数据库"

# 连接池
Pool = PooledDB(
    creator=pymysql,
    maxconnections=5,
    mincached=1,
    maxcached=4,
    blocking=True,
    maxusage=None,
    ping=1,
    host=mysql_host_name,
    user=mysql_username,
    port=mysql_port_number,
    password=mysql_host_password,
    database=mysql_database_name_1
)