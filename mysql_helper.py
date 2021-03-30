import pymysql


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
        try:
            conn = pymysql.Connect(host=self.host, user=self.user, passwd=self.pwd, database=self.db)
            return conn
        except Exception as e:
            self.state = False
            print('数据库连接异常：', e)

    def query(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            return data
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            # self.conn.close()

    def update(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            # self.conn.close()

    def close(self):
        self.conn.close()
