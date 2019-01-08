#coding=utf-8
from flask import Flask,render_template
from werkzeug.routing import BaseConverter
from flask import request,Response,abort,make_response,jsonify,g,redirect,url_for,session,flash
import json
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import PasswordField,StringField,SubmitField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Regexp,Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail,Message
# 创建app并制定目录文件
app = Flask(__name__,static_folder='static',template_folder='templates')
app.config.from_pyfile('confing.cfg')
db = SQLAlchemy(app)
Migrate(app,db)
manager = Manager(app)
mail = Mail(app)

manager.add_command("db",MigrateCommand)
class User(db.Model):
    id = db.Column()



class Regex(BaseConverter):
    def __init__(self,url_map,regex):
        super(Regex, self).__init__(url_map)
        self.regex = regex
app.url_map.converters['re'] = Regex

def sendmail():
    msg = Message(u'主题',sender="qiyuemail@126.com",recipients=["1107926620@qq.com"])
    msg.body = 'hello'
    mail.send(msg)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/str",methods=["POST","GET"])
def mystr():
    print app.config.get("STR")
    print app.url_map
    return 'haha'

@app.route("/h1")
@app.route("/h2")
def doubleurl():
    return 'h1 or h2'

@app.route("/lian")
def lian():
    return render_template("lian.html")

@app.route("/intpage/<int:num>")
def intpage(num):
    return "The num is %s"%num

@app.route("/mobile/<re(r'1[3568]\d{9}'):mobile>")
def mobile(mobile):
    return 'Your mobile phone is %s'%mobile

@app.route("/pg",methods=["POST","GET"])
def pg():
    if request.method == "GET":
        return render_template("post.html")
    else:
        name = request.form.get('name','')
        return render_template("post.html",name = name)
@app.route("/upload",methods=["POST","GET"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    else:
        if request.files.get('pic') is None:
            return u'没有上传'
        else:
            filename = request.files.get('pic').filename
            data = request.files.get('pic')
            print filename
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
        if request.form is None:
            return u'什么都没写'
        else:
            session['name'] = request.form.get('name','')
            return redirect(url_for("loginname"))
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
app.add_template_filter(qiepian2,'qiepian2')

@app.route("/li")
def li():
    return render_template("li.html",li=[1,2,5,6,4,2,8])

class RegisterForm(FlaskForm):
    username = StringField(label=u'用户名',validators=[DataRequired(message=u'密码不为空'),Length(min=5,max=10,message=u'用户名在5-10位之间')],render_kw={"placeholder":"haha","class":"ww"})
    password = PasswordField(label=u'密码',validators=[DataRequired(message=u'密码不为空')])
    password2 = PasswordField(label=u'确认密码',validators=[DataRequired(message=u'不为空'),EqualTo('password',message=u'两次不一致')])
    submit = SubmitField(label=u'提交')
#
#
@app.route("/registers",methods=["POST" , "GET"])
def userregister():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        password2 = form.password2.data
        session['name'] = username
        print username,password,password2
        return render_template("index.html",name=username)
    return render_template("register.html",form = form)

@app.route("/macro")
def macro():
    return render_template("macro_son.html")


@app.route("/flash")
def flash():
    flash("haha",)
    return render_template("flash.html")

if __name__ == '__main__':
    app.run()