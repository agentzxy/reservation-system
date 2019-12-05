from threading import Thread
from flask import current_app
from flask import Flask
import redis
import random
import os
from datetime import datetime
from datetime import timedelta
from flask_mail import Mail,Message

app=Flask(__name__)
app.config ['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.qq.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USERNAME'] = '1420445740@qq.com'
app.config['MAIL_PASSWORD'] = 'wakfumlwmpizbagj'
app.config['MAIL_DEFAULT_SENDER'] = '1420445740@qq.com'
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
r = redis.Redis(connection_pool=pool)

def send_async_email(app, msg):
    with app.app_context():   #确认程序上下文被激活
        mail.send(msg)

def send_mail(nickname,email):
    ret = ""
    for i in range(6):
        num = random.randint(0, 9)
        letter = chr(random.randint(97, 122))#取小写字母
        Letter = chr(random.randint(65, 90))#取大写字母
        s = str(random.choice([num,letter,Letter]))
        ret += s
    r.set(email,ret,ex=60)
    msg=Message('您的账号注册验证码',sender='1420445740@qq.com',recipients=[email])
    msg.body='sended by flask-email'
    msg.html='''
    <h1>
        亲爱的 {nickname},
    </h1>
    <h3>
        欢迎来到 <b>中国矿业大学博物馆预约系统</b>!
    </h3>
    <p>
        您的验证码为 &nbsp;&nbsp; <b>{ret}</b> &nbsp;&nbsp; 赶快去完善注册信息吧！！！
    </p>
    <p>感谢您的支持和理解</p>
    <p>来自：中国矿业大学博物馆</p>
    <p><small>{time}</small></p>
    '''.format(nickname=nickname,ret=ret,time=datetime.utcnow)
    thread=Thread(target=send_async_email,args=[app,msg])
    thread.start()
    