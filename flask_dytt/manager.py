# coding:utf8
import time
from db import db_session,init_db
from flask import Flask, request, render_template, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/cpu", methods=["POST"])
def mainpage():
    pass


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
