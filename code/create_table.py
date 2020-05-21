import pymysql

DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = 'password' #这里一定一定一定换成你设置的password，可以为了方便设置成password
DBNAME = 'dbtest' #这里一定一定要换成你设置的database名字，可以为了方便设置成dbtest，否则跑其他代码可能出错

try:
    db = pymysql.connect(DBHOST, DBUSER, DBPASS, DBNAME) 
    cur = db.cursor()
    cur.execute('DROP TABLE IF EXISTS user')
    sqlQuery = "CREATE TABLE user(user CHAR(20), password CHAR(20))"
    cur.execute(sqlQuery)
    print('表格创建成功!')
except pymysql.Error as e:
    print('数据库连接失败'+str(e))