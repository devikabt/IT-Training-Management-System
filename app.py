from flask import Flask, render_template, flash, redirect, url_for, request, session, logging
from flask_mysqldb import MySQL
from wtforms import Form,  TextAreaField, PasswordField, validators, RadioField, SelectField, IntegerField, Field
from datetime import datetime, time
from wtforms.fields import DateField, TimeField, StringField
from wtforms.validators import InputRequired
from passlib.hash import sha256_crypt

from functools import wraps
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'trainingManagement'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


mysql = MySQL(app)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Nice try, Tricks don\'t work, bud!! Please Login :)', 'danger')
            return redirect(url_for('login'))
    return wrap

def is_trainor(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['prof'] == 3:
            return f(*args, **kwargs)
        else:
            flash('You are probably not a trainor!!, Are you?', 'danger')
            return redirect(url_for('login'))
    return wrap

def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['prof'] == 1:
            return f(*args, **kwargs)
        else:
            flash('You are probably not an admin!!, Are you?', 'danger')
            return redirect(url_for('login'))
    return wrap

def is_recep_level(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['prof'] <= 2:
            return f(*args, **kwargs)
        else:
            flash('You are probably not an authorised to view that page!!', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute('SELECT * FROM info WHERE username = %s', [username])
        #print(result)
        if result>0:
            data = cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                session['prof'] = data['prof']
                flash('You are logged in', 'success')
                if session['prof'] == 1:
                    return redirect(url_for('adminDash'))
                if session['prof'] == 3:
                    return redirect(url_for('trainorDash'))
                if session['prof'] == 2:
                    return redirect(url_for('recepDash'))
                return redirect(url_for('memberDash', username = username))
            else:
                error = 'Invalid login'
                return render_template('login.html', error = error)

            cur.close();
        else:
            error = 'Username NOT FOUND'
            return render_template('login.html', error = error)

    return render_template('login.html')


class ChangePasswordForm(Form):
    old_password = PasswordField('Existing Password')
    new_password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords aren\'t matching pal!, check \'em')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/update_password/<string:username>', methods = ['GET', 'POST'])
def update_password(username):
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        new = form.new_password.data
        entered = form.old_password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM info WHERE username = %s", [username])
        old = (cur.fetchone())['password']
        if sha256_crypt.verify(entered, old):
            cur.execute("UPDATE info SET password = %s WHERE username = %s", (sha256_crypt.encrypt(new), username))
            mysql.connection.commit()
            cur.close()
            flash('New password will be in effect from next login!!', 'info')
            return redirect(url_for('memberDash', username = session['username']))
        cur.close()
        flash('Old password you entered is wrong!!, try again', 'warning')
    return render_template('updatePassword.html', form = form)

@app.route('/adminDash')
@is_logged_in
@is_admin
def adminDash():
    return render_template('adminDash.html')

values = []
choices = []
expertises = []

class AddTrainorForm(Form):
    name = StringField('Name', [validators.Length(min = 1, max = 100)])
    username = StringField('Username', [validators.InputRequired(), validators.NoneOf(values = values, message = "Username already taken, Please try another")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords aren\'t matching pal!, check \'em')
    ])
    confirm = PasswordField('Confirm Password')
    expertise = SelectField('expertise', choices = expertises)
    street = StringField('Street', [validators.Length(min = 1, max = 100)])
    city = StringField('City', [validators.Length(min = 1, max = 100)])
    prof = 3
    phone = StringField('Phone', [validators.Length(min = 1, max = 100)])


@app.route('/addTrainor', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def addTrainor():
    values.clear()
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT username FROM info")
    b = cur.fetchall()
    for i in range(q):
        values.append(b[i]['username'])

    q = cur.execute("SELECT course_name FROM course")
    b = cur.fetchall()
    for i in range(q):
        expertises.append(b[i]['course_name'])

    cur.close()
    form = AddTrainorForm(request.form)
    if request.method == 'POST' and form.validate():
        #app.logger.info("setzdgxfhcgjvkhbjlkn")
        name = form.name.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        expertise = form.expertise.data
        street = form.street.data
        city = form.city.data
        prof = 2
        phone = form.phone.data

        cur = mysql.connection.cursor()


        cur.execute("SELECT id FROM course WHERE course_name = %s", [expertise])
        courseidresult = cur.fetchall()
        courseid_val = courseidresult[0]['id']

        cur.execute("INSERT INTO info(name, username, password, street, city, prof, phone) VALUES(%s, %s, %s, %s, %s, %s, %s)", (name, username, password, street, city, 3,phone))
        cur.execute("INSERT INTO trainors(username, expertise, courseID) VALUES(%s, %s, %s)", (username, expertise, courseid_val))
        mysql.connection.commit()
        cur.close()
        expertises.clear()
        flash('You recruited a new Trainor!!', 'success')
        return redirect(url_for('adminDash'))
    return render_template('addTrainor.html', form=form)



class DeleteRecepForm(Form):
    username = SelectField(u'Choose which one you wanted to delete', choices=choices)



@app.route('/deleteTrainor', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def deleteTrainor():
    choices.clear()
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT username FROM trainors")
    b = cur.fetchall()
    for i in range(q):
        tup = (b[i]['username'],b[i]['username'])
        choices.append(tup)
    form = DeleteRecepForm(request.form)
    if len(choices)==1:
        flash('You cannot remove your only Tutor!!', 'danger')
        return redirect(url_for('adminDash'))
    if request.method == 'POST':
        username = form.username.data
        q = cur.execute("SELECT username FROM trainors WHERE username != %s", [username])
        b = cur.fetchall()
        new = b[0]['username']
        cur.execute("UPDATE members SET trainor = %s WHERE trainor = %s", (new, username))
        cur.execute("DELETE FROM trainors WHERE username = %s", [username])
        cur.execute("DELETE FROM info WHERE username = %s", [username])
        cur.execute("DELETE FROM batch WHERE trainername = %s", [username])
        mysql.connection.commit()
        cur.close()
        choices.clear()
        flash('You removed your Trainor!!', 'success')
        return redirect(url_for('adminDash'))
    return render_template('deleteRecep.html', form = form)


@app.route('/addRecep', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def addRecep():
    values.clear()
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT username FROM info")
    b = cur.fetchall()
    for i in range(q):
        values.append(b[i]['username'])
    cur.close()
    form = AddTrainorForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        street = form.street.data
        city = form.city.data
        phone = form.phone.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO info(name, username, password, street, city, prof, phone) VALUES(%s, %s, %s, %s, %s, %s, %s)", (name, username, password, street, city, 2,phone))
        cur.execute("INSERT INTO receps(username) VALUES(%s)", [username])
        mysql.connection.commit()
        cur.close()
        flash('You recruited a new Receptionist!!', 'success')
        return redirect(url_for('adminDash'))
    return render_template('addRecep.html', form=form)

class DeleteRecepForm(Form):
    username = SelectField(u'Choose which one you wanted to delete', choices=choices)



@app.route('/deleteRecep', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def deleteRecep():
    choices.clear()
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT username FROM receps")
    b = cur.fetchall()
    for i in range(q):
        tup = (b[i]['username'],b[i]['username'])
        choices.append(tup)
    if len(choices)==1:
        flash('You cannot remove your only receptionist!!', 'danger')
        return redirect(url_for('adminDash'))
    form = DeleteRecepForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        cur.execute("DELETE FROM receps WHERE username = %s", [username])
        cur.execute("DELETE FROM info WHERE username = %s", [username])
        mysql.connection.commit()
        cur.close()
        choices.clear()
        flash('You removed your receptionist!!', 'success')
        return redirect(url_for('adminDash'))
    return render_template('deleteRecep.html', form = form)

@app.route('/addCourse')
@is_logged_in
@is_admin
def addCourse():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM course")
    data = cur.fetchall()
    cur.close()
    print(data)
    return render_template('course.html', course = data)


@app.route('/insert', methods = ['POST'])
@is_logged_in
@is_admin
def insert():

    if request.method == "POST":
        flash("Data Inserted Succesfully")
        courseduration = request.form['courseduration']
        coursename = request.form['coursename']
        coursedescription = request.form['coursedescription']
        courseprice = request.form['courseprice']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO course (course_name, course_description, course_duration, course_price) VALUES (%s, %s, %s,%s)", (coursename, coursedescription, courseduration, courseprice))
        mysql.connection.commit()
        return redirect(url_for('addCourse'))
    
@app.route('/update', methods = ['POST', 'GET', 'PUT'])
@is_logged_in
@is_admin
def update():
    if request.method == 'POST':
    
        id_data = request.form['id']
        courseduration = request.form['courseduration']
        coursename = request.form['coursename']
        coursedescription = request.form['coursedescription']
        courseprice = request.form['courseprice']

        cur = mysql.connection.cursor()
        cur.execute(""" 
        UPDATE course
        SET course_name =%s, course_description=%s, course_duration=%s, course_price=%s
        WHERE id = %s 
        """, (coursename, coursedescription, courseduration, courseprice, id_data) )

        cur.execute(""" 
        UPDATE batch
        SET coursename =%s, courseduration=%s
        WHERE courseID = %s 
        """, (coursename, courseduration, id_data) )
        
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('addCourse'))
    
@app.route('/delete/<string:id_data>', methods = ['POST', 'GET', 'DELETE'])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("SELECT course_name FROM course WHERE id = %s", [id_data])
    result = cur.fetchall()
    course_name = result[0]['course_name']
    cur.execute("DELETE FROM course WHERE id = %s", [id_data])
    cur.execute("DELETE FROM batch WHERE coursename = %s", [course_name])
    flash("Deleted Successfully")
    mysql.connection.commit()
    return redirect(url_for('addCourse'))

choices4 = []
choices5 = []
choices6 = []
@app.route('/addBatch')
@is_logged_in
@is_admin
def addBatch():
    choices5.clear()
    choices4.clear()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM batch")
    batch = cur.fetchall()
    cur.execute("SELECT * FROM course")
    cours = cur.fetchall()
    cur.close()
    return render_template('addBatch.html',  batch = batch,  cours = cours)

@app.route('/insertBatchForCourse/<string:course_name>/<string:course_duration>', methods = ['GET', 'POST'])
@is_logged_in
@is_admin
def insertBatchForCourse(course_name, course_duration):
    course_name = course_name
    course_duration = course_duration
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT username FROM trainors where expertise = %s",[course_name])
    b = cur.fetchall()
    for i in range(q):
        tup = (b[i]['username'],b[i]['username'])
        choices5.append(tup)
    return render_template('addBatchForCourse.html', course_name = course_name, course_duration = course_duration, choices5 = choices5)

@app.route('/insertBatch', methods = ['POST'])
@is_logged_in
@is_admin
def insertBatch():
    
    if request.method == "POST":
        flash("Data Inserted Succesfully")
        batchname = request.form['batchname']
        coursename = request.form['coursename']
        trainername = request.form['trainername']
        courseduration = request.form['courseduration']
        batchstartdate = request.form['batchstartdate']
        batchenddate = request.form['batchenddate']
        batchtime = request.form['time-range']
        cur = mysql.connection.cursor()
        cur.execute("SELECT id from course where course_name=%s", [coursename])
        result = cur.fetchall()
        id_val = result[0]['id']
        cur.execute("INSERT INTO batch (batchname, coursename, courseID, trainername, courseduration, batchstartdate, batchenddate,  batchtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (batchname, coursename, id_val, trainername, courseduration, batchstartdate, batchenddate,  batchtime))
        mysql.connection.commit()
        return redirect(url_for('addBatch'))
    
@app.route('/updateBatch', methods = ['POST', 'GET', 'PUT'])
@is_logged_in
@is_admin
def updateBatch():
    if request.method == 'POST':
    
        id = request.form['id']
        batchname = request.form['batchname']
        coursename = request.form['coursename']
        trainername = request.form['trainername']
        batchstartdate = request.form['batchstartdate']
        batchenddate = request.form['batchenddate']
        batchtime = request.form['batchtime']

        cur = mysql.connection.cursor()
       
        p = cur.execute("SELECT username FROM trainors WHERE expertise = %s", [coursename])
        enteredT = []
        q = cur.fetchall()
        for i in range(p):
            enteredT.append(q[i]['username'])
            

        if trainername in enteredT:
            cur.execute("SELECT id FROM course WHERE course_name = %s", [coursename])
            result = cur.fetchall()
            id_val = result[0]['id']
            cur.execute(""" 
            UPDATE batch
            SET batchname =%s, coursename=%s, courseID=%s, trainername=%s, batchstartdate=%s, batchenddate=%s, batchtime=%s
            WHERE id = %s 
            """, (batchname, coursename, id_val, trainername,  batchstartdate, batchenddate, batchtime, id) )

            cur.execute("""
            UPDATE members
            SET batch =%s WHERE coursename = %s AND trainor = %s """, (batchname, coursename, trainername) )

            cur.execute("""
            UPDATE progress
            SET batchname =%s WHERE batchID = %s  """, (batchname, id) )

            flash("Data Updated Successfully")
            mysql.connection.commit()
        else:
            flash("Invalid TrainerName")
        return redirect(url_for('addBatch'))
    
@app.route('/deleteBatch/<string:id>', methods = ['POST', 'GET', 'DELETE'])
def deleteBatch(id):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM batch WHERE id = %s", [id])
    flash("Deleted Successfully")
    mysql.connection.commit()
    return redirect(url_for('addBatch'))

choices3 = []

choices2 = []

class AddMemberForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.InputRequired(), validators.NoneOf(values = values, message = "Username already taken, Please try another")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    plan = StringField('Plan', [validators.Length(min = 1, max = 100)])
    trainor = StringField('Trainor', [validators.Length(min = 1, max = 100)])
    batch = StringField('Batch', [validators.Length(min = 1, max = 100)])
    street = StringField('Street', [validators.Length(min = 1, max = 100)])
    city = StringField('City', [validators.Length(min = 1, max = 100)])
    phone = StringField('Phone', [validators.Length(min = 1, max = 100)])

@app.route('/addMemberr/<string:trainername>/<string:coursename>/<string:batchname>', methods = ['GET', 'POST'])
@is_logged_in
@is_recep_level
def addMemberr(trainername, coursename, batchname):
    
    cur = mysql.connection.cursor()
    
    q = cur.execute("SELECT username FROM info")
    b = cur.fetchall()
    for i in range(q):
        values.append(b[i]['username'])
        
    cur.close()
    
    form = AddMemberForm(request.form)
    form.plan.data = coursename
    form.trainor.data = trainername
    form.batch.data = batchname
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        street = form.street.data
        city = form.city.data
        phone = form.phone.data
        plan = form.plan.data
        trainor = form.trainor.data
        batch = form.batch.data
        cur = mysql.connection.cursor()

        cur.execute("SELECT id FROM course WHERE course_name = %s", [coursename])
        courseidresult = cur.fetchall()
        courseid_val = courseidresult[0]['id']

        cur.execute("SELECT id FROM batch WHERE batchname = %s", [batchname])
        batchidresult = cur.fetchall()
        batchid_val = batchidresult[0]['id']

        cur.execute("INSERT INTO info(name, username, password, street, city, prof, phone) VALUES(%s, %s, %s, %s, %s, %s, %s)", (name, username, password, street, city, 4,phone))
        cur.execute("INSERT INTO members(username, coursename, trainor, batch, courseID, batchID) VALUES(%s, %s, %s, %s, %s, %s)", (username, plan, trainor, batch, courseid_val, batchid_val))
        mysql.connection.commit()
        cur.close()
        flash('You added a new member!!', 'success')
        if(session['prof']==1):
            return redirect(url_for('adminDash'))
        return redirect(url_for('recepDash'))
    return render_template('addMember.html', form=form)



@app.route('/addMember', methods = ['GET', 'POST'])
@is_logged_in
@is_recep_level
def addMember():
    choices.clear()
    choices2.clear()
    cur = mysql.connection.cursor()
    
    q = cur.execute("SELECT username FROM info")
    b = cur.fetchall()
    for i in range(q):
        values.append(b[i]['username'])
    
    q = cur.execute("SELECT CourseName FROM courseregister")
    b = cur.fetchall()
    for i in range(q):
        tup = (b[i]['CourseName'],b[i]['CourseName'])
        choices.append(tup)
    
    q = cur.execute("SELECT TrainerName FROM courseregister")
    b = cur.fetchall()
    for i in range(q):
        tup = (b[i]['TrainerName'],b[i]['TrainerName'])
        choices2.append(tup)
            
        
    cur.close()
    
    form = AddMemberForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        street = form.street.data
        city = form.city.data
        phone = form.phone.data
        plan = form.plan.data
        trainor = form.trainor.data
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO info(name, username, password, street, city, prof, phone) VALUES(%s, %s, %s, %s, %s, %s, %s)", (name, username, password, street, city, 4,phone))
        cur.execute("INSERT INTO members(username, plan, trainor) VALUES(%s, %s, %s)", (username, plan, trainor))
        mysql.connection.commit()
        cur.close()
        choices2.clear()
        choices.clear()
        flash('You added a new member!!', 'success')
        if(session['prof']==1):
            return redirect(url_for('adminDash'))
        return redirect(url_for('recepDash'))
    return render_template('addMember.html', form=form)


@app.route('/deleteMember', methods = ['GET', 'POST'])
@is_logged_in
@is_recep_level
def deleteMember():
    choices.clear()
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT username FROM members")
    b = cur.fetchall()
    for i in range(q):
        tup = (b[i]['username'],b[i]['username'])
        choices.append(tup)
    form = DeleteRecepForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM members WHERE username = %s", [username])
        cur.execute("DELETE FROM info WHERE username = %s", [username])
        cur.execute("DELETE FROM progress WHERE username = %s", [username])

        mysql.connection.commit()
        cur.close()
        choices.clear()
        flash('You deleted a student from institute!!', 'success')
        if(session['prof']==1):
            return redirect(url_for('adminDash'))
        return redirect(url_for('recepDash'))
    return render_template('deleteRecep.html', form = form)

@app.route('/viewDetails')
def viewDetails():
    return render_template('viewDetails.html')

@app.route('/trainers')
def trainers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM info WHERE prof=3")
    result = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM info WHERE prof=3")
    count = cur.fetchone()
    return render_template('user.html', result = result, user = "Trainers", count = count)

@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM info WHERE prof=4")
    result = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM info WHERE prof=4")
    count = cur.fetchone()
    return render_template('user.html', result = result, user = "Student", count = count)

@app.route('/batches')
def batches():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM batch")
    result = cur.fetchall()
    cur.execute("SELECT COUNT(*)  FROM batch")
    count = cur.fetchone()
    return render_template('batch.html', result = result, count = count)

@app.route('/batchDetails/<string:batch>')
def batchDetails(batch):
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM members where batch =%s",[batch])
    result = cur.fetchall()
    cur.execute("SELECT * FROM batch where batchname =%s",[batch])
    batchinfo = cur.fetchall()
    cur.execute("SELECT COUNT(*)  FROM members where batch =%s",[batch])
    count = cur.fetchone()
    cur.close()
    return render_template('user.html', result = result, user=batch+" Students", count = count, batchinfo = batchinfo)

@app.route('/receptionist')
def receptionist():
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM info WHERE prof=2")
    result = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM info WHERE prof=2")
    count = cur.fetchone()
    return render_template('user.html', result = result, user = "Receptionist", count = count)

@app.route('/courseHandling')
def courseHandling():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM batch")
    result = cur.fetchall()
    return render_template('courseHandling.html', result = result)

@app.route('/recepDash')
@is_recep_level
def recepDash():
    return render_template('recepDash.html')

@app.route('/courseList')
def courseList():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from course")
    result = cur.fetchall()
    return render_template('courseDetails.html', result = result)

@app.route('/batchList')
def batchList():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from batch")
    result = cur.fetchall()
    return render_template('batchDetails.html', result = result)

testchoices=[]
batchchoices=[]
class trainorForm(Form):
    name = RadioField('Select Username', choices = choices)
    dateTest = DateField('testdate', format='%Y-%m-%d')
    batchname = StringField('BatchName')
    date = DateField('Date', format='%Y-%m-%d')
    report = StringField('Report', [validators.InputRequired()])
    rate = RadioField('Result', choices = [('good', 'good'),('average', 'average'),('poor', 'poor') ])

@app.route('/batchUnder/<string:batch>', methods = ['GET', 'POST'])
@is_logged_in
@is_trainor
def batchUnder(batch):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id FROM batch WHERE batchname = %s", [batch])
    result = cur.fetchall()
    idval = result[0]['id']
    cur.execute("SELECT testdate FROM test WHERE batchID = %s", [idval])
    testdate_tuple = cur.fetchone()

    if testdate_tuple:
        q = cur.execute("SELECT username FROM members WHERE batch = %s", [batch])
        b = cur.fetchall()
        for i in range(q):
            tup = (b[i]['username'],b[i]['username'])
            choices.append(tup)
        cur.close()

        form = trainorForm(request.form)
        form.dateTest.data = testdate_tuple['testdate']
        batch = [batch]
        form.batchname.data = batch[0]

        if request.method == 'POST':
            date = form.date.data
            dateTest = form.dateTest.data
            batchname = form.batchname.data
            username = form.name.data
            report = form.report.data
            rate = form.rate.data
            if rate == 'good':
                rate = 1
            elif rate == 'average':
                rate = 2
            else:
                rate = 3

            if datetime.now().date()!=date :
                flash('Enter todays Date ', 'warning')
                choices.clear()
                return redirect(url_for('trainorDash'))
            
            
            cur = mysql.connection.cursor()

            testdate = testdate_tuple['testdate'] # extract the date object from the tuple
            print(testdate)
            evaluatingdate = datetime.strptime(date.strftime('%Y-%m-%d'), '%Y-%m-%d').date()
            print(evaluatingdate)
            if testdate > evaluatingdate:
                flash('You cannot predict furture!!Wait for test to finish', 'warning')
                return redirect(url_for('trainorDash'))

            p = cur.execute("SELECT date FROM progress WHERE username = %s", [username])
            entered = []
            q = cur.fetchall()
            for i in range(p):
                entered.append(q[i]['date'])
            

            if date in entered:
                cur.execute("UPDATE progress SET daily_result = %s, rate = %s WHERE username = %s and date = %s", (report,rate, username, date))
                mysql.connection.commit()
                cur.close()
                choices.clear()
                flash('Succesfully updated!', 'success')
                return redirect(url_for('trainorDash'))
            
            cur.execute("SELECT id FROM batch WHERE batchname = %s", [batchname])
            result = cur.fetchall()
            id_val = result[0]['id']
            

            cur.execute("INSERT INTO progress(username, testdate, batchname, date, daily_result, rate, batchID) VALUES(%s, %s, %s, %s, %s, %s, %s)", (username, dateTest, batchname, date, report, rate, id_val))
            mysql.connection.commit()
            cur.close()
            choices.clear()
            flash('Progress updated and Reported', 'info')
            return redirect(url_for('trainorDash'))
    else:
        flash('Test Date is not finalised. You cannot evaluate.', 'warning')
        return redirect(url_for('trainorDash'))

    return render_template('evaluation.html', batch = batch, form = form)


@app.route('/trainorDash', methods = ['GET'])
@is_logged_in
@is_trainor
def trainorDash():
    choices.clear()
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM members WHERE trainor = %s", [session['username']])
    members_under = cur.fetchall()	
    cur.execute("SELECT batchname, coursename, batchstartdate, batchenddate, batchtime FROM batch WHERE trainername = %s", [session['username']])
    batch = cur.fetchall()
    cur.execute("SELECT batchname FROM batch WHERE trainername = %s", [session['username']])
    batch_under = cur.fetchall()
    cur.close()
    cur = mysql.connection.cursor()

    return render_template('trainorDash.html', batch = batch, batch_under = batch_under, members=members_under)

choices7 = []
choices8 = []
class UpdatePlanForm(Form):

    coursename = SelectField('coursename', choices = choices7)
    batchname = SelectField('batchname', choices = choices8)
    testname = StringField('testname', [validators.Length(min=1, max=50)])
    testdate = DateField('testdate', format='%Y-%m-%d')
    teststarttime = TimeField('teststarttime', validators=[InputRequired()])
    testendtime = TimeField('testendtime', validators=[InputRequired()])

   

@app.route('/updatePlans', methods = ['GET', 'POST'])
@is_trainor
def updatePlans():
    choices7.clear();
    choices8.clear();
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT coursename FROM batch WHERE trainername = %s", [session['username']])
    b = cur.fetchall()
    for i in range(q):
        tup = (b[i]['coursename'],b[i]['coursename'])
        choices7.append(tup)
    

    q = cur.execute("SELECT batchname FROM batch WHERE trainername = %s", [session['username']])
    b = cur.fetchall()
    for i in range(q):
        tup = (b[i]['batchname'],b[i]['batchname'])
        choices8.append(tup)

   
    form = UpdatePlanForm(request.form)
    if request.method == 'POST' and form.validate():
        coursename = form.coursename.data
        batchname = form.batchname.data
        testname = form.testname.data
        testdate = form.testdate.data
        teststarttime = form.teststarttime.data
        testendtime = form.testendtime.data
        cur = mysql.connection.cursor()
        
        if datetime.now().date()!=testdate :
                flash('Enter todays Date ', 'warning')
                choices.clear()
                return redirect(url_for('updatePlans'))
        
        cur.execute("SELECT id FROM batch WHERE batchname = %s", [batchname])
        result = cur.fetchall()
        idval = result[0]['id']
        cur.execute("SELECT batchstartdate FROM batch WHERE id = %s", [idval])
        testdate_tuple = cur.fetchone()

        startdate = testdate_tuple['batchstartdate'] # extract the date object from the tuple
        print(testdate)
        evaluatingdate = datetime.strptime(testdate.strftime('%Y-%m-%d'), '%Y-%m-%d').date()
        print(evaluatingdate)
        if startdate > evaluatingdate:
            flash('Batch Not yet started', 'warning')
            return redirect(url_for('updatePlans'))


        cur.execute("SELECT id FROM course WHERE course_name = %s", [coursename])
        result = cur.fetchall()
        course_id_val = result[0]['id']
        cur.execute("SELECT id FROM batch WHERE batchname = %s", [batchname])
        result = cur.fetchall()
        batch_id_val = result[0]['id']
        cur.execute("INSERT INTO test(coursename, batchname, testname, testdate, teststarttime, testendtime, courseID, batchID)VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (coursename, batchname, testname, testdate, teststarttime, testendtime, course_id_val, batch_id_val))
      
        mysql.connection.commit()
        cur.close()
        choices7.clear()
        choices8.clear()
        flash('You have updated the plan schemes', 'success')
        return redirect(url_for('trainorDash'))
    return render_template('addTest.html', form = form)



@app.route('/memberDash/<string:username>') 
@is_logged_in
def memberDash(username):
    if session['prof']==4 and username!=session['username']:
        flash('You aren\'t authorised to view other\'s Dashboards', 'danger')
        return redirect(url_for('memberDash', username = session['username'])) 
    cur = mysql.connection.cursor()
    cur.execute("SELECT batch FROM members WHERE username = %s", [username])
    batchname = (cur.fetchone())['batch']

    cur.execute("SELECT coursename FROM members WHERE username = %s", [username])
    coursename = (cur.fetchone())['coursename']

    cur.execute("SELECT  trainor, batch FROM members WHERE username = %s", [username])
    trainorBatch = cur.fetchall()
    
    cur.execute("SELECT course_description, course_duration, course_price FROM course WHERE course_name = %s", [coursename])
    course = cur.fetchall()

    cur.execute("SELECT id FROM batch WHERE batchname = %s", [batchname])
    result = cur.fetchall()
    
    if not result:
        flash("Currently batch is not available")
        return render_template('usernotfound.html')

    idval = result[0]['id']
    cur.execute("SELECT batchtime FROM batch WHERE id = %s", [idval])
    batchtime = cur.fetchall()
    print(batchtime)
    cur.execute("SELECT * FROM test WHERE batchID = %s ", [idval])
    testdetails = cur.fetchall()
    print(testdetails)


    n = cur.execute("SELECT date, daily_result, rate FROM progress WHERE username = %s ORDER BY date DESC", [username])
    progress = cur.fetchall()
    result = []
    if n:
        for i in range(n):
            result.append(int(progress[i]['rate']))
            good = result.count(1)
            poor = result.count(3)
            average = result.count(2)
            total = good + poor + average
            print(total)
            good = round((good/total) * 100, 2)
            average = round((average/total) * 100, 2)
            poor = round((poor/total) * 100, 2)
        cur.close()
        return render_template('memberDash.html',user = username, course = course,  coursename=coursename, progress = progress, good = good, poor = poor, average = average, trainorBatch = trainorBatch, testdetails = testdetails, batchtime= batchtime)    
    cur.close()
    return render_template('memberDash.html',user = username, course = course,  coursename=coursename, trainorBatch = trainorBatch, testdetails = testdetails, batchtime= batchtime)



@app.route('/profile/<string:username>')
@is_logged_in
def profile(username):
    if username == session['username'] or session['prof']==1 or session['prof']==2:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM info WHERE username = %s", [username])
        result = cur.fetchone()
        cur.execute("SELECT * FROM trainors WHERE username = %s", [username])
        iftrainors = cur.fetchone()
        return render_template('profile.html', result = result, iftrainors = iftrainors)
    flash('You cannot view other\'s profile', 'warning')
    if session['prof']==3:
        return redirect(url_for('trainorDash'))
    return redirect(url_for('memberDash', username = username))

class EditForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    street = StringField('Street', [validators.Length(min = 1, max = 100)])
    city = StringField('City', [validators.Length(min = 1, max = 100)])
    phone = StringField('Phone', [validators.Length(min = 1, max = 100)])


@app.route('/edit_profile/<string:username>', methods = ['GET', 'POST'])
@is_logged_in
def edit_profile(username):

    if username != session['username']:
        flash('You aren\'t authorised to edit other\'s details', 'warning')
        if session['prof']==4:
            return redirect(url_for('memberDash', username = username))
        if session['prof']==1:
            return redirect(url_for('adminDash'))
        if session['prof']==2:
            return redirect(url_for('recepDash', username = username))
        if session['prof']==3:
            return redirect(url_for('trainorDash', username = username))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM info WHERE username = %s", [username]);
    result = cur.fetchone()

    form = EditForm(request.form)
    
    form.name.data = result['name']
    form.street.data = result['street']
    form.city.data = result['city']
    form.phone.data = result['phone']
 
    cur.close()

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        street = request.form['street']
        city = request.form['city']
        phone = request.form['phone']
        app.logger.info(name)
        app.logger.info(street)
        app.logger.info(city)
        cur = mysql.connection.cursor()

        q = cur.execute("UPDATE info SET name = %s, street = %s, city = %s, phone = %s WHERE username = %s", (name, street, city, phone, username))
        app.logger.info(q)
        mysql.connection.commit()
        cur.close()
        flash('You successfully updated your profile!!', 'success')
        if session['prof']==4:
            return redirect(url_for('memberDash', username = username))
        if session['prof']==1:
            return redirect(url_for('adminDash'))
        if session['prof']==2:
            return redirect(url_for('recepDash', username = username))
        if session['prof']==3:
            return redirect(url_for('trainorDash', username = username))
    return render_template('edit_profile.html', form=form)


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.secret_key = '528491@JOKER'
    app.debug = True
    app.run()



