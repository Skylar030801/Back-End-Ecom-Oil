import sqlite3
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

con = sqlite3.connect("HN.db")
con.execute("DROP TABLE users")
con.commit()

if __name__=="__main__":
    app.run(debug=True)
