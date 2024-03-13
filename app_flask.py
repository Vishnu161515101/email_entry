from flask import Flask,render_template,request
from flask import redirect
import re
import pymysql
import random
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_mail import Mail, Message 
from flask import *
app=Flask(__name__)


# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jayaramireddy063@gmail.com'  # Replace with your email address
app.config['MAIL_PASSWORD'] = 'qwgh ulfg xtnl zgaf'  # Replace with your email password

mail = Mail(app)

# Create a single time database connection object
db_mysql = pymysql.connect(host='localhost', user='root', password='', db='vishnu')

# Create a cursor object from the connection
db_cursor = db_mysql.cursor()


# Make login function for login and also make 
# session for login and registration system 
# and also fetch the data from MySQL


@app.route('/index',methods=['POST','GET'])
def index():
	message = ''
	if request.method == 'POST' and 'name' in request.form and 'password' in request.form and'email' in request.form:
			userName = request.form['name']
			password = request.form['password']
			email = request.form['email']
			sql1="select * from login where email_id='{}' and password='{}' ".format(email,password)
			db_cursor.execute(sql1)
			data=db_cursor.fetchall()
			if data:
				message = 'Account already exists !'
				# return 'helo'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
				message = 'Invalid email address !'
				# return 'helo'
			elif not userName or not password or not email:
				message = 'Please fill out the form !'
				# return 'helo'
			else:
				number = random.randint(1111, 9999)
				names1212="Hi"+userName 
				msg = Message(subject=names1212, sender='jayaramireddy063@gmail.com', recipients=[email])
				msg.html = "Hello " +"   "+    userName + "<br>" + \
                        "Thank you for registering!" + "<br>" + \
                        "Your username: " + userName +str(number)+"<br>" \
                        "Your password: " + password + "<br>"
				user_names=userName +str(number)
				sql="insert into login(name,password,email_id,user_name)values('{}','{}','{}','{}')".format(userName,password,email,user_names)
				db_cursor.execute(sql)
				db_mysql.commit()
				

				# msg.body = "Hello " + userName + "<br><br>"
				# msg.body += "Thank you for registering!" + "<br><br>"
				# msg.body += "Your username: " + userName + "<br>"
				# msg.body = f" how {userName} Please find the Below UserName {userName} + str(number) +: Password : {password}"  # Concatenate message body and random number
				# msg.body = "Hello {userName},\n\nThank you for registering!\n\nYour username: {userName}\nYour password: {password}\n\nBest regards,\nYour Application Team"
				mail.send(msg)
				message = 'You have successfully registered !'
				# return 'hello vishnu this register page'
			# return 'hello'
	elif request.method == 'POST':
		message = 'Please fill out the form !'
		# return render_template('register.html', message=message)
	return render_template('entry_page.html', message=message)


@app.route('/login' ,methods=['GET', 'POST'])
def login():
		message = ''
		if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
				email = request.form['email']
				password = request.form['password']
				sql1="select * from login where (email_id='{}' or user_name='{}') and password='{}' ".format(email,email,password)
				db_cursor.execute(sql1)
				data=db_cursor.fetchall()
				if data:
					message = 'Logged in successfully !'
					return render_template('admin.html', message=message)
				else:
					message = 'Please enter correct email / password !'
					# return 'hello vishnu it is succesfull'
				# return render_template('login.html', message=message)
		return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/email_send')
def email_send():
    
    try:
        number = random.randint(1111, 9999)
        msg = Message( sender='jayaramireddy063@gmail.com', recipients=['bvishnuvardhan12345@gmail.com'])
        msg.body = f" hello vishnu how are this is you code : {number}"  # Concatenate message body and random number
        mail.send(msg)
        return "Message sent!"
    except Exception as e:
        return str(e)
	

@app.route('/test')
def test():
	return render_template('test_login.html')



@app.route('/logaas' ,methods=['GET', 'POST'])
def logaas():
		message = ''
		if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
				email = request.form['email']
				password = request.form['password']
				sql1="select * from login where (email_id='{}' or user_name='{}') and password='{}' ".format(email,email,password)
				return sql1

@app.route('/update_password')
def update_password():
	return render_template('update_passowrds.html')

@app.route('/opt_page' ,methods=['GET', 'POST'])
def opt_page():
	try:
		if request.method == 'POST' and 'email' in request.form:
			email = request.form['email']
			sql1="select email_id from login where (email_id='{}' or user_name='{}')  ".format(email,email)
			db_cursor.execute(sql1)
			data=db_cursor.fetchall()
			if data:
				# return data
				number = random.randint(1111, 9999)
				msg = Message( sender='jayaramireddy063@gmail.com', recipients=[data])
				msg.body = f" hello vishnu how are this is you code : {number}"  # Concatenate message body and random number
				mail.send(msg)
				return render_template('otp_pages.html',number1=number)
	except Exception as e:
		return str(e)
	

	
if __name__ =='__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)