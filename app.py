from flask import Flask, request
from flask import render_template
from flask import redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask import g, url_for
import os
"""
To do list for andela bootcamp using flask  sessions 
"""
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

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


@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		session.pop('user',None)
		if request.form['password'] == 'MasterPass' and request.form['username'] == 'Admin' :
			session['user'] = request.form['username']
			return redirect(url_for('list'))
	return render_template('login.html')


@app.route('/list')
def list():
        if g.user:
                tasks = Task.query.all()
                return render_template('list.html', tasks=tasks)
        

@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error requesting form'

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/list')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    return redirect('/list')

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
	
@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']
		
@app.route('/getsession')
def getsession():
	if 'user' in session:
		return session['user']
	return 'in'
		
@app.route('/dropsession')
def dropsession():
	session.pop('user', None)
	return redirect('/')
	
if __name__ == '__main__':
	app.run (debug=True)
		
		
