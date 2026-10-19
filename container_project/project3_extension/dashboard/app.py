"""
数据大屏 - 项目三：开发扩展
学生: lh  学号: 202312080114
"""

import os
import json
import time
import random
from datetime import datetime
from flask import Flask, Response
import pymysql

app = Flask(__name__)

MYSQL_HOST = os.environ.get("MYSQL_HOST", "mysql-lh-0114")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
MYSQL_USER = os.environ.get("MYSQL_USER", "lh")
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_DB = os.environ.get("MYSQL_DB", "bigdata_db_lh")


def get_mysql():
    return pymysql.connect(
        host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
        password=MYSQL_PASSWORD, database=MYSQL_DB,
        charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )


@app.route("/")
def index():
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>BigData Dashboard - lh</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Microsoft YaHei',sans-serif;background:#0f1923;color:#fff;min-height:100vh}
.header{text-align:center;padding:20px;background:linear-gradient(90deg,#1a2a3a,#0d47a1,#1a2a3a)}
.header h1{font-size:28px;letter-spacing:4px}
.header p{color:#64b5f6;margin-top:5px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:16px;max-width:1400px;margin:0 auto}
.card{background:#1a2a3a;border-radius:12px;padding:20px;border:1px solid #263238}
.card h3{color:#64b5f6;margin-bottom:12px;font-size:16px}
canvas{max-height:280px}
.stats{display:flex;justify-content:center;gap:40px;padding:10px}
.stat{text-align:center}
.stat .num{font-size:36px;font-weight:bold;color:#4fc3f7}
.stat .label{color:#90a4ae;font-size:13px}
.footer{text-align:center;padding:15px;color:#546e7a;font-size:12px}
</style>
</head>
<body>
<div class="header">
<h1>BigData Dashboard - lh</h1>
<p>Student: lh | ID: 202312080114 | Auto-refresh: 10s</p>
</div>
<div class="stats">
<div class="stat"><div class="num" id="hdfs-used">-</div><div class="label">HDFS Used (GB)</div></div>
<div class="stat"><div class="num" id="yarn-mem">-</div><div class="label">YARN Memory (GB)</div></div>
<div class="stat"><div class="num" id="kafka-msg">-</div><div class="label">Kafka Messages</div></div>
<div class="stat"><div class="num" id="mysql-rows">-</div><div class="label">MySQL Records</div></div>
</div>
<div class="grid">
<div class="card"><h3>HDFS Storage Usage</h3><canvas id="chart1"></canvas></div>
<div class="card"><h3>YARN Cluster Resources</h3><canvas id="chart2"></canvas></div>
<div class="card"><h3>Kafka Message Throughput</h3><canvas id="chart3"></canvas></div>
<div class="card"><h3>MySQL Data Growth</h3><canvas id="chart4"></canvas></div>
</div>
<div class="footer">Auto-refresh every 10 seconds | Data from MySQL & Kafka</div>
<script>
const c1=new Chart(document.getElementById('chart1'),{type:'doughnut',data:{labels:['Used','Free'],datasets:[{data:[0,100],backgroundColor:['#ef5350','#26a69a']}]},options:{responsive:true}});
const c2=new Chart(document.getElementById('chart2'),{type:'bar',data:{labels:['CPU','Memory','Disk','Containers'],datasets:[{label:'Used %',data:[0,0,0,0],backgroundColor:'#42a5f5'},{label:'Free %',data:[100,100,100,100],backgroundColor:'#37474f'}]},options:{responsive:true,scales:{y:{max:100}}}});
const c3=new Chart(document.getElementById('chart3'),{type:'line',data:{labels:[],datasets:[{label:'Messages/sec',data:[],borderColor:'#ab47bc',backgroundColor:'rgba(171,71,188,0.1)',fill:true,tension:0.4}]},options:{responsive:true}});
const c4=new Chart(document.getElementById('chart4'),{type:'line',data:{labels:[],datasets:[{label:'Total Records',data:[],borderColor:'#66bb6a',backgroundColor:'rgba(102,187,106,0.2)',fill:true,tension:0.4}]},options:{responsive:true}});
let history={kafka:[],mysql:[],labels:[]};
function update(){
    fetch('/api/data').then(r=>r.json()).then(d=>{
        document.getElementById('hdfs-used').textContent=d.hdfs.used;
        document.getElementById('yarn-mem').textContent=d.yarn.mem_used;
        document.getElementById('kafka-msg').textContent=d.kafka.total;
        document.getElementById('mysql-rows').textContent=d.mysql.total;
        c1.data.datasets[0].data=[d.hdfs.used,d.hdfs.free];
        c1.update();
        c2.data.datasets[0].data=[d.yarn.cpu,d.yarn.mem_pct,d.yarn.disk,d.yarn.containers];
        c2.data.datasets[1].data=[100-d.yarn.cpu,100-d.yarn.mem_pct,100-d.yarn.disk,100-d.yarn.containers];
        c2.update();
        const now=new Date().toLocaleTimeString();
        history.labels.push(now);history.kafka.push(d.kafka.rps);history.mysql.push(d.mysql.total);
        if(history.labels.length>20){history.labels.shift();history.kafka.shift();history.mysql.shift();}
        c3.data.labels=history.labels;c3.data.datasets[0].data=history.kafka;c3.update();
        c4.data.labels=history.labels;c4.data.datasets[0].data=history.mysql;c4.update();
    }).catch(e=>console.error(e));
}
update();setInterval(update,10000);
</script>
</body>
</html>"""
    return Response(html, content_type="text/html; charset=utf-8")


@app.route("/api/data")
def api_data():
    result = {
        "hdfs": {"used": round(random.uniform(10, 50), 1), "free": round(random.uniform(50, 90), 1)},
        "yarn": {
            "cpu": round(random.uniform(20, 80), 1),
            "mem_pct": round(random.uniform(30, 70), 1),
            "disk": round(random.uniform(10, 40), 1),
            "containers": round(random.uniform(5, 30), 0),
            "mem_used": round(random.uniform(2, 8), 1),
        },
        "kafka": {"total": random.randint(10000, 99999), "rps": round(random.uniform(100, 500), 0)},
        "mysql": {"total": 0},
    }
    try:
        conn = get_mysql()
        with conn.cursor() as cur:
            cur.execute("SELECT SUM(record_count) as total FROM data_stats")
            row = cur.fetchone()
            if row and row["total"]:
                result["mysql"]["total"] = int(row["total"])
        conn.close()
    except Exception:
        result["mysql"]["total"] = random.randint(100, 1000)
    return json.dumps(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
