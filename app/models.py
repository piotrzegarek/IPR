from datetime import datetime
from typing import Optional
from sqlalchemy.sql import func, desc
from flask_login import logout_user

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
    
    def logout(self):
        logout_user()


class Buyer(db.Model):
    __tablename__ = "buyer"
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self):
        self.offers_controller = OffersController()
        self.comments_controller = CommentsController()
        
    def edit_offer(self, offer_id: int, form_data):
        self.offers_controller.patch({
            "id": offer_id,
            "name": form_data.get("name"),
            "description": form_data.get("description"),
            "date": form_data.get("date"),
            "status": form_data.get("status")
        })
        


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
    
    def patch(self, update_data: dict):
        user = self.get(update_data.get("id"))
        if "password" in update_data.keys():
            user.password = update_data.get("password")
        if "imie" in update_data.keys():
            user.imie = update_data.get("imie")
        if "nazwisko" in update_data.keys():
            user.nazwisko = update_data.get("nazwisko")
        db.session.commit()
    
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
    
    def patch(self, update_data: dict):
        pass

    def get(self, id: int) -> Machine:
        machine = Machine.query.filter_by(id=id).first()
        return machine
    

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
    content = db.Column(db.String(400), nullable=False)

    @property
    def author(self):
        user = UserController().get(self.author_id)
        return f"{user.imie} {user.nazwisko}"
        


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
        if filters:
            comments_query = Comment.query.order_by(Comment.id)
            if "offer_id" in filters.keys():
                comments_query = comments_query.filter_by(offer_id=filters["offer_id"])

            comments = comments_query.all()
        else:
            comments = Comment.query.all()

        return comments
    
    def patch(self, update_data: dict):
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
    status = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    approver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    @property
    def author(self):
        user = UserController().get(self.author_id)
        return f"{user.imie} {user.nazwisko}"
    
    @property
    def approver(self):
        if self.approver_id:
            user = UserController().get(self.approver_id)
            return f"{user.imie} {user.nazwisko}"
        else:
            return "Nie zatwierdzone"
        

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
        if filters:
            offer_query = Offer.query.order_by(Offer.name)
            if "name" in filters.keys():
                offer_query = offer_query.filter(Offer.name.ilike(f"%{filters['name']}%"))
            if "status" in filters.keys():
                offer_query = offer_query.filter(Offer.status.ilike(f"%{filters['status']}%"))
            if "date" in filters.keys():
                offer_query = offer_query.filter(Offer.date == filters["date"])
            if "exclude" in filters.keys():
                offer_query = offer_query.filter(Offer.id != filters["exclude"])
            offers = offer_query.all()
        else:
            offers = Offer.query.all()

        return offers
    
    def patch(self, update_data: dict):
        offer = self.get(update_data.get("id"))
        if "name" in update_data.keys():
            offer.name = update_data.get("name")
        if "description" in update_data.keys():
            offer.description = update_data.get("description")
        if "status" in update_data.keys():
            offer.status = update_data.get("status")
        if "date" in update_data.keys():
            offer.date = update_data.get("date")
        db.session.commit()

    def get(self, id: int) -> Offer:
        offer = Offer.query.filter_by(id=id).first()
        return offer
    