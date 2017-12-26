from flask import render_template
from . import main
from app.db import Film

@main.route("/", methods=["GET"])
def index():
    #film = Film()
    films = Film.query.all()
    return render_template("index.html",films=films)

