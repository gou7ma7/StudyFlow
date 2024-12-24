---
title: K8s App Setup
date: 2023-05-16 21:00:10
tags: setup
categories: DevOps
---
# 依赖
[可用的外部可访问的k8s集群](https://gou7ma7.github.io/2023/05/11/devops/Kubernetes/)

# 部署并访问 Bookinfo
## 开启网关
在依赖中我们开启了集群网关，提供了外部访问KubeSphere整个集群的入口。

<!--more-->

<!-- 
而我们这里需要开启的是(项目网关)[https://www.kubesphere.io/zh/docs/v3.3/project-administration/project-gateway/#%e8%ae%be%e7%bd%ae%e7%bd%91%e5%85%b3]，提供外部访问Bookinfo这个应用的入口。

        KubeSphere 项目中的网关是一个 NGINX Ingress 控制器，KubeSphere 内置的用于 HTTP 负载均衡的机制称为应用路由，它定义了从外部到集群服务的连接规则。

之前我们开启了集群网关，这里发现上述链接教程中的项目里面的网关设置无法使用； -->

因为如果同时存在集群网关和项目网关，项目网关禁用后无法再次启用。建议仅使用集群网关或仅使用项目网关。
<!-- 
为了验证教程，因此先切换回admin账号关闭集群网关，然后开启项目网关。 -->

由于开启了集群网关，发现创建出项目之后已经自动绑定到集群网关上，因此不做额外设置。

## 创建 DevOps 项目
(步骤 5：创建 DevOps 项目)[https://www.kubesphere.io/zh/docs/v3.3/quick-start/create-workspace-and-project/]

是时候体验一下全家桶DevOps的区别了。

