#coding=utf-8
from flask import Flask,render_template
from werkzeug.routing import BaseConverter
from flask import request
# 创建app并制定目录文件
app = Flask(__name__,static_folder='static',template_folder='templates')
app.config.from_pyfile('confing.cfg')
class Regex(BaseConverter):
    def __init__(self,url_map,regex):
        super(Regex, self).__init__(url_map)
        self.regex = regex
app.url_map.converters['re'] = Regex
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


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)