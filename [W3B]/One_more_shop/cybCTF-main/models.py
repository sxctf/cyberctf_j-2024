import sqlite3
from sqlite3 import Error
from os import path


db_file = path.abspath(path.dirname(__file__))
db_file = path.join(db_file, 'db.db')

sql_create_users_table = """ CREATE TABLE IF NOT EXISTS "users" (
                            "id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            "user" text NOT NULL,
                            "password" text,
                            "adress" text,
                            "money" integer,
                            "isadmin" integer); """

sql_create_products_table = """ CREATE TABLE IF NOT EXISTS "products" (
                            "id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            "name" text,
                            "price" int
                            );"""

sql_create_bucket_table = """CREATE TABLE IF NOT EXISTS "bucket" (
                            "id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            "user" text NOT NULL,
                            "product" text
                            );"""

sql_create_orders_table = """CREATE TABLE IF NOT EXISTS "orders" (
                            "order_id" integer PRIMARY KEY NOT NULL,
                            "data" text NOT NULL,
                            "user" text NOT NULL
                            );"""

sql_insert_products_table = """INSERT INTO products (id, name, price) VALUES 
                                        ('5', 'Кольцевой ключ', '400'),
                                        ('4', 'Торцовый ключ', '100'),
                                        ('3', 'Разводной ключ', '300'),
                                        ('2', 'Гаечный ключ', '200'),
                                        ('1', 'Молоток', '1500');
                                        """

sql_insert_users_admin = """INSERT INTO users (id, user, password, adress ,isadmin) VALUES 
                                    ('1', 'admin', 'HelloIAmAdmin','flag{fWNtSLGxPEOQByiellmvlhtH}', True),
                                    ('2', 'Bob', 'DontTryToHack','', '0'),
                                    ('3', 'Alice', 'DontTryToHackMeToo','', '0');
                                        """

sql_insert_orders = """INSERT INTO orders (order_id, data,user) VALUES 
                                        ('1', '9:45:55', 'admin'),
                                        ('2', '10:33:24', 'Bob'),
                                        ('3', '11:46:56', 'Alice');
                                        """

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        c.fetchall()
    except Error as e:
        print(e)

def insert_data_to_table(conn,expression):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(expression)
        row = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def createDB():
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_products_table)
        create_table(conn, sql_create_bucket_table)
        create_table(conn, sql_create_orders_table)
        insert_data_to_table(conn, sql_insert_products_table)
        insert_data_to_table(conn, sql_insert_users_admin)
        insert_data_to_table(conn, sql_insert_orders)
         
    if not path.exists(db_file):
        def create_connection(db_file):
            conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

#Продукты
def getProduct(id):
    conn=create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * from products where id=?",(id))
    row = cur.fetchall()
    return row
def getAllProducts():
    conn = ""
    try:
       conn=sqlite3.connect(db_file)
       cur = conn.cursor()
       cur.execute("SELECT * from products")
       row = cur.fetchall()
       return row
    except Error as e:
       print(e)
    finally:
        if conn:
            conn.close()

#Корзина
def getBasket(user):
    conn=sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * from bucket where user=?;",(user,))
    row = cur.fetchall()
    return row
def insertProductsToBasket(user,product):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("INSERT into bucket (user,product) values (?,?);",(user,product))
        row = cur.fetchall()
        cur.execute("select * from bucket;")
        row = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
def deleteProductsFromBasket(user):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("DELETE from bucket WHERE user = ?;",(user,))
        row = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

#Заказы
def insertOrder(user,datetime):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("INSERT into orders (data, user) values (?,?);",(datetime, user))
        row = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
def getOrders():
    conn=sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * from orders;")
    row = cur.fetchall()
    return row
def getOrdersByUser(user):
    conn=sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * from orders where user = ?;", (user,))
    row = cur.fetchall()
    return row

#Пользователи
def insertUser(user,password):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("INSERT into users(user,password) values (?,?);",(user,password))
        row = cur.fetchall()
        conn.commit()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
def updateUser(user,password):
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("UPDATE users SET password = ? WHERE user = ?;", (password,user))
        row = cur.fetchall()
        conn.commit()
        return conn.total_changes
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
def getUser(user):
    row = ""
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT * from users where user=?",(user,))
        row = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            return row
def getUserID(user):
    row = ""
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("SELECT id from users where user=?",(user,))
        row = cur.fetchall()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            return row
   