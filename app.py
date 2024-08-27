from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_mail import Mail, Message
from collections import defaultdict

import re
import os
import random
import time
import threading

application = Flask(__name__)


application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1910@localhost/userinfo'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
application.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=1)

application.config['MAIL_SERVER'] = 'smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USERNAME'] = 'jmlee2147@gmail.com'
application.config['MAIL_PASSWORD'] = 'irwjgpldnvmlzkxd'
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
mail = Mail(application)

db = SQLAlchemy(application)
migrate = Migrate(application, db)

login_manager = LoginManager()
login_manager.init_app(application)
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
    groupnumber = db.Column(db.String(50), nullable=True)
    end = db.Column(db.Boolean, default=None, nullable=True)

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

@application.route('/signup_data', methods=['GET', 'POST'])
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

        existing_user = Fcuser.query.filter_by(email=email).first()
        if existing_user:
            flash("이미 존재하는 이메일입니다.")
            return redirect(url_for('signup_data'))

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

@application.route('/login', methods=['GET', 'POST'])
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

@application.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        profile_picture = request.form.get('profile_picture')
        if profile_picture:
            current_user.profile_picture = profile_picture
            db.session.commit()
            flash("회원가입이 완료되었습니다. 로그인해주세요.")
            logout_user()
            return redirect(url_for('profile'))
        flash("프로필 사진을 선택해 주세요.")
        return redirect(url_for('profile'))
    return render_template('profile.html', gender=current_user.gender, profile_picture=current_user.profile_picture)

@application.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('_flashes', None)
    return redirect(url_for('start'))

@application.route('/')
def start():
    return render_template('start.html')

@application.route('/signup_1')
def signup_1():
    return render_template('signup_1.html')

@application.route('/signup_2')
def signup_2():
    return render_template('signup_2.html')

@application.route('/signup_3')
def signup_3():
    return render_template('signup_3.html')

@application.route('/signup_4')
def signup_4():
    return render_template('signup_4.html')

@application.route('/signup_5')
def signup_5():
    return render_template('signup_5.html')

@application.route('/index')
@login_required
def index():
    user = current_user
    team = Team.query.get(user.team_id) if user.team_id else None
    team_members = Team.query.get(user.team_id).members if team else []
    return render_template('index.html', user=user, team_members=team_members,team_id=user.team_id, matching=user.matching,requested=user.requested)

@application.route('/settings')
def settings():
    return render_template('settings.html')


@application.route('/team_register', methods=['GET', 'POST'])
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
            return redirect(url_for('team_register'))

        new_team = Team()

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
            return redirect(url_for('team_register')) 
        else:
            db.session.rollback()
            flash("팀원들의 학과와 성별이 일치하지 않습니다.")
        
        return redirect(url_for('team_register'))

    return render_template('team_register.html')

@application.route('/team_leave', methods=['POST'])
@login_required
def team_leave():
    # 현재 사용자가 속한 팀을 가져오기
    team = Team.query.filter(Team.members.any(id=current_user.id)).first()

    if not team:
        flash("현재 팀에 속해있지 않습니다.")
        return redirect(url_for('settings'))

    if current_user.requested:
        flash("매칭 요청 중에는 팀에서 나갈 수 없습니다.")
        return redirect(url_for('settings'))

    # 팀 삭제
    db.session.delete(team)
    db.session.commit()

    flash("팀이 성공적으로 삭제되었습니다.")
    return redirect(url_for('settings'))

@application.route("/email", methods=['POST', 'GET'])
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
    
@application.route("/email_verification", methods=['POST', 'GET'])
def email_verificiation():
    entered_code = request.form['enter_code']
    stored_code = session.get('verification_code')

    if entered_code == str(stored_code):
        return redirect(url_for('signup_data'))
    else:
        return render_template('email_verification.html', content="인증코드가 올바르지 않습니다")

@application.route('/match_teams', methods=['POST'])
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

     # groupnumber 생성
    groupnumber = f"{current_team_id}_{random_team_id}"


    for user in current_team_users:
        user.matching = True
        user.matched_team_id = random_team_id
        user.groupnumber = groupnumber
        db.session.add(user)
    
    for user in users_in_random_team:
        user.matching = True
        user.matched_team_id = current_team_id
        user.groupnumber = groupnumber
        db.session.add(user)
    
    db.session.commit()

    matched_result_current_team = f"{users_in_random_team[0].department}와 매칭되었습니다!"

    return jsonify({
        "current_team_result": matched_result_current_team
    })

@application.route('/fetch_matching_status', methods=['GET'])
@login_required
def fetch_matching_status():
    current_team_id = current_user.team_id

    if not current_team_id:
        return jsonify({"message": "팀 등록을 먼저 해주세요."}), 400

    current_team_users = Fcuser.query.filter_by(team_id=current_team_id).all()
    if not current_team_users:
        return jsonify({"message": "현재 팀 정보를 찾을 수 없습니다."}), 400

    requested = any(user.requested for user in current_team_users)
    
    matching = any(user.matching for user in current_team_users)

    if matching:
        matched_team_id = next((user.matched_team_id for user in current_team_users if user.matching), None)
        matched_team_users = Fcuser.query.filter_by(team_id=matched_team_id).all()
        matched_team_department = matched_team_users[0].department if matched_team_users else "알 수 없음"
        current_team_department = current_team_users[0].department

        if matched_team_department != current_team_department:
            message = f"<span class='matched-department'>{matched_team_department}</span>와 매칭되었습니다!"
            chat_message = f"{matched_team_department}와 대화중이에요."
        else:
            message = "매칭이 완료되었습니다!"
        return jsonify({"message": message, "chat_message": chat_message, "requested": requested, "matching": matching})
    
    if requested:
        return jsonify({"message": "상대 팀을 찾고 있어요.", "requested": requested, "matching": matching})
    
    return jsonify({"message": "매칭하기 버튼을 눌러 과팅을 시작해보세요.", "requested": requested, "matching": matching})

@application.route('/cancel_match', methods=['POST'])
@login_required
def cancel_match():
    current_team_id = current_user.team_id

    if not current_team_id:
        return jsonify({"message": "팀 등록을 먼저 해주세요."}), 400

    current_team_users = Fcuser.query.filter_by(team_id=current_team_id).all()
    if not current_team_users:
        return jsonify({"message": "현재 팀 정보를 찾을 수 없습니다."}), 400

    for user in current_team_users:
        user.requested = False
        db.session.add(user)
    
    db.session.commit()

    return jsonify({"message": "매칭 요청이 취소되었습니다."})

@application.route('/delete_account', methods=['POST', 'GET'])
@login_required
def delete_account():
    user = current_user

    if user.team_id is not None:
        flash("팀에 속해 있는 경우 회원 탈퇴를 할 수 없습니다. 먼저 팀을 탈퇴하세요.")
        return redirect(url_for('settings'))

    else:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('start'))
        

@application.route('/chatroom')
@login_required
def chatroom():
    user = current_user
    matched_team_members = []

    # 본인 팀의 멤버들
    team_members = []
    if user.team_id:
        team = Team.query.get(user.team_id)
        if team:
            team_members = team.members

    # 매칭된 팀의 멤버들
    if user.matched_team_id:
        matched_team = Team.query.get(user.matched_team_id)
        if matched_team:
            department_dict = defaultdict(list)
            for member in matched_team.members:
                department_dict[member.department].append(member)

            for members in department_dict.values():
                matched_team_members.extend(members[:3])

            matched_team_members = matched_team_members[:6]

    final_members = sorted(set(team_members) | set(matched_team_members), key=lambda x: x.id)[:6]

    room = f'room{user.groupnumber}'

    if not room:
        return jsonify({"message": "매칭된 팀이 없거나 그룹이 생성되지 않았습니다."}), 400

    return render_template('chatroom.html', matched_team_members=final_members, room=room)

chat_rooms = defaultdict(lambda: defaultdict(list))

@application.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    room = data.get('room')
    user = data.get('from')
    message = data.get('message')

    if room and user and message:
        new_message = ChatMessage(user=user, room=room, message=message)
        db.session.add(new_message)
        db.session.commit()
        return jsonify({'status': 'Message received'})
    return jsonify({'status': 'Invalid data'}), 400

@application.route('/receive_message/<room>', methods=['GET'])
def receive_message(room):
    try:
        messages = ChatMessage.query.filter_by(room=room).order_by(ChatMessage.timestamp.asc()).all()
        response = [{'id': msg.id, 'user': msg.user, 'message': msg.message} for msg in messages]
        return jsonify(response)
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return jsonify({'error': 'Unable to fetch messages'}), 500

class ChatMessage(db.Model):
    __tablename__ = 'chat_message'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(50))
    room = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())


@application.route('/get_user_info', methods=['GET'])
@login_required
def get_user_info():
    user = current_user
    return jsonify({'user_id': user.userid, 'user_name': user.username, 'chat_room': f'room{user.groupnumber}'})

@application.route('/agree', methods=['POST'])
@login_required
def agree():
    user = Fcuser.query.get(current_user.id)
    
    if not user:
        return jsonify(success=False, error="User not found"), 404

    if user.end:
        return jsonify(success=False, error="Already agreed"), 400

    user.end = True
    db.session.commit()

    users_in_group = Fcuser.query.filter_by(groupnumber=user.groupnumber).all()

    # 동의한 사용자 수 계산
    agree_count = sum(1 for u in users_in_group if u.end)

    if agree_count >= 4:
        ChatMessage.query.filter_by(room=f'room{user.groupnumber}').delete()
        for u in users_in_group:
            u.matching = False
            u.requested = False
            u.matched_team_id = None
            u.groupnumber = None
            u.end = None
        db.session.commit()


    return jsonify(success=True, count=agree_count, total=len(users_in_group)), 200
    
if __name__ == '__main__':
    application.run(debug=True,host='0.0.0.0')