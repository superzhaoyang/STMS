#encoding=utf-8
import pymssql


def conn():
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS') #服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    return connect

def create_table():

    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute("create table stu(id varchar(20),name char(20),age int)")  # 执行sql语句
    connect.commit()  # 提交
    cursor.close()  # 关闭游标
    connect.close()  # 关闭连接

def add_data():
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print('连接成功')

    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行

    sql = "insert into sc values('555','201800800374',1,'12','1')"
    sql2 = "insert into student values ('1','1','1','1','1999-09-18','1','1')"
    cursor.execute(sql2)  # 执行sql语句
    connect.commit()
    cursor.close()
    connect.close()
def insert_data(type,data):
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print('连接成功')
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    sql = "insert into "+ type + " values('" + data['cno'] +"','"+data['sno']+"'," + str(data['grade'])+",'"+data['time']+"','" +data['course_no']+"')"
    print(sql)
    res = cursor.execute(sql)  # 执行sql语句
    print(res)
    connect.commit()
    cursor.close()
    connect.close()
def insertstu(data):
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print('连接成功')

    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    print(12346546)
    sql = "insert into student values ('%s','%s','%s', '%s','%s', '%s','%s')  " % (
        data['sno'],data['sname'], data['mname'],data['ssex'], data['birth'], data['classname'], data['spw'])
    cursor.execute(sql)  # 行sql语句
    connect.commit()
    cursor.close()
    connect.close()
def search(sql):
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(sql)  # 执行sql语句
    row = cursor.fetchone()  # 读取查询结果,
    list = []
    # while row:  # 循环读取所有结果
    #     print(  row[0]  ,row[1].strip(),row[2])  # 输出结果
    #     list.append(row[0])
    #     list.append(row[1])
    #     list.append(row[2])
    #     list.append(row[3])
    #     list.append(row[4])
    #     list.append(row[5])
    #     list.append(row[6])
    #
    #     row = cursor.fetchone()

    list.append(row)
    cursor.close()
    connect.close()

    return list


def search_2dimen(sql):
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(sql)  # 执行sql语句
    row = cursor.fetchone()  # 读取查询结果,
    list = []
    while row:  # 循环读取所有结果
        #print(row[0], row[1].strip(), row[2])  # 输出结果
        list.append(row)
        row = cursor.fetchone()
    cursor.close()
    connect.close()
    return list
def del_course(cno,course_no):
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")

    cursor = connect.cursor()  # 创建
    sql = "delete from lesson where cno = '%s' and course_no = '%s'" %(cno,course_no)
    print(sql)
    cursor.execute(sql)  # 行sql语句
    connect.commit()
    cursor.close()
    connect.close()

def insert_course(data):
    # data = dict(
    #     term=request.form['term'],
    #     cno=request.form['cno'],
    #     cnoth=request.form['cnoth'],
    #     cname=request.form['cname'],
    #     type=request.form['type'],
    #
    #     classname=request.form['classname'],
    #     credit=request.form['credit'],
    #     period=request.form['period'],
    #     peonum=request.form['peonum'],
    #    tname = request.form['tname'],

    # )
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")

    sql = "select tno from teacher where tname = '%s'" % (data['tname'])
    tno = search(sql)
    cursor = connect.cursor()
    sql = "insert into lesson values ('%s','%s','%s','%s','%s','%s',%f,%d,%d,'%s')" % (
        data['term'],data['cno'],data['course_no'],data['cname'],data['type'],data['classname'],float(data['credit']),
        int(data['xueshi']),int(data['maxpeople']),tno[0][0])


    cursor.execute(sql)
    connect.commit()
    cursor.close()
    connect.close()
def update():
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    sql = "update stu set name = 'superzhaoyang' where name = 'super'"
    cursor.execute(sql)  # 执行sql语句
    sql = "select id,name,age from stu"
    cursor.execute(sql)  # 执行sql语句
    row = cursor.fetchone()  # 读取查询结果,
    while row:  # 循环读取所有结果
        print(row[0], row[1].strip(), row[2])  # 输出结果
        row = cursor.fetchone()
    connect.commit()
    cursor.close()
    connect.close()

def updatepassword(identity,password,username):
    connect = conn()
    c = connect.cursor()
    if identity == 'student':
        c.execute("update student set spw='%s' where sno='%s'" % (password, username))
    elif identity == 'jiaowuyuan':
        c.execute("update jiaowuyuan set jpassword='%s' where jno='%s'" % (password,username))
    elif identity == 'teacher':
        c.execute("update teacher set tpw='%s' where tno='%s'" % (password, username))
    connect.commit()
    c.close()
    connect.close()
def updatestu(data):
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")


    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    print(12346546)
    sql = "update student set sname = '%s', mname = '%s',ssex = '%s', sbirth = '%s', classname = '%s'  where sno = '%s' " % (
        data['sname'], data['mname'], data['ssex'], data['birth'], data['classname'], data['sno'])
    cursor.execute(sql)  # 行sql语句
    connect.commit()
    cursor.close()
    connect.close()
def delete_stu(sno):
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    sql = "delete from student where sno = '%s'" % sno
    cursor.execute(sql)  # 执行sql语句
    connect.commit()
    cursor.close()
    connect.close()


def del_sc(cno,table):
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")
    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行

    sql = "delete sc where cno = "+ cno
    cursor.execute(sql)
    connect.commit()
    cursor.close()
    connect.close()


def alterscore(data):
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")

    cursor = connect.cursor()  # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    sql = "update sc set grade = %f  where sno = '%s' and cno = '%s' " % (float(data['grade']),data['sno'],data['cno'])
    cursor.execute(sql)  # 执行sql语句

    connect.commit()
    cursor.close()
    connect.close()


def update_lesson(data):
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")

    cursor = connect.cursor()

    teacher_tno = search("select tno from teacher where tname = '%s'" % data['tname'])
    print(teacher_tno)
    sql = "update lesson set term = '%s',course_no = '%s',cname = '%s',type = '%s',classname = '%s'," \
          "credit = %f,xueshi = %d,maxpeople = %d,tno = '%s' where cno = '%s'" % (data['term'],data['course_no'],data['cname'],data['type'],data['classname'],float(data['credit']),int(data['xueshi']),int(data['maxpeople']),teacher_tno[0][0],data['cno']  )
    cursor.execute(sql)  # 执行sql语句

    connect.commit()
    cursor.close()
    connect.close()


def insert_stu_grade(data):
    connect = pymssql.connect('(local)', 'sa', 'superzhaoyang1', 'TSMS')  # 建立连接
    if connect:
        print("连接成功!")


    sql = "insert into sc values ('%s','%s',%f,'%s','%s')" %(data['cno'],data['sno'],float(data['score']),data['time'],data['course_no'])
    print(sql)
    cursor = connect.cursor()
    cursor.execute(sql)  # 执行sql语句
    connect.commit()
    cursor.close()
    connect.close()
if __name__ == '__main__':
    delete()