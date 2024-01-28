from flask import redirect, url_for, request, render_template
from flask_login import login_required, current_user

from app import app
from .forms import LoginForm, ChangePasswordForm, WarehouseSearchForm, OfferCreateForm, OfferSearchForm, AddCommentForm
from .auth import AuthService
from .models import MachineController, Offer, OffersController, CommentsController, Comment


@app.route("/")
@login_required
def home():

    return render_template("home.html")


@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    error = False

    if request.method == 'POST' and form.validate():
        data = request.form
        auth = AuthService(data.get("username"))
        if auth.validatePassword(password=data.get("password")):
            auth.login(password=data.get("password"))
            return redirect(url_for("home"))
        else:
            error = True
            
    return render_template('login.html', form=form, error=error)


@app.route("/change-password", methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)

    if request.method == 'POST' and form.validate():
        data = request.form
        auth = AuthService(current_user.username)
        if auth.changePassword(data.get("old_password"), data.get("new_password"), data.get("confirm_password")):
            return render_template('change_password.html', form=form, success=True)
        else:
            return render_template('change_password.html', form=form, error=True)

    return render_template('change_password.html', form=form)


@app.route("/warehouse", methods=['GET','POST'])
@login_required
def warehouse():
    form = WarehouseSearchForm(request.form)
    controler = MachineController()

    filters = {"owned": True}
    if request.method == 'POST' and form.validate():
        if request.form.get("name"):
            filters["name"] = request.form.get("name")
        if request.form.get("model"):
            filters["model"] = request.form.get("model")

    data = controler.list(filters)

    return render_template("warehouse.html", form=form, data=data)


@app.route("/offers", methods=['GET','POST'])
@login_required
def offers():
    form = OfferSearchForm()
    controler = OffersController()
    filters = {}
    if request.method == 'POST' and form.validate():
        if request.form.get("name"):
            filters["name"] = request.form.get("name")
        if request.form.get("status"):
            filters["status"] = request.form.get("status")
        if request.form.get("date"):
            filters["date"] = request.form.get("date")


    data = controler.list(filters)

    return render_template("offers.html", form=form, data=data)


@app.route("/offers/new", methods=['GET', 'POST'])
@login_required
def new_offer():
    form = OfferCreateForm()
    if request.method == 'POST' and form.validate():
        data = request.form
        offer = Offer(
            name=data.get("name"),
            description=data.get("description"),
            date=data.get("date"),
            status=data.get("status"),
            author_id=current_user.id
        )
        buyer = Buyer()
        buyer.offers_controller.add(offer)
        return render_template("new_offer.html", form=form, success=True)
        
    return render_template("new_offer.html", form=form)


@app.route("/offer/<int:id>", methods=['GET','POST'])
@login_required
def view_offer(id: int):
    controller = OffersController()
    offer = controller.get(id)
    others = controller.list({"exclude": offer.id})
    comment_form = AddCommentForm()
    comments_controller = CommentsController()
    comments = comments_controller.list({"offer_id": id})

    return render_template("view_offer.html", offer=offer, others=others, form=comment_form, comments=comments)


@app.route("/add-comment", methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)

    if form.validate():
        new_comment = Comment()
        new_comment.content = request.form.get("content")
        new_comment.offer_id = request.form.get("offer_id")
        new_comment.author_id = current_user.id
        controller = CommentsController()
        controller.add(new_comment)
    
    return redirect(url_for('view_offer', id=request.form.get("offer_id")))


@app.route("/logout")
@login_required
def logout():
    user = User()
    user.logout()
    return redirect(url_for('login'))


############################################### HELP  ROUTES
from .models import User, Buyer
from app import bcrypt, db

@app.route("/add-user")
def add_user():
    hash_password = bcrypt.generate_password_hash("testuser").decode("utf-8")
    user = User(
        username = "testuser",
        password = hash_password,
        imie = "Test",
        nazwisko = "User"
    )
    db.session.add(user)
    db.session.commit()

    buyer = Buyer()
    buyer.user_id = user.id
    buyer.department = "Department A"
    db.session.add(buyer)
    db.session.commit()
    
