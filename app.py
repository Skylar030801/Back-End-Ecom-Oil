import sqlite3
from flask import Flask, request, render_template
from flask_cors import CORS


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Database opened successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS register_table(''registerid INTEGER PRIMARY KEY AUTOINCREMENT,'
                 'fullname TEXT,'
                 'usernameTEXT,'
                 'email TEXT,'
                 'password TEXT,')
    print("register_table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS user_table('
                 'userid INTEGER PRIMARY KEY AUTOINCREMENT,'
                 'username TEXT, '
                 'password TEXT,')
    print("user_table created successfully")



    cursor = conn.cursor()
    cursor.execute("SELECT * FROM register_table")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_table")

    print(cursor.fetchall())

init_sqlite_db()

app = Flask(__name__)
CORS(app)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/register/')
def register_test():
    return render_template('register_text.html')


@app.route('/register-user/', methods=["POST"])
def register_user():
    if request.method == 'POST':
        msg = None
        try:
            post_data = request.get_json()
            fullname = post_data['fullname']
            username = post_data['Username']
            email = post_data['email']
            password = post_data['Password']
            with sqlite3.connect('database.db') as conn:

                conn.row_factory = dict_factory

                cur = conn.cursor()
                cur.execute("INSERT INTO user_table(fullname, username, email, password)VALUES "
                            "(?, ?, ?, ?)", (fullname, username, email, password))
                conn.commit()
                msg = "user added succesfully."

        except Exception as e:
            return {'error': str(e)}
        finally:
            conn.close()
            return {'msg': msg}

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/login-user/' , methods=["GET"])
def login_user():
    if request.method == 'GET':
        response = {}
        response['msg'] = None
        response['body'] = []

        try:
            # get_data = request.get_json()
            # username = get_data['username']
            # password = get_data['password']

            with sqlite3.connect('database.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                sql_stmnt = ('SELECT * FROM owner_table')
                cur.execute(sql_stmnt)
                admins = cur.fetchall()
                conn.commit()
                response['body'] = admins
                response['msg'] = "user logged in succesfully."

        except Exception as e:
            conn.rollback()
            response['msg'] = "Something went wrong while verifying a record: " + str(e)

        finally:
            return response

@app.route('/create-blog/', methods=["POST"])
def create_blog():
    if request.method == 'POST':
        msg = None
        try:
            post_data = request.get_json()
            dog_name = post_data['dogname']
            dog_type = post_data['dogtype']
            dog_age = post_data['dogage']
            dog_weight = post_data['weight']
            image_url = post_data['imageurl']
            description = post_data['description']
            with sqlite3.connect('database.db') as conn:

                conn.row_factory = dict_factory

                cur = conn.cursor()
                cur.execute("INSERT INTO dog_table(dogname, dogtype, dogage, weight , imageurl, description)VALUES "
                            "(?, ?, ?, ?, ?, ?)", (dog_name, dog_type, dog_age, dog_weight, image_url[12:], description))
                conn.commit()
                msg = "blog added succesfully."

        except Exception as e:
            return {'error': str(e)}
        finally:
            conn.close()
            return {'msg': msg}

@app.route('/display-content/' , methods=["GET"])
def display_rec():
    if request.method == 'GET':
        response = {}
        response['msg'] = None
        response['body'] = []

        try:
            # get_data = request.get_json()
            # username = get_data['username']
            # password = get_data['password']

            with sqlite3.connect('database.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                sql_stmnt = ('SELECT * FROM dog_table')
                cur.execute(sql_stmnt)
                admins = cur.fetchall()
                conn.commit()
                response['body'] = admins
                response['msg'] = "records on display"

        except Exception as e:
            conn.rollback()
            response['msg'] = "Something went wrong while displaying a record: " + str(e)

        finally:
            return response
