from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

def read_data(file_name):
    if not os.path.exists(file_name):
        with open(file_name, 'w') as f:
            json.dump([], f)
    with open(file_name, 'r') as f:
        return json.load(f)

def write_data(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    projects = read_data('projects.json')
    return render_template('projects.html', projects=projects)

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        date = request.form['date']
        projects = read_data('projects.json')
        projects.append({'title': title, 'description': description, 'location': location, 'date': date})
        write_data('projects.json', projects)
        return redirect(url_for('projects'))
    return render_template('new_project.html')

@app.route('/projects/reset', methods=['POST'])
def reset_projects():
    write_data('projects.json', [])
    return redirect(url_for('projects'))

@app.route('/volunteers')
def volunteers():
    volunteers = read_data('volunteers.json')
    return render_template('volunteers.html', volunteers=volunteers)

@app.route('/volunteers/new', methods=['GET', 'POST'])
def new_volunteer():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        date = request.form['date']
        volunteers = read_data('volunteers.json')
        volunteers.append({'title': title, 'description': description, 'location': location, 'date': date})
        write_data('volunteers.json', volunteers)
        return redirect(url_for('volunteers'))
    return render_template('new_volunteer.html')

@app.route('/volunteers/reset', methods=['POST'])
def reset_volunteers():
    write_data('volunteers.json', [])
    return redirect(url_for('volunteers'))

if __name__ == '__main__':
    app.run(debug=True)

