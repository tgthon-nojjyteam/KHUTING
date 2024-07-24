from flask import Flask, render_template, request #render_template으로 html파일 렌더링
from models import db
import os
from models import Fcuser
app = Flask(__name__)

@app.route('/signup_data', methods=['GET','POST'])
def signup_data():
    if request.method == 'GET':
        return render_template("signup_data.html")
    else:
        #회원정보 생성
        userid = request.form.get('userid') 
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        print(password) # 들어오나 확인해볼 수 있다. 


        if not (userid and username and password and re_password) :
            return "모두 입력해주세요"
        elif password != re_password:
            return "비밀번호를 확인해주세요"
        else: #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
            fcuser = Fcuser()         
            fcuser.password = password           #models의 FCuser 클래스를 이용해 db에 입력한다.
            fcuser.userid = userid
            fcuser.username = username      
            db.session.add(fcuser)
            db.session.commit()
            return "회원가입 완료"

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
    basedir = os.path.abspath(os.path.dirname(__file__))  # database 경로를 절대경로로 설정함
    dbfile = os.path.join(basedir, 'db.sqlite') # 데이터베이스 이름과 경로
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True     # 사용자에게 원하는 정보를 전달완료했을때가 TEARDOWN, 그 순간마다 COMMIT을 하도록 한다.라는 설정
    #여러가지 쌓아져있던 동작들을 Commit을 해주어야 데이터베이스에 반영됨. 이러한 단위들은 트렌젝션이라고함.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # True하면 warrnig메시지 유발, 

    db.init_app(app) #초기화 후 db.app에 app으로 명시적으로 넣어줌
    db.app = app

    with app.app_context():
        db.create_all() 
        
    app.run(host='0.0.0.0')