#!/usr/bin/env python3
"""Kafka Producer - 模拟数据写入"""
import json
import time
import random
from datetime import datetime

# 使用 kafka-python 或直接调用 kafka CLI
import subprocess

TOPIC = "bigdata_topic_0114"
BOOTSTRAP = "kafka-1-lh-0114:9092"

def produce():
    count = 0
    while True:
        data = {
            "timestamp": datetime.now().isoformat(),
            "source": random.choice(["sensor-a", "sensor-b", "sensor-c"]),
            "value": round(random.uniform(10, 100), 2),
            "count": count
        }
        msg = json.dumps(data)
        cmd = f'echo "{msg}" | docker exec -i kafka-1-lh-0114 kafka-console-producer --topic {TOPIC} --bootstrap-server {BOOTSTRAP}'
        subprocess.run(cmd, shell=True, capture_output=True)
        count += 1
        print(f"[Producer] Sent message {count}: {msg}")
        time.sleep(2)

if __name__ == "__main__":
    produce()
