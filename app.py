from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# === DATABASE SETUP ===
def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            age TEXT,
            address TEXT,
            zip_code TEXT,
            country TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.close()

init_db()


# === HOME (SHOW WEBSITE IF LOGGED IN) ===
@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return redirect(url_for('login'))


# === LOGIN PAGE ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = user[1]  # first name
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message="Invalid email or password")

    return render_template('login.html')


# === REGISTER ===
@app.route('/register', methods=['POST'])
def register():
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        address = request.form['address']
        zip_code = request.form['zip_code']
        country = request.form['country']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (first_name, last_name, age, address, zip_code, country, email, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, age, address, zip_code, country, email, password))
        conn.commit()
        conn.close()

        session['user'] = first_name
        return redirect(url_for('home'))
    except sqlite3.IntegrityError:
        return render_template('login.html', message="Email already registered. Please log in.")


# === LOGOUT ===
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
