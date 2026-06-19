FROM docker.m.daocloud.io/library/python:3.11-slim
LABEL maintainer="lh"
ENV TZ=Asia/Shanghai
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY && \
    pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com flask pymysql
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
