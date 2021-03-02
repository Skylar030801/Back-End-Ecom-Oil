import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        return d


def init_sqlite_db():

    con = sqlite3.connect('database.db')
    print("Opened database successfully")

    con.execute('CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT, price TEXT, brand TEXT, picture BLOB)')
    print("Item table created successfully")
    con.close()


init_sqlite_db()


app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/add-new-record/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            product_name = post_data['product_name']
            price = post_data['price']
            brand = post_data['brand']
            picture = post_data['picture']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO items (product_name, price, brand, picture) VALUES (?, ? , ? ,?)" , (product_name, price, brand, picture))
                con.commit()
                msg = product_name + " was successfully added to the database."

        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            con.close()
            return jsonify(msg)

@app.route('/login/', methods=["POST"])
def login():

    msg = None
    try:
        post_data = request.get_json()
        username=post_data['username']
        password=post_data['password']
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            sql = ("SELECT * FROM admin WHERE username = ? and password = ?")
            cur.execute(sql,[username, password])
            records=cur.fetchall()

    except Exception as e:
        con.rollback()
        msg = "Error occurred when fetching results from the database: " + str(e)
    finally:
        con.close()
        return jsonify(msg)

@app.route('/show-records/', methods=["GET"])
def show_records():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory()
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database. ")
    finally:
        con.close()
        return jsonify(records)


@app.route('/delete-student/<int:student_id>/', methods=["GET"])
def delete_student(student_id):

    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM student WHERE id=" + str(student_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return jsonify(delete_student)





if __name__=="__main__":
    app.run()
