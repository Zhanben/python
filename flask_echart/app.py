# coding:utf8
import psutil
import time
from db import db_session, Cpu, init_db
from flask import Flask, request, render_template, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/cpu", methods=["POST"])
def cpu():
    if request.method == "POST":
        res = db_session.query(Cpu).filter(Cpu.id > int(request.form['id'])) # 返回1条或多条数据

    return jsonify(insert_time=[x.time for x in res],
                   cpu1=[x.cpu1 for x in res],
                   cpu2=[x.cpu2 for x in res],
                   cpu3=[x.cpu3 for x in res],
                   cpu4=[x.cpu4 for x in res])  # 返回json格式数据


def get_cpu_percent():
    while True:
        cpus = psutil.cpu_percent(interval=30, percpu=True)
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        cpu = Cpu()
        cpu.time = t
        cpu.cpu1 = cpus[0]
        cpu.cpu2 = cpus[1]
        cpu.cpu3 = cpus[2]
        cpu.cpu4 = cpus[3]
        db_session.add(cpu)
        db_session.commit()


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
    get_cpu_percent()
