# flask Demo
#数据库迁移
python main.py db init

python main.py db migrate

python main.py db upgrade
#数据库历史迁移
python main.py db history
#数据库历史迁移回退
python main.py db downgrade
#gunicorn服务器启动flask
gunicorn -w 8 -b 127.0.0.1:5000 -D --access-logfile ./logs/log main:app