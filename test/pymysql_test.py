import pymysql

db = pymysql.connect(host='localhost', user='root', passwd='241429', database='testdb')

cursor = db.cursor()

# SQL 插入语句
sql = "INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) \
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"
try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except Exception:
    # 如果发生错误则回滚
    db.rollback()

db.close()
