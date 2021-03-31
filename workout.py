from flask import Flask, render_template, request, url_for, session, redirect, g
from model import db, User, Exercises, Exercise, Set, Workout
import bcrypt
from datetime import datetime

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

        username = User.query.filter_by(name=pending_user).first()

        if username is None:
            new_user = User(name=pending_user, password_hash=request.form['password_hash'])
            db.session.add(new_user)
            db.session.commit()

            session['username'] = pending_user
            return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))


@app.route('/add_workout', methods=['POST', 'GET'])
def add_workout():
    if request.method == 'POST':
        user = User.query.filter_by(name=session['username']).first()

        workout = Workout(date=datetime.utcnow(), user=user)
        print("request form = ", request.form)
        exercise_count = int(request.form['exercise_count'])

        for exercise_num in range(1, exercise_count + 1):
            exercise = Exercise(order=exercise_num, exercise_id=request.form['exercise'+ str(exercise_num)] , workout=workout)
            print('exercise = ', exercise)
            weights = request.form.getlist('weight' + str(exercise_num))
            reps = request.form.getlist('reps' + str(exercise_num))

            set_order = 1

            for weight, rep in zip(weights, reps):
                work_set = Set(order=set_order, exercise=exercise, weight=weight,
                               reps=rep)
                set_order += 1


        db.session.add(workout)
        db.session.commit()

        return redirect(url_for('index'))

    exercises = Exercises.query.all()

    return render_template('add_workout.html', exercises=exercises)


if __name__ == '__main__':
    app.run(debug=True, port=8002)