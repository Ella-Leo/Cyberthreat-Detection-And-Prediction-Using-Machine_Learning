from flask import Flask, render_template, request, redirect, url_for, flash, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF

# ---------------- APP INIT ----------------
app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

REPORT_FOLDER = os.path.join(os.getcwd(), "generated_reports")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------------- FOLDERS ----------------
REPORT_FOLDER = "generated_reports"
UPLOAD_FOLDER = "uploads"

os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            role = request.form.get("role", "user")

            if not username or not email or not password:
                return "Missing form data", 400

            if User.query.filter_by(email=email).first():
                return "Email already exists"

            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                role=role
            )

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("home"))

        except IntegrityError:
            db.session.rollback()
            return "User already exists"

    return render_template("index.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form.get("role")

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):

        if user.role != role:
            return "Incorrect role selected"

        login_user(user)

        if user.role == "admin":
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("dashboard"))

    return "Invalid login details"

# ---------------- DASHBOARDS ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@app.route("/admin_dashboard")
@login_required
def admin_dashboard():

    users = User.query.all()

    return render_template(
        "admin_dashboard.html",
        user=current_user,
        users=users,
        total_users=len(users),
        total_threats=0,
        high_risk=0,
        predictions=0,
        alerts=[]
    )

# ---------------- SOC DASHBOARD ----------------
STREAMLIT_URL = "https://cyberthreat-detection-and-prediction-using-machinelearning-qep.streamlit.app/"

@app.route("/soc_dashboard")
@login_required
def soc_dashboard():
    return redirect(STREAMLIT_URL)

# ---------------- REPORTS ----------------
@app.route("/generate_reports")
@login_required
def generate_reports():
    reports = os.listdir(REPORT_FOLDER)
    return render_template("generate_reports.html", reports=reports)


@app.route("/generate_reports/create/<filetype>")
@login_required
def create_report(filetype):

    data = {
        "threat": ["SQL Injection", "DDoS", "Phishing"],
        "severity": ["High", "Critical", "Medium"],
        "time": [datetime.now(), datetime.now(), datetime.now()]
    }

    df = pd.DataFrame(data)

    filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.{filetype}"
    path = os.path.join(REPORT_FOLDER, filename)

    if filetype == "csv":
        df.to_csv(path, index=False)

    elif filetype == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for i in range(len(df)):
            pdf.cell(200, 10, txt=str(df.iloc[i].to_dict()), ln=True)

        pdf.output(path)

    flash("Report generated successfully!", "success")
    return redirect(url_for("generate_reports"))

@app.route("/download_report/<filename>")
@login_required
def download_report(filename):
    return send_from_directory(REPORT_FOLDER, filename, as_attachment=True)


@app.route("/delete_report/<filename>")
@login_required
def delete_report(filename):
    path = os.path.join(REPORT_FOLDER, filename)

    if os.path.exists(path):
        os.remove(path)
        flash("Report deleted", "success")
    else:
        flash("File not found", "danger")

    return redirect(url_for("generate_reports"))

# ---------------- THREAT PREDICTION ----------------
@app.route("/threat_prediction", methods=["GET", "POST"])
@login_required
def threat_prediction():

    if request.method == "POST":

        # 1. Check request contains file
        if "file" not in request.files:
            flash("No file part found in request", "danger")
            return redirect(url_for("threat_prediction"))

        uploaded_file = request.files["file"]

        # 2. Check file selected
        if uploaded_file.filename == "":
            flash("No file selected", "danger")
            return redirect(url_for("threat_prediction"))

        # 3. Optional: check CSV extension
        if not uploaded_file.filename.endswith(".csv"):
            flash("Only CSV files allowed", "danger")
            return redirect(url_for("threat_prediction"))

        # 4. Save file safely
        filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(filepath)

        # 5. Read CSV safely
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            flash(f"Error reading CSV file: {str(e)}", "danger")
            return redirect(url_for("threat_prediction"))

        # 6. Mock prediction
        df["Prediction"] = "Normal"

        return render_template(
            "threat_prediction.html",
            raw_data=df.head(50).to_html(classes="table table-dark", index=False),
            results=df[["Prediction"]].head(50).to_html(classes="table table-dark", index=False)
        )

    return render_template("threat_prediction.html")

# ---------------- MANAGE USERS----------------
@app.route("/manage_users", methods=["GET", "POST"])
@login_required
def manage_users():

    if current_user.role != "admin":
        flash("Access denied. Admins only.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if not username or not email or not password:
            flash("All fields are required", "danger")
            return redirect(url_for("manage_users"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for("manage_users"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        flash("User added successfully", "success")
        return redirect(url_for("manage_users"))

    users = User.query.all()
    return render_template("manage_users.html", users=users)

# ---------------- DELETE USER ----------------
@app.route("/delete_user/<int:user_id>")
@login_required
def delete_user(user_id):

    if current_user.role != "admin":
        flash("Access denied", "danger")
        return redirect(url_for("dashboard"))

    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("manage_users"))

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")
    return redirect(url_for("manage_users"))

# ---------------- LOGOUT ----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# ---------------- CREATE DB ----------------
with app.app_context():
    db.create_all()

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)