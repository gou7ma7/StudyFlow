---
title: Kubernetes Setup in Local Physical Servers
# date: 2023-04-30 15:54:17
tags: setup
categories: DevOps
---

# 选择
在我自己在作为一名初学者学习编程的时候，曾看到过一位前辈在知乎日报中写道：

他们当年学习编程痛苦在根本找不到参考资料，只能自己硬着头皮摸索前进，不过好处是每个方向的技术选型基本上是固定的，不会有纠结；

而现在的初学者在一开始学习编程，就会很容易迷失在面对浩如烟海的技术路线选择中，尤其是热门的方向，总有前人做好了各种版本的教程、工具，完全不知道从哪里开始。

在我一开始学习DevOps的时候背过官方推荐的minikube教程， 到后来也尝试过搭建轻量化的k3s环境，算上业务中的阿里云容器服务Kubernetes版（Alibaba Cloud Container Service for Kubernetes，简称容器服务ACK），最终发现“搭建环境”本身也是造轮子的一部分，对提高**理解应用能力**甚微。

因此本文选择最简单的一种方式：
[在 Linux 上以 All-in-One 模式安装 KubeSphere](https://kubesphere.io/zh/docs/v3.3/quick-start/all-in-one-on-linux/)（以下简称**官方文档**），直接最简化地安装，然后再在使用中进行学习，毕竟**背诵任何的学习资料都不如自己动手部署一遍**。

<!--more-->
# 声明
本文仅供学习使用，生产环境请使用云服务厂商提供的成熟的Kubernetes环境。

# Master Node
Ubuntu 实体机 in roy-qtc6（有些时候master node的名字可能是这个），这是一台2013年刚上大学时候买的HASEE 神舟 精盾 K580S-i7D1，三千六就拿到当时平民级最强的CPU和显卡，甚至到10年后的今天不管是装Windows娱乐还是装Linux学习性能都充裕，对比一会儿提到的同龄人简直是扬我国威。

按照[官方文档](https://kubesphere.io/zh/docs/v3.3/quick-start/all-in-one-on-linux/)中的步骤进行安装。


由于kubernetes与kubesphere之间存在一个版本匹配问题，因此我这里直接使用example中推荐的版本
``` bash
$ ./kk create cluster --with-kubernetes v1.22.12 --with-kubesphere v3.3.2
```
当运行上述命令时，会检查机器是否安装依赖。

  在我这台机器上，只需要预先手动安装conntrack socat ebtables ethtool，其他组件会自动安装。

    `$ apt-get install conntrack socat ebtables ethtool`

| name           | sudo | curl | openssl | ebtables | socat | ipset | ipvsadm | conntrack | chrony | docker | containerd | nfs client | ceph client | glusterfs client |
|  ----  | ----  |  ----  | ----  |  ----  | ----  |  ----  | ----  |  ----  | ----  |  ----  | ----  |  ----  | ----  |  ----  |
| master | y    | y    | y       | y        | y     |       |         | y         |        |        |            |            |             |                  |

查看log会发现 在依次安装kubelet、kubectl、helm、kubecni、crictl、etcd、docker等，在之后的教程里，会解释组件的作用。

经过漫长的等待之后，当console中出现Welcome hints、ip地址与默认admin账号密码， 就表示Kubenets安装完成。

``` bash
❯ Welcome to KubeSphere!
```
这个时候可以登录http://ip:30880/dashboard 进行可视化操作。

以上安装过程基本上是一键安装，在物理机器与Ubuntu系统没有太大问题的情况下，一小时之内能完成。

如果要安装官方的Kubernetes Dashboard的话，还需要手动安装、并配置外部访问与账号，这些额外的概念无疑会在一开始极大的增加初学者的负担。

而这些步骤/组件 **KubeSphere全家桶**全都集成了，让开发者将更多的经历集中在理解与应用k8s核心组件与部署业务代码上。

接下来可以跟着官方文档应用学习其中组件了。

## Troubleshooting
### [WARNING FileExisting-ethtool]: ethtool not found in system path
``` bash
$ apt-get install ebtables ethtool
```
这两个依赖是必须的，但是官方文档中没有列出来。

### kubectl Please wait for the installation to complete
安装的一直卡在这个命令，推测可能是kube-system中的k8s自己的pod没有就绪，另外启动一个shell查询pod状况；

``` bash
❯ kubectl get pod -A
NAMESPACE           NAME                                           READY   STATUS    RESTARTS   AGE
...
kube-system         openebs-localpv-provisioner-57bbf864d5-zhl6k   0/1     Pending   0          26m
kubesphere-system   ks-installer-85d6fb8c97-mns4d                  0/1     Pending   0          26m
```

查看其中一个pod的Events
``` bash
❯ kubectl describe pod openebs-localpv-provisioner-57bbf864d5-zhl6k -n kube-system
Name:           openebs-localpv-provisioner-57bbf864d5-zhl6k
...
Events:
  Type     Reason            Age                 From               Message
  ----     ------            ----                ----               -------
  Warning  FailedScheduling  97s (x35 over 36m)  default-scheduler  0/1 nodes are available: 1 node(s) had taint {node-role.kubernetes.io/master: }, that the pod didn't tolerate.
```
发现openebs-localpv-provisioner与ks-installer的STATUS均是Pending，通过Events里面的描述，发现是因为有taints所以pod调度不上去。

查看node的taints
``` bash
❯ kubectl get nodes -o json | jq '.items[].spec'
{
  "taints": [
    {
      "effect": "NoSchedule",
      "key": "node-role.kubernetes.io/master"
    },
    {
      "effect": "NoSchedule",
      "key": "node.kubernetes.io/not-ready"
    }
  ]
}
```
means that no pod can be scheduled on the master node unless it has a toleration for this taint123， 意思就是说不能在master节点上的和not-ready的pod不允许调度到我这个节点上。

The OpenEBS Local PV provisioner is designed to run on worker nodes and not on master nodes1. If you want to deploy the OpenEBS Local PV provisioner on a master node, you can do so by adding the label openebs.io/engine=provisioner to the master node2. However, it is not recommended to run the provisioner on master nodes as it can cause issues with the Kubernetes control plane

污点（Taint）是 Kubernetes 中的一个概念，它是一种标记，用于标识节点上的一些特殊条件，例如节点上的硬件故障或其他不可用性。 污点可以阻止 Pod 调度到具有特定污点的节点上。 有关更多信息，请参见[官方文档](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)。

Taints and Tolerations 是一起组合使用的，相当于“黑名单”机制，前者配置在nodes上，只能配置过后者的pod；

    简单但是不推荐的做法： 将taints删除
> :warning: **不如直接用minikube单节点部署**: 这里的意思是这个pod不能调度在master节点上，如果删了这个污点，相当于是强行调度在master上了。

执行`kubectl taint nodes --all node-role.kubernetes.io/master-`, 这个命令是在将所有节点的node-role.kubernetes.io/master 污点删除，以便可以在这些节点上调度非 master Pod。

然后发现唯一node上的taint没有了(这里换一个方法查看taints)
``` bash
❯ kubectl describe node master | grep Taints
Taints:             <none>
```

    正规做法：先跳过这个pod的安装，参照下文先安装一个worker node并注册到cluster，然后再重复安装步骤安装。

完成安装worker node并注册到cluster后，验证查看当前nodes
``` bash
❯ kubectl get nodes
NAME             STATUS   ROLES                  AGE    VERSION
worker           Ready    worker                 9h     v1.22.12
master           Ready    control-plane,master   4d3h   v1.22.12
```

当看到出现STATUS为Ready的worker时候，就可以再执行`./kk create cluster --with-kubernetes v1.22.12 --with-kubesphere v3.3.2`，然后经过漫长的等待即可。


# Worker Node
Ubuntu 实体机 in roy-macbookair（有些时候worker node的名字可能是这个），这是一台2013款的具有10年历史的老机器，陪我拿到了第一家上市公司的offer，但目前已经无法正常运行macOS，因此安装Ubuntu（图形化模式略微卡顿，使用命令行模式才能流畅运行k8s）。

按照[在 Linux 上多节点安装](https://kubesphere.io/zh/docs/v3.3/installing-on-linux/introduction/multioverview/)中的步骤进行安装。

将一台新准备好的Linux物理机， 作为Node（不管Worker是Master）添加到cluster只需要KubeKey + SSH 就能完成。

那么同样地，先安装相关地依赖
`$ apt install conntrack socat ebtables ethtool`

然后在当前目录下创建一个config-sample.yaml的文件（这一步可以在新机器的终端上完成，也可也在已有集群的任意一个物理机的终端上完成）
`$ ./kk create config`

在我这里，config-sample.yaml的内容如下，其中的ssh相关的信息需要自己填写，这里我使用的是密码登录，因此需要填写密码，如果使用的是ssh key登录，则不需要填写密码（但是需要配置ssh-key）。

然后按照教程中的配置文件，结合自己的node name与ip，修改配置文件，然后执行`$ ./kk create cluster -f config-sample.yaml`（集群未安装）/ `/kk add nodes -f sample.yaml`（集群已安装），等待一段时间后，集群就安装好了。

在经过以上操作后，可以看到我成功的创建了一个一共拥有3个Node的Cluster，就可以开始自己的kubenets操作了。

``` bash
13:09:53 CST success: [roy-qtc6]
13:09:53 CST success: [roy-300]
13:09:53 CST success: [roy-macbookair]
13:09:53 CST Pipeline[AddNodesPipeline] execute successfully
❯ kubectl get nodes
NAME             STATUS   ROLES                  AGE     VERSION
roy-300          Ready    worker                 2m41s   v1.22.12
roy-macbookair   Ready    worker                 23h     v1.22.12
roy-qtc6         Ready    control-plane,master   4d18h   v1.22.12
``` 

安装出了问题也别急，`./kk delete cluster`解君愁。

# 角色、权限等配置
就像大多数成熟的管理系统一样，初始化安装之后会分配一个admin账户，然后再通过该账户创建一个业务账户，之后大多数操作都应该通过业务账户进行操作。

而这些概念、操作在每个云平台上略有不同，且不影响k8s的核心组件，同时又都是基本都能在Web UI进行点点点操作，所以本段略。

可以参考[在kubesphere创建企业空间、项目、用户和平台角色](https://kubesphere.io/zh/docs/v3.3/quick-start/create-workspace-and-project/)

# 外部访问
在安装好Cluster之后，可以看到每个Node连接的IP地址是10开头的，这个明显是Kubernetes Cluster的IP地址， 不是外部可以访问的IP地址，因此需要一个网关来提供外部访问。
## 启动网关
网关是在项目中运行的 [NGINX Ingress 控制器](https://github.com/kubernetes/ingress-nginx)。
    
[在安装后启用服务网格](https://www.kubesphere.io/zh/docs/v3.3/pluggable-components/service-mesh/)

    本段为KubeSphere的配置，其他云平台可能不同
使用定制资源定义（CRD）里面的clusterconfiguration的ks-installer进行安装，看名字就知道是KubeSphere自己的，其他云平台没有。

## 提供外部访问
[设置集群网关](https://www.kubesphere.io/zh/docs/v3.3/cluster-administration/cluster-settings/cluster-gateway/)
访问模式设置为 NodePort，选择确定之后，集群网关详情里面会出现一个和宿主机网段相同的局域网网关IP地址（在我这里是192开头的），这个是可以访问的。

[通过使用 kubeconfig 文件配置访问集群](https://www.kubesphere.io/zh/docs/v3.3/multicluster-management/enable-multicluster/retrieve-kubeconfig/#%E8%8E%B7%E5%8F%96-kubeconfig)
除了上面链接中的方法外，还可以在KubeSphere UI右下角的工具箱图标上悬停，然后在弹出菜单中选择 kubeconfig，点击右上角的下载按钮，就可以直接下载连接K8s的kubeconfig.yaml。

特别注意的是需要把Cluster里面的server IP替换为局域网的IP
```yaml
apiVersion: v1
clusters:
- cluster:
    server: https://10.233.0.1:443  # 替换为集群网关详情里面和宿主机网段相同的局域网网关IP地址
```

# KubeSphere DevOps 系统
    本段为KubeSphere的配置，其他云平台可能不同，步骤在[KubeSphere DevOps 系统](https://kubesphere.io/zh/docs/v3.3/pluggable-components/devops/)
KubeSphere全家桶的DevOps 系统基于 Jenkins 的 KubeSphere DevOps 系统是专为 Kubernetes 中的 CI/CD 工作流设计的，它提供了一站式的解决方案，帮助开发和运维团队用非常简单的方式构建、测试和发布应用到 Kubernetes。(得了，感觉以前的工作又是造轮子了，这叫深度业务定制开发！)

> :warning: **整个集群内存最好25Gi以上**: 我一开始安装的时候就遇到了各种卡住且没有提示的问题，其实就是内存不够，但是增加内存是需要硬件成本的，排查的时候花了很多的精力和时间。

## Troubleshooting
在之前工作中用过实体机上的Jenkins，也用过k8s节点中的Jenkins，但从来没用过全家桶的Jenkins，因此本段就算安装不上，也完全不影响使用。

### 安装一直卡住，没有任何提示与报错
很自然去查看pod状况。

``` bash
❯ kubectl get pod -n kubesphere-devops-system
devops-jenkins-c8b495c5-4hqwf        0/1     Pending     0          19h

❯ kubectl describe pod devops-jenkins-c8b495c5-4hqwf -n kubesphere-devops-system
...
Containers:
  devops-jenkins:
...
    Requests:
      cpu:      2
      memory:   2Gi
Events:
  Type     Reason            Age    From               Message
  ----     ------            ----   ----               -------
  Warning  FailedScheduling  69m    default-scheduler  0/1 nodes are available: 1 node(s) had taint {node.kubernetes.io/memory-pressure: }, that the pod didn't tolerate.
```
（这里有时Events里面会是空的，就只能靠其他信息推测了）

但是很神奇的是查看node本身并没有添加任何污点
``` bash
❯ kubectl get nodes -o json | jq '.items[].spec.taints'
null
``` 
然后再仔细审视`describe pod devops-jenkins`pod的描述，报错是内存pressure，多半是内存不足，然后惊讶地发现需要2Gi的内存，而我的传家宝MacBook Air只剩下可怜的不到1Gi，由于这是物理资源的不足，无法弥补，要么放弃体验KubeSphere DevOps全家桶，要么只能自己在另一台物理机/node上安装jenkins。

一想到某人那种32Gi的电脑沉迷召唤师峡谷，就想悄悄给装一个Ubuntu上去996.

（2天后更新： 结果把自己的神船刷Ubuntu了，然后去给朋友搬家捡了的PC）

整一些内存大的电脑添加到Cluster 成为Node就好了。

实测发现要装KubeSphere DevOps 系统最好还是保证整个集群内存有25Gi以上的容量，否则会出现各种问题，为此时隔十多年我又玩起了虚拟机，这里**只推荐正统的VMware，VirtualBox**这种，否则虚拟化的大坑欢迎您。

# Cluster Uninstall
当Cluster出现某些问题，且安装上面的排查依旧不能解决的时候，就使用重装大法，DevOps的其中一个特质就是无状态、重装方便，在应用部署上这是巨大的进步。

首先需要一个config-sample.yaml来配置集群的信息，比如Master / Worker Node 的IP，账户等，如果没有的话，`./kk create config-sample.yaml`生成一下新的。

然后`./kk delete cluster -f config-sample.yaml`

接着SSH到每一台Worker Node机器上，进行[深度清理](https://stackoverflow.com/questions/44698283/how-to-completely-uninstall-kubernetes)

``` bash
kubeadm reset
sudo apt-get purge kubeadm kubectl kubelet kubernetes-cni kube*   
sudo apt-get autoremove  
sudo rm -rf ~/.kube
``` 
上面这个命令是把包都干掉了（而且实测不用重启机器就生效）

If you are clearing the cluster so that you can start again, then, in addition do the following to ensure my systems are in a state ready for kubeadm init again:

``` bash
kubeadm reset -f
rm -rf /etc/cni /etc/kubernetes /var/lib/dockershim /var/lib/etcd /var/lib/kubelet /var/run/kubernetes ~/.kube/*
iptables -F && iptables -X
iptables -t nat -F && iptables -t nat -X
iptables -t raw -F && iptables -t raw -X
iptables -t mangle -F && iptables -t mangle -X
systemctl restart docker
``` 

这个时候就算清理干净了，最后再回到Master Node机器上，执行`./kk create cluster -f config-sample.yaml`，等待一段时间后，集群就重新安装好了。

# 后记
本文历时半个月，从4月13号被干掉，休息半个月，5月1号开始搭环境，经过了半个月走走停停，不断地试错，查资料，写总结，才终于在5月20号地今天完成这个学习计划的开头 ————环境搭建。

这一个月里，有耍到接近昏迷，也有一天4个场面试的高强度，有点回到了快毕业那会的节奏。只是再也不像当初那么无助，迷茫而又没用行动力了。
