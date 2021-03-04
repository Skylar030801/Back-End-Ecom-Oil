import sqlite3
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

def create_user():
    connected = sqlite3.connect('HN.db')
    print("created database")
    connected.execute('CREATE TABLE IF NOT EXISTS users('
                      'fullname,'
                      'username,'
                      'email,'
                      'password)'
                      )
    print("user table created")

create_user()

app = Flask(__name__)
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/user-register/', methods=["POST"])
def register():
    try:
        post = request.get_json()
        fullname = post['fullname']
        username = post['username']
        email = post['email']
        password = post['password']

        with sqlite3.connect('HN.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users(fullname, username, email, password)VALUES"
                        "(?, ?, ?, ?)",(fullname, username, email, password))
            print(cur)
            con.commit()
            message = "Registered"
    except Exception as e:
        print(e)
    finally:
        con.close()
        return {'message':message}

@app.route('/show-records/' , methods=["GET"])
def records():
    if request.method == 'GET':
        response = {}
        response['msg'] = None
        response['body'] = []

        try:
            # get_data = request.get_json()
            # username = get_data['username']
            # password = get_data['password']

            with sqlite3.connect('HN.db') as conn:
                conn.row_factory = dict_factory
                cur = conn.cursor()
                sql_stmnt = ('SELECT * FROM users')
                cur.execute(sql_stmnt)
                admins = cur.fetchall()
                conn.commit()
                response['body'] = admins
                response['msg'] = "records on display"

        except Exception as e:
            conn.rollback()
            response['msg'] = "Something went wrong while displaying a record: " + str(e)

        finally:
            return jsonify(records)

