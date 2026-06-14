from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ---------------- DATABASE MODEL ----------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="user")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------
from sqlalchemy.exc import IntegrityError

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already exists. Please use another email."

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )

        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "User already exists."

        return redirect(url_for("home"))

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)

        # redirect based on role
        if user.role == "admin":
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("dashboard"))

    return "Invalid login details"


# ---------------- USER DASHBOARD ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
@login_required
def admin_dashboard():
    return render_template("admin_dashboard.html", user=current_user)
# ---------------- LOGOUT ----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


# ---------------- CREATE DB ----------------
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)