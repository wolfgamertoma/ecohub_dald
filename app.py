from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os

app = Flask(__name__)

# Definim calea absolută a fișierului de bază de date
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'database.db')

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    try:
        db = get_db()
        cur = db.execute('SELECT title, description, location, date FROM projects')
        projects = cur.fetchall()
        return render_template('projects.html', projects=projects)
    except Exception as e:
        return str(e), 500

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            location = request.form['location']
            date = request.form['date']
            db = get_db()
            db.execute('INSERT INTO projects (title, description, location, date) VALUES (?, ?, ?, ?)',
                       [title, description, location, date])
            db.commit()
            return redirect(url_for('projects'))
        except Exception as e:
            return str(e), 500
    return render_template('new_project.html')

@app.route('/projects/reset', methods=['POST'])
def reset_projects():
    try:
        db = get_db()
        db.execute('DELETE FROM projects')
        db.commit()
        return redirect(url_for('projects'))
    except Exception as e:
        return str(e), 500

@app.route('/volunteers')
def volunteers():
    try:
        db = get_db()
        cur = db.execute('SELECT title, description, location, date FROM volunteers')
        volunteers = cur.fetchall()
        return render_template('volunteers.html', volunteers=volunteers)
    except Exception as e:
        return str(e), 500

@app.route('/volunteers/new', methods=['GET', 'POST'])
def new_volunteer():
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            location = request.form['location']
            date = request.form['date']
            db = get_db()
            db.execute('INSERT INTO volunteers (title, description, location, date) VALUES (?, ?, ?, ?)',
                       [title, description, location, date])
            db.commit()
            return redirect(url_for('volunteers'))
        except Exception as e:
            return str(e), 500
    return render_template('new_volunteer.html')

@app.route('/volunteers/reset', methods=['POST'])
def reset_volunteers():
    try:
        db = get_db()
        db.execute('DELETE FROM volunteers')
        db.commit()
        return redirect(url_for('volunteers'))
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
