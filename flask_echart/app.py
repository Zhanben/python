# coding:utf8
import psutil
from db import db_session, Cpu
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

#cpus = psutil.cpu_percent(interval=5, percpu=True)
#print(cpus)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/cpu", methods=["POST"])
def cpu():
    if request.method == "POST":
        res = db_session.query(Cpu).filter(Cpu.id < int(request.form['id'])) # 返回1条或多条数据

    return jsonify(insert_time=[x[1] for x in res],
                   cpu1=[x[2] for x in res],
                   cpu2=[x[3] for x in res],
                   cpu3=[x[4] for x in res],
                   cpu4=[x[5] for x in res])  # 返回json格式数据


if __name__ == "__main__":
    app.run(debug=True)