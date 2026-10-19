<div align="center">

# 🐳 ContainerOps

**容器化自动运维平台 · 自定义镜像 → 多容器编排 → 大规模集群扩展**

<br>

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Hadoop](https://img.shields.io/badge/Hadoop-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=black)
![Kafka](https://img.shields.io/badge/Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)

<br>

三个递进式实验：5 容器编排 → 18 容器 Hadoop/Kafka 集群 · 完整 Dockerfile + Compose 配置

[系统概述](#系统概述) · [技术栈](#技术栈) · [快速启动](#快速启动) · [项目结构](#项目结构)

</div>

---

## 系统概述

ContainerOps 是一套容器化自动运维实践平台，通过三个递进式实验完整覆盖 Docker 生态的核心能力：

| 实验 | 目标 | 规模 |
|------|------|------|
| **实验一** | 自定义基础镜像构建 | 单容器 |
| **实验二** | 多容器服务编排 | 5 容器 |
| **实验三** | 大规模集群扩展 | 18 容器 |

### 实验二：5 容器编排架构

```
┌─────────┐     ┌──────────┐     ┌──────────┐
│  Nginx  │────▶│  Flask1  │────▶│  Redis   │
│  :80    │     │          │     │  缓存层   │
└─────────┘     └──────────┘     └──────────┘
     │                               │
     ▼          ┌──────────┐         ▼
               │  Flask2  │────▶┌──────────┐
               │          │     │  MySQL   │
               └──────────┘     │  持久层   │
                                └──────────┘
```

- **Nginx** — 反向代理 & 负载均衡
- **Flask ×2** — 应用实例（双副本）
- **Redis** — 缓存 & 访问计数（AOF + RDB 持久化）
- **MySQL** — 持久化数据存储

### 实验三：18 容器集群架构

```
┌─────────────────────────────────────────────────────┐
│                   Docker Swarm                       │
│                                                     │
│  ┌─────────────┐  ┌──────────────────────────────┐  │
│  │ ZooKeeper x3│  │      Hadoop HA               │  │
│  │  集群选举    │  │  NameNode x2 (Active/Standby)│  │
│  └─────────────┘  │  ResourceManager x2           │  │
│                    │  DataNode + NodeManager x4    │  │
│                    │  JournalNode x3               │  │
│                    └──────────────────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │
│  │ Kafka x2    │  │   MySQL     │  │ Dashboard  │  │
│  │ 消息队列     │  │   数据存储   │  │  数据大屏   │  │
│  └─────────────┘  └─────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 技术栈

| 技术 | 用途 |
|------|------|
| Docker / Docker Compose / Swarm | 容器化 / 编排 / 集群管理 |
| Nginx | 反向代理 / 负载均衡 |
| Flask | Web 应用框架 |
| Redis | 内存缓存（AOF + RDB 持久化） |
| MySQL 8.0 | 关系型数据库 |
| Hadoop 3.3.6 | 分布式存储 & 计算（HA 模式） |
| ZooKeeper 3.8 | 分布式协调 / 集群选举 |
| Kafka 7.5.0 | 消息队列 |

---

## 快速启动

### 实验一：构建基础镜像

```bash
cd container_project/project1_base
docker build -t ubuntu-lh:0114 .
docker run -it ubuntu-lh:0114
./info_script.sh
```

### 实验二：启动 5 容器架构

```bash
cd container_project/project2_design
cp .env.example .env
docker compose up -d
docker compose ps
curl http://localhost
```

### 实验三：启动 18 容器集群

```bash
cd container_project/project3_extension
cp .env.example .env
docker compose up -d
docker compose ps
```

服务访问：

| 服务 | 地址 |
|------|------|
| Hadoop NameNode UI | http://localhost:9870 |
| YARN ResourceManager | http://localhost:8088 |
| Dashboard 数据大屏 | http://localhost:8080 |
| Kafka | localhost:9092 |
| MySQL | localhost:3307 |

---

## 项目结构

```
container_project/
├── project1_base/                # 实验一：自定义镜像
│   ├── Dockerfile
│   ├── info_script.sh
│   └── audit_report.txt
├── project2_design/              # 实验二：5 容器编排
│   ├── docker-compose.yml
│   ├── flask/                    # Flask 应用
│   ├── mysql/                    # MySQL 初始化
│   └── nginx/                    # Nginx 配置
├── project3_extension/           # 实验三：集群扩展
│   ├── docker-compose.yml
│   ├── dashboard/                # 数据大屏
│   ├── hadoop/                   # Hadoop 配置
│   ├── kafka/                    # Kafka 生产者/消费者
│   ├── mysql/                    # MySQL 初始化
│   └── zookeeper/                # ZooKeeper 配置
├── 关键步骤截图/                  # 实验过程截图
└── 配置文档.docx                  # 详细配置文档
```

---

## 开源许可

MIT
