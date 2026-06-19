# 🐳 容器化自动运维课程设计

Docker 容器化课程设计项目，包含三个递进式实验：自定义镜像构建、多容器编排、大规模集群扩展。

## 📋 项目概览

### 项目一：自定义基础镜像

基于 Ubuntu 18.04 构建自定义镜像 `ubuntu-lh:0114`，预装 nginx、net-tools 等工具，创建普通用户并配置系统信息脚本。

### 项目二：5 容器编排架构

使用 Docker Compose 编排 5 个容器：

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
- **Flask x2** — 应用实例（双副本）
- **Redis** — 缓存 & 访问计数（AOF + RDB 持久化）
- **MySQL** — 持久化数据存储

### 项目三：大规模集群扩展（18 容器）

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

- **ZooKeeper 集群**（3 节点）— 分布式协调
- **Hadoop HA** — NameNode/ResourceManager 高可用
- **HDFS** — 4 DataNode + 3 JournalNode
- **Kafka 集群**（2 Broker）— 消息队列
- **MySQL** — 结构化数据存储
- **Dashboard** — 数据可视化大屏

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| Docker | 容器化引擎 |
| Docker Compose | 多容器编排 |
| Docker Swarm | 集群管理 |
| Nginx | 反向代理 / 负载均衡 |
| Flask | Web 应用框架 |
| Redis | 内存缓存 |
| MySQL 8.0 | 关系型数据库 |
| Hadoop 3.3.6 | 分布式存储 & 计算 |
| ZooKeeper 3.8 | 分布式协调服务 |
| Kafka 7.5.0 | 消息队列 |

## 🚀 快速开始

### 项目一：构建基础镜像

```bash
cd container_project/project1_base
docker build -t ubuntu-lh:0114 .
docker run -it ubuntu-lh:0114
./info_script.sh
```

### 项目二：启动 5 容器架构

```bash
cd container_project/project2_design
docker compose up -d
docker compose ps
curl http://localhost
```

### 项目三：启动 18 容器集群

```bash
cd container_project/project3_extension
docker compose up -d
docker compose ps

# 访问服务
# Hadoop NameNode UI:  http://localhost:9870
# YARN ResourceManager: http://localhost:8088
# Dashboard 大屏:       http://localhost:8080
# Kafka:                localhost:9092
# MySQL:                localhost:3307
```

## 📁 项目结构

```
docker/
└── container_project/
    ├── project1_base/          # 项目一：自定义镜像
    │   ├── Dockerfile
    │   ├── info_script.sh
    │   └── audit_report.txt
    ├── project2_design/        # 项目二：5 容器编排
    │   ├── docker-compose.yml
    │   ├── flask/              # Flask 应用
    │   ├── mysql/              # MySQL 初始化
    │   └── nginx/              # Nginx 配置
    ├── project3_extension/     # 项目三：集群扩展
    │   ├── docker-compose.yml
    │   ├── dashboard/          # 数据大屏
    │   ├── hadoop/             # Hadoop 配置
    │   ├── kafka/              # Kafka 生产者/消费者
    │   ├── mysql/              # MySQL 初始化
    │   └── zookeeper/          # ZooKeeper 配置
    ├── 关键步骤截图/            # 实验过程截图
    └── 配置文档.docx            # 详细配置文档
```

## 📸 关键截图

项目截图存放在 `container_project/关键步骤截图/` 目录下，包含镜像构建、容器运行状态、负载均衡验证、Hadoop UI、Dashboard 大屏等关键步骤的截图记录。

## 📄 License

MIT
