from flask import Flask, render_template, url_for, request, redirect, current_app, g, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from FDataBase import FDataBase
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from UserLogin import UserLogin
import sqlite3
import os


DATABASE = 'data.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'data.db')))
app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизируйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"
@login_manager.user_loader
def load_user(user_id):
    print("load user")
    return UserLogin().fromDB(user_id, dbase)
#   !!!!! Print можно убрать


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]


@app.route("/")
def index():
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.route("/add_post", methods=["POST", "GET"])
def addPost():
    if request.method == "POST":
        if len(request.form['name']) > 1 and len(request.form['post']) > 1:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления проекта', category='error')
            else:
                flash('Проект добавлен успешно', category='success')
        else:
            flash('Ошибка добавления проекта', category='error')

    return render_template('add_post.html', menu=dbase.getMenu(), title="")


@app.route("/post/<alias>")
@login_required
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


dbase = None
@app.before_request
def before_request():
    """" Установление соединения с БД перед выполнением запроса """
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/about")
def about():
    return render_template('about.html', title="О сайте", menu=menu)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', title="Обратная связь", menu=menu)


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu)


# @app.route("/log", methods=["POST", "GET"])
# def login():
#     if 'userLogged' in session:
#         return redirect(url_for('profile', username=session['userLogged']))
#     elif request.method == 'POST' and request.form['username'] == "admin" and request.form['psw'] == "123":
#         session['userLogged'] = request.form['username']
#         return redirect(url_for('profile', username=session['userLogged']))
#
#     return render_template('log.html', title="", menu=menu)


# @app.route("/profile/<username>")
# def profile(username):
#     if 'userLogged' not in session or session['userLogged'] != username:
#         abort(401)
#     return f"Пользователь: {username}"










#@app.route('/')
#def index():
#    return render_template('index.html')


#app.route('/login')
#def login():
#    return render_template("login.html")


# @app.route('/signup')
# def signup():
#     return render_template("signup.html")


#@app.route('/profile')
#def profile():
#    return render_template("profile.html")

#!!!!!!!!!!!!!!!!!! Старая авторизация
# @app.route('/login', methods=['GET', 'POST'])
# def form_authorization():
#     if request.method == 'POST':
#         Login = request.form.get('Login')
#         Password = request.form.get('Password')
#
#         db_lp = sqlite3.connect('login_password.db')
#         cursor_db = db_lp.cursor()
#         cursor_db.execute(('''SELECT password FROM passwords
#                                                WHERE login = '{}';
#                                                ''').format(Login))
#         pas = cursor_db.fetchall()
#
#         cursor_db.close()
#         try:
#             if pas[0][0] != Password:
#                 return render_template('auth_bad.html')
#         except:
#             return render_template('auth_bad.html')
#
#         db_lp.close()
#         return render_template('successauth.html')
#
#     return render_template('login.html')


#!!!!!!!!!!!!!!!!!! Старая регистрация
# @app.route('/signup', methods=['GET', 'POST'])
# def form_registration():
#     if request.method == 'POST':
#         Login = request.form.get('Login')
#         Password = request.form.get('Password')
#
#         db_lp = sqlite3.connect('login_password.db')
#         cursor_db = db_lp.cursor()
#         sql_insert = '''INSERT OR IGNORE INTO passwords VALUES('{}','{}');'''.format(Login, Password)
#
#         cursor_db.execute(sql_insert)
#
#         cursor_db.close()
#
#         db_lp.commit()
#         db_lp.close()
#
#         return render_template('successregis.html')
#     return render_template('signup.html')


#!!!!!!!!!!!!!!!!!!!!!!!!!! about
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['login']) > 4 and len(request.form['email']) > 4 \
                and len (request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['login'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегестрировались", "success")
                return redirect(url_for('about'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")

    return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['psw'], request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Неверная пара логин/пароль", "error")

    return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")


@app.route('/profile')
@login_required
def profile():
    return f"""<p><a href="{url_for('logout')}">Выйти из профиля</a>
                <p>user info: {current_user.get_id()}"""


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
