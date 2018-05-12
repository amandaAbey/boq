from flask import Flask, render_template, redirect, request, session, url_for, json, Response, jsonify
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'development'

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))

# database connection
try:
    conn_string = "host = 'localhost' dbname = 'project' user = 'postgres' password = 'admin'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print "DataBase Successfully Connected"


    # load the default page
    @app.route('/')
    def index():
        if session.get('logged_in'):
            return render_template('navi.html')
        else:
            return render_template("main.html")


    # load the signup page
    @app.route('/signup')
    def signup():
        return render_template('signup.html')


    # check session
    @app.route('/login')
    def login_users():
        # if not session.get('logged_in'):
        #     return redirect(url_for('login_user'))
        # else:
        return render_template('login.html')


    # login to the system
    @app.route('/login_user', methods=['POST'])
    def login_user():
        email = request.form['email']
        password = request.form['password']
        error = None
        sql = "select email, password, role from users where email='" + email + "'and password='" + password + "'"
        cursor.execute(sql)
        conn.commit()
        value = cursor.fetchall()
        if not value:
            error = 'Invalid Username or Password'
            return render_template('login.html', error=error)

        elif value:
            role = value[0][2].strip()
            if request.method == 'POST':
                session['logged_in'] = True
                session['role'] = value[0][2].strip()
            if role == 'admin':
                return render_template('adminNavi.html')
            elif role == 'manager':
                return render_template('navi.html')

        return render_template('navi.html')

        # elif request.method == 'POST':
        #     session['logged_in'] = True
        #     return render_template('navi.html')


    @app.route('/ilp')
    def ilp():
        if session.get('logged_in') == True:
            if session.get('role') == 'admin':
                return render_template('adminNavi.html')
            elif session.get('role') == 'manager':
                return render_template('navi.html')


    # create user accounts
    @app.route('/signup_registration', methods=['POST'])
    def signup_registration():
        try:
            if not session.get('logged_in'):
                return render_template('login.html')
                # get the user count
            select_query = "SELECT COUNT (empid) FROM users"
            cursor.execute(select_query)
            count = int(cursor.fetchall()[0][0])
            count += 1

            firstname = request.form['first_name']
            lastname = request.form['last_name']
            contact = request.form['contact_number']
            company = request.form['company']
            email = request.form['email']
            username = request.form['user_name']
            passwords = request.form['password']
            role = request.form['role']
            package = request.form['package']
            try:
                insert_query = "INSERT INTO users(empid, fname, lname, contact, companyname, email, username, password, role, packagename) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                data = (str(count), str(firstname), str(lastname), int(contact), str(company), str(email), str(username), str(passwords),
                        str(role), str(package),)
                cursor.execute(insert_query, data)
                conn.commit()
                print "Data Successfully added to the user table"
                return render_template('login.html')
            except:
                print"Error"
                return redirect(url_for('index'))
        except:
            print "failed"
            return render_template('signup.html')


    # Show users in the table
    @app.route('/table', methods=['GET', 'POST'])
    def table():
        if not session.get('logged_in'):
            return render_template('login.html')
        select_query = "SELECT * FROM users"
        cursor.execute(select_query)
        conn.commit()
        values = cursor.fetchall()
        return render_template('viewusers.html', values=values)

    @app.route('/tnc')
    def tnc():
        return render_template('tnc.html')


    # load the navigation page
    @app.route('/navi')
    def navi():
        return render_template('navi.html')


    @app.route('/payment')
    def payment():
        return render_template('payment.html')


    @app.route('/packageDetail')
    def packagedetails():
        return render_template('package_details.html')


    # @app.route('/viewusers')
    # def viewusers():
    #     return render_template('viewusers.html')


    @app.route('/open')
    def open_notes():
        select_q = "SELECT COUNT (id) FROM notes"
        cursor.execute(select_q)
        count = int(cursor.fetchall()[0][0])
        count += 1

        title = request.form['title']
        try:
            insert_query = u"INSERT INTO users(id, title) VALUES ('%s', '%s')" % (
                str(count),
                title)
            cursor.execute(insert_query)
            conn.commit()
            print "Data Successfully added to the notes table"
            return render_template('notes.html')
        except:
            print"Error"
            return redirect(url_for('notes'))


    @app.route('/notes')
    def notes():
        return render_template('notes.html')


    @app.route('/create')
    def create():
        return render_template('create.html')


    @app.route('/ongoing')
    def ongoing():
        return render_template('ongoing.html')


    @app.route('/wbs')
    def wbs():
        return render_template('wbs.html')


    @app.route('/uploadautocad')
    def uploadautocad():
        return render_template('uploadautocad.html')


    # Show data in the table
    @app.route('/boq1', methods=['GET', 'POST'])
    def boq1():
        if not session.get('logged_in'):
            return render_template('login.html')
        select_query = "SELECT * FROM boqlines1"
        cursor.execute(select_query)
        conn.commit()
        values = cursor.fetchall()

        # load data into drop down list
        select = "SELECT unitid FROM units"
        cursor.execute(select)
        conn.commit()
        value = cursor.fetchall()

        return render_template('boq1.html', values=values, units=value)

    @app.route('/boq2')
    def boq2():
        if not session.get('logged_in'):
            return render_template('login.html')
        select_query = "SELECT * FROM boqlines2"
        cursor.execute(select_query)
        conn.commit()
        values = cursor.fetchall()


        # load data into drop down list
        select = "SELECT unitid FROM units"
        cursor.execute(select)
        conn.commit()
        value = cursor.fetchall()

        return render_template('boq2.html', values=values, units=value)

    @app.route('/boq3')
    def boq3():
        if not session.get('logged_in'):
            return render_template('login.html')
        select_query = "SELECT * FROM boqlines3"
        cursor.execute(select_query)
        conn.commit()
        values = cursor.fetchall()

        # load data into drop down list
        select = "SELECT unitid FROM units"
        cursor.execute(select)
        conn.commit()
        value = cursor.fetchall()

        return render_template('boq3.html', values=values, units=value)

    @app.route('/boq4')
    def boq4():
        if not session.get('logged_in'):
            return render_template('login.html')
        select_query = "SELECT * FROM boqlines4"
        cursor.execute(select_query)
        conn.commit()
        values = cursor.fetchall()

        # load data into drop down list
        select = "SELECT unitid FROM units"
        cursor.execute(select)
        conn.commit()
        value = cursor.fetchall()

        return render_template('boq4.html', values=values, units=value)

    @app.route('/boq5')
    def boq5():
        if not session.get('logged_in'):
            return render_template('login.html')
        select_query = "SELECT * FROM boqlines5"
        cursor.execute(select_query)
        conn.commit()
        values = cursor.fetchall()

        # load data into drop down list
        select = "SELECT unitid FROM units"
        cursor.execute(select)
        conn.commit()
        value = cursor.fetchall()

        return render_template('boq5.html', values=values, units=value)


    @app.route('/cancel')
    def cancel():
        return render_template('main.html')


    @app.route('/feedback')
    def feedback():
        return render_template('feedback.html')


    @app.route('/upload')
    def upload():
        target = os.path.join(UPLOAD_FOLDER, 'images/')
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.file.getlist('file'):
            print(file)
            filename = file.filename
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)

        return render_template("create.html")

    # profile settings
    @app.route('/profile')
    def profile():
        if not session.get('logged_in'):
            return render_template('login.html')
        user_id = session["empid"]
        return render_template('profile.html')


    @app.route('/overview')
    def overview():
        return render_template('overview.html')

    labels = [
        'JAN', 'FEB', 'MAR', 'APR'
    ]

    values = [
        967.67, 190.89, 1379.75, 349.19
    ]

    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA"
    ]


    @app.route('/bar')
    def bar():
        bar_labels = labels
        bar_values = values
        return render_template('bar_chart.html', title='project1', max=17000, labels=bar_labels,
                               values=bar_values)


    @app.route('/line')
    def line():
        line_labels = labels
        line_values = values
        return render_template('line_chart.html', title='project2', max=17000, labels=line_labels,
                               values=line_values)


    @app.route('/pie')
    def pie():
        pie_labels = labels
        pie_values = values
        return render_template('pie_chart.html', title='Project 3', max=17000, set=zip(values, labels, colors))


    # logout from the system
    @app.route('/logout')
    def logout():
        session['logged_in'] = False
        session.pop = ['logged_in', None]
        session.clear()
        return redirect(url_for('login_users'))


    # clear the cache after logout
    @app.after_request
    def add_header(response):
        response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
        return response



    if __name__ == '__main__':
        app.run(debug=True)
except:
    print 'Database Connection Failed'
