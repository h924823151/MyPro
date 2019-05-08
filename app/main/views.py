from . import main

from .. import db
from ..models import *
from flask import render_template,request,session,redirect
from werkzeug.security import generate_password_hash,check_password_hash
import json,datetime,os,random


# 验证码生成函数
def create_code():
    arr = ['1','2','3','4','5','6','7','8','9','0','A','a',
          'V','G','E','R','T','Y','N','J','K',
           'a','z','x','c','d','g','u']
    l = len(arr)
    res = ''
    for _ in range(6):
        a = random.randint(0,l-1)
        res += arr[a]
    return res

#首页
@main.route('/')
@main.route('/index')
def index_views():
    if 'uname' in session:
        uname = session['uname']
        user = User.query.filter_by(uname=uname).first()
    if 'uname' in request.cookies:
        uname = request.cookies['uname']
        user = User.query.filter_by(uname=uname).first()
        
    return render_template('index.html',params=locals())

# 资讯
@main.route('/news')
def news():
    return render_template('news.html')

@main.route('/hero_news')
def hero_news():
    return render_template('hero_news.html')


# 相关文章
@main.route('/index_news01')
def index_news01():
    return render_template('index_news01.html')

@main.route('/index_news02')
def index_news02():
    return render_template('index_news02.html')

@main.route('/index_news03')
def index_news03():
    return render_template('index_news03.html')


# 单击更换验证码
@main.route('/change_code')
def change_code():
    session['res'] = create_code()
    res = session['res']
    return res


# 登陆功能
@main.route('/login',methods=['GET','POST'])
def login_views():
    res = session['res']
    if request.method == 'GET':
        # 获取请求源地址,没有则为'/'
        url = request.headers.get('Referer','/')
        session['url'] = url
        # 判断session中是否有uname
        if 'uname' in session:
            return redirect(url)
        else:
            # 判断cookie是否有uname
            if 'uname' in request.cookies:
                # cookie中有登陆信息
                # 取出uname的值判断正确性
                uname = request.cookies['uname']
                user = User.query.filter_by(uname=uname).first()
                if user: 
                    # 说明uname是正确的,则保存进session
                    session['uname'] = uname
                return redirect(url)
            return render_template('login.html',params=locals())
    else:
        uname = request.form['uname']
        upwd = request.form['upwd']
        code = request.form['code']
        print(request.form)
        user = User.query.filter_by(uname=uname).first()
        # 验证传输过来的upwd是否和数据库一致
        if res.upper() == code.upper():
            if user and check_password_hash(user.upwd,upwd):
                # 一致,保存进session
                session['uname'] = uname
                # 从session中获取url,构建响应对象   
                url = session.get('url','/')
                resp = redirect(url)
                # 判断是否记住密码
                if 'isSaved' in request.form:
                    resp.set_cookie('uname',uname,3600*24*365*2)
                return resp
            else:
                # 登陆失败,返回登陆界面
                msg='用户名或密码错误!!'
                return render_template('login.html',params=locals())
        else:
            msg='验证码不正确!!'
            return render_template('login.html',params=locals())


# 退出功能
@main.route('/logout')
def logout():
    url = request.headers.get('Referer','/')
    resp = redirect(url)
    if 'uname' in session or 'uname' in request.cookies:
        if 'uname' in session:
            del session['uname']
        resp.delete_cookie('uname')

    return resp


# 注册功能
@main.route('/regsiter',methods=['GET','POST'])
def regsiter():
    if request.method == 'GET':
        # 获取请求源地址,并存进session
        url = request.headers.get('Referer','/')
        session['url']=url
        return render_template('/regsiter.html')
    else:
        # 获取发送过来的数据
        uname = request.form['uname']
        upwd = request.form['upwd']
        upwd1 = request.form['upwd1']

        # 密码一致,验证用户是否存在
        if upwd == upwd1:
            user=User.query.filter_by(uname=uname).all()
            # 用户存在,则注册失败
            if user:
                return render_template('/regsiter.html',msg='注册失败')
            # 判断密码是否小于6位
            if len(upwd)<6:
                return render_template('/regsiter.html',msg='密码长度过短')
            # 用户不存在,则进行加密,并存入数据库
            upwd = generate_password_hash(upwd)
            user = User(uname,upwd)
            db.session.add(user)
            # 注册成功,uname存session
            session['uname']=uname
            # 获取请求源地址
            url = session.get('url','/')
            return redirect(url)

        else:
            return render_template('/regsiter.html',msg='密码输入不一致')
        return render_template('/regsiter.html')


# 验证用户名是否存在
@main.route('/checkuname')
def checkuname():
    uname = request.args['uname']
    print(uname)
    user = User.query.filter_by(uname=uname).first()
    # print(user)

    if user:
        return '用户名已存在'
    elif len(uname)<1:
        return '用户名不允许为空'
    else:
        return '通过'


# 英雄查询功能
@main.route('/hero_query',methods=['GET','POST'])
def hero():
    session['url'] = 'http://127.0.0.1:5000/hero_query'
    if request.method == 'GET':
        if 'uname' in session:
            return render_template('hero_query.html',params=locals())
        if 'uname' in request.cookies:
            return render_template('hero_query.html',params=locals())
        else:
            err="请登录后操作"
            return render_template('login.html',params=locals())
    else:
        name = request.form['input_hero']
        print(name)
        hero = Hero.query.filter_by(name=name).first()
        if hero:
            skill = hero.skill.all()
            return render_template('hero_expression.html',params=locals())
        else:
            msg = '英雄不存在!!'
            return render_template('hero_query.html',params=locals())


# 聊天室功能
@main.route('/getip')
def index():
    session['url'] = 'http://127.0.0.1:5000/getip'
    if 'uname' in session:
        return render_template('getip.html')
    if 'uname' in request.cookies:
        return render_template('getip.html')
    else:
        err="请登录后操作"
        return render_template('login.html',params=locals())

@main.route('/rechat',methods=['GET','POST'])
def rechat():
    if request.method=='POST':
        name=request.form['name']
        url=request.headers.get('Referer','/')
        print('请求地址：',url)
        msg=Msg()
        msg.name=name
        msg.address=url
        db.session.add(msg)
        return render_template('chart.html',rname=name)
    else:
        return '这不是post请求'

@main.route('/refuse')
def refuse():
    name=request.args['rname']
    heros=Msg.query.all()
    list=[]
    for x in heros:
        if x.name!=name:
            list.append(x.to_dict())
    return list

@main.route('/reuser')
def reuser():
    msg=Msg.query.all()
    list=[]
    for x in msg:
        list.append(x.to_dict())
    res=json.dumps(list)
    print('获取字典的数据：'+res)
    return res

@main.route('/sendall')
def sendall():
    content=request.args['name']
    return content

@main.route('/delete')
def delete():
    name=request.args['name']
    print(name)
    men=Msg.query.filter_by(name=name).first()
    db.session.delete(men)
    return redirect('/')


#数据添加
@main.route('/01-add',methods=['GET','POST'])
def add_views():
    if request.method == 'GET':
        return render_template('01-add.html')
    else:
        f1 = request.files['avautar_img']
        ftime1 = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        # 获取当前文件的扩展名
        ext1 = f1.filename.split('.')[1]
        # 组合新的文件名
        filename1 = ftime1 + '.' + ext1
        # 获取绝对路径
        basedir1 = os.path.dirname(__file__)
        # 完整路径 = 绝对路径 + 保存目录 + 文件名称
        upload_path1 = os.path.join(basedir1, 'static/upload', filename1)
        f1.save('static/upload/' + filename1)
        print("保存成功")

        f2 = request.files['picture_img']
        ftime2 = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        # 获取当前文件的扩展名
        ext2 = f2.filename.split('.')[1]
        # 组合新的文件名
        filename2 = ftime2 + '.' + ext2
        # 获取绝对路径
        basedir2 = os.path.dirname(__file__)
        # 完整路径 = 绝对路径 + 保存目录 + 文件名称
        upload_path2 = os.path.join(basedir2, 'static/upload', filename2)
        f2.save('static/upload/' + filename2)
        print("保存成功")

        name = request.form['name']
        avautar = upload_path1
        picture = upload_path2
        hero_story = request.form['hero_story']

        hero = Hero(name,avautar,picture,hero_story)

        db.session.add(hero)
        return "添加成功"


@main.route('/02-add_skin',methods=['GET','POST'])
def skin_views():
    if request.method == 'GET':
        return render_template('02-add_skin.html')
    else:
        f = request.files['skill_pic']
        ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        #获取当前文件的扩展名
        ext = f.filename.split('.')[1]
        #组合新的文件名
        filename = ftime + '.' + ext
        #获取绝对路径
        basedir = os.path.dirname(__file__)
        # 完整路径 = 绝对路径 + 保存目录 + 文件名称
        upload_path = os.path.join(basedir,'static/upload',filename)
        f.save('static/upload/'+filename)
        print("保存成功")

        skill_name = request.form['skill_name']
        skill_content = request.form['skill_content']
        skill_exp = request.form['skill_exp']
        skill_pic = upload_path
        skill_hero_id = request.form['skill_hero_id']
        skill = Skill(skill_name,skill_content,skill_exp,skill_pic,skill_hero_id)
        db.session.add(skill)
        return "保存成功"