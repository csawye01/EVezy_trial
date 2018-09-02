import os
from flask import Flask
from flask import render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, login_required
from models import User, Permission, Cars, Bookings
from forms import LoginForm, BookingsForm
from decorators import permission_required
from datetime import datetime


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "cardatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route("/", methods=["GET", "POST"])
def home():
    form = BookingsForm()
    if form.validate_on_submit():
        item_add = Bookings(email=form.email.data, start_date=form.start_date.data,
                            duration=form.duration.data, start_time=form.start_time.data, car_make=form.car_make.data,
                            car_model=form.car_model.data)

        db.session.add(item_add)
    else:
        flash('Booking not available.')

    cars = Cars.query.all()
    return render_template("index.html", cars=cars)


@login_required
@permission_required(Permission.EDIT_DB)
@app.route("/update", methods=["POST"])
def update():
    try:
        newregistration = request.form.get("newregistration")
        oldregistration = request.form.get("oldregistration")
        car = Cars.query.filter_by(registration=oldregistration).first()
        car.registration = newregistration
        db.session.commit()
    except Exception as e:
        print("Couldn't update car inventory")
        print(e)
    return redirect("/")


@login_required
@permission_required(Permission.EDIT_DB)
@app.route("/delete", methods=["POST"])
def delete():
    registration = request.form.get("registration")
    car = Cars.query.filter_by(registration=registration).first()
    db.session.delete(car)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)