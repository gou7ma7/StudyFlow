---
title: use docker Q&A
date: 2022-05-29 08:48:59
tags: linux
categories: Install
---

<!--more-->

# install

# connect

# setting

# usage

# docker container 互联
背景：  我现在启动了n个container，他们之前需要通过端口互相访问，但是按照docker的默认网络模式，是会自己拉一个小局域网的，服务部署好了也访问不进去。

尝试1: 更改`docker run --network=net`模式，直接共享宿主机的网络，然后开心的发现 -p 暴露的端口没了，服务一样的无法被访问了。

尝试2: 改用`docker run --link=container1`互相关联起来，然后可以ping了，但是发现通过端口访问container1的服务还是不行，后来发现互联和端口能访问是两个东西。。。然后灵光一闪，把container1别名设置成`localhost`然后就能访问了。。。

正确做法： 使用docker-compose进行编排啊，想暴露什么端口暴露什么端口，哦豁，这下要提前看docker的东西了。