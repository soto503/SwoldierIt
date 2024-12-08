from flask import Flask, render_template, request, redirect, url_for, flash, session
from forms import LoginForm, CreateAccountForm
import mysql.connector
from config import Config
import random
import bcrypt

app = Flask(__name__)
app.config.from_object(Config)

def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        port=app.config['MYSQL_PORT'],
        database=app.config['MYSQL_DATABASE']
    )

@app.route('/')
def home():
    if 'userid' in session:
        return redirect(url_for('user_profile'))
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        session['userid'] = user['userid']
        flash('Login successful!', 'success')
        return redirect(url_for('user_profile'))
    else:
        flash('Invalid credentials, please try again.', 'error')
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return 'Welcome to the dashboard!'

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/user_profile', methods=['GET'])
def user_profile():
    if 'userid' not in session:
        flash('You need to log in first.', 'error')
        return redirect(url_for('home'))

    user_id = session['userid']
    split_type = request.args.get('split_type', '5_day')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT first_name, last_name, username FROM users WHERE userid = %s', (user_id,))
    user = cursor.fetchone()

    if split_type == '5_day':
        headers = ["Chest", "Back", "Legs", "Biceps", "Shoulders"]
        data_sources = [
            ("Chest", (19, 20, 23, 30, 31)),
            ("Back", (45, 52, 54, 55, 58)),
            ("Legs", (1, 8, 10, 13, 16)),
            ("Biceps", (56, 59, 60, 63, 66)),
            ("Shoulders", (32, 35, 42, 46, 44))
        ]
    elif split_type == 'ppl':
        headers = ["Push", "Legs", "Pull", "Rest", "Rest"]
        data_sources = [
            ("Chest", (20, 21, 22, 23, 26)),
            ("Legs", (2, 3, 5, 6, 4)),
            ("Back", (46, 50, 53, 47, 52)),
            (None, ()),
            (None, ())
        ]
    elif split_type == 'total_body':
        headers = ["Total Body", "Rest", "Total Body", "Rest", "Total Body"]
        data_sources = [
            ("Chest", (17, 18, 19, 24, 26, 27)),
            (None, ()),
            ("Legs", (1, 2, 3, 16, 15, 14)),
            (None, ()),
            ("Shoulders", (32, 33, 35, 36, 37, 38))
        ]

    exercises = []
    for table, ids in data_sources:
        if table and ids:
            cursor.execute(f"SELECT Exercise FROM {table} WHERE Routine_ID IN {ids}")
            exercises.append(cursor.fetchall())
        else:
            exercises.append([])

    cursor.close()
    conn.close()

    table_data = list(zip(headers, exercises))

    return render_template(
        'user_profile.html',
        user=user,
        table_data=table_data,
        split_type=split_type
    )

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        username = request.form['username']
        password = request.form['password']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Retrieve the next user_id
        cursor.execute('SELECT IFNULL(MAX(userid), 0) + 1 AS next_id FROM users')
        next_id = cursor.fetchone()['next_id']

        cursor.execute(
            'INSERT INTO users (userid, first_name, last_name, email, phone, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (next_id, first_name, last_name, email, phone, username, hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Account created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_account.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/public_workoutdatabases')
def public_workoutdatabases():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    chest_routine_ids = (17, 18, 19)
    back_routine_ids = (45, 46, 47)
    biceps_routine_ids = (56, 57, 58)
    triceps_routine_ids = (67, 68, 69)
    legs_routine_ids = (1, 2, 3)
    shoulders_routine_ids = (32, 33, 34)
    cardio_routine_ids = (78, 79, 80)

    cursor.execute(f"SELECT Exercise FROM Chest WHERE Routine_ID IN {chest_routine_ids}")
    chest_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Back WHERE Routine_ID IN {back_routine_ids}")
    back_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Biceps WHERE Routine_ID IN {biceps_routine_ids}")
    biceps_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Triceps WHERE Routine_ID IN {triceps_routine_ids}")
    triceps_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Legs WHERE Routine_ID IN {legs_routine_ids}")
    legs_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Shoulders WHERE Routine_ID IN {shoulders_routine_ids}")
    shoulders_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Cardio WHERE Routine_ID IN {cardio_routine_ids}")
    cardio_workouts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'public_workoutdatabases.html',
        chest_workouts=chest_workouts,
        back_workouts=back_workouts,
        biceps_workouts=biceps_workouts,
        triceps_workouts=triceps_workouts,
        legs_workouts=legs_workouts,
        shoulders_workouts=shoulders_workouts,
        cardio_workouts=cardio_workouts
    )

@app.route('/workoutdatabases')
def workoutdatabases():
    # Check if the user is logged in
    if 'userid' not in session:
        flash('You need to log in first to access this page.', 'error')
        return redirect(url_for('home'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Define empty tuples for Routine_IDs (fill these later)
    chest_routine_ids = (17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
    back_routine_ids = (45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58)
    biceps_routine_ids = (56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66)
    triceps_routine_ids = (67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77)
    legs_routine_ids = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
    shoulders_routine_ids = (32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46)
    cardio_routine_ids = (78, 79, 80, 81, 82, 83, 84, 85)

    # Query for each muscle group
    cursor.execute(f"SELECT Exercise FROM Chest WHERE Routine_ID IN {chest_routine_ids}")
    chest_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Back WHERE Routine_ID IN {back_routine_ids}")
    back_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Biceps WHERE Routine_ID IN {biceps_routine_ids}")
    biceps_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Triceps WHERE Routine_ID IN {triceps_routine_ids}")
    triceps_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Legs WHERE Routine_ID IN {legs_routine_ids}")
    legs_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Shoulders WHERE Routine_ID IN {shoulders_routine_ids}")
    shoulders_workouts = cursor.fetchall()

    cursor.execute(f"SELECT Exercise FROM Cardio WHERE Routine_ID IN {cardio_routine_ids}")
    cardio_workouts = cursor.fetchall()

    cursor.close()
    conn.close()

    # Pass all workouts to the template
    return render_template(
        'workoutdatabases.html',
        chest_workouts=chest_workouts,
        back_workouts=back_workouts,
        biceps_workouts=biceps_workouts,
        triceps_workouts=triceps_workouts,
        legs_workouts=legs_workouts,
        shoulders_workouts=shoulders_workouts,
        cardio_workouts=cardio_workouts
    )
if __name__ == '__main__':
    app.run(debug=True)
