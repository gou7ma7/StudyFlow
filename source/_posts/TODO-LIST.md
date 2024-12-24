---
title: Tech Stack TODO LIST  
date: 2022-05-29 08:48:59  
tags: TodoList  
categories: Career  
---

# 0. Blog  
- [ ] LeetCode Solutions: [数据结构与算法](docs/数据结构的轮子与算法.md)  
- [x] Blogging: 技术文章撰写和发布
- [ ] Flask 源码分析：分析 HTTP 请求处理、路由机制
- [ ] Selenium 源码分析：浏览器自动化的内部实现
- [ ] Requests 源码分析：探索 HTTP 请求库的设计
- [ ] Python 源码分析：内置模块实现（如 `json`、`collections` 等）
- [ ] Python 各版本差异对比：关注常用特性变更和性能提升

<!--more-->
# 1. 虚拟化与容器编排
## 1.1 虚拟化
- [ ] Docker 组件分析：深入理解容器、镜像、网络、存储卷
- [ ] Docker 源码阅读：学习核心组件代码，理解容器化的实现原理
- [ ] Docker 深度配置：练习 Volume、网络配置、多阶段构建优化镜像
## 1.2 容器编排
- [x] Kubernetes 集群[搭建](https://gou7ma7.github.io/2023/05/11/devops/Kubernetes/)  -- 2024.12
- [x] Kubernetes 日常使用：掌握 `kubectl` 命令、命名空间管理（已完成于业务环境）
- [ ] Kubernetes 组件深入理解：API Server、Controller Manager、Scheduler 等的作用和原理
- [ ] Kubernetes 源码阅读：深入 kube-apiserver、kubelet 实现，理解调度、负载均衡

# 2. 持续集成与交付（CI/CD）

## 2.1 CI/CD 工具
- [x] Jenkins 基础搭建与使用：安装配置、Pipeline 基本语法（已完成）
- [x] Jenkins 插件选型与管理：参数化构建、蓝绿部署、流水线插件的使用
- [ ] Jenkins 源码阅读：学习插件系统实现和 Pipeline DSL
- [ ] GitLab CI/CD 工作流优化：多项目流水线配置、环境管理和测试集成
- [ ] Argo CD：学习自动化交付，配置 GitOps 流水线，管理 Kubernetes 应用

## 2.2 代码质量管理
- [ ] SonarQube 文档阅读：熟悉代码质量指标、静态分析
- [ ] SonarQube 环境搭建：服务器配置、权限管理
- [ ] SonarQube 深度集成：配置与 Jenkins 集成，实现代码质量检测自动化
- [ ] Checkmarx / OWASP ZAP：学习代码安全性分析，配置静态与动态安全扫描

## 2.3 基础设施即代码（IaC）与云基础设施管理
- [ ] Terraform 基础学习：资源声明、模块化配置
- [ ] CloudFormation：学习 AWS 的 IaC 实践，模板与栈管理
- [x] Ansible 配置管理：理解配置编写、模块使用，批量管理服务器配置

## 2.4 构建与制品管理
- [ ] Docker 基础与镜像管理：多阶段构建、优化镜像大小
- [ ] Artifactory / Nexus：制品管理工具使用，配置 Maven 和 Docker 仓库
- [ ] Harbor：Docker 私有仓库的配置和镜像管理，设置同步和清理策略

## 2.5 监控与日志分析
- [ ] Prometheus：学习系统监控，配置报警规则和数据采集
- [ ] Grafana：数据可视化，创建业务和系统指标仪表盘
- [ ] ELK Stack (Elasticsearch + Logstash + Kibana)：日志收集与分析，配置告警

## 2.6 部署策略
- [x] 蓝绿部署 / 灰度发布：配置 Jenkins/GitLab 流水线，实现多环境发布和流量控制
- [ ] 滚动更新：配置 Kubernetes 滚动更新，确保应用无中断发布

# 3. 业务开发系统回顾与查漏补缺
## 3.1 Web 前端
- [x] React 快速上手：组件创建、生命周期、状态管理
- [ ] Vue 基础学习：组件、指令、Vuex 状态管理
- [ ] 前端开发流程标准化：使用 Linter、Prettier，配置 ESLint 规则
## 3.2 Web 后端
- [ ] Django 框架入门：安装配置、路由与模型管理
- [ ] Django REST framework：创建 API，Token 认证、权限配置
- [ ] Flask 标准开发流程：项目结构、扩展使用（如 SQLAlchemy、Flask-Login）
## 3.3 后端其他语言
- [ ] Go 语言基础：语法、并发模型（goroutines、channels）
- [ ] Java Spring Boot 入门：依赖注入、REST API、数据库集成
- [ ] Java Gradle 构建流程：项目配置、依赖管理、打包
## 3.4 部署
- [ ] uWSGI/Gunicorn + Nginx 部署：配置反向代理，环境变量管理，性能调优

# 4. 数据库与搜索引擎
## 4.1 数据库
- [ ] MySQL 语法与操作：基础 SQL 查询，索引优化
- [ ] MySQL 事务与一致性：锁机制、事务隔离级别
- [ ] MySQL 引擎深入：InnoDB 与 MyISAM 特性比较
## 4.2 搜索引擎
- [ ] Elasticsearch 核心概念：索引、分片、查询分析
- [ ] Elasticsearch 配置优化：节点配置、集群管理、性能优化

# 5. 计算机基础知识
## 5.1 计算机网络
- [x] HTTP 协议：请求头与响应头，状态码，HTTPS 原理 (看完《图解HTTP》)  -- 2024.10
- [x] TCP/IP 轮廓了解  (看完《图解TCP/IP》，现阶段任务够了)  -- 2024.10
- [ ] TCP/IP 协议族，重点学习： TCP 三次握手、四次挥手、UDP 差异 （等业务上用得到再看吧）
- [ ] Socket 编程：使用 Python/C 进行简单 Socket 通信编程
## 5.2 计算机组成原理
- [ ] 计算机组成原理：深入理解 CPU、内存、IO 子系统的基本原理
## 5.3 操作系统
- [ ] Linux 内核：进程管理、文件系统、网络管理的基础知识
- [ ] Linux 性能调优：理解常用内核参数，调整网络、内存优化系统性能

# 6. 信息安全
- [ ] HTTPS 与 SSL/TLS：加密原理，CA 证书，握手过程
- [ ] 常见加密算法：AES、RSA、SHA 算法学习
- [ ] 《图解密码技术》阅读：了解基础加密概念与应用场景

# 7. 数据科学与大数据
## 7.1 AI 与数据科学
- [ ] 机器学习基础：监督学习、无监督学习、常用算法
- [ ] PyTorch / TensorFlow 使用：张量操作、自动微分、神经网络训练
## 7.2 大数据技术
- [ ] Hadoop 基础使用：HDFS、MapReduce 原理
- [ ] Spark 快速上手：数据操作、RDD、DataFrame、数据处理案例

---

# Abandoned
- Selenium 异步标签页池：使用 Puppeteer/Playwright 完成，避免业务耦合。
