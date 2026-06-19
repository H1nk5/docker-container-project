#!/bin/bash
# =============================================================
# 系统信息采集脚本
# 学生: lh  学号: 202312080114
# =============================================================

echo "=========================================="
echo "  容器化自动运维 - 系统信息报告"
echo "=========================================="

# 1. 当前时间
echo ""
echo "[1] 当前时间:"
date "+%Y-%m-%d %H:%M:%S"

# 2. 当前用户
echo ""
echo "[2] 当前用户:"
whoami

# 3. 学生信息
echo ""
echo "[3] 学生信息:"
echo "  姓名: lh"
echo "  学号: 202312080114"

# 4. 卷挂载测试
echo ""
echo "[4] 卷挂载测试:"
if [ -d "/data" ]; then
    echo "  /data 目录已挂载"
    echo "  挂载内容:"
    ls -la /data/
    echo ""
    echo "  写入测试文件..."
    echo "Test by lh at $(date)" | sudo tee /data/test_mount.txt > /dev/null
    echo "  已写入 /data/test_mount.txt"
    cat /data/test_mount.txt
else
    echo "  /data 目录未挂载 (容器启动时需加 -v 参数)"
    echo "  示例: docker run -v /host/data:/data ubuntu-lh:0114"
fi

# 5. 网络信息
echo ""
echo "[5] 网络信息:"
if command -v ifconfig &> /dev/null; then
    ifconfig | grep -A 2 "eth0"
else
    ip addr show | grep -A 2 "eth0"
fi

# 6. 磁盘使用
echo ""
echo "[6] 磁盘使用:"
df -h / | tail -1 | awk '{print "  总空间: "$2" | 已用: "$3" | 可用: "$4" | 使用率: "$5}'

echo ""
echo "=========================================="
echo "  报告生成完毕"
echo "=========================================="
