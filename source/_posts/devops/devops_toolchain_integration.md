---
title: DevOps Toolchain Integration Setup
# date: 2023-04-30 15:54:17
tags: setup
categories: DevOps
---

# 期望
作为个人工作中实际用到的DevOps相关工具链的整合搭建，同时也作为新手上手DevOps的Quick Setup。

# 背景
长话短说:

- 数据分析师: 作为一名**数学专业**的划水学生，毕业之后无比**憧憬**能成为一名“数据分析师”，然后被**忽悠**到“信老师”（化名，具体内容可以参见[我的一个视频总结](https://www.bilibili.com/video/BV1Wv411b7Gm)）旗下工作；

- 爬虫：老师告诉我，**数据平台还没搭建好**，这样吧，你先自己去**公网上爬取数据**；

- 爬虫 *2： 第一份正式的工作，技术栈是**自动化**的请求接口 / **操作浏览器界面**完成业务；

- 测试开发 + DevOps：凭借上述后者，找到了**UI自动化测试开发**的工作；再在工作中要用到**整合流水线**为业务开发同事提供服务，于是职位变成了DevOps；

- DevOps：来到上海成为专职DevOps，负责Daily CI/CD & Release platform 的搭建。

之前的工作中部分组件是我去的时候已经安装、配置好了的，因此在这里把用到的工具链进行全流程的安装，回顾并系统的梳理技术栈，同时也作为新手上手DevOps的Quick Setup。

<!--more-->

# 机器
Ubuntu 实体机 *2 （不要用WSL）

一个作为master，另一个作为node，搭建一个最小的集群。

# Kubernetes
之前业务上主要使用的是阿里云容器服务Kubernetes版（Alibaba Cloud Container Service for Kubernetes，简称容器服务ACK）

同时在私有化部署的时候使用[kubesphere](https://kubesphere.io/zh/)，本文主要使用后者进行物理机上的部署。

[Kubernetes Setup in Local Physical Servers](https://gou7ma7.github.io/2023/05/11/devops/Kubernetes/)

# Helm
The package manager for Kubernetes

简单来说，我的包管理方式经过一下迭代

1. exe / other executable file / tar & scp;
2. Docker Image;
3. Helm Charts;
