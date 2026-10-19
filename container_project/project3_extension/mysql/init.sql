-- =============================================================
-- MySQL 初始化脚本 - 项目三：开发扩展
-- 学生: lh  学号: 202312080114
-- =============================================================

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE IF NOT EXISTS bigdata_db_lh
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE bigdata_db_lh;

-- 数据统计表
CREATE TABLE IF NOT EXISTS data_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_source VARCHAR(100) NOT NULL COMMENT '数据来源',
    record_count BIGINT NOT NULL DEFAULT 0 COMMENT '记录数',
    update_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据统计表';

-- 插入初始数据
INSERT INTO data_stats (data_source, record_count) VALUES
    ('HDFS', 156),
    ('Kafka', 2847),
    ('YARN', 89);

-- 数据库用户和授权由 MySQL 镜像的 MYSQL_USER/MYSQL_PASSWORD 创建。
