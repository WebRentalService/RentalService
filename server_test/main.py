import mariadb
import sys
from flask import Flask, render_template, request
app = Flask(__name__)

def get_conn():
    conn = mariadb.connect(
        user = "shk",
        password = "494081",
        host = "localhost",
        port = 3306,
        database = "flask_db"
    )
    return conn



@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/signup", methods=['POST'])
def welcome():
    # 회원가입 로직
    # 유효성 검사
    return render_template('welcome.html')

# http://localhost:5000/edit?id=아이디번호
@app.route("/reporter_edit")
def reporter_edit():
    # 현재 자신의 정보를 보여준다.
    return render_template('reporter_edit.html')

@app.route("/reporter_edit", methods=['POST'])
def reporter_update():
    # 수정된 정보를 반영한다.
    return render_template('reporter.html')

@app.route("/reporter_pw")
def reporter_pw():
    return render_template('reporter_pw.html')


@app.route("/reporter_pw", methods=['POST'])
def reporter_pw_update():
    value = request.form['test']
    return value

@app.route("/reporters")
def reporters():
    import mariadb
    import sys

    sql = "SELECT r_id, nick_name, phone FROM reporter"
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            sql
        )
        result = ""
        result += "<ul>"
        for (r_id, nick_name, phone) in cur:
            # print("{},{}".format(nick_name, phone))
            result += "<li><a href=\"/reporter?id={id}\">{name}</a>, {phone}</li>".format(id=r_id, name=nick_name, phone=phone)   
        result += "</ul>"
    except mariadb.Error as e:
        print("ERR: {}".format(e))
        sys.exit(1)
    if conn:
        conn.close()

    return render_template('reporter_list.html', content = result)

# http://localhost:5000/reporter?id=아이디번호
@app.route('/reporter')
def reporter():
    r_id = request.args.get('id')
    sql = "SELECT r_id as id, nick_name, part, reg_date, email, phone FROM reporter WHERE r_id = {}".format(r_id)

    result = ""

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            sql
        )
        result += '<ul>'
        # (쿼리결과,) ==> 쿼리결과
        for (id, nick_name, part, reg_date, email, phone) in cur:
            result += """
                <li>아이디 = {0}</li>
                <li>별명 = {1}</li>
                <li>부서 = {2}</li>
                <li>가입일 = {3}</li>
                <li>이메일 = {4}</li>
                <li>전화번호 = {5}</li>
                """.format(id, nick_name, part, reg_date, email, phone)
        result += '</ul>'

    except mariadb.Error:
        result = "사용자없음."
        sys.exit(1)
    except TypeError  as e:
        print(e)
    finally:
        if conn:
            conn.close()

    return render_template('reporter.html', content = result)


@app.route('/login')
def login():
    return render_template('login.html')


def reporter_insert():
    # login에서 요청받은 회원정보를 DB에 입력
    # 입력 후 회원목록 페이지로 이동
    return


@app.route('/logout')
def logout():
    # 홈페이지로 이동한다.
    return


@app.route("/posts")
def posts():
    sql = "select p2.p_id, p2.title, r2.r_id , r2.nick_name\
         FROM post p2 left join reporter r2 on p2.reporter = r2.r_id"
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            sql
        )
        result = ""
        result += "<ul>"
        for (p_id, title, r_id, nick_name) in cur:
            # print("{},{}".format(nick_name, phone))
            result += "<li><a href=\"/post?id={pid}\">{title}</a>, <a href=\"/reporter?id={rid}\">{name}</a></li>".format(pid=p_id, title=title, name=nick_name, rid=r_id)   
        result += "</ul>"
    except mariadb.Error as e:
        print("ERR: {}".format(e))
        sys.exit(1)
    if conn:
        conn.close()

    return render_template('post_list.html', content = result)

# http://localhost:5000/post?id=기사번호
@app.route('/post')
def post():
    p_id = request.args.get('id')
    sql = "SELECT p2.p_id, p2.title, p2.content, p2.reg_date, \
        r2.r_id , r2.nick_name \
        FROM post p2 \
        LEFT JOIN reporter r2 on p2.reporter = r2.r_id \
        WHERE p2.p_id = {id}".format(id=p_id)

    result = ""

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            sql
        )
        result += '<ul>'
        # (쿼리결과,) ==> 쿼리결과
        for (p_id, title, content, reg_date, r_id, nick_name) in cur:
            result += """
                <li>기사번호 = {pid}</li>
                <li>기사제목 = {title}</li>
                <li>본문 = {content}</li>
                <li>작성일 = {regdate}</li>
                <li>작성자 = <a href="/reporter?id={rid}">{name}</a></li>
                """.format(pid=p_id, title=title, content=content, \
                    regdate=reg_date, rid=r_id, name=nick_name)
        result += '</ul>'

    except mariadb.Error:
        result = "사용자없음."
        sys.exit(1)
    except TypeError  as e:
        print(e)
    finally:
        if conn:
            conn.close()

    return render_template('reporter.html', content = result)

# 비동기 요청처리
# http://localhost:5000/ajax/checkid?nick_name=신규이름
@app.route('/ajax/checkid')
def checkid():
    nick_name = request.args.get('nick_name')
    # SELECT r_id FROM reporter r2 WHERE nick_name = 'new_user_name'
    sql = "SELECT r_id FROM reporter r2 WHERE nick_name = '{}'".format(nick_name)
    #                                                       ㄴ {}(String타입)을 쓸땐 ' ' 를 꼭 넣어주자

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            sql
        )
        # row에 Tuple 타입으로 데이터가 저장됨. ex)=> (1,)
        row = cur.fetchone()
        result = str(row[0])
    except mariadb.Error as e:
        print("ERR: {}".format(e))
        sys.exit(1)
    except TypeError as e:
        # 쿼리 결과가 없으면 TypeError가 발생
        result = ""
    if conn:
        conn.close()
    
    return result


@app.route('/test')
def test_get():
    # return render_template('test.html')
    return "<div><h1>카리스마대빵큰오리</h1><p>작은오리</p><button>그저 버튼</button></div>"


@app.route('/ajax/test')
def test():
    print("요청을 받았습니다.")
    return "hoho"

    # return "a"    
    # # return 'hiho'
    # # return 123
    # # return <p> 바람이 분다<p>
   


@app.route('/test2')
def test2_get():
    return render_template('test2.html')

@app.route('/ajax/test2')
def test2():
    return '무엇을 넣을까요'



if __name__ == "__main__":
    app.run(host='0.0.0.0')
