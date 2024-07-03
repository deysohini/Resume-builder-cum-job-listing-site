from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import uuid
app = Flask(__name__)
app.secret_key = 'your_secret_key'


conn = sqlite3.connect('rbcjm.db')

# Home page
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/jobseeker')
def jobseeker():
    return render_template('jobseeker.html')

@app.route('/employer')
def employer():
    return render_template('employer.html')

@app.route('/registeremp')
def registeremp():
    return render_template('registeremp.html')

@app.route('/registerjs')
def registerjs():
    return render_template('registerjs.html')

@app.route('/us')
def us():
    return render_template('about.html')

@app.route('/dashboard_employer')
def dashboard_employer():
    return render_template('dashboard_employer.html',name=session['name'])

@app.route('/dashboard_job_seeker')
def dashboard_job_seeker():
    return render_template('dashboard_job_seeker.html',name=session['name'])

@app.route('/resume')
def resume():
    return render_template('resume.html')


'''@app.route('/resumes')
def resumes():
    return render_template('resumes.html')'''

@app.route('/post_job')
def postjob():
    return render_template('post_job.html')


@app.route('/loginemp', methods=['GET','POST'])
def loginemp():
    if request.method == 'POST':
        userid = request.form['name']
        pwd = request.form['pwd']
        conn = sqlite3.connect('rbcjm.db')
        cursor = conn.cursor()
        sql = 'SELECT * FROM employer WHERE name = ? AND pwd = ?'
        values = (userid, pwd)
        cursor.execute(sql, values)        
        user = cursor.fetchone()
        
        if user:
            session['loggedin']=True
            session['name'] = user[1]
            #session['pwd'] = user[4]
            return redirect(url_for('dashboard_employer'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')



@app.route('/loginjs', methods=['GET','POST'])
def loginjs():
    if request.method == 'POST':
        userid = request.form['name']
        pwd = request.form['pwd']
        conn = sqlite3.connect('rbcjm.db')
        cursor = conn.cursor()
        sql = 'SELECT * FROM seeker WHERE name = ? AND pwd = ?'
        values = (userid, pwd)
        cursor.execute(sql, values)        
        user = cursor.fetchone()
        #conn.close()

        if user:
            session['loggedin']=True
            session['name'] = user[1]
            #session['pwd'] = user[4]
            return redirect(url_for('dashboard_job_seeker'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')




#@app.route('/upload',methods=['POST'])
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        user_id = str(uuid.uuid4())
        name = request.form['name']
        email = request.form['email']
        phn = request.form['phn']
        pwd = request.form['pwd']
        company=request.form['company']
        conn = sqlite3.connect('rbcjm.db')
        cursor = conn.cursor()
        sql = "INSERT INTO employer (userid, name, phn, email, pwd, company) VALUES (?, ?, ?, ?, ?, ?)"
        val = (user_id, name, phn, email, pwd, company)
        cursor.execute(sql,val)
        conn.commit()
        conn.close()

        return f"Received data: User ID - {user_id}, Name - {name}, Email - {email}, Phone Number - {phn}, Password - {pwd},Company - {company}"
    return render_template('register.html')

@app.route('/uploadseeker', methods=['POST'])
def uploadseeker():
    if request.method == 'POST':
        user_id = str(uuid.uuid4())
        name = request.form['name']
        email = request.form['email']
        phn = request.form['phn']
        pwd = request.form['pwd']
        conn = sqlite3.connect('rbcjm.db')
        cursor = conn.cursor()
        sql = "INSERT INTO seeker (userid, name, phn, email, pwd) VALUES (?, ?, ?, ?, ?)"
        val = (user_id, name, phn, email, pwd)
        cursor.execute(sql,val)
        conn.commit()
        conn.close()

        return f"Received data: User ID - {user_id}, Name - {name}, Email - {email}, Phone Number - {phn}, Password - {pwd}"
    return render_template('register.html')



@app.route('/resumeup', methods=['GET','POST'])
def resumeup():
    if request.method == 'POST':
        id=str(uuid.uuid4())
        name = request.form['name']
        qualification = request.form['qualification']
        about = request.form['about']
        skills = request.form['skills']
        exp= request.form['exp']
        location = request.form['location']
        conn = sqlite3.connect('rbcjm.db')
        cursor = conn.cursor()
        sql = "INSERT INTO resume (id,name, qualification, about, skills, exp, location) VALUES (?, ?, ?, ?, ?, ?, ?)"
        val = (id,name, qualification, about, skills, exp, location)
        cursor.execute(sql,val)
        conn.commit()
        conn.close()
        return redirect(url_for('resume'))

    return render_template('resume.html')


@app.route('/resumes')
def resumes():
    id = session['name']
    conn = sqlite3.connect('rbcjm.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM resume WHERE name = ?', (id,))
    resumes = cursor.fetchone()
    conn.close()

    return render_template('resumes.html', resumes=resumes)

#Job Seeker: View and Apply to Jobs
@app.route('/view_job')
def view_job():
    
    conn = sqlite3.connect('rbcjm.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs')
    jobs = cursor.fetchall()
    conn.close()

    return render_template('view_job.html', jobs=jobs)


@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
        if request.method == 'POST':
            jobname = request.form['jobname']
            jobdesc = request.form['jobdesc']
            vacancy = request.form['vacancy']
            conn = sqlite3.connect('rbcjm.db')
            cursor = conn.cursor()
            sql = 'INSERT INTO jobs VALUES (?, ?, ?)'
            values = (jobname, jobdesc, vacancy)
            cursor.execute(sql, values)            
            conn.commit()
            conn.close()

            return render_template('post_job.html')

        return redirect(url_for('post_job'))

if __name__ == '__main__':
    app.run(debug=True,port=8080) 
