from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages #render_template으로 html파일 렌더링
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2147@localhost/userinfo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Fcuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.String(10), nullable=False)
    mbti = db.Column(db.String(4), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return Fcuser.query.get(int(user_id))
    

@app.route('/signup_data', methods=['GET', 'POST'])
def signup_data():
    if request.method == 'GET':
        return render_template("signup_data.html")
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        gender = request.form.get('gender')
        department = request.form.get('department')
        student_id = request.form.get('student_id')
        mbti = request.form.get('mbti')

        if not (userid and password and password_confirm and gender and department and student_id):
            return "모두 입력해주세요"
        elif password != password_confirm:
            return "비밀번호를 확인해주세요"
        else:
            hashed_password = generate_password_hash(password, method='sha256')
            fcuser = Fcuser(
                userid=userid,
                password=hashed_password,  # 해시된 비밀번호 저장
                gender=gender,
                department=department,
                student_id=student_id,
                mbti=mbti
            )
            db.session.add(fcuser)
            db.session.commit()
            return redirect(url_for('index'))

        
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form.get('userid')
        password = request.form.get('password')
        
        user = Fcuser.query.filter_by(userid=userid).first()
        
        if user and check_password_hash(user.password, password):
            session['userid'] = user.userid
            return redirect(url_for('index'))
        else:
            return "로그인 실패: 아이디나 비밀번호를 확인하세요"
        

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

@app.route('/index')
def index():
    return render_template('index.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
