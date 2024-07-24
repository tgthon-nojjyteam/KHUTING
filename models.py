from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Fcuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
# 하잉