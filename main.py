#coding=utf-8
# 导入flask和模板渲染工具
from flask import Flask,render_template
# 导入查询字符串匹配工具基类
from werkzeug.routing import BaseConverter
# 导入工具函数
from flask import request,Response,abort,make_response,jsonify,g,redirect,url_for,session,flash
import json
# 导入管理器工具
from flask_script import Manager
# 导入表单工具
from flask_wtf import FlaskForm
# 表单字段
from wtforms import PasswordField,StringField,SubmitField
# 表单验证器
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Regexp,Length
# 数据库ORM工具
from flask_sqlalchemy import SQLAlchemy
# 数据库迁移工具
from flask_migrate import Migrate,MigrateCommand
# flask邮件发送工具
from flask_mail import Mail,Message
# 数据库查询工具
from sqlalchemy import or_,func
# 导入蓝图,这个导入的是蓝图工具不是视图函数
from app_orders import orders
# 创建app并制定目录文件
app = Flask(__name__,static_folder='static',template_folder='templates')
# 对app进行配置
app.config.from_pyfile('confing.cfg')
# 创建数据库管理工具
db = SQLAlchemy(app)
Migrate(app,db)
# 创建app管理工具
manager = Manager(app)
# 创建邮件管理工具
mail = Mail(app)
# 注册蓝图,注册的时蓝图工具不是蓝图里的视图函数,url_prefix是各蓝图模块的url前缀
app.register_blueprint(orders,url_prefix = "/orders")
# 向管理器添加功能
manager.add_command("db",MigrateCommand)
# 创建模型类
class User(db.Model):
    # 指定数据表的名字
    __tablename__ = 'tbl_user'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80),unique = True,nullable=False)
    password = db.Column(db.String(60),unique=True,nullable=False)
    # 建立外键指定对谁建立
    role_id = db.Column(db.Integer,db.ForeignKey("tbl_role.id"))
    # 该数据库的数据对象显示的名字
    def __repr__(self):
        return '<User %r>' %self.name

class Role(db.Model):
    __tablename__ = 'tbl_role'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(80),unique=True,nullable = False)
    # 为关联查询方便并不存在于数据库的,只是类层面上的
    users = db.relationship('User',backref='role')

# 定义查询字符串提取工具
class Regex(BaseConverter):
    def __init__(self,url_map,regex):
        super(Regex, self).__init__(url_map)
        self.regex = regex
        # 对该工具命名
app.url_map.converters['re'] = Regex
# 发送邮件函数
def sendmail():
    msg = Message(u'主题',sender="qiyuemail@126.com",recipients=["1107926620@qq.com"])
    msg.body = 'hello'
    mail.send(msg)

@app.route("/")
def index():
    # 返回模板
    return render_template("index.html")
# 指定该函数可以访问的方式
@app.route("/str",methods=["POST","GET"])
def mystr():
    # 读取配置文件的信息
    print app.config.get("STR")
    # 路由映射列表
    print app.url_map
    return 'haha'
# 一个函数有两个访问路径
@app.route("/h1")
@app.route("/h2")
def doubleurl():
    return 'h1 or h2'

@app.route("/lian")
def lian():
    return render_template("lian.html")
# 提取查询字符串
@app.route("/intpage/<int:num>")
def intpage(num):
    return "The num is %s"%num
# 使用自定义的提取查询字符串工具
@app.route("/mobile/<re(r'1[3568]\d{9}'):mobile>")
def mobile(mobile):
    return 'Your mobile phone is %s'%mobile
# 按照访问方式的不同同一个函数提供多种功能
@app.route("/pg",methods=["POST","GET"])
def pg():
    if request.method == "GET":
        return render_template("post.html")
    else:
        name = request.form.get('name','')
        return render_template("post.html",name = name)
    # 文件上传
@app.route("/upload",methods=["POST","GET"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else:
        if request.files.get('pic') is None:
            return u'没有上传'
        else:
            # 获取文件的名字
            filename = request.files.get('pic').filename
            # 获取文件实体
            data = request.files.get('pic')
            with open("media/"+filename,"wb+")as draw:
                for msg in data:
                    draw.write(msg)
            return u'上传成功'
# 几种设置异常的方式
# 第一种
@app.errorhandler(404)
def error_handle_404(msg):
    return u'页面出错了，错误信息是%s'%msg
# 第二种
@app.route("/errorr")
def error_500():
    abort(Response('服务器错误'))
# 第三种
@app.route("/get_error")
def get_error():
    return "错误",404,[("server","zhangshuo")]
# 使用make_response设置状态信息页
@app.route("/makeresponse")
def makeresponse():
    resp = make_response(render_template("make_response.html"))
    # 设置状态码以及对状态码的说明
    resp.status = '666 hello'
    resp.headers['city'] = 'bejing'
    return resp
# 向前端传递json格式数据的三种方式
# 序列化成json字符串然后修改响应头
@app.route("/getjson")
def getjson():
    dict={"server":"zjhang"}
    jsonstr = json.dumps(dict)
    return jsonstr,200,[("Content-Type","application/json")]
# 使用jsonify模块序列化字典
@app.route("/jsonifytest")
def jsonifytest():
    dict = {"server": "shuo"}
    return jsonify(dict)
# 使用jsonify序列化字典的另一种表示形式
@app.route("/jsonifytest2")
def jsonifytest2():
    return jsonify(city = "beijing",country = "China")
# 用户第一次访问时该网站时被执行
# @app.before_first_request
# def handle_before_first():
#     print "执行了handle_before_first"
#     return "before_first_request"
# # 用户试图函数处理完毕且没有未处理的异常时被执行
# @app.after_request
# def after_request(response):
#     print "执行了after_request"
#     return response
# # 视图函数处理完不管有没有异常都执行
# @app.teardown_request
# def teardown_request(response):
#     print "执行了teardown_request"
#     return response



@app.route("/saveg",methods = ['POST','GET'])
def saveg():
    if request.method == 'GET':
        return render_template('saveg.html')
    else:
        g.user_name = request.form['name']
        print g.user_name
        # 视图函数要用引号不然成了本函数内的局部变量
        # g变量在同一个视图函数内使用若要跨视图使用需要调用函数并对它传入参数g
        return readg(g)

def readg(g):
    myname = g.user_name
    return 'hello:%s'%myname
# 设置cookie
@app.route("/cookiesave")
def cookiesave():
    resp = make_response('hello world')
    resp.set_cookie('city','beijing',max_age = 3600)
    return resp
# 获取cookie
@app.route("/getcookie")
def getcookie():
    cookies = request.cookies.get('city','mieyou cookie')
    return cookies
# 删除cookie
@app.route("/delcookie")
def delcookie():
    resp = make_response('hello')
    resp.delete_cookie('city')
    return resp
# 通过设置响应头的方式设置cookie和过期时间的方法
@app.route("/setcookie")
def setcookie():
    resp = make_response('setcookie')
    resp.headers['Set-Cookie'] = "mycookie = zzz; Max-Age = 3600;"
    return resp
@app.route("/userlogin",methods = ["POST","GET"])
def userlogin():
    if request.method == "GET":
        return render_template('login.html')
    else:
        # 判断传入数据是否为空
        if request.form is None:
            return u'什么都没写'
        else:
            session['name'] = request.form.get('name','')
            return redirect(url_for("loginname"))
        # 配合上边视图的视图函数
@app.route("/loginname")
def loginname():
    name = session.get('name','')
    if name:
        return 'hello:%s'%name
    else:
        return '未登陆'
# ============================自定义过滤器============================
# 自定义过滤器第一种方法
@app.template_filter('qiepian')
def qiepian(li):
    return li[:-3]
# 自定义过滤器第二种方法
def qiepian2(li):
    return li[3::2]
# 第二种方法要注册自己的过滤器
app.add_template_filter(qiepian2,'qiepian2')
# 测试自定义过滤器
@app.route("/li")
def li():
    return render_template("li.html",li=[1,2,5,6,4,2,8])
# 创建表单模型render_kw会在前端起作用
class RegisterForm(FlaskForm):
    username = StringField(label=u'用户名',validators=[DataRequired(message=u'密码不为空'),Length(min=5,max=10,message=u'用户名在5-10位之间')],render_kw={"placeholder":"haha","class":"ww"})
    password = PasswordField(label=u'密码',validators=[DataRequired(message=u'密码不为空')])
    password2 = PasswordField(label=u'确认密码',validators=[DataRequired(message=u'不为空'),EqualTo('password',message=u'两次不一致')])
    submit = SubmitField(label=u'提交')
#
#前段数据接收并根据定义的表单类进行验证
@app.route("/registers",methods=["POST" , "GET"])
def userregister():
    # 如果前端有数据传入则在表单实例化的时候数据会填充进去
    form = RegisterForm()
    # 表单验证都为真是才为真
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        password2 = form.password2.data
        session['name'] = username
        print username,password,password2
        return render_template("index.html",name=username)
    return render_template("register.html",form = form)
# 宏测试函数
@app.route("/macro")
def macro():
    return render_template("macro_son.html")

# 闪现测试函数
@app.route("/flash")
def flash():
    flash("haha",)
    return render_template("flash.html")
# 数据库数据查询
@app.route("/selectsql/<int:num>")
def selectsql(num):
    # get只接受id进行查询
    user = User.query.get(num)
    # 查询第一个
    user2 = User.query.first()
    # 查询所有
    userall = User.query.all()
    # 过滤查询
    user3 = User.query.filter_by(name="zhang")
    # 或查询
    user4 = User.query.filter(or_(User.name=="zhang",User.password=="165"))
    # 分页查询
    user5 = User.query.offset(1).limit(2).all()
    # 聚合查询
    listss = db.session.query(User.id,func.count(User.id)).group_by(User.id).all()
    return render_template("sql.html",listss=listss,user=user,user2=user2,user3=user3,user4=user4,userall=userall,user5=user5)

@app.route("/ship/<int:num>")
def ship(num):
    # 关联查询
    user = User.query.get(num)
    roless = user.role
    ro = Role.query.get(num)
    userss = ro.users
    return render_template("ship.html",roless=roless,userss=userss)
# 修改数据
@app.route("/changesql/<int:num>/<int:num2>")
def changesql(num,num2):
    user = User.query.get(num)
    user.name = 'zhangshuoooo'
    db.session.add(user)
    db.session.commit()
    # 修改数据第二种方法
    User.query.filter_by(id=num2).update({"name":'hahahaha'})
    db.session.commit()
    return '修改成功！'
# 删除数据
@app.route("/delsql/<int:num>")
def delsql(num):
    user = User.query.get(num)
    db.session.delete(user)
    db.session.commit()
    return '删除成功！'



if __name__ == '__main__':
    # 程序运行
    app.run()