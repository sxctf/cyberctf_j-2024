from sqlite3 import Error
from os import path


db_file = path.abspath(path.dirname(__file__))
db_file = path.join(db_file, 'db.db')

sql_create_trains_table = """ CREATE TABLE IF NOT EXISTS "train" (
                            "id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            "name" text NOT NULL,
                            "maxPassengers" int); """

sql_create_cargo_table = """ CREATE TABLE IF NOT EXISTS "cargo" (
                            "id" integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            "name" text NOT NULL,
                            "amount" int,
                            "train_ID" int);  """

sql_insert_into_trains_table = """INSERT INTO train (id, name, maxPassengers) VALUES 
                                        ('1', 'Синий', '10'),
                                        ('2', 'Красный', '30'),
                                        ('3', 'Зеленый', '50' ),
                                        ('4', 'Коричневый', '20'),
                                        ('5', 'Белый', '40');
                                        """


sql_insert_into_cargo_table = """INSERT INTO cargo (id, name, amount, train_ID) VALUES 
                                        ('1', 'Дрова', '1000', '5'),
                                        ('2', 'Железо', '500', '4'),
                                        ('3', 'Химикаты', '400', '3' ),
                                        ('4', 'Краска', '300', '2'),
                                        ('5', 'Органика', '100', '1');
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
        print(sqlite3.version)
        cur = conn.cursor()
        cur.execute(expression)
        row = cur.fetchall()
        conn.commit()
        print(row)
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
        create_table(conn, sql_create_trains_table)
        create_table(conn, sql_create_cargo_table)
        insert_data_to_table(conn, sql_insert_into_trains_table)
        insert_data_to_table(conn, sql_insert_into_cargo_table)
         
    if not path.exists(db_file):
        def create_connection(db_file):
            conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

#Продукты
def getCargo(train_ID):
    conn=create_connection(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * from cargo where train_ID=?",(train_ID,))
    row = cur.fetchall()
    return row

#Поезда
def getTrains():
    conn=sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT * from trains;")
    row = cur.fetchall()
    return row
