from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify, flash
import mariadb
import sys

app = Flask(__name__)
#session 사용을 위한 secret_key 정의
app.secret_key = b'_5#y2L"F4Q8z\\n\\xec]/'

def mariadb_conn():
    try:
        db = mariadb.connect(
            user = 'mtp',
            password = 'password',
            host = 'localhost',
            port = 3306,
            database = 'Users'
            )

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return db
    

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
        degree = register_info['degree']

        print(name, username, hashed_password, phone, degree)
        conn = mariadb_conn()
        cur = conn.cursor()
        sql = "INSERT INTO UserInfo (name, username, hashed_password, phone, degree) VALUES (?, ?, ?, ?, ?)"
        cur.execute(sql, (name, username, hashed_password, phone, degree)) 
        conn.commit()
        conn.close()

    return redirect(url_for('login_page'))


@app.route('/login', methods=['POST'])
def login_info():
    if request.method == 'POST':
        login_info = request.form
        #로그인 사이트에서 username, password 값이 post로 요청되면 아래와 같이 변수에 저장
        username = login_info['username']
        password = login_info['password']
        #쿼리문 실행해서 값을 가져오고 그값을 rows변수에 담는다
        conn = mariadb_conn()
        cur = conn.cursor()
        sql = "SELECT username, hashed_password, degree FROM UserInfo WHERE username=?"
        cur.execute(sql, (username,))
        rows = cur.fetchall() #cur.fetchall() -> 쿼리문으로 실행된 데이터베이스 정보를 list로 저장
        conn.close()
        print(len(rows))
        print(rows)

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
                    session['degree'] = rows[0][2]
                    print(session)
                    return redirect(url_for('calendar'))
            else:
                flash("비밀번호가 틀립니다.")
                return render_template("login.html")
                
        else:
            flash("회원정보가 없습니다.")
            return render_template("login.html")
    
    return redirect(url_for('calendar'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login_page"))

#로그인 상태 유무 확인 및 로그인 유지
#app.before_request -> 사이트가 요청될때마다 route가 실행되기전 항상 먼저 실행된다
@app.before_request
def load_logged_in_user():
    username = session.get('loginned_user')
    degree = session.get('degree') #session 에 'loginned_user' 내용을 가져옴
    # session 에 값이 없을 경우 g.uer(회원정보) 값은 None, 값이 있을경우 회원정보에 username값을 저장
    if username is None:
        g.user = None
    else:
        g.user = username, degree
        print(g.user[1])

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/calendar')
def calendar():
    if g.user is None:
        flash("로그인을 먼저 해주세요.")
        return redirect(url_for("login_page"))
    
    conn = mariadb_conn()
    cur = conn.cursor()

    sql = "SELECT id, title FROM modalContent"
    cur.execute(sql)


    html = ""
    for id, title in cur:
        html += "<li><a href='/calendar/status={id}'>{title}</a></li>".format(id=id, title=title)
        print(id, title)
    conn.close
    
    return render_template('calendar.html', data = html)

@app.route('/modal_data', methods=['POST'])
def modal_data():
    data = request.get_json()

    title = data.get('title')
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    room = data.get('room')
    message_text = data.get('message_text')
    start = data.get('start')
    end = data.get('end')

    sql = """
        INSERT INTO modalContent (title, recipient_name, email, phone_number, room, message_text, start, end) 
        VALUES (?, ?, ?, ?, ?, ?, ? ,?)
        """
    conn = mariadb_conn()
    cur = conn.cursor()
    cur.execute(sql, (title, name, email, phone_number, room, message_text, start, end))
    conn.commit()
    conn.close

    return jsonify(result = "success", result2= data)
 

def data():

    conn = mariadb_conn()
    cur = conn.cursor()
    sql = "SELECT * FROM modalContent"
    cur.execute(sql)
    data_list = []

    for title, recipient_name, email, phone_number, room, message_text, start, end in cur: 
        data_dict = {
            'title': f'{title}',
            'recipient_name': f'{recipient_name}',
            'email': f'{email}',
            'phone_number': f'{phone_number}',
            'room': f'{room}',
            'message_text': f'{message_text}',
            'start': f'{start}',
            'end': f'{end}'
            } 
        
        data_list.append(data_dict)
        print(data_list)
    conn.close
    return data_list

@app.route('/calendar/status=<title_id>')
def status(title_id):

    conn = mariadb_conn()
    cur = conn.cursor()

    sql = "SELECT * FROM modalContent WHERE id={}".format(title_id)
    cur.execute(sql)
    data_list = []

    for id, title, recipient_name, email, phone_number, room, message_text, start, end in cur: 
        data_dict = {
        'id' : f'{id}',
        'title': f'{title}',
        'recipient_name': f'{recipient_name}',
        'email': f'{email}',
        'phone_number': f'{phone_number}',
        'room': f'{room}',
        'message_text': f'{message_text}',
        'start': f'{start}',
        'end': f'{end}'
        } 
    
    data_list.append(data_dict)
    print(data_list)
    conn.close
    return data_dict


if __name__ == "__main__":
    app.debug=True
    app.run(host="0.0.0.0")





