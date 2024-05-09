from flask import Flask, redirect, render_template, request, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user
import models
import time
import array
import re

app = Flask(__name__)
models.createDB()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
userlogin = ""

app.config['SECRET_KEY'] = 'a really really really really long secret key'

headings = ("Номер","Наименование","Цена")
data = (
    ("Гаечный ключ","200","accountName"),
    ("Разводной ключ","300","accountName"),
    ("Торцовый ключ","100","accountName"),
    ("Кольцевой ключ","400","accountName")
)

@app.route('//')
def main():
    if request.method == "GET":
        row = ""
        row = models.getOrders()
        return render_template("index.html", headings = ("Номер заказа","Дата заказа", "Пользователь"), data = row)
    return render_template("index.html")

@app.route('/products', methods=['GET', 'POST'])
@login_required
def products():
    row = models.getAllProducts()
    if request.method == "GET":
        return render_template("products.html",headings = headings, data = row)
    if request.method == "POST":
        username = session['username']
        product_id = request.form.get('product_id')
        models.insertProductsToBasket(username,product_id)
        flash("Продукт добавлен в корзину")
        return render_template("products.html",headings = headings, data = row)

@app.route('/profile')
@login_required
def profile():
    content = {}
    content ['username'] = []
    content ['username'] = session['username']
    flash("Флаг:")
    flash(session['flag'])
    row = models.getOrdersByUser(session['username'])

    return (render_template("profile.html",context = content, headings = ("Номер заказа","Время","Пользователь"), data = row))
    

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        login = str(request.form['username'])
        password = str(request.form['password'])
        if not validate(str(login)):
            flash("Допускается вводить только буквы и цифры")
            return render_template("registration.html")
        if not validate(str(password)):
            flash("Допускается вводить только буквы и цифры")
            return render_template("registration.html")
        out = str(models.updateUser(login,password))
        if(out!='0'):
            flash("Пароль изменен")
        else:
            models.insertUser(login,password)
        return redirect(url_for('login'))
    return render_template("registration.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        validated_username = str(request.form['username']) 
        validated_password = str(request.form['password'])
        if not validate(str(validated_username)):
            flash("Допускается вводить только буквы и цифры")
            return render_template("login.html")
        if not validate(str(validated_password)):
            flash("Допускается вводить только буквы и цифры")
            return render_template("login.html")

        session['username'] = validated_username
        session['password'] = validated_password
        row = models.getUser(session['username'])
        arr = []
        if len(row)!=0:
            for i in row[0]:
                arr.append(i)
            if(session['password']!=arr[2]):
                flash("Неверный пароль / логин")
                return render_template("login.html")
            else:
                userlogin = UserLogin().create(arr[1])
                login_user(userlogin)
                flash("Успешный вход")
                content = {}
                content ['username'] = []
                content ['username'] = session['username']
                session['flag'] = arr[3]
                session['authenticated'] = "1"
                return render_template("profile.html",context = content)
        else:
            flash("Неверный пароль / логин")
            return render_template("login.html")

    if request.method == 'GET':
        return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    session.pop('authenticated','0')
    session.pop('username','0')
    session.pop('password','0')
    flash("Вы вышли из аккаунта","success")
    return redirect(url_for('login'))

@app.route('/basket',methods=['GET','POST'])
@login_required
def basket():
    if request.method == 'GET':
        row=[]
        products = models.getAllProducts()
        username = session['username']
        userproducts = models.getBasket(username)
        for prod in products:
            for userprod in userproducts:
                if userprod[2]==str(prod[0]):
                    row.append(prod)
        if len(row)== 0:
            flash("Корзина пустая")      
        return render_template('basket.html', headings = headings, data = row)
    if request.method == 'POST':
        row = []
        username = session['username']
        userproducts = models.getBasket(username)
        if len(userproducts)!= 0:
            t = time.localtime() 
            current_time = time.strftime("%H:%M:%S", t)
            models.insertOrder(username, current_time)
            models.deleteProductsFromBasket(username)
            flash ("Заказ сделан")
        else:
            flash ("Корзина пустая")
        
        content = {}
        content ['username'] = []
        content ['username'] = session['username']
        row = models.getOrdersByUser(session['username'])
    return (render_template("profile.html",context = content, headings = ("Номер заказа","Время","Пользователь"), data = row))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(userlogin):
    return UserLogin().fromDB(userlogin)


def validate(s):
    # Регулярное выражение для проверки, содержит ли строка только буквы и цифры
    regex = re.compile(r'^[a-zA-Z0-9]+$')
    ss = str(s)
    a = regex.match(str(s))
    if a !=None:
        return True
    else:
        return False

class UserLogin():
    def fromDB(self,user):  
        self.__user = models.getUserID(user)
        return self
    def create (self,user):
        self.__user=user
        return self
    def is_authenticated(self):

            return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        out = ""
        id = models.getUserID(self.__user)
        if len(id)!=0:
            for i in id:
                out = i
                break
            return out[0]
        else:
            return NULL

if __name__ == '__main__':
    app.run(debug=False, port = 8001, host='0.0.0.0')
