from flask import Flask, render_template, request, Response, redirect, url_for, flash, session, send_file
from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors
import logging
import re

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'Notes'


mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('notes_home.html')


@app.route('/register',methods=['GET','POST'])
def register():
	msg=''

	if request.method =='POST' and 'email' in request.form and 'password' in request.form:

	
		full_name=request.form['full_name']
		email=request.form['email']
		password=request.form['password']
		
		
		cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)

		cursor.execute('SELECT * FROM Notes.users WHERE email= %s',(email, ))
		userdata=cursor.fetchone()

		if userdata:
			msg="Account already exists !!"

		elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$',email):
			msg="Invalid email address!!"

		elif not email or not password :
			msg="Please fill out the form !!"

		else:
			cur=mysql.connection.cursor()

			cur.execute('INSERT INTO users (full_name, email, password) VALUES(%s,%s,%s)',(full_name,email,password))
			mysql.connection.commit()
			msg="You have Succesfully Registered !!"

	elif request.method=='POST':
		msg="Please fill out the form !!"

	return render_template('notes_register.html', msg=msg)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cursor:
                cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
                user = cursor.fetchone()

                if user:
                    session['user_id'] = user['user_id']
                    flash('Login successful!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid credentials!', 'error')
        except Exception as e:
            logging.error(f"Login error: {e}")
            flash('An error occurred during login.', 'error')

    return render_template('notes_login.html')

@app.route('/dashboard')
def dashboard():
	return render_template("notes_dashboard.html")


@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
    if 'user_id' not in session:
        return redirect(url_for('login')) # Redirect if not logged in.

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        try:
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO notes (user_id, title, content) VALUES (%s, %s, %s)', (session['user_id'], title, content))
            mysql.connection.commit()
            return redirect(url_for('view_notes')) # Redirect to view notes after creation
        except Exception as e:
            print(f"Error creating note: {e}")
            return "An error occurred while creating the note."

    return render_template('create_note.html')

@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM notes WHERE note_id = %s AND user_id = %s', (note_id, session['user_id']))
        note = cur.fetchone()

        if not note:
            flash('Note not found or you do not have permission to edit it.', 'error')
            return redirect(url_for('view_notes'))

        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            cur.execute('UPDATE notes SET title = %s, content = %s WHERE note_id = %s AND user_id = %s', (title, content, note_id, session['user_id']))
            mysql.connection.commit()
            flash('Note updated successfully!', 'success')
            return redirect(url_for('view_notes'))

        return render_template('edit_note.html', note=note)

    except Exception as e:
        print(f"Error editing note: {e}")
        flash('An error occurred while editing the note.', 'error')
        return redirect(url_for('view_notes'))

@app.route('/delete_note/<int:note_id>')
def delete_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM notes WHERE note_id = %s AND user_id = %s', (note_id, session['user_id']))
        mysql.connection.commit()
        flash('Note deleted successfully!', 'success')
    except Exception as e:
        print(f"Error deleting note: {e}")
        flash('An error occurred while deleting the note.', 'error')

    return redirect(url_for('view_notes'))

@app.route('/view_notes')
def view_notes():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM notes WHERE user_id = %s', (session['user_id'],))
        notes = cur.fetchall()
        return render_template('view_notes.html', notes=notes)

    except Exception as e:
        print(f"Error viewing notes: {e}")
        flash('An error occurred while retrieving notes.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove the user_id from the session
    flash('You have been logged out!', 'success')
    return redirect(url_for('login'))
    
# running application 
if __name__ == '__main__': 
    app.run(debug=True) 
