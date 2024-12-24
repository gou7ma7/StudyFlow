---
title: use MySQL Q&A
date: 2022-05-29 08:48:59
tags: linux
categories: Install
---

<!--more-->

# install

# connect


# setting


# usage
## MySQL clinet局域网访问 mysqld
1. （使用docker启动）这个没啥说的，直接docker run 一把过，唯一注意的就是如果宿主机上在已经启动过mysqld了，那么docker run -p的端口号就要换一个了；ps: 密码是通过docker run  -e MYSQL_ROOT_PASSWORD='pwd'启动的时候传环境变量设置的；
2. （我就是要练习自己搭建，咋说）：按照教程里面进入>mysql，也创建用户update user set user.Host='%' where user.User='root'; 本机连接是没有问题的，但是另一台机器client局域网登录的时候就报61 "Connection refused"；
3. 之前在公司里面都是叫网管然后秒解决，现在要自力更生了。
4. 首先再另一台机器client里面乱输入一个ip地址，报错为"Unknown MySQL server host"，不同于之前的被拒绝连接，说明当前host是ok，使用netstat -apn | grep 3306，看到tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      1016/mysqld         绑定到127.0.0.1，也就是回环了；
5. 目前既然知道是由于网络没有走通，那肯定就是配置的问题了，我找到mysql的配置文件，其中关于当前mysql用的是哪个配置文件里面有很多种说法，我不愿意深究，改成功的是/etc/mysql/mysql.conf.d/mysqld.cnf里边的bind-address;
6. 之后连接提示为1698 - Access denied for user 'root'@'IP'，说明现在的问题是密码设置的问题，大概要做的就是在启动的时候或者配置文件里面弄好连接密码，到时候client连接对口供就ok，我这边用在局域网又只玩就直接空密码了，反正以后也不会去没有网管的公司。 ps: 实际的默认密码在配置文件 /etc/mysql/debian.cnf 里面。
