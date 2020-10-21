from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify, flash
import mariadb
import sys

app = Flask(__name__)
#session 사용을 위한 secret_key 정의
app.secret_key = b'_5#y2L"F4Q8z\\n\\xec]/'

try:
    db = mariadb.connect(
<<<<<<< HEAD
        user = 'mtp',
        password = 'password',
        host = 'localhost',
        port = 3306,
=======
        user = 'lyw',
        password = 'lee',
        host = 'localhost',
        port = 13306,
>>>>>>> lee
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
        hashed_password = register_info['password']
        phone = register_info['phone']

        print(name, username, hashed_password, phone)
        sql = "INSERT INTO UserInfo (name, username, hashed_password, phone) VALUES (?, ?, ?, ?)"
        cur.execute(sql, (name, username, hashed_password, phone)) 
        db.commit()
<<<<<<< HEAD
        db.close()

        print(request.url)

    return render_template('login.html')
=======
        # db.close()

    return redirect(url_for('login_page'))
>>>>>>> lee


@app.route('/login', methods=['POST'])
def login_info():
    if request.method == 'POST':
        login_info = request.form
        #로그인 사이트에서 username, password 값이 post로 요청되면 아래와 같이 변수에 저장
        username = login_info['username']
        password = login_info['password']
        #쿼리문 실행해서 값을 가져오고 그값을 rows변수에 담는다
        sql = "SELECT username, hashed_password FROM UserInfo WHERE username=?"
        cur.execute(sql, (username,))
        rows = cur.fetchall() #cur.fetchall() -> 쿼리문으로 실행된 데이터베이스 정보를 list로 저장
        print(len(rows))

        #post로 요청한 username에 값이 데이터 베이스에 있을경우 len(rows)=1, 없을경우 len(lows)=0
        if len(rows) > 0:
            print("user info: ", rows[0])
            #요청한 값이 있을경우 비밀번호 확인
            if password == rows[0][1]:
                password_check = True
                print("password check: ", password_check)

                if password_check == True:
                    session.clear()
                    session['loginned_user'] = username
                    print(session)
                    return redirect(url_for('calendar'))
            else:
                flash("비밀번호가 틀립니다.")
<<<<<<< HEAD
=======
                print("비밀번호가 틀립니다.")
>>>>>>> lee
                return render_template("login.html")
                
        else:
            flash("회원정보가 없습니다.")
<<<<<<< HEAD
            return render_template("login.html")
    
    return redirect(url_for('calendar'))
=======
            print("회원정보가 없습니다.")
            return render_template("login.html")
    # return redirect(url_for('calendar'))
>>>>>>> lee

@app.route('/logout')
def logout():
    session.clear()
<<<<<<< HEAD
    return redirect(url_for("login_page"))
=======
    print(session)
    return render_template('main.html')
>>>>>>> lee

#로그인 상태 유무 확인 및 로그인 유지
#app.before_request -> 사이트가 요청될때마다 route가 실행되기전 항상 먼저 실행된다
@app.before_request
def load_logged_in_user():
    username = session.get('loginned_user') #session 에 'loginned_user' 내용을 가져옴
    # session 에 값이 없을 경우 g.uer(회원정보) 값은 None, 값이 있을경우 회원정보에 username값을 저장
    if username is None:
        g.user = None
    else:
<<<<<<< HEAD
        g.user = username

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/create')
=======
        sql = "SELECT username FROM UserInfo WHERE username=?"
        cur.execute(sql, (username,))
        user = cur.fetchall()
        print(user)
        g.user = user[0][0]
        print(g.user)

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/create', methods=['GET'])
>>>>>>> lee
def create():
    return render_template('create.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/calendar')
def calendar():
<<<<<<< HEAD
    if g.user is None:
        flash("로그인을 먼저 해주세요.")
        return redirect(url_for("login_page"))

=======
>>>>>>> lee
    return render_template('calendar.html')

if __name__ == "__main__":
    app.debug=True
<<<<<<< HEAD
    app.run(host="0.0.0.0")
=======
    app.run()
    # app.secret_key = 'super secret key'
    # app.config['SEESION_TYPE'] = 'filesystem'
>>>>>>> lee



