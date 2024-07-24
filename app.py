from flask import Flask, render_template, request
from models import db, Fcuser
import os

app = Flask(__name__)

@app.route('/signup_data', methods=['GET', 'POST'])
def signup_data():
    try:
        if request.method == 'GET':
            return render_template("signup_data.html")
        else:
            # 회원정보 생성
            userid = request.form.get('userid')
            username = request.form.get('username')
            password = request.form.get('password')
            re_password = request.form.get('re_password')

            if not (userid and username and password and re_password):
                return "모두 입력해주세요"
            elif password != re_password:
                return "비밀번호를 확인해주세요"
            else:  # 모두 입력이 정상적으로 되었다면 밑에 명령 실행(DB에 입력됨)
                fcuser = Fcuser()
                fcuser.password = password
                fcuser.userid = userid
                fcuser.username = username
                db.session.add(fcuser)
                db.session.commit()
                return "회원가입 완료"
    except Exception as e:
        return f"에러 발생: {str(e)}"

@app.route('/')
def start():
    return render_template('start.html')

@app.route('/signup_1')
def signup_1():
    return render_template('signup_1.html')

@app.route('/signup_2')
def signup_2():
    return render_template('signup_2.html')

@app.route('/signup_3')
def signup_3():
    return render_template('signup_3.html')

@app.route('/signup_4')
def signup_4():
    return render_template('signup_4.html')

@app.route('/signup_5')
def signup_5():
    return render_template('signup_5.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    basedir = os.path.abspath(os.path.dirname(__file__))  # 데이터베이스 경로를 절대경로로 설정
    dbfile = os.path.join(basedir, 'db.sqlite')  # 데이터베이스 이름과 경로
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    db.app = app
    app.run(port=5001)
    
    with app.app_context():
        db.create_all()  # 테이블 생성

    app.run(host='0.0.0.0', debug=True)  # 디버그 모드 활성화