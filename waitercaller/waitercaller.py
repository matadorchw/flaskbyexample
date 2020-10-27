import datetime

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user

from passwordhelper import PasswordHelper
from bitlyhelper import BitlyHelper
from user import User

from forms import RegistrationForm

import config

if config.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
app.secret_key = 'tPXJY3X37Qybz4QykV+hOyUxVQeEXf1Ao2C8upz+fGQXKsM'
login_manager = LoginManager(app)

DB = DBHelper()
PH = PasswordHelper()
BH = BitlyHelper()


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    stored_user = DB.get_user(email)
    if stored_user and PH.validate_password(password,
                                            stored_user['salt'],
                                            stored_user['hashed']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    return home()


@app.route("/register", methods=["POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template("home.html", loginform=None,
                                   registrationform=form)
        salt = PH.get_salt()
        hashed = PH.get_hash(form.password2.data + salt)
        DB.add_user(form.email.data, salt, hashed)
        return render_template("home.html", loginform=None,
                               registrationform=form,
                               onloadmessage="Registration successful. Please Log in.")
    return render_template("home.html", loginform=None, registrationform=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/")
def home():
    return render_template("home.html", loginform=None,
                           registrationform=RegistrationForm())


@app.route("/dashboard")
@login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_requests(current_user.get_id())
    for req in requests:
        deltaseconds = (now - req['time']).seconds
        req['wait_minutes'] = "{}.{}".format((deltaseconds // 60),
                                             str(deltaseconds % 60).zfill(2))
    return render_template("dashboard.html", requests=requests)


@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
    request_id = request.args.get("request_id")
    DB.delete_request(request_id)
    return redirect(url_for('dashboard'))


@app.route("/account")
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html", tables=tables)


@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
    tablename = request.form.get('tablenumber')
    tableid = DB.add_table(tablename, current_user.get_id())
    new_url = BH.shorten_url(config.base_url + "newrequest/" + tableid)
    DB.update_table(tableid, new_url)
    return redirect(url_for('account'))


@app.route("/account/deletetable")
@login_required
def account_deletetable():
    tableid = request.args.get("tableid")
    DB.delete_table(tableid)
    return redirect(url_for('account'))


@app.route("/newrequest/<tid>")
def new_request(tid):
    DB.add_request(tid, datetime.datetime.now())
    return "Your request has been logged and a waiter will be with you shortly"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
