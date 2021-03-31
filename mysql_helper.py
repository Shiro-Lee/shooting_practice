import pymysql
from pymysql.cursors import DictCursor


class MySQLHelper:
    """数据库连接类"""
    def __init__(self, host, user, pwd, db):
        self.host = host    # 数据库地址
        self.user = user    # 用户名
        self.pwd = pwd      # 密码
        self.db = db        # 数据库名
        self.state = True   # 连接状态
        self.conn = self.get_conn()

    def get_conn(self):
        """获取数据库连接"""
        try:
            conn = pymysql.Connect(host=self.host, user=self.user, passwd=self.pwd, database=self.db)
            return conn
        except Exception as e:
            self.state = False
            print('数据库连接异常：', e)

    def query_many(self, sql, num):
        """查询多条数据"""
        cursor = self.conn.cursor(DictCursor)
        try:
            cursor.execute(sql)
            data = cursor.fetchmany(num)
            return data
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def query_all(self, sql):
        """查询全部数据"""
        cursor = self.conn.cursor(DictCursor)
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            return data
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def query_one(self, sql):
        """查询单条数据"""
        cursor = self.conn.cursor(DictCursor)
        try:
            cursor.execute(sql)
            data = cursor.fetchone()
            return data
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def execute(self, sql):
        """执行"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)     # 异常回滚
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
        finally:
            cursor.close()

    def close(self):
        self.conn.close()
