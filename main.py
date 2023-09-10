import hashlib
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm  # Импортируем форму из отдельного файла

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '2khjgh59687ldnmrnvk5'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        # Хешируем пароль с использованием hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Создаем нового пользователя
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)

        # Добавляем пользователя в базу данных
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('registration_success'))

    return render_template('register.html', form=form)


@app.route('/registration_success')
def registration_success():
    return render_template('teg_success.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
