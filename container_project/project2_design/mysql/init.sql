-- =============================================================
-- MySQL 初始化脚本 - 容器化自动运维课程设计
-- 学生: lh  学号: 202312080114
-- 功能: 创建数据库、表结构、插入初始数据
-- =============================================================

-- 设置连接字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS appdb
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE appdb;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '学生姓名',
    first_access_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '首次访问时间',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户访问记录表';

-- 插入初始记录：lh，首次访问时间为当前时间
INSERT INTO users (name, first_access_time) VALUES ('lh', NOW());

-- 数据库用户和授权由 MySQL 镜像的 MYSQL_USER/MYSQL_PASSWORD 创建。
