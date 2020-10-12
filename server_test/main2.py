from flask import Flask, render_template, request
app = Flask(__name__)


'''
Mariadb 연결 위치
def get_conn():
    conn = mariadb.connect(
        user = "shk",
        password = "494081",
        host = "localhost",
        port = 3306,
        database = "flask_db"
    )
    return conn
'''


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login')
def login():
    return pass

@app.route('/sign_up')
def sign_up():
    return pass

@app.route('/student')
def student():
    return pass

@app.route('/find_class')
def find_class():
    return pass

@app.route('/login')
def login():
    return pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5002')