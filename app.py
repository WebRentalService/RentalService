from flask import Flask, render_template, request, redirect, url_for
import hashlib
import bcrypt
import mariadb
import sys

app = Flask(__name__)

try:
    db = mariadb.connect(
        user = 'ges',
        password = 'ges',
        host = 'localhost',
        port = 3306,
        database = 'Users'
        )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


cur = db.cursor()

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        register_info = request.form
        
        name = register_info['name']
        username = register_info['username']
        hashed_password = bcrypt.hashpw(register_info['password'].encode('utf-8'), bcrypt.gensalt())
        phone = register_info['phone']
        job = register_info['job']

        # print(name, username, hashed_password, phone, job)
        sql = "INSERT INTO UserInfo (name, username, hashed_password, phone, job) VALUES (?, ?, ?, ?, ?)"
        cur.execute(sql, (name, username, hashed_password, phone, job)) 
        db.commit()
        db.close()


        print(request.url)
        return redirect(request.url)

    return render_template('login.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/create', methods=['GET'])
def create():
    return render_template('create.html')

# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         login_info = request.form

#         username = login_info['username']
#         password = login_info['password']

#         sql = "SELECT * FROM UserInfo WHERE username='{}'".format(username)
#         rows_count = cur.execute(sql)

#         if rows_count > 0:
#             user_info = cur.fetchone()
#             print("user_info", user_info)

#             is_pw_correct = bcrypt.checkpw(password.encode('UTF-8'), user_info[2].encode('UTF-8'))
#             print("password_check: ", is_pw_correct)

#         else:
#             print("User does not exist")

#         return redirect(request.url)

#     return render_tamplate('login.html')

