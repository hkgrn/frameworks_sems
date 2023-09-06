from flask import Flask, request, redirect, make_response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Данные из формы

        user_name = request.form['user_name']
        user_email = request.form['user_email']

        # Создаем cookie файл с данными

        resp = make_response(redirect('/welcome'))
        resp.set_cookie('user_name', user_name)
        resp.set_cookie('user_email', user_email)
        return resp

    return '''
    <form method="POST" action="/">
        <label for="user_name">Имя:</label>
        <input type="text" name="user_name" id="user_name"><br>
        <label for="user_email">Email:</label>
        <input type="text" name="user_email" id="user_email"><br>
        <input type="submit" value="Отправить">
    </form>
    '''


@app.route('/welcome')
def welcome():
    # Данные пользователя из cookie
    user_name = request.cookies.get('user_name')

    if user_name:
        return f'Привет, {user_name}! <a href="/logout">Выйти</a>'
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    # Удаляем cookie файл
    resp = make_response(redirect('/'))
    resp.delete_cookie('user_name')
    resp.delete_cookie('user_email')
    return resp


if __name__ == '__main__':
    app.run(debug=True)