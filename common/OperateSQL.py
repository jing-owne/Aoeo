# -*- coding: utf-8 -*-

import pymysql
import os
from Logger import EnhancedLogger
from ReadINI import ConfigINI

# 先创建实例，再调用方法
logger = EnhancedLogger()  # 实例化
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

data = ConfigINI()
config_handler = ConfigINI("../config/setting.ini")  # 修复路径
data = config_handler.load_ini()
logger.info(f'读取结果: {data}')

database_config = data.get('Database', {})
host = database_config.get('mysql_host')
print("读取结果:", host)




DB_CONF = {
    "host": conne['MYSQL_HOST'],
    "port": int(conne['MYSQL_PORT']),
    "user": conne['MYSQL_USER'],
    "password": conne['MYSQL_PASSWD'],
    "database": conne['MYSQL_DB'],
}




class MysqlOperate:
    def __init__(self, db_conf=DB_CONF):
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        self.conn.close()
        self.cursor.close()

    def select_db(self, sql):
        """ 查询 """
        # 检查连接是否断开，如果断开进行重连
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        # 使用fetchall()获取查询结果
        query_result = self.cursor.fetchall()
        logger.info(f'查询SQL：{sql},\n返回查询结果：{query_result}')
        return query_result

    def execute_db(self, sql):
        """更新 / 新增 / 删除"""
        try:
            # 检查是否断开，断开重连
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql)
            # 提交事物
            self.conn.commit()
        except Exception as e:
            logger.info(f'操作mysql出现错误，错误原因为：{e}')
            # 回滚所有更改
            self.conn.rollback()


db = MysqlOperate(DB_CONF)
# if __name__ == '__main__':
#     aa = db.select_db("SELECT * from t_user where user_id='35000598';")
#     print(aa)
    # bb = db.execute_db("DELETE FROM `lawson_db`.`t_user_coupon` WHERE `id` = 10052734")
    # if bb == None:
    #     print(f"执行结果{bb}，删除成功")

