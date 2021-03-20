from flask import Flask, render_template, request, url_for, session, redirect, g
from model import db, User
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretKey1'


@app.route('/')
def index():
    if g.user:
        return 'Currently logged in as ' + g.user
    return render_template('index.html')


@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']


@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(name=request.form['username']).first()
    if user is not None:
        if request.form['password_hash'] == user.password_hash:
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'Password is incorect'

    return 'User does not exists!'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        pending_user = request.form['username']
        username = User.query.filter_by(name=pending_user)

        if username is None:
            pass

        return
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)