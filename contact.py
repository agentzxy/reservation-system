from flask import Flask,session, render_template, request, flash, redirect, url_for
from single_forms import singleContactForm
from group_forms import groupContactForm
from single_forms import hour_choices
from single_forms import singleCancel
import os
import send_email
import pymysql
import redis
app=Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['PERMANENT_SESSION_LIFETIME'] =600
r = redis.Redis(host='localhost', port=6379, decode_responses=True)   # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379


@app.route('/user',methods=['GET','POST'])
def home_page():
    global password
    if request.form.get('username'):
        username=request.form.get('username')
        password=request.form.get('password')
        session['username']=username
    if 'username' in session:
        db=pymysql.connect("localhost","root","nn456wsx","booking",charset='utf8')
        cursor=db.cursor()
        sql=("SELECT * FROM user_information WHERE username='%s' AND password='%s'"%(session['username'],password))
        if cursor.execute(sql)==1:
            db.commit()
            row_all=()
            db=pymysql.connect("localhost","root","nn456wsx","booking",charset='utf8')
            cursor=db.cursor()
            sql=("SELECT * FROM SINGLE WHERE 用户='%s'"%(session['username']))
            if cursor.execute(sql)!=0:
                row_all=cursor.fetchall()
            sql=("SELECT * FROM group_r WHERE 用户='%s'"%(session['username']))
            if cursor.execute(sql)!=0:
                row_all=row_all+cursor.fetchall()
            b=len(row_all)
            group_name=[0 for _ in range(b)]
            name=[0 for _ in range(b)]
            cellphone=[0 for _ in range(b)]
            num=[0 for _ in range(b)]
            date=[0 for _ in range(b)]
            j=0
            for i in row_all:
                if j==b:
                    break
                if len(i)==6:
                    group_name[j]=i[1]
                    name[j]=i[2]
                    cellphone[j]=i[3]
                    num[j]=i[4]
                    date[j]=i[5]
                else:
                    name[j]=i[1]
                    cellphone[j]=i[2]
                    num[j]=i[3]
                    date[j]=i[4]
                j=j+1
            return render_template('home_page.html',b=b,user=session['username'],name=name,cellphone=cellphone,num=num,date=date,group_name=group_name)
        else:
            flash("用户名或密码错误，请重新输入")
            return redirect(url_for('login'))

@app.route('/admin',methods=['GET','POST'])
def admin():
    admin_name=request.form.get('username')
    code=request.form.get('password')
    db=pymysql.connect("localhost","root","nn456wsx","booking",charset='utf8')
    cursor=db.cursor()
    sql=("SELECT * FROM admin_information WHERE admin='%s' AND passwd='%s'"%(admin_name,code))
    if cursor.execute(sql)==1:
        row_all=()
        sql=("SELECT * FROM SINGLE")
        if cursor.execute(sql)!=0:
            row_all=cursor.fetchall()
        sql=("SELECT * FROM group_r")
        if cursor.execute(sql)!=0:
            row_all=row_all+cursor.fetchall()
        b=len(row_all)
        group_name=[0 for _ in range(b)]
        name=[0 for _ in range(b)]
        cellphone=[0 for _ in range(b)]
        num=[0 for _ in range(b)]
        date=[0 for _ in range(b)]
        j=0
        for i in row_all:
            if j==b:
                break
            if len(i)==6:
                group_name[j]=i[1]
                name[j]=i[2]
                cellphone[j]=i[3]
                num[j]=i[4]
                date[j]=i[5]
            else:
                name[j]=i[1]
                cellphone[j]=i[2]
                num[j]=i[3]
                date[j]=i[4]
            j=j+1
        return render_template('all_recording.html',b=b,name=name,cellphone=cellphone,num=num,date=date,group_name=group_name)
    else:
        flash("用户名或密码错误，请重新输入")
        return redirect(url_for('login'))

#首页，用作用户登录页面
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/registered')
def registered():
    return render_template('registered.html')

#registered的表单发送验证码返回
@app.route('/return_ret',methods=['GET','POST'])
def return_ret():
    #email=request.form.get('email')     
    if request.form.get('email')!=None:
        session['email']=request.form.get('email')
        send_email.send_mail(request.form.get('username'),request.form.get('email'))
    if request.form.get('username')!=None:
        session['nickname']=request.form.get('username')    
    if request.form.get('password')!=None:
        session['password']=request.form.get('password')
    session.permanent = True
    
    while request.form.get('mailcode')==None:
        continue
    if 'email' in session and 'nickname' in session and 'password' in session:
        if request.form.get('mailcode')==r.get(session['email']):
            
            db=pymysql.connect("localhost","root","nn456wsx","booking",charset='utf8')
            cursor=db.cursor()
            sql=("INSERT INTO USER_INFORMATION(username,password)" "VALUES(%s,%s)")
            
            s=(session['nickname'],session['password'])
            cursor.execute(sql,s)
            db.commit()
            flash("注册成功，请您重新登录")
            return redirect(url_for('login'))
        else:
            flash("验证码输入错误，请重新输入")
    #获取表单输入的随机数字，与redius数据库作比较



@app.route('/single_contact/<user>',methods=['GET','POST'])
def single_contact(user):
    single_form=singleContactForm()
    if request.method == 'POST':
       if single_form.validate() == False:
          flash("需填写所有信息")
          return render_template('single_contact.html',user=user, single_form = single_form)
       else:
          return render_template('single_contact.html',user=user, single_form = single_form)
    elif request.method == 'GET':
          return render_template('single_contact.html',user=user, single_form = single_form)

@app.route('/group_contact/<user>',methods=['GET','POST'])
def group_contact(user):
    group_form=groupContactForm()
    if request.method == 'POST':
       if group_form.validate() == False:
          flash("需填写所有信息")
          return render_template('group_contact.html', group_form = group_form,user=user)
       else:
          return render_template('group_contact.html', group_form = group_form,user=user)
    elif request.method == 'GET':
          return render_template('group_contact.html', group_form = group_form,user=user)

@app.route('/single_contact/s_recordings/<user>',methods=['GET','POST'])
def s_recordings(user):
    name=request.form.get('name')
    cellphone=request.form.get('cellphone')
    num=request.form.get('people_num')
    year=request.form.get('year')
    month=request.form.get('month')
    time=dict(hour_choices).get(request.form.get('time'))
    date=str(year)+'.'+str(month)+'.'+request.form.get('date')+'日'+str(time)
    db=pymysql.connect("localhost","root","nn456wsx","booking",charset='utf8')
    cursor=db.cursor()
    #sql_date=("SELECT * FROM SINGLE WHERE 预约时间=%s"%(date))
    #count=cursor.execute(sql_date)
    #if count<=10:
        #cursor=db.cursor()
    sql=("INSERT INTO SINGLE(用户,姓名,手机号,预约人数,预约时间)" "VALUES(%s,%s,%s,%s,%s)")
    s=(user,name,cellphone,num,date)
    cursor.execute(sql,s)
    db.commit()
    return render_template('s_recordings.html',year=year,month=month,name=name,cellphone=cellphone,num=num,date=date)
    #else:
        #flash('该时间段预约人数已满')
        #return redirect(url_for('single_contact'))

@app.route('/group_contact/g_recordings/<user>',methods=['GET','POST'],)
def g_recordings(user):
    group_name=request.form.get('group_name')
    name=request.form.get('name')
    cellphone=request.form.get('cellphone')
    num=request.form.get('people_num')
    year=request.form.get('year')
    month=request.form.get('month')
    time=dict(hour_choices).get(request.form.get('time'))
    date=str(year)+'.'+str(month)+'.'+request.form.get('date')+'日'+str(time)
    db=pymysql.connect("localhost","root","nn456wsx","booking",charset='utf8')
    cursor=db.cursor()
    sql=("INSERT INTO GROUP_R(用户,团体名称,负责人姓名,手机号,预约人数,预约时间)" "VALUES(%s,%s,%s,%s,%s,%s)")
    s=(user,group_name,name,cellphone,num,date)
    cursor.execute(sql,s)
    db.commit()
    return render_template('g_recordings.html',name=name,cellphone=cellphone,num=num,date=date,group_name=group_name)

@app.route('/cancel/<user>/<i>')
def cancel(user,i):
    db=pymysql.connect("localhost","root","nn456wsx","booking",charset='utf8')
    cursor=db.cursor()
    if int(i)==0:
        if cursor.execute("SELECT * FROM SINGLE WHERE 用户='%s'"%(user))>0:
            sql="delete from single where 预约时间 in (SELECT 预约时间 from (select 预约时间 from single limit "+i+","+str(int(i)+1)+") as temp where 用户='%s')"%(user)
            cursor.execute(sql)
        else:
            sql="delete from group_r where 预约时间 in (SELECT 预约时间 from (select 预约时间 from group_r limit "+i+","+str(int(i)+1)+") as temp where 用户='%s')"%(user)
            cursor.execute(sql)
    else:
        if cursor.execute("select * from single where 用户='%s'"%(user))>int(i):
            sql="delete from single where 预约时间 in (SELECT 预约时间 from (select 预约时间 from single limit "+(i)+","+(i)+") as temp where 用户='%s')"%(user)
            cursor.execute(sql)
        else:
            count=cursor.execute("select * from single where 用户='%s'"%(user))
            if count==int(i):
                sql="delete from group_r where 预约时间 in (SELECT 预约时间 from (select 预约时间 from group_r limit "+str(0)+","+str(1)+") as temp where 用户='%s')"%(user)
                cursor.execute(sql)
            else:
                i=str(int(i)-count)
                sql="delete from group_r where 预约时间 in (SELECT 预约时间 from (select 预约时间 from group_r limit "+i+","+(i)+") as temp where 用户='%s')"%(user)
                cursor.execute(sql)
    db.commit()
    return redirect('http://localhost:5000/user')

if __name__=='__main__':
    app.run(debug=True)