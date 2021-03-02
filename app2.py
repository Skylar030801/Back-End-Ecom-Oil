from flask import jsonify, Flask, request, render_template
import sqlite3
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.config["DEBUG"] = True
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        return  d

@app.route('/landing/', methods=['GET'])
def landing_page():
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
    return jsonify(data)

@app.route('/user/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        mesg = None
        try:
            post_data = request.get_json()
            fullname = post_data['fullname']
            username = post_data['username']
            email = post_data['email']
            password = post_data['password']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (full_name, username, email, password) VALUES (?, ?, ? ,?)", (fullname, username, email, password))
                cur.commit()
                mesg = "Record successfully added."
        except Exception as e:
            con.rollback()
            msg = "Error ocurred in insert operation: " + e
        finally:
            con.close()
            return jsonify(msg)

if __name__=="__main__":
    app.run()














