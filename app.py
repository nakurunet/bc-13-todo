from flask import Flask, request
from flask import render_template
from flask import redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask import g, url_for
import os
"""
To do list for andela bootcamp using flask  sessions 
"""
#Create object of Flask class,
#Randomize thesecret key for session
#then create an instance of sqlalchemy
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#Defining/initializing database columns
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False

    def __repr__(self):
        return '<Content %s>' % self.content

db.create_all()

#check for both GET  and POST methods
#Redirect to url for the list function
# Generate html with render_template method
@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session.pop('user',None)
		pwds = request.form['password']
		Admn = request.form['username']
		if pwds == 'MasterPass' and Admn == 'Admin' :
			session['user'] = request.form['username']
			return redirect(url_for('list'))
	return render_template('login.html')

#Route() function binds list function to /list url
#which renders the list.html
@app.route('/list')
def list():
        if g.user:
                tasks = Task.query.all()
                return render_template('list.html', tasks=tasks)
        
#add_task() method adds input list
#items to the database.
@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error requesting form'
    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/list')

#delete_task method handles
#deleting tasks from the task list
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/list')
    db.session.delete(task)
    db.session.commit()
    return redirect('/list')

#resolve_task() checks if the task
#value has been checked and checks it.
@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/list')

# Make sure user have an active session 
# before executing any other functions	
@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']

#Check the session status		
@app.route('/getsession')
def getsession():
	if 'user' in session:
		return session['user']
	return 'in'

#exit the session 		
@app.route('/dropsession')
def dropsession():
	session.pop('user', None)
	return redirect('/')
	
if __name__ == '__main__':
	app.run (debug=True)
		
		
