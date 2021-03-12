import sqlite3
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

def create_user():
    connected = sqlite3.connect('HN.db')
    print("created database")
    connected.execute('CREATE TABLE IF NOT EXISTS users(' 
                      'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                      'fullname TEXT,'
                      'username TEXT,'
                      'email TEXT,'
                      'password TEXT)'
                      )
    print("user table created")

create_user()

def create_product():
    connected = sqlite3.connect('HN.db')
    print("created database")
    connected.execute('CREATE TABLE IF NOT EXISTS products('
                      'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                      'products TEXT,'
                      'price TEXT,'
                      'description TEXT,'
                      'image TEXT)'
                      )
    print("products table created")

create_product()



app = Flask(__name__)
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
@app.route('/user-register/', methods=["POST"])
def register():
    if request.method == "POST":
        msg = None
    try:
        post = request.get_json()
        fullname = post['fullname']
        username = post['username']
        email = post['email']
        pin = post['pin']

        with sqlite3.connect('HN.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (fullname, username, email, password) VALUES"
                        "(?, ?, ?, ?)",(fullname, username, email, pin))
            print(cur)
            con.commit()
            msg = "You have successfully registered"
    except Exception as e:
        print(e)
    finally:
        return jsonify(msg = msg)

@app.route('/login_user/<int:login_id>/', methods=["POST"])
def login(login_id):
    if request.method == 'POST':
        response = {}
        response['msg'] = None
        response['body'] = []

        try:
            POST = request.get_json()
            get_data = request.get_json()
            username = get_data['username']
            password = get_data['password']

            with sqlite3.connect('HN.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                sql_stmnt = ('SELECT * FROM users WHERE id=' + str(login_id))
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


@app.route('/show-records/' , methods=["GET"])
def records():
    admins = []
    try:

            with sqlite3.connect('HN.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                sql_stmnt = ('SELECT * FROM users')
                cur.execute(sql_stmnt)
                admins = cur.fetchall()

    except Exception as e:
        conn.rollback()
        print("Something went wrong while displaying a record: " + str(e))

    finally:
        return jsonify(admins)


@app.route('/products/', methods=["POST"])
def products():
    try:
        post = request.get_json()
        products = post['product']
        price = post['price']
        description = post['description']
        image = post['image']
        with sqlite3.connect('HN.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO products (products, price, description, image) VALUES"
                        "(?, ?, ?, ?)",(products, price, description, image))
            print(cur)
            con.commit()
            message = "You have successfully entered a product"
    except Exception as e:
        print(e)
    finally:
        con.close()
        return {'message':message}


@app.route('/show-products/' , methods=["GET"])
def showprods():
    admins = []

    try:

            with sqlite3.connect('HN.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                sql_stmnt = ('SELECT * FROM products')
                cur.execute(sql_stmnt)
                admins = cur.fetchall()

    except Exception as e:
        conn.rollback()
        print("Something went wrong while displaying a record: " + str(e))

    finally:
        return jsonify(admins)


@app.route('/show-product/<int:product_id>/', methods=["GET"])
def show_single_product(product_id):
    product = []

    try:

            with sqlite3.connect('HN.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                sql_stmnt = ('SELECT * FROM products WHERE id=' + str(product_id))
                cur.execute(sql_stmnt)
                product = cur.fetchone()

    except Exception as e:
        conn.rollback()
        print("Something went wrong while displaying a record: " + str(e))

    finally:
        return jsonify(product)


if __name__=="__main__":
    app.run()


