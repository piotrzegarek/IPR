from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    imie = db.Column(db.String(120), nullable=False)
    nazwisko = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username