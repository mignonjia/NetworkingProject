import pymysql
from werkzeug.security import generate_password_hash

DBHOST = 'localhost'
DBUSER = 'dt_0409_admin' #管理员账户
DBPASS = 'dt2020' #设置的password
DBNAME = 'my_database' #设置的database名字

    
try:
    db = pymysql.connect(DBHOST, DBUSER, DBPASS, DBNAME) 
    cursor = db.cursor()
    
    sql = "INSERT INTO departments (name, description) VALUES (%s, %s)"
    data = [
        ("OPR", "office of professional responsibility."),
        ("White Collar", "An elite group in FBI, catching white collar criminals."),]
    cursor.executemany(sql, data)
    db.commit()
    sql = "INSERT INTO roles (name, description) VALUES (%s, %s)"
    data = [
        ("S.A.", "senior agent"),
        ("C.I.", "criminal intelligent"),
        ("Agent", "Agent")]
    cursor.executemany(sql, data)
    db.commit()
    
    sql = "INSERT INTO employees " \
        "(email, username, first_name, last_name, password_hash, " \
        "department_id, role_id, age, gender, health_status) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data = [
        ("neal@wc.fbi", "CharmingSmile", "Neal", "Caffrey", generate_password_hash("Rat"), 2, 2, 30, "male", "Normal"),
        ("peter@wc.fbi", "Suit", "Peter", "Burke", generate_password_hash("Suit"), 2, 1, 32, "male", "Normal"),
        ("diana@wc.fbi", "Diana", "Diana", "Berrigan", generate_password_hash("Womansuit"), 2, 1, 32, "female", "Normal"),
        ("fowler@opr.us", "ManWithTheRing", "Garrett", "Fowler", generate_password_hash("MusicBox"), 1, 3, 40, "male", "Confirmed Case"),
        ]
    cursor.executemany(sql, data)
    db.commit()
    cursor.close()
    db.close()
    
    
    print('表格创建成功!')
except pymysql.Error as e:
    print('数据库连接失败'+str(e))
    

'''
# 批量
# 导入pymysql模块
import pymysql
# 连接database
conn = pymysql.connect(host=“你的数据库地址”, user=“用户名”,password=“密码”,database=“数据库名”,charset=“utf8”)
# 得到一个可以执行SQL语句的光标对象
cursor = conn.cursor()
sql = "INSERT INTO USER1(name, age) VALUES (%s, %s);"
data = [("Alex", 18), ("Egon", 20), ("Yuan", 21)]
try:
    # 批量执行多条插入SQL语句
    cursor.executemany(sql, data)
    # 提交事务
    conn.commit()

except Exception as e:
    # 有异常，回滚事务
    conn.rollback()
cursor.close()
conn.close()
'''
