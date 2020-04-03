# -*- coding:utf-8 -*-

from flask import Flask, render_template, flash, request,  redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import importlib,sys 
importlib.reload(sys)

app = Flask(__name__)

# 数据库配置: 数据库地址/关闭自动跟踪修改
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1/dbtest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'itheima'

# 创建数据库对象
db = SQLAlchemy(app)

'''
1. 配置数据库
    a. 导入SQLAlchemy扩展
    b. 创建db对象, 并配置参数
    c. 终端创建数据库
2. 添加用户和类型模型
    a. 模型继承db.Model
    b. __tablename__:表名
    c. db.Column:字段
    d. db.relationship: 关系引用
3. 添加数据
4. 使用模板显示数据库查询的数据
    a. 查询所有的类型信息, 让信息传递给模板
    b. 模板中按照格式, 依次for循环类型和用户即可 (类型获取用户, 用的是关系引用)
5. 使用WTF显示表单
    a. 自定义表单类
    b. 模板中显示
    c. secret_key / 编码 / csrf_token
6. 实现相关的增删逻辑
    a. 增加数据
    b. 删除用户  url_for的使用 /  for else的使用 / redirect的使用
    c. 删除类型 
'''


# 定义用户和类型模型
# 类型模型
class Title(db.Model):
    # 表名
    __tablename__ = 'titles'

    # 字段
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)

    # 关系引用
    # users是给自己(Title模型)用的, title是给User模型用的
    users = db.relationship('User', backref='title')

    def __repr__(self):
        return 'Title: %s' % self.name


# 用户模型
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True)
    gender = db.Column(db.String(2), unique=False)
    title_id = db.Column(db.Integer, db.ForeignKey('titles.id'))

    def __repr__(self):
        return 'User: %s %s' % (self.name, self.title_id)


# 自定义表单类
class TitleForm(FlaskForm):
    title = StringField('类型', validators=[DataRequired()])
    user = StringField('姓名', validators=[DataRequired()])
    gender = StringField('性别', validators=[DataRequired()])
    submit = SubmitField('提交')

class QueryForm(FlaskForm):
    query = StringField('姓名', validators=[DataRequired()])
    submit = SubmitField('提交')

class QueryTitleForm(FlaskForm):
    query_title = StringField('类型', validators=[DataRequired()])
    submit = SubmitField('提交')

@app.route('/back')
def back():
    return redirect(url_for('index'))

@app.route('/query_users', methods=['GET', 'POST'])
def query_users():
    query_form = QueryForm()
    if query_form.validate_on_submit():
        user_name = query_form.query.data
        user = User.query.filter_by(name=user_name).first()
        if user:
            flash('该用户存在', 'query')
            flash('类型为'+user.title.name+' 性别为'+user.gender, 'query')
        else:
            flash('该用户不存在', 'query')
    return render_template('user1.html', queryform = query_form)

@app.route('/query_titles', methods=['GET', 'POST'])
def query_titles():
    query_title_form = QueryTitleForm()
    if query_title_form.validate_on_submit():
        title_name = query_title_form.query_title.data
        title = Title.query.filter_by(name=title_name).first()
        if title:
            for user in title.users:
                flash(user.name, 'user')
        else:
            flash('不存在', 'error')
    return render_template('titles.html', queryform = query_title_form)

@app.route('/show_user/<user_name>', methods=['GET', 'POST'])
def show_user(user_name):
    s = 'user/'+user_name+'.html'
    return render_template('user/Alice.html')

# 删除类型
@app.route('/delete_title/<title_id>', methods=['GET', 'POST'])
def delete_title(title_id):

    # 查询数据库, 是否有该ID的类型, 如果有就删除(先删用户, 再删类型), 没有提示错误
    # 1. 查询数据库
    title = Title.query.get(title_id)

    # 2. 如果有就删除(先删用户, 再删类型)
    if title:
        try:
            # 查询之后直接删除
            User.query.filter_by(title_id=title_.id).delete()

            # 删除类型
            db.session.delete(title)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除用户出错')
            db.session.rollback()

    else:
        # 3. 没有提示错误
        flash('类型找不到')

    return redirect(url_for('index'))


# 删除用户 --> 网页中删除-->点击需要发送用户的ID给删除用户的路由 --> 路由需要接受参数
@app.route('/delete_user/<user_id>', methods=['GET', 'POST'])
def delete_user(user_id):

    # 1. 查询数据库, 是否有该ID的用户, 如果有就删除, 没有提示错误
    user = User.query.get(user_id)

    # 2. 如果有就删除
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除用户出错')
            db.session.rollback()

    else:
        # 3. 没有提示错误
        flash('用户找不到')

    # redirect: 重定向, 需要传入网络/路由地址
    # url_for('index'): 需要传入视图函数名, 返回改视图函数对应的路由地址
    print(url_for('index'))
    return redirect(url_for('index'))

    # 如何返回当前网址 --> 重定向
    # return redirect('www.itheima.com')
    # return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def index():
    # 创建自定义的表单类
    title_form = TitleForm()
    '''
    验证逻辑:
    1. 调用WTF的函数实现验证
    2. 验证通过获取数据
    3. 判断类型是否存在
    4. 如果类型存在, 判断用户是否存在, 没有重复用户就添加数据, 如果重复就提示错误
    5. 如果类型不存在, 添加类型和用户
    6. 验证不通过就提示错误
    '''

    # 1. 调用WTF的函数实现验证
    if title_form.validate_on_submit():

        # 2. 验证通过获取数据
        title_name = title_form.title.data
        user_name = title_form.user.data
        gender = title_form.gender.data

        # 3. 判断类型是否存在
        title = Title.query.filter_by(name=title_name).first()

        # 4. 如果类型存在
        if title:
            #  判断用户是否存在
            user = User.query.filter_by(name=user_name).first()

            # 如果重复就提示错误
            if user:
                flash('已存在该用户')

            # 没有重复用户就添加数据
            else:
                try:
                    new_user = User(name=user_name, title_id=title.id, gender=gender)
                    db.session.add(new_user)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash('添加用户失败')
                    db.session.rollback()

        else:
            # 5. 如果类型不存在, 添加类型和用户
            try:
                new_title = Title(name=title_name)
                db.session.add(new_title)
                db.session.commit()

                new_book = User(name=user_name, title_id=new_title.id, gender=gender)
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                print (e)
                flash('添加类型和用户失败')
                db.session.rollback()
    #else:
        #6. 验证不通过就提示错误
        #if request.method == 'POST':
        #    flash('参数不全')

    # 查询所有的类型信息, 让信息传递给模板
    titles = Title.query.all()

    return render_template('users.html', titles=titles, form=title_form)


if __name__ == '__main__':

    db.drop_all()
    db.create_all()

    # 生成数据
    tp1 = Title(name='确诊')
    tp2 = Title(name='疑似')
    tp3 = Title(name='普通')
    # 把数据提交给用户会话
    db.session.add_all([tp1, tp2, tp3])
    # 提交会话
    db.session.commit()
    ur1 = User(name='Alice', title_id=tp1.id, gender = 'F')
    ur2 = User(name='Bob', title_id=tp1.id, gender = 'M')
    ur3 = User(name='Carlo', title_id=tp2.id, gender = 'F')
    ur4 = User(name='Dave', title_id=tp3.id, gender = 'M')
    ur5 = User(name='Eve', title_id=tp3.id, gender = 'M')
    # 把数据提交给用户会话
    db.session.add_all([ur1, ur2, ur3, ur4, ur5])
    # 提交会话
    db.session.commit()

    app.run(debug=True)
