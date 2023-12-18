# Modules used
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap


# Flask instance
app = Flask(__name__)
bootstrap = Bootstrap(app)

# Set the secret key for CSRF protection
app.config['SECRET_KEY'] = "b'\xcd\xa5\x8e\xa1\xaeT\xf0l\xb5cALR\x06q\xd3\xb3\xc8\xad\xf0\x99\x99\xc8\x8f'"


registered_users = {}

# Define the LoginForm using FlaskForm
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min= 8)])
    submit = SubmitField(label="Log In", validators=[DataRequired()])

# Define the RegistrationForm using FlaskForm
class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min= 8)])
    submit = SubmitField(label="Log In", validators=[DataRequired()])

# Route for user registration
@app.route("/register", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        registered_users[email] = {"email": email, "password": password}
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

# Route for the home page
@app.route("/")
def home():
    return render_template('index.html')

# Route for user login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    form.validate_on_submit()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if email in registered_users and registered_users[email]["password"] == password:
            return render_template("success.html", form=form)
        else:
            return render_template("denied.html", form=form)
    return render_template("login.html", form=form)

#  Run the Flask app if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
