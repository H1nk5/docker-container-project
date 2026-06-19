#!/bin/bash
set -e

ROLE=${HADOOP_ROLE:-""}
NODE_ID=${NODE_ID:-""}

# 格式化 HDFS（仅首次）
format_namenode() {
    if [ ! -f /hadoop/tmp/dfs/name/current/VERSION ]; then
        echo "Formatting NameNode..."
        hdfs namenode -format -clusterId mycluster -force
    fi
}

# 启动 JournalNode
start_journalnode() {
    echo "Starting JournalNode..."
    hdfs journalnode &
    sleep 5
    tail -f /hadoop/logs/*.log 2>/dev/null || sleep infinity
}

# 初始化 ZKFC
init_zkfc() {
    echo "Initializing ZKFC..."
    hdfs zkfc -formatZK -force 2>/dev/null || true
}

# 启动 NameNode
start_namenode() {
    format_namenode
    echo "Starting NameNode..."
    hdfs namenode &
    sleep 10
    # 如果是 standby，需要从 active 同步
    if [ "$NODE_ID" = "nn2" ]; then
        hdfs namenode -bootstrapStandby -force 2>/dev/null || true
    fi
    hdfs zkfc &
    tail -f /hadoop/logs/*.log 2>/dev/null || sleep infinity
}

# 启动 DataNode
start_datanode() {
    echo "Starting DataNode..."
    hdfs datanode &
    yarn nodemanager &
    tail -f /hadoop/logs/*.log 2>/dev/null || sleep infinity
}

# 启动 ResourceManager
start_resourcemanager() {
    echo "Starting ResourceManager..."
    yarn resourcemanager &
    tail -f /hadoop/logs/*.log 2>/dev/null || sleep infinity
}

case "$ROLE" in
    journalnode)  start_journalnode ;;
    namenode)     start_namenode ;;
    datanode)     start_datanode ;;
    resourcemanager) start_resourcemanager ;;
    *)
        echo "Unknown role: $ROLE"
        sleep infinity
        ;;
esac
