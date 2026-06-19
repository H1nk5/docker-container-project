#!/usr/bin/env python3
"""Kafka Consumer - 消费数据并统计"""
import subprocess
import json
from datetime import datetime

TOPIC = "bigdata_topic_0114"
BOOTSTRAP = "kafka-1-lh-0114:4092"

def consume():
    count = 0
    sources = {}
    cmd = f'docker exec kafka-1-lh-0114 kafka-console-consumer --topic {TOPIC} --bootstrap-server kafka-1-lh-0114:9092 --from-beginning'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for line in proc.stdout:
        line = line.strip()
        if line:
            count += 1
            try:
                data = json.loads(line)
                src = data.get("source", "unknown")
                sources[src] = sources.get(src, 0) + 1
            except json.JSONDecodeError:
                pass
            print(f"[Consumer] Received {count} | Sources: {sources}")

if __name__ == "__main__":
    consume()
