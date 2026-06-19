# =============================================================
# 自定义基础镜像 - 容器化自动运维课程设计
# 学生: lh  学号: 202312080114
# 镜像名: ubuntu-lh:0114
# =============================================================

FROM docker.m.daocloud.io/library/ubuntu:18.04

# 镜像元数据
LABEL maintainer="lh <lh@example.com>"
LABEL description="Custom Ubuntu image for Container O&M course"
LABEL student_id="202312080114"

# 设置环境变量，避免交互式安装提示
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV TZ=Asia/Shanghai
ENV STUDENT_NAME=lh
ENV STUDENT_ID=202312080114

# 设置工作目录
WORKDIR /home/lh

# 替换 apt 源为阿里云镜像（加速安装）
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

# 更新软件源并安装 nginx 和 net-tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nginx \
    net-tools \
    vim \
    curl \
    sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 创建用户 lh（普通用户，带 home 目录）
RUN useradd -m -s /bin/bash lh && \
    echo "lh:123456" | chpasswd && \
    echo "lh ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# 拷贝信息脚本
COPY info_script.sh /home/lh/info_script.sh
RUN chmod +x /home/lh/info_script.sh && \
    chown lh:lh /home/lh/info_script.sh

# 切换到 lh 用户
USER lh

# 暴露端口（80=nginx，2000=自定义服务端口）
EXPOSE 80
EXPOSE 2000

# 容器启动时保持运行
CMD ["bash"]
