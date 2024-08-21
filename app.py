from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_mail import Mail, Message

import re
import os
import random
import string

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2147@localhost/userinfo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jmlee2147@gmail.com'
app.config['MAIL_PASSWORD'] = 'irwjgpldnvmlzkxd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    members = db.relationship('Fcuser', backref='team', foreign_keys='Fcuser.team_id')

class Fcuser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    userid = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.String(10), nullable=False)
    mbti = db.Column(db.String(4), nullable=True)
    profile_picture = db.Column(db.String(50), nullable=True)
    unique_number = db.Column(db.Integer, unique=True, nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    matching = db.Column(db.Boolean, default=False)
    requested = db.Column(db.Boolean, default=False)
    matched_team_id = db.Column(db.Integer, nullable=True)  # 매칭된 팀 ID

@login_manager.user_loader
def load_user(user_id):
    return Fcuser.query.get(int(user_id))

def is_valid_userid(userid):
    if len(userid) < 5 or len(userid) > 20:
        return False
    if not re.match("^[a-zA-Z0-9_]+$", userid):
        return False
    return True

def is_valid_password(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

@app.route('/signup_data', methods=['GET', 'POST'])
def signup_data():
    if request.method == 'POST':
        username = request.form.get('username')
        userid = request.form.get('userid')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        email = session.get('email_receiver')
        gender = request.form.get('gender')
        department = request.form.get('department')
        student_id = request.form.get('student_id')
        mbti = request.form.get('mbti')

        if not (username and userid and password and password_confirm and gender and department and student_id):
            flash("모두 입력해주세요.")
            return redirect(url_for('signup_data'))
        elif not is_valid_userid(userid):
            flash("아이디는 5~20자 영문자와 숫자로만 구성되어야 합니다.")
            return redirect(url_for('signup_data'))
        elif not is_valid_password(password):
            flash("비밀번호는 최소 8자 이상이어야 하며, 영문자, 숫자, 특수문자를 포함해야 합니다.")
            return redirect(url_for('signup_data'))
        elif password != password_confirm:
            flash("비밀번호가 같지 않습니다.")
            return redirect(url_for('signup_data'))
        else:

            try:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                unique_number = random.randint(1000, 9999)
                profile_picture = f'{gender}1.png'
                fcuser = Fcuser(
                    username=username,
                    userid=userid,
                    password=hashed_password,
                    email=email,                    
                    gender=gender,
                    department=department,
                    student_id=student_id,
                    mbti=mbti,
                    unique_number=unique_number,
                    profile_picture=profile_picture
                )
                db.session.add(fcuser)
                db.session.commit()
                
                login_user(fcuser)
                return redirect(url_for('profile'))
            except Exception as e:
                db.session.rollback()
                flash(f"회원가입 실패: {str(e)}")
                return redirect(url_for('signup_data'))

    return render_template("signup_data.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('userid')
        password = request.form.get('password')

        user = Fcuser.query.filter_by(userid=userid).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("아이디나 비밀번호를 확인하세요")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        profile_picture = request.form.get('profile_picture')
        if profile_picture:
            current_user.profile_picture = profile_picture
            db.session.commit()
            flash("회원가입이 완료되었습니다. 다시 로그인해주세요.")
            logout_user()
            return redirect(url_for('profile'))
        flash("프로필 사진을 선택해 주세요.")
        return redirect(url_for('profile'))
    return render_template('profile.html', gender=current_user.gender, profile_picture=current_user.profile_picture)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('start'))

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
@login_required
def index():
    user = current_user
    team = Team.query.get(user.team_id) if user.team_id else None
    team_members = Team.query.get(user.team_id).members if team else []
    return render_template('index.html', user=user, team_members=team_members)

@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/team_register', methods=['GET', 'POST'])
@login_required
def team_register():
    if request.method == 'POST':
        user1_number = request.form.get('user1')
        user2_number = request.form.get('user2')

        current_user_number = current_user.unique_number

        if user1_number == str(current_user_number) or user2_number == str(current_user_number):
            flash("자신의 고유번호를 팀원으로 사용할 수 없습니다.")
            return redirect(url_for('team_register'))

        existing_team = Team.query.filter(Team.members.any(id=current_user.id)).first()
        if existing_team:
            flash("이미 팀에 등록되어 있습니다.")
            return redirect(url_for('index'))

        new_team = Team()  # 이름 없이 팀 생성

        team_member_numbers = [user1_number, user2_number, str(current_user_number)]

        users = Fcuser.query.filter(Fcuser.unique_number.in_(team_member_numbers)).all()

        if len(users) != 3:
            db.session.rollback()
            flash("팀원 고유번호가 올바르지 않습니다.")
            return redirect(url_for('team_register'))

        departments = {user.department for user in users}
        genders = {user.gender for user in users}

        if len(departments) == 1 and len(genders) == 1:
            for user in users:
                user.team = new_team

            db.session.add(new_team)
            db.session.commit()
            flash("팀이 성공적으로 등록되었습니다.")
            return redirect(url_for('index')) 
        else:
            db.session.rollback()
            flash("팀원들의 학과와 성별이 일치하지 않습니다.")
        
        return redirect(url_for('team_register'))

    return render_template('team_register.html')

@app.route("/email", methods=['POST', 'GET'])
def email():
    if request.method == 'POST':
        receiver = request.form['email_receiver'] + '@khu.ac.kr'

        verification_code = random.randint(1000, 999999)
        content = f"인증코드 : {verification_code}"
        session['verification_code'] = verification_code
        session['email_receiver'] = receiver

        recipients = [receiver]   
        result = send_email(recipients, content)
       
        if not result:
            return render_template('email_verification.html', message="인증코드가 발송되었습니다.", status="success")
        else:
            return render_template('email.html', message="이메일을 다시 확인해주세요.", status="error")
       
    else:
        return render_template('email.html')
   
def send_email(recipients, content):
    msg = Message('인증코드', sender = 'jmlee2147@gmail.com (쿠팅)', recipients = recipients)
    msg.body = content

    try:
        mail.send(msg)
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e)
    
@app.route("/email_verification", methods=['POST', 'GET'])
def email_verificiation():
    entered_code = request.form['enter_code']
    stored_code = session.get('verification_code')

    if entered_code == str(stored_code):
        return redirect(url_for('signup_data'))
    else:
        return render_template('email_verification.html', content="인증코드가 올바르지 않습니다")

@app.route('/match_teams', methods=['POST'])
@login_required
def match_teams():
    current_team_id = current_user.team_id

    if not current_team_id:
        return jsonify({"message": "팀 등록을 먼저 해주세요."}), 400

    current_team_users = Fcuser.query.filter_by(team_id=current_team_id).all()
    if not current_team_users:
        return jsonify({"message": "현재 팀 정보를 찾을 수 없습니다."}), 400
    current_user_gender = current_team_users[0].gender
    current_user_department = current_team_users[0].department

    current_user.requested = True
    db.session.add(current_user)
    
    for user in current_team_users:
        user.requested = True
        db.session.add(user)
    db.session.commit()

    requested_teams = db.session.query(Fcuser.team_id).distinct().filter(
        Fcuser.requested.is_(True),
        or_(Fcuser.matching.is_(None), Fcuser.matching.is_(False)),
        Fcuser.team_id != current_team_id,
        Fcuser.gender != current_user_gender,
        Fcuser.department != current_user_department
    ).all()

    if not requested_teams:
        return jsonify({"message": "상대 팀을 찾고 있어요."}), 400

    random_team_id = random.choice([team_id[0] for team_id in requested_teams])
    users_in_random_team = Fcuser.query.filter_by(team_id=random_team_id).all()

    if not users_in_random_team:
        return jsonify({"message": "랜덤 팀의 정보를 찾을 수 없습니다."}), 400

    for user in current_team_users:
        user.matching = True
        user.matched_team_id = random_team_id
        db.session.add(user)
    
    for user in users_in_random_team:
        user.matching = True
        user.matched_team_id = current_team_id
        db.session.add(user)
    
    db.session.commit()

    matched_result_current_team = f"{users_in_random_team[0].department}와 매칭되었습니다! 팀 ID: {random_team_id}"

    return jsonify({
        "current_team_result": matched_result_current_team
    })

@app.route('/fetch_matching_status', methods=['GET'])
@login_required
def fetch_matching_status():
    current_team_id = current_user.team_id

    if not current_team_id:
        return jsonify({"message": "팀 등록을 먼저 해주세요."}), 400

    current_team_users = Fcuser.query.filter_by(team_id=current_team_id).all()
    if not current_team_users:
        return jsonify({"message": "현재 팀 정보를 찾을 수 없습니다."}), 400

    if any(user.requested for user in current_team_users):
        if any(user.matching for user in current_team_users):
            matched_team_id = next((user.matched_team_id for user in current_team_users if user.matching), None)
            matched_team_users = Fcuser.query.filter_by(team_id=matched_team_id).all()
            matched_team_department = matched_team_users[0].department if matched_team_users else "알 수 없음"
            current_team_department = current_team_users[0].department

            if matched_team_department != current_team_department:
                message = f"{matched_team_department}와 매칭되었습니다! 팀 ID: {matched_team_id}"
            else:
                message = "매칭이 완료되었습니다!"
            return jsonify({"message": message})
        else:
            return jsonify({"message": "상대 팀을 찾고 있어요."})
    else:
        return jsonify({"message": "매칭하기 버튼을 눌러 과팅을 시작해보세요"})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')