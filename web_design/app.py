from flask import Flask,request,render_template,session,flash,redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlserver import *
from os import path
from werkzeug.utils import secure_filename
import datetime
import xlrd
app = Flask(__name__)
glovar = ''
app.secret_key = 'superzhaoyang1.'
'''
表单验证函数
'''
def Check_Login():
    if 'username' not in session:
        return False
    return True

'''
返回各个角色的主页
'''
@app.route('/', methods=['GET'])

def index():
    if not Check_Login():
        return redirect(url_for('login'))
    dt = datetime.datetime.now()
    time = '今天是' + dt.strftime('%Y-%m-%d') + ',' #构造表示日期的字符串
    weekday = {}
    weekday['1'] = '一'
    weekday['2'] = '二'
    weekday['3'] = '三'
    weekday['4'] = '四'
    weekday['5'] = '五'
    weekday['6'] = '六'
    weekday['0'] = '日'

    week = '星期' + weekday[dt.strftime('%w')]
    if session['identity'] == 'student':
        if session['username'] == '201800800374':   #如果是特定的学生则设置特定头像
            avatar_path = '/static/images/avatar2.jpg'
            sql = "select sname from student where sno = '%s'" % session['username']
            username = search(sql)
        return render_template('student/index.html',avatar_path = avatar_path,username = username[0][0],time = time,week = week)

    elif session['identity'] == 'jiaowuyuan':

        avatar_path = '/static/images/avatar_adm.jpg' #教务员头像统一
        sql = "select jname from jiaowuyuan where jno = '%s'" % session['username']
        username = search(sql) #查询名字
        return render_template('jiaowuyuan/index.html',username = username[0][0],time = time,week = week,avatar_path = avatar_path)

    elif session['identity'] == 'teacher':   #教师头像统一
        avatar_path = 'static/images/avatar_tea.jpg'
        if session['username'] == 't001':
            sql = "select tname from teacher where tno = '%s'" % session['username']
            username = search(sql)

        return render_template('teacher/index.html' ,avatar_path = avatar_path, username = username[0][0],time = time,week = week) #每次渲染界面都要传头像和用户名称参数
    return redirect(url_for('/'))

'''
登陆函数
'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    dt = datetime.datetime.now()
    time = '今天是'+dt.strftime( '%Y-%m-%d' )+','
    weekday = {}
    weekday['1'] = '一'
    weekday['2'] = '二'
    weekday['3'] = '三'
    weekday['4'] = '四'
    weekday['5'] = '五'
    weekday['6'] = '六'
    weekday['0'] = '日'

    week = '星期'+weekday[dt.strftime( '%w' )]
    if request.method == "GET":
        return render_template('login.html')

    if request.form['identity'] == 'student':
        result = search("select * from student where sno='%s'" % request.form['username'])
        if request.form['username'] == '201800800374':
            avatar_path = '/static/images/avatar2.jpg'

        if result ==[None]: #没有改用户的话，会进行为空的判定，不让页面出现bug界面
            flash('用户名或者密码有误!')
            return render_template('login.html')
        elif len(result) > 0 and check_password_hash(result[0][6], request.form['pwd']):
            username = result[0][1]
            session['username'] = request.form['username']
            session['identity'] = request.form['identity']
            if session['username'] == '201800800374':
                avatar_path = '/static/images/avatar2.jpg'
            return render_template('student/index.html',avatar_path = avatar_path,username = username,time = time,week = week)
        else:
            flash('用户名或者密码有误！')
            return redirect(url_for('login'))
    elif request.form['identity'] == 'jiaowuyuan':
        result = search("select * from jiaowuyuan where jno='%s'" % request.form['username'])
        username = request.form['username']
        sql = "select jname from jiaowuyuan where jno = '%s' " % username
        username = search(sql)
        avatar_path = '/static/images/avatar_adm.jpg'
        if result == [None]:
            flash('用户名或者密码有误！')
            return render_template('login.html')
        elif len(result) > 0 and check_password_hash(result[0][2], request.form['pwd']):
            session['username'] = request.form['username']
            session['identity'] = request.form['identity']
            return render_template('jiaowuyuan/index.html',username = username[0][0],time = time,week = week,avatar_path = avatar_path)
        else:
            flash('用户名或者密码有误！')
            return redirect(url_for('login'))


    elif request.form['identity'] == 'teacher':
        result = search("select * from teacher where tno='%s'" % request.form['username'])

        avatar_path = '/static/images/avatar_tea.jpg'
        if result == [None]:
            flash('用户名或者密码有误')
            return render_template('login.html')
        elif len(result) > 0 and check_password_hash(result[0][3], request.form['pwd']):
            session['username'] = request.form['username']
            session['identity'] = request.form['identity']
            session['tname'] = result[0][1]
            sql = "select tname from teacher where tno = '%s'" % session['username']
            username = search(sql)
            return render_template('teacher/index.html',avatar_path = avatar_path,username = username[0][0],time = time,week = week)
        else:
            flash('用户名或者密码有误！')
            return redirect(url_for('login'))

'''
密码修改函数
'''
@app.route('/passwordChange', methods=['GET', 'post'])
def passwordChange():
    if not Check_Login():
        return redirect(url_for("login"))
    return render_template('password_change.html')

@app.route('/changePassword', methods=['GET', 'post'])
def changePassword():
    if not Check_Login():
        return redirect(url_for("login"))
    else:
        if session['identity'] == 'student':
            result= search("select * from student where sno='%s'" % session['username'])
            temp = 6
        elif session['identity'] == 'jiaowuyuan':
            result =  search("select * from jiaowuyuan where jno='%s'" % session['username'])
            temp = 2
        elif session['identity'] == 'teacher':
            result = search("select * from teacher where tno='%s'" % session['username'])
            temp = 3
        if len(result) > 0 and check_password_hash(result[0][temp],request.form['prepw']): #运用用韵哈希判定来验证密码
            if request.form['nowpw'] == request.form['repw']:
                password = generate_password_hash(request.form['nowpw'])
                updatepassword(session['identity'],password,session['username'])
                flash('修改密码成功!')
            else:
                flash('两次密码不一致!')
        else:
            flash('原密码输入错误!')
        return render_template('password_change.html')
@app.route('/course_selection', methods=['GET', 'post'])
def course_selection():
    if not Check_Login():
        return redirect(url_for("login"))
    else:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month  #获取系统时间
        if int(month) in [3,4,5,6,7,8]:       # 表示第2学期
            term = str(year -1) + '-' + str(year) + '-' + '2'
        else:
            if int(month) in [1,2,9,10,11,12]: #表示第一学期
                term = str(year) + '-' + str(year + 1) + '-' + '1'

        if(session['username'] == '201800800374'):
            avatar_path = '/static/images/avatar2.jpg'

        #查询出已选课程
        result = search_2dimen ("select lesson.term,lesson.cno,lesson.course_no,lesson.cname, \
             lesson.type,teacher.tname,lesson.classname,lesson.credit,lesson.xueshi,lesson.maxpeople \
             from lesson,sc,teacher where lesson.cno=sc.cno and teacher.tno = lesson.tno and sc.sno='%s' and lesson.term='%s'" % (
                 session['username'], term))
        #查询出本学期待选择课程
        result2 = search_2dimen(
            "select lesson.term,lesson.cno,lesson.course_no,lesson.cname,lesson.type,teacher.tname,lesson.classname,lesson.credit,lesson.xueshi,lesson.maxpeople \
            from lesson,student,teacher where lesson.type='必修' and student.sno='%s' and student.classname=lesson.classname and teacher.tno = lesson.tno and lesson.term='%s'" % (
                session['username'], term))
        sql = "select sname from student where sno = '%s'" % session['username']
        username = search(sql) #查询姓名

        return render_template('student/course_selection.html', datas=result,  datas2=result2,avatar_path = avatar_path,username = username[0][0] )
'''
必修课选课函数
'''
@app.route('/bixiu', methods=['GET', 'post'])
def bixiu():
    if not Check_Login():
        return redirect(url_for("login"))
    else:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        if int(month) in [3,4,5,6,7,8]:
            term = str(year -1) + '-' + str(year) + '-' + '2'
        else:
            if int(month) in [1,2,9,10,11,12]:
                term = str(year) + '-' + str(year + 1) + '-' + '1'
        result = search_2dimen("select lesson.term,lesson.cno,lesson.course_no,lesson.cname, \
                     lesson.type,teacher.tname,lesson.classname,lesson.credit,lesson.xueshi,lesson.maxpeople \
                     from lesson,sc,teacher where lesson.cno=sc.cno and teacher.tno = lesson.tno and sc.sno='%s' and lesson.term='%s'" % (
            session['username'], term))
        result2 = search_2dimen(
            "select lesson.term,lesson.cno,lesson.course_no,lesson.cname,lesson.type,teacher.tname,lesson.classname,lesson.credit,lesson.xueshi,lesson.maxpeople \
            from lesson,student,teacher where lesson.type='必修' and student.sno='%s' and student.classname=lesson.classname and teacher.tno = lesson.tno and lesson.term='%s'" % (
                session['username'], term))
        if (session['username'] == '201800800374'):
            avatar_path = '/static/images/avatar2.jpg'
        sql = "select sname from student where sno = '%s'" % session['username']
        username = search(sql)

        return render_template('student/course_selection.html', datas=result,  datas2=result2,avatar_path = avatar_path,username = username[0][0])
'''
通选课
'''
@app.route('/tongxuan', methods=['GET', 'post'])
def tongxuan():
    if not Check_Login():
        return redirect(url_for("login"))
    else:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        if int(month) in [3,4,5,6,7,8]:
            term = str(year -1) + '-' + str(year) + '-' + '2'
        else:
            if int(month) in [1,2,9,10,11,12]:
                term = str(year) + '-' + str(year + 1) + '-' + '1'

        if (session['username'] == '201800800374'):
            avatar_path = '/static/images/avatar2.jpg'
        sql = "select sname from student where sno = '%s'" % session['username']
        username = search(sql)
        result = search_2dimen("select lesson.term,lesson.cno,lesson.course_no,lesson.cname, \
                     lesson.type,teacher.tname,lesson.classname,lesson.credit,lesson.xueshi,lesson.maxpeople \
                     from lesson,sc,teacher where lesson.cno=sc.cno and teacher.tno = lesson.tno and sc.sno='%s' and lesson.term='%s'" % (
            session['username'], term))
        result2 = search_2dimen(
            "select lesson.term,lesson.cno,lesson.course_no,lesson.cname,lesson.type,teacher.tname,lesson.classname,lesson.credit,lesson.xueshi,lesson.maxpeople \
            from lesson,student,teacher where lesson.type='通选' and student.sno='%s' and student.classname=lesson.classname and teacher.tno = lesson.tno and lesson.term='%s'" % (
                session['username'], term))
        return render_template('student/course_selection.html', datas=result,  datas2=result2,avatar_path = avatar_path,username = username[0][0])

'''
专业限选课
'''

@app.route('/xianxuan', methods=['GET', 'post'])
def xianxuan():
    if not Check_Login():
        return redirect(url_for("login"))
    else:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        if int(month) in [3,4,5,6,7,8]:
            term = str(year -1) + '-' + str(year) + '-' + '2'
        else:
            if int(month) in [1,2,9,10,11,12]:
                term = str(year) + '-' + str(year + 1) + '-' + '1'
        if (session['username'] == '201800800374'):
            avatar_path = '/static/images/avatar2.jpg'
        sql = "select sname from student where sno = '%s'" % session['username']
        print(sql)
        username = search(sql)
        result = search_2dimen("select lesson.term,lesson.cno,lesson.course_no,lesson.cname, \
                     lesson.type,teacher.tname,lesson.classname,lesson.credit,lesson.xueshi,lesson.maxpeople \
                     from lesson,sc,teacher where lesson.cno=sc.cno and teacher.tno = lesson.tno and sc.sno='%s' and lesson.term='%s'" % (
            session['username'], term))
        result2 = search_2dimen(
            "select lesson.term,lesson.cno,lesson.course_no,lesson.cname,lesson.type,teacher.tname,lesson.classname,lesson.credit,lesson.xueshi,lesson.maxpeople \
            from lesson,student,teacher where lesson.type='专业选修' and student.sno='%s' and student.classname=lesson.classname and teacher.tno = lesson.tno and lesson.term='%s'" % (
                session['username'], term))
        return render_template('student/course_selection.html', datas=result,  datas2=result2,avatar_path = avatar_path,username = username[0][0])

'''
选课函数
'''
@app.route('/add/<cno>,<course_no>,<time>', methods=['GET', 'post'])
def add(cno, course_no, time):
    if not Check_Login():
        return redirect(url_for("login"))
    data = dict(
        cno=cno,
        sno=session['username'],
        course_no=course_no,
        grade=-1,
        time=time,
    )
    try:
        insert_data("sc",data) #插入选课数据
        flash('成功选课')
    except:
        flash('已选此课程,请勿重复选课','warning')

    return redirect(url_for("course_selection"))

'''
退课函数
'''
@app.route('/del/<id>', methods=['GET'])
def delete(id):
    if not Check_Login():
        return redirect(url_for("login"))
    del_sc(id, "sc") #删除选课数据
    return redirect(url_for("course_selection"))


@app.route('/seegrade', methods=['GET', 'post'])
def grade():
    if not Check_Login():
        return redirect(url_for("login"))
    else:
        chengji =  search_2dimen(  # 查询已修读成绩
            "select lesson.cno,lesson.cname,lesson.course_no,lesson.term,lesson.type,lesson.credit,lesson.xueshi,sc.grade "
            "from lesson,sc where lesson.cno=sc.cno and lesson.course_no=sc.course_no and sc.sno='%s' and sc.grade!=-1 " %
            session['username'])

        info = search_2dimen(  # 查询本人信息
            "select * from student where sno='%s'" % session['username'])
        sno = session['username']
        name = info[0][1]
        dept = info[0][2]
        sex = info[0][3]
        classname = info[0][5]
        grade1 = sno[0:4] + '级'
        inschool = (sno[0:4]) + '/' + '09'
        outschool = str(int(sno[0:4]) + 4) + '/' + '06'
        if int(sno[0:4]) + 4 >= datetime.datetime.now().year:
            state = '在读'
        else:
            state = '离校'
        result1 =  search(
            "select sum(lesson.credit) from lesson,sc where lesson.cno=sc.cno and lesson.course_no=sc.course_no and sc.sno='%s' and lesson.type='必修' and sc.grade!=-1 " %
            session['username'])
        bixiu_xuefen = result1[0][0]


        result2 = search(
            "select sum(lesson.credit) from lesson,sc where lesson.cno=sc.cno and lesson.course_no=sc.course_no and sc.sno='%s' and lesson.type='专业选修' and sc.grade!=-1 " %
            session['username'])
        xianxuan_xuefen = result2[0][0]


        result3 = search(
            "select sum(lesson.credit) from lesson,sc where lesson.cno=sc.cno and lesson.course_no=sc.course_no and sc.sno='%s' and lesson.type='通选' and sc.grade!=-1 " %
            session['username'])

        tongxuan_xuefen = result3[0][0]
        zong_xuefen = bixiu_xuefen + xianxuan_xuefen + tongxuan_xuefen

        result4 = search(
            "select sum(lesson.credit*sc.grade) from lesson,sc where lesson.cno=sc.cno and lesson.course_no=sc.course_no and sc.sno='%s' and sc.grade!=-1 " %
            session['username'])

        print(result4[0])
        jidian = result4[0][0] / zong_xuefen
        jidian = round(jidian,2)

        if session['username'] == '201800800374':
            avatar_path = 'static/images/avatar2.jpg'
        sql = "select sname from student where sno = '%s'" % session['username']
        username = search(sql)

        return render_template('student/grade.html', datas=chengji,  sno=sno,
                               name=name, dept=dept, sex=sex, classname=classname, grade1=grade1, inschool=inschool,
                               outschool=outschool,
                               state=state, bixiu_xuefen=bixiu_xuefen, xianxuan_xuefen=xianxuan_xuefen,
                               tongxuan_xuefen=tongxuan_xuefen,
                               zong_xuefen = zong_xuefen, jidian=jidian,username = username[0][0],avatar_path = avatar_path)


'''
教师查看课程信息函数
'''

@app.route('/course_info', methods=['GET'])
def course_info():
    if not Check_Login():
        return redirect(url_for('login'))
    avatar_path = '/static/images/avatar_tea.jpg'

    result =  search_2dimen(
        "select term,cno,course_no,cname,type,classname,credit,xueshi,maxpeople from lesson where tno = '%s' " % session['username'])
    sql = "select tname from teacher where tno = '%s'" % session['username']
    username = search(sql)


    return render_template('teacher/course_info.html', datas=result,avatar_path = avatar_path,username = username[0][0])

'''
教师查看学生成绩函数
'''

@app.route('/stu_grade_manage')
def stu_grade_manage():
    if not Check_Login():
        return redirect(url_for("login"))
    username = session['username']

    avatar_path = '/static/images/avatar_tea.jpg'
    sql = "select lesson.cno,lesson.course_no,lesson.cname from lesson where lesson.tno = '%s' " % username
    result = search_2dimen(sql) #查询选了该门课的学生
    sql = "select tname from teacher where tno = '%s'" % session['username']
    username = search(sql)
    return render_template('teacher/select_course.html', datas=result,avatar_path = avatar_path,username = username[0][0])

'''
该函数的作用是，首先利用上个函数选择老师所教的具体课程
然后再查看相应的选这门课程的学生
'''

@app.route('/navi',methods=['POST','GET'])
def navi():
    if not Check_Login():
        return redirect(url_for("login"))
    username = session['username']

    avatar_path = '/static/images/avatar_tea.jpg'
    if request.method == 'POST':
        global glovar
        glovar = request.form['combobox'] #获取表单数据
    sql = "select lesson.cno,lesson.course_no,s.sno,s.sname,s.mname,s.classname,sc.grade from student s,sc,lesson where s.sno = sc.sno and lesson.cno = sc.cno and lesson.tno = '%s' and lesson.cname = '%s'" % (username,glovar)
    result = search_2dimen(sql)
    sql = "select tname from teacher where tno = '%s'" % session['username']
    username = search(sql)
    return render_template('teacher/change_grade.html', datas=result, avatar_path=avatar_path,username = username[0][0])


#上传页面
@app.route('/writesc',methods=['GET','PSOT'])
def writesc():
    if not Check_Login():
        return redirect(url_for("login"))
    username = session['username']

    avatar_path = '/static/images/avatar_tea.jpg'
    sql = "select cname from lesson where tno = '%s'" % username
    result = search_2dimen(sql)
    username = search( "select tname from teacher where tno = '%s' " % username)
    return render_template('teacher/writesc.html',username = username[0][0],avatar_path = avatar_path,result =result)

'''
成绩修改函数
'''
@app.route('/altergrade', methods=['POST','GET'])
def altergrade():
    if not Check_Login():
        return redirect(url_for("login"))

    data = dict( #将数据组成字典传入 数据库
        cno=request.form['cnos'],
        course_no=request.form['course_nos'],
        sno=request.form['snos'],
        grade=request.form['grades'],
    )

    grade = request.form['grades'],
    if float(grade[0]) > 100 or float(grade[0]) <  0: #数据判定
        flash('成绩处于异常区间，修改无效')
        return redirect(url_for("navi")) #重定向
    else:
        alterscore(data) #数据库进行数据修改
        flash('成绩修改成功')
        return redirect(url_for("navi"))
'''
课程管理函数
'''
@app.route('/courseManage', methods=['GET', 'post'])
def courseManage():
    if not Check_Login():
        return redirect(url_for("login"))
    else:
        term = "2019-2020-1"
        #筛选出各个信息传入html界面
        result2 = search_2dimen("select cno from lesson")
        result3 = search_2dimen("select distinct course_no from lesson")
        result4 = search_2dimen("select distinct type from lesson")
        result5 = search_2dimen("select  tname from teacher ")
        result6 = search_2dimen("select classname from class")
        result7 = search_2dimen("select distinct term from lesson")
        result8 = search("select distinct cname from lesson")
        result = search_2dimen(
            "select lesson.term,lesson.cno,lesson.course_no,lesson.cname,lesson.type,teacher.tname,lesson.classname,lesson.credit,lesson.xueshi,lesson.maxpeople from lesson,teacher where  "
            " lesson.tno = teacher.tno " )

        username = search("select jname from jiaowuyuan where jno = '%s'" % session['username'])

        avatar_path = '/static/images/avatar_adm.jpg'
        return render_template('jiaowuyuan/course_manage.html', datas=result, datas2=result2,
                               datas3=result3,  datas4=result4,  datas5=result5,
                                datas6=result6,  datas7=result7,
                               datas8=result8,  term=term,avatar_path = avatar_path,username = username[0][0])

@app.route('/student', methods=['GET', 'post'])
def student():
    if not Check_Login():
        return redirect(url_for("login"))
    mname = ""
    sno = ""
    sname = ""
    classname = ""
    result2 =  search_2dimen("select classname from class")
    result3 = search_2dimen("select mname from major")
    print(result2,result3)
    result = search_2dimen(
        "select student.sno,student.sname,student.mname,student.ssex,student.sbirth,student.classname from student")
    username = search("select jname from jiaowuyuan where jno = '%s'" % session['username'])

    avatar_path = '/static/images/avatar_adm.jpg'
    return render_template('jiaowuyuan/stu_manage.html', datas=result,  datas2=result2,
                           datas3=result3,  mname2=mname, classname2=classname, sno2=sno, sname2=sname,username = username[0][0],avatar_path = avatar_path)



@app.route('/updateStudent', methods=['GET', 'post'])
def updateStudent():
    if not Check_Login():
        return redirect(url_for("login"))
    if request.method == 'POST':
        data = dict( #讲数据组成字典
            sno=request.form['sno'],
            sname=request.form['sname'],
            mname=request.form['AreaId'],
            birth=request.form['birth'],
            ssex=request.form['ssex'],
            classname=request.form['banji']
        )
    updatestu(data)  #更新学生信息
    return redirect(url_for("student"))


@app.route('/addstu', methods=['GET', 'post'])
def addstu():
    if not Check_Login():
        return redirect(url_for("login"))
    else:
        data = dict( #数据组成字典
            sno=request.form['sno'],
            sname=request.form['sname'],
            mname=request.form['mname'],
            ssex=request.form['ssex'],
            birth=request.form['birth'],
            classname=request.form['classname'],
            spw=generate_password_hash('111111')
        )
        insertstu(data) #新增学生信息
        return redirect(url_for("student"))


@app.route('/select', methods=['GET', 'post'])
def select():
    if not Check_Login():
        return redirect(url_for("login"))
    temp = []
    if "sname" in request.args:
        sname = request.args["sname"]
        if sname != "":
            temp.append("sname like '%%%s%%'" % sname)

    if "sno" in request.args:
        sno = request.args["sno"]
        if sno != "":
            temp.append("sno = '%s'" % sno)

    if "classname" in request.args:
        classname = request.args["classname"]
        if classname != "":
            temp.append("classname = '%s'" % classname)

    if "mname" in request.args:
        mname = request.values.get("mname")
        if mname != "":
            temp.append("mname = '%s'" % mname)
    sql = "select student.sno,student.sname,student.mname,student.ssex,student.sbirth,student.classname from student"
    if len(temp) > 0:
        sql = sql + " where " + " and ".join(temp)

    result =  search_2dimen(sql)
    result2 = search_2dimen("select classname from class")
    result3 =  search_2dimen("select mname from major")
    print(classname)

    avatar_path = '/static/images/avatar_adm.jpg'
    sql = "select jname from jiaowuyuan where jno = '%s'" % session['username']
    username = search(sql)
    return render_template('jiaowuyuan/stu_manage.html', datas=result, datas2=result2,
                           datas3=result3,  mname2=mname, classname2=classname, sno2=sno, sname2=sname,username = username[0][0],avatar_path = avatar_path)


#删除学生信息
@app.route('/delstu/<id>', methods=['GET'])
def deletestu(id):
    if not Check_Login():
        return redirect(url_for("login"))
    delete_stu(id)
    flash('删除成功')
    return redirect(url_for("student"))

#更新课程信息
@app.route('/updatelesson', methods=['GET', 'post'])
def updatelesson():
    if not Check_Login():
        return redirect(url_for("login"))
    data = dict(
        cno=request.form['cno'],
        term=request.form['term'],
        course_no =request.form['cnoth'],
        cname=request.form['cname'],
        type=request.form['type'],
        tname=request.form['tname'],
        classname=request.form['classname'],
        credit=request.form['credit'],
        xueshi=request.form['period'],
        maxpeople=request.form['peonum'],
    )

    update_lesson(data)

    return redirect(url_for("courseManage"))

#筛选课程信息函数
@app.route('/screenlesson', methods=['GET', 'post'])
def screenlesson():
    if not Check_Login():
        return redirect(url_for("login"))

    temp = []
    if "term" in request.args:
        term = request.args["term"]
        if term != "":
            temp.append("term like '%%%s%%'" % term)

    if "cno" in request.args:
        cno = request.args["cno"]
        if cno != "":
            temp.append("cno = '%s'" % cno)

    if "tname" in request.args:
        tname = request.args["tname"]
        if tname != "":
            temp.append("tname = '%s'" % tname)

    if "cnoth" in request.args:
        course_no = request.args["cnoth"]
        if course_no != "":
            temp.append("course_no = '%s'" % course_no)

    if "classname" in request.args:
        classname = request.values.get("classname")
        if classname != "":
            temp.append("classname = '%s'" % classname)
    if "course_name" in request.args:
        course_name = request.args['course_name']
        if course_name != "":
            temp.append("cname like '%%%s%%'" % course_name)

    sql = "SELECT lesson.term,lesson.cno,lesson.course_no,lesson.cname,lesson.type,teacher.tname,lesson.classname,lesson.credit,lesson.xueshi,lesson.maxpeople FROM lesson,teacher where lesson.tno = teacher.tno"

    if len(temp) > 0:
        sql = sql + " and " + " and ".join(temp)
    print(sql)
    #查询相应的信息，传入网页
    result = search_2dimen(sql)
    result2 = search_2dimen("select cno from lesson")
    result3 = search_2dimen("select distinct course_no from lesson")
    result4 = search_2dimen("select distinct type from lesson")
    result5 = search_2dimen("select distinct tname from teacher")
    result6 = search_2dimen("select classname from class")
    result7 = search_2dimen("select distinct term from lesson")
    result8 = search_2dimen("select distinct cname from lesson")
    print(result)
    avatar_path = '/static/images/avatar_adm.jpg'
    sql = "select jname from jiaowuyuan where jno = '%s'" % session['username']
    username = search(sql)
    return render_template('jiaowuyuan/course_manage.html', datas=result,  datas2=result2,
                           datas3=result3,  datas4=result4,  datas5=result5,datas6=result6,  datas7=result7,datas8=result8,
                           cno=cno, cnoth=course_no, type=type, tname=tname, classname=classname, term=term,username = username[0][0],avatar_path = avatar_path)

#excel上传函数
@app.route("/upload", methods=['GET', 'POST'])
def upload():

    course_name = request.form['combobox']
    cno = search("select cno from lesson where cname = '%s'" % course_name) #获取课程号
    course_no = search("select course_no from lesson where cname = '%s'" % course_name)#获取课序号
    term = search("select term from lesson where cname = '%s'" % course_name)#获取学期
    if request.method == 'POST':
        file = request.files["file"] #获取文件
        base_path = path.abspath(path.dirname(__file__)) #获取路径
        upload_path = path.join(base_path, 'static/upload/')
        file_name = upload_path + secure_filename(file.filename)
        file.save(file_name)  #获取文件

        workbook = xlrd.open_workbook(file_name) #打开excel文件
        Data_sheet = workbook.sheets()[0] #获取excel的一个sheet
        nrows = Data_sheet.nrows          #获取行数和列数
        ncols = Data_sheet.ncols
        list = []
        for i in range(1, nrows):
            rowlist = []
            for j in range(ncols):
                rowlist.append(Data_sheet.cell_value(i, j)) #用二重循环取出sheet中的数据
            list.append(rowlist) #加入列表

        for a in list: #遍历列表
            data = dict( #将每一行数据租场一个字典，准备送入数据库
                cno = cno[0][0],
                course_no = course_no[0][0],
                score = a[4],
                sno = str(a[0])[:-2],
                time = term[0][0]
            )
            print(data['cno'],data['sno'])
            insert_stu_grade(data)
        flash('写入成绩成功')

        username = session['username']

        avatar_path = '/static/images/avatar_tea.jpg'
        sql = "select lesson.cno,lesson.course_no,lesson.cname from lesson where lesson.tno = '%s' " % username
        result = search_2dimen(sql)
        sql = "select tname from teacher where tno = '%s'" % session['username']
        username = search(sql)
        return render_template('teacher/select_course.html', datas=result, avatar_path=avatar_path,
                               username=username[0][0])


        return redirect(url_for('upload'))
    return render_template('teacher/change_grade.html')


@app.route('/addgrade2',methods=['POST'])
def addgrade2():
    data = dict (
        cno = request.form['cno2'],
        sno = (search("select sno from student where sname = '%s' " % request.form['sname']))[0][0],
        score = request.form['grade'],
        time = (search("select term from lesson where cno = '%s'" % request.form['cno2']))[0][0],
        course_no = request.form['course_no']
    )
    insert_stu_grade(data)

    return redirect(url_for('navi'))
@app.route('/student_info', methods=['GET'])
def student_info():
    if not Check_Login():
        return redirect(url_for('login'))

    username = session['username']
    sql = "select s.sname,s.mname,s.classname,lesson.cname from student s,lesson,sc where s.sno = sc.sno and " \
          "sc.cno = lesson.cno and lesson.tno = '%s'" % username
    result = search_2dimen(sql)

    avatar_path = '/static/images/avatar_tea.jpg'
    sql = "select distinct tname from teacher where tno = '%s'" % session['username']
    username = search(sql)
    sql = "select lesson.cname from lesson where tno = '%s'" % session['username']
    course = search_2dimen(sql)
    student_name = search_2dimen("select distinct sname from  sc,lesson,student where sc.cno = lesson.cno and sc.sno = student.sno and lesson.tno = '%s' " % session['username'])
    return render_template('teacher/student_info.html', result = result,username = username[0][0],avatar_path = avatar_path,course = course,
                           student_name = student_name)
@app.route('/screenstudent',methods=['GET','POST'])
def screenstudent():
    if not Check_Login():
        return redirect(url_for("login"))

    temp = []
    if "stu_name" in request.args:
        stu_name = request.args["stu_name"]
        if stu_name != "" and stu_name != '全部':
            temp.append("sname ='%s' " % stu_name)

    if "course_name" in request.args:
        course_name = request.args["course_name"]
        if course_name != "" and course_name!= '全部':
            temp.append("cname ='%s' " % course_name)

    sql = "select sname,mname,student.classname,lesson.cname from student,lesson,sc where student.sno = sc.sno and sc.cno = lesson.cno and tno = '%s'" % session['username']
    if len(temp) > 0:
        sql = sql + " and " + " and ".join(temp)
    print(sql)
    result = search_2dimen(sql)

    return render_template('teacher/student_info.html',result = result)

@app.route('/addlesson', methods=['GET', 'post'])
def addlesson():
    if not Check_Login():
        return redirect(url_for("login"))
    data = dict(
        term=request.form['term'],
        cno=request.form['cno'],
        course_no=request.form['cnoth'],
        cname=request.form['cname'],
        type=request.form['type'],
        tname=request.form['tname'],
        classname=request.form['classname'],
        credit=request.form['credit'],
        xueshi=request.form['period'],
        maxpeople=request.form['peonum'],

    )
    insert_course(data)
    return redirect(url_for("courseManage"))

#删除课程信息
@app.route('/dellesson/<cno>,<course_no>', methods=['GET'])
def dellesson(cno, course_no):
    if not Check_Login():
        return redirect(url_for("login"))
    del_course(cno,course_no) #删除课程信息
    flash('删除成功')
    return redirect(url_for("courseManage"))

if __name__ == "__main__":
    app.run(debug = True)