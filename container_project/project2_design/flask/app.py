"""
Flask Web 应用 - 容器化自动运维课程设计
学生: lh  学号: 202312080114
架构: Nginx -> Flask -> Redis + MySQL
"""

import os
import socket
from datetime import datetime

from flask import Flask, Response
import redis
import pymysql

app = Flask(__name__)

# =============================================================
# 配置
# =============================================================
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
MYSQL_HOST = os.environ.get("MYSQL_HOST", "mysql")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
MYSQL_USER = os.environ.get("MYSQL_USER", "lh")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "123456")
MYSQL_DB = os.environ.get("MYSQL_DB", "appdb")


def get_redis_client():
    """获取 Redis 连接"""
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
        socket_connect_timeout=5,
        retry_on_timeout=True,
    )


def get_mysql_connection():
    """获取 MySQL 连接"""
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5,
    )


def get_container_id():
    """动态获取当前容器 ID（短 ID）"""
    hostname = socket.gethostname()
    return hostname[:12]


@app.route("/")
def index():
    """主页 - 展示访问次数和容器信息"""

    container_id = get_container_id()

    # --- Redis: 访问计数 ---
    try:
        r = get_redis_client()
        visit_count = r.incr("visit_count")
        r.close()
    except Exception as e:
        visit_count = f"Redis 连接失败: {e}"

    # --- MySQL: 读取用户信息 ---
    student_name = "lh"
    first_access_time = "未知"
    try:
        conn = get_mysql_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT name, first_access_time FROM users ORDER BY id LIMIT 1"
            )
            row = cursor.fetchone()
            if row:
                student_name = row["name"]
                first_access_time = str(row["first_access_time"])
        conn.close()
    except Exception as e:
        first_access_time = f"MySQL 连接失败: {e}"

    # --- 生成 HTML 页面 ---
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>容器化自动运维 - 课程设计</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Microsoft YaHei', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            .card {{
                background: white;
                border-radius: 16px;
                padding: 40px 50px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 600px;
                text-align: center;
            }}
            h1 {{
                color: #333;
                margin-bottom: 10px;
                font-size: 28px;
            }}
            .subtitle {{
                color: #888;
                margin-bottom: 30px;
                font-size: 14px;
            }}
            .info {{
                text-align: left;
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px 25px;
                margin: 20px 0;
                line-height: 2.2;
                font-size: 16px;
                color: #444;
            }}
            .info strong {{
                color: #667eea;
            }}
            .container-id {{
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 2px 10px;
                border-radius: 4px;
                font-family: monospace;
                font-size: 14px;
            }}
            .footer {{
                margin-top: 25px;
                color: #aaa;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>容器化自动运维</h1>
            <p class="subtitle">课程设计 - Docker Compose 多容器架构</p>
            <div class="info">
                <strong>Hello:</strong> {student_name} <br>
                <strong>当前服务容器ID:</strong> <span class="container-id">{container_id}</span> <br>
                <strong>访问次数:</strong> {visit_count} <br>
                <strong>首次访问时间:</strong> {first_access_time}
            </div>
            <p class="footer">
                当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
                Nginx -> Flask -> Redis + MySQL
            </p>
        </div>
    </body>
    </html>
    """
    return Response(html, content_type="text/html; charset=utf-8")


@app.route("/health")
def health():
    """健康检查端点"""
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
