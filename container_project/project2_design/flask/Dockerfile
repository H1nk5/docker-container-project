# =============================================================
# Flask 应用镜像 - 容器化自动运维课程设计
# 学生: lh  学号: 202312080114
# =============================================================

FROM docker.m.daocloud.io/library/python:3.11-slim

LABEL maintainer="lh"
LABEL description="Flask app for Container O&M course"

# 环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV TZ=Asia/Shanghai

# 工作目录
WORKDIR /app

# 先复制依赖文件，利用 Docker 缓存层
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt

# 复制应用代码
COPY app.py .

# 创建非 root 用户运行
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

# 用 gunicorn 启动，2 个 worker
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
