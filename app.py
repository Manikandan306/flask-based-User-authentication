from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sky"
)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    age = request.form['age']
    city = request.form['city']
    
    try:
        # Insert data into MySQL from the form
        cursor.execute("INSERT INTO quickle (name, age, city) VALUES (%s, %s, %s)", (name, age, city))
        db.commit()
        flash('Sign-up successful! Please log in.', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    city = request.form['city']
    
    # Check if the user exists in the database
    cursor.execute("SELECT * FROM quickle WHERE name=%s AND city=%s", (name, city))
    user = cursor.fetchone()
    
    if user:
        session['username'] = name  # Storing name as username for simplicity
        flash('Login successful!', 'success')
        return redirect(url_for('jane'))
    else:
        flash('Login failed! Name and city combination not found.', 'danger')
        return redirect(url_for('home'))

@app.route('/jane')
def jane():
    # Check if the user is logged in
    if 'username' in session:
        return render_template('jane.html')
    else:
        flash('You need to login first.', 'error')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
