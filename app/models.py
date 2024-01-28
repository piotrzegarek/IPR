from datetime import datetime
from typing import Optional
from sqlalchemy.sql import func

from app import db
from .controllers import Controller

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    imie = db.Column(db.String(120), nullable=False)
    nazwisko = db.Column(db.String(120), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    buyer = db.relationship("Buyer", uselist=False, backref="buyer")
    
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return str(self.id)

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Buyer(db.Model):
    __tablename__ = "buyer"
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self):
        self.offers_controller = OffersController()
        self.comments_controller = CommentsController()


class UserController(Controller):
    def add(self, obj: User) -> User:
        db.session.add(obj)
        db.session.commit()
        db.session.flush() # Refresh obj with user id

        return obj
    
    def delete(self, id: int):
        user = User.query.filter_by(id=id).first()

        if user:
            db.session.delete(user)
            db.session.commit()

    def list(self, filters: Optional[dict] = None):
        pass

    def get(self, id: int) -> User:
        user = User.query.filter_by(id=id).first()
        return user
    
    def find_by_username(self, username: str) -> User:
        """Get user by its username"""
        user = User.query.filter_by(username=username).first()
        return user
    

class Machine(db.Model):
    __tablename__ = "machine"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    owned = db.Column(db.Boolean, default=False)


class MachineController(Controller):
    def add(self, obj: Machine) -> Machine:
        db.session.add(obj)
        db.session.commit()
        db.session.flush() # Refresh obj with machine id

        return obj
    
    def delete(self, id: int):
        machine = Machine.query.filter_by(id=id).first()

        if machine:
            db.session.delete(machine)
            db.session.commit()

    def list(self, filters: Optional[dict] = None):
        if filters:
            mach_query = Machine.query.with_entities(
                Machine.name, Machine.model, func.count().label('count')
                ) \
                .group_by(Machine.name, Machine.model) \
                .order_by(Machine.name)
            if "owned" in filters.keys():
                mach_query = mach_query.filter_by(owned=True)
            if "name" in filters.keys():
                mach_query = mach_query.filter(Machine.name.ilike(f"%{filters['name']}%"))
            if "model" in filters.keys():
                mach_query = mach_query.filter(Machine.model.ilike(f"%{filters['model']}%"))
            machines = mach_query.all()
        else:
            machines = Machine.query.all()

        return machines

    def get(self, id: int) -> Machine:
        machine = Machine.query.filter_by(id=id).first()
        return machine
    

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.String(400), nullable=False)


class CommentsController(Controller):
    def add(self, obj: Comment) -> Comment:
        db.session.add(obj)
        db.session.commit()
        db.session.flush() # Refresh obj with comment id

        return obj
    
    def delete(self, id: int):
        comment = Comment.query.filter_by(id=id).first()

        if comment:
            db.session.delete(comment)
            db.session.commit()

    def list(self, filters: Optional[dict] = None):
        pass

    def get(self, id: int) -> Comment:
        comment = Comment.query.filter_by(id=id).first()
        return comment
    

class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class OffersController(Controller):
    def add(self, obj: Offer) -> Offer:
        db.session.add(obj)
        db.session.commit()
        db.session.flush() # Refresh obj with offer id

        return obj
    
    def delete(self, id: int):
        offer = Offer.query.filter_by(id=id).first()

        if offer:
            db.session.delete(offer)
            db.session.commit()

    def list(self, filters: Optional[dict] = None):
        pass

    def get(self, id: int) -> Offer:
        offer = Offer.query.filter_by(id=id).first()
        return offer
    