last updated 2022 - 6 - 29

#schema

数据表图式。

## 门店拜访记录

### 门店拜访记录

    create table `门店拜访记录` (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        `是否预约` varchar(5),
        `预约日期` Date,
        `销售编号` varchar(20),
        `拜访目的` varchar(20),
        `门店经销商` varchar(60),
        `门店/经销商名称` varchar(60),
        `门店/经销商联系人名称` varchar(20),
        `门店/经销商电话` varchar(60),
        `门店/经销商地址` varchar(60),
        `拜访日期` Date,
        `拜访结果` varchar(255),
        `下次拜访日期` Date,
        `部门` varchar(20),
        `成员` varchar(20),
    );