import os
import random

import mysql.connector
from flask import Flask, render_template, request, flash, redirect, url_for, session, send_from_directory

UPLOAD_FOLDER = '/home/mohammad.n@TA.COM/jobApplicationPortal/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = '29e317c131a9eb03a8d7ad0817c281a7'
app.config['ALLOWED_EXTENSIONS'] = ['pdf', 'docx']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_URL'] = "uploads/"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3306",
    password="root@123",
    database="jobApplication"
)
cursor = db.cursor()


def get_position_name(position_id):
    cursor.execute(f"SELECT position_name FROM jobApplication.position WHERE position_id = {position_id}")
    data = cursor.fetchone()
    return data[0]


@app.route('/admin', methods=['GET'])
def admin():
    if 'email' not in session:
        return "404 Not Found"
    search = request.args.get('search')
    position_filter = request.args.get('filter')
    sql = "SELECT * FROM jobApplication.applicant"
    if search or position_filter:
        sql += " WHERE "
    if search:
        sql += (f"applicant_name LIKE '%{search}%' OR  applicant_email LIKE '%{search}%' OR registration_number "
                f"LIKE '%{search}%'")
    if position_filter:
        if search:
            sql += "AND "
        sql += f"position_id = '{int(position_filter)}'"
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    formatted_data = []
    for d in data:
        conv_list = list(d)
        conv_list.append(app.config['UPLOAD_URL'] + conv_list[-1])
        conv_list[3] = get_position_name(conv_list[3])
        formatted_data.append(conv_list)
    print(formatted_data)
    headings = ("registration_number", "applicant_name", "applicant_email", "position_id", "resume")
    return render_template("table.html", headings=headings, formated_data=formatted_data)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        email = email.lower()
        password = request.form.get('password')
        cursor.execute(f"SELECT * FROM jobApplication.Admin WHERE email = '{email}';")
        user = cursor.fetchone()

        if not user:
            flash(f'Unauthorized User', 'error')
            return redirect(url_for('login'))
        if user[2] == password:
            session['email'] = email
            return redirect(url_for('admin'))
        flash(f'Unauthorized User', 'error')
        return redirect(url_for('login'))


@app.route('/uploads/<file>', methods=['GET'])
def get_files(file):
    return send_from_directory(app.config['UPLOAD_FOLDER'], file)


@app.route("/application", methods=['POST', 'GET'])
def application():
    if request.method == 'GET':
        cursor.execute(f"SELECT * FROM jobApplication.position;")
        positions = cursor.fetchall()
        return render_template('application.html', positions=positions)
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        position = int(request.form.get('position'))
        cursor.execute(f"SELECT * FROM applicant WHERE position_id='{position}' and applicant_email = '{email}'")
        if cursor.fetchone():
            flash("You cant apply for same position again.", "error")
            return redirect(url_for('application'))
        if 'resume' not in request.files:
            flash("Please add Resume", "error")
        resume = request.files['resume']
        if resume.filename == '':
            flash("Please add Resume", "error")
            return redirect(url_for('application'))
        filename, extension = resume.filename.split(".")
        if resume:
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                flash("You can't only upload resumes in DOC and PDF formats.", "error")
                return redirect(url_for('application'))
        reg_number = generate_registration_number()
        while True:
            cursor.execute(f"SELECT * FROM jobApplication.applicant WHERE registration_number = '{reg_number}'")
            if cursor.fetchone():
                reg_number = generate_registration_number()
            else:
                break
        filename = filename + reg_number + "." + extension
        resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        sql = (
                  f"INSERT INTO jobApplication.applicant  ( applicant_name, applicant_email, registration_number, "
                  f"position_id, resume) VALUES ('%s', '%s', '%s', %s, '%s')") % (
                  name, email, reg_number, position, filename)

        cursor.execute(sql)
        db.commit()
        flash(f'Your application is success your tracking id is: {reg_number}', 'success')
        return redirect(url_for('home'))


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


def generate_registration_number():
    prefix = 'REG'
    number = random.randint(100_000, 999_999)
    registration_number = f'{prefix}-{number}'
    return registration_number


if __name__ == '__main__':
    app.run(debug=True)
