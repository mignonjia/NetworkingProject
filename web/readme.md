## Health Information Management System

使用python3+virtualenv，其他的依赖在`requirements.txt`中列出。

目录结构：

```
├── web
       ├── app
       ├── instance
       ├── migrations
       ├── venv
       ├── config.py
       ├── requirements.txt
       └── run.py
```

1.配置virtualenv环境

```
# cd <my_path>\web
> virtualenv venv #新建环境，名字为venv
> .\venv\Scripts\activate 
> pip install -r requirements.txt #安装对应的包
```

2.新建MySQL数据库：

```
> mysql -u root -p
mysql> CREATE USER 'dt_admin'@'localhost' IDENTIFIED BY 'dt2020';

mysql> CREATE DATABASE dbtest;

mysql> GRANT ALL PRIVILEGES ON dbtest . * TO 'dt_admin'@'localhost';

```

如果修改了管理员用户名/密码/数据库名，需要修改`instance\config.py`。目前的config为：

```
SQLALCHEMY_DATABASE_URI = 'mysql://dt_admin:dt2020@localhost/dbtest'
```

导入数据库：

```
mysql -u root -p dbtest < database_dump.txt #导入已有的数据库
```

导出数据库：

```
mysqldump -u root -p dbtest > database_dump.txt #导出
```



3.启动。

如果是Windows系统，打开cmd，依次执行：

```
set FLASK_CONFIG=development
set FLASK_APP=run.py
```

如果是Linux/Mac系统，打开bash按如下操作

```
$export FLASK_CONFIG=development
$export FLASK_APP=run.py
```



```
flask db init
flask db migrate
flask db upgrade

```

**update**: 可以不设置`FLASK_CONFIG`和`FLASK_APP`,直接使用`python run.py`运行

update: 用设置`FLASK_CONFIG`和`FLASK_APP`的方法更加规范，而且方便区分开发部署。


如果在Migrate阶段报错`ERROR [root] Error: Can't locate revision identified by '0066c544c2f8'           `, 那么需要把dbtest中的版本信息删除。

```
>mysql -u root -p
use dbtest;
drop table alembic_version;
```

对模型的任何修改，都要再执行flask db migrate, flask db upgrade. 

添加管理员账户：

```
>flask shell

from app.models import Patient
from app import db
admin = Patient(phone_number="00000000000",username="admin",password="admin2016",is_admin=True)
db.session.add(admin)
db.session.commit()
```

最后，运行

```
flask run
```

在浏览器打开`localhost:5000`访问网页。

最后，运行`flask run`，在浏览器打开`localhost:5000`访问网页。



### 服务器部署

`ssh root@60.205.255.187`登录服务器,密码为`Networking2020`

项目位于`/var/www/web`目录中

nginx配置文件位于`/etc/nginx/sites-enabled/default`

uwsgi配置文件位于`/var/www/web/config.ini`