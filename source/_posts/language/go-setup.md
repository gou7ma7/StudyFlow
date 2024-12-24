---
title: 初学 Goland
date: 2023-05-19 21:00:10
tags: setup, go
categories: Language
---
# 背景
早在成都公司，就听闻 Go 大名， 当时业务后台正在从 Java 逐步重写过来，当时还经常在技术周会上听到大家的分享学习心得。
当时的领导说的，不要觉得自己学的时候有多聪明而洋洋得意，是因为 Go 的设计者足够优秀，才让这个语言如此容易上手。

# 学习路线
官方文档看一遍
https://go.dev/learn/#

example 看一遍
https://go.dev/tour/welcome/1

# 目标
写一个 restful 的 api，实现前端传入 cmd 后端执行。（比如 pwd, ls 那种）
<!--more-->

# 包管理
看到 go 的包是直接放在代码托管平台，而不是传统的包管理系统（如 Python 的 PyPI）， 很有意思，问了 chatGPT，主要原因就是灵活和间接。

# Coding
goland + vscode

## 安装 vscode, goland, plugin ect
略
## 安装 Delve 调试器
为了能在 vscode 中轻松愉快地 run and debug go， 需要安装调试器先。

`go install github.com/go-delve/delve/cmd/dlv@latest`

装不上请咨询 chatGPT

## Build Error: go build -o ...

```
Starting: /Users/admin/go/bin/dlv dap --listen=127.0.0.1:49829 --log-dest=3 from /Users/admin/code/go_test
DAP server listening at: 127.0.0.1:49829
Build Error: go build -o /Users/admin/code/go_test/__debug_bin1492456118 -gcflags all=-N -l .
go: go.mod file not found in current directory or any parent directory; see 'go help modules' (exit status 1)
```

可以，果然一开始启动就有问题，在见多识广的 chatGPT 分析下，都不用手动挡查资料了。

## Rosetta 笑死了， m2 不兼容
我明明用的 brew 装的，就离谱，不过我还有 Linux 机器，重新装一下环境吧。
```
Failed to launch: could not launch process: can not run under Rosetta, check that the installed build of Go is right for your CPU architecture
```

# 成果
```go
package main

import ( 
	"fmt"
	"log"
	"net/http"
	"os/exec"
)

func cmdHandler(w http.ResponseWriter, r *http.Request) {
	// 获取请求中的命令参数
	command := r.URL.Query().Get("cmdString")
	if command == "" {
		http.Error(w, "Missing cmdString parameter", http.StatusBadRequest)
		return
	}

	// 执行命令
	out, err := exec.Command(command).Output()
	if err != nil {
		http.Error(w, fmt.Sprintf("Error executing command: %s", err), http.StatusInternalServerError)
		return
	}

	// 输出命令结果
	w.Write(out)
}

func main() {
	http.HandleFunc("/cmd", cmdHandler)
	fmt.Println("Starting server on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

## 请求
http://localhost:8080/cmd?cmdString=ls
返回
go.mod
main.go

http://localhost:8080/cmd?cmdString=pwd
返回
/Users/admin/Code/go_test

http://localhost:8080/cmd?cmdString=ls%20-la
返回
Error executing command: exec: "ls -la": executable file not found in $PATH
（哈哈，没想到吧，我也没想到）
## 解析
最后想了一下，不部署前端了，直接拿 url 中的 query 执行得了。

- 用了标准库 net/http ，这个看起来应该类似 Python 中的 http.server (我从来没有用过这个)，通过 ListenAndServe 监听端口， HandleFunc 注册路径， 最后的 nil 是 go 的传统艺能 零值；

- cmdHandler 函数中，通过 r.URL.Query().Get() 去拿请求 url 中的参数；
- 通过 exec 函数去执行 cmdString
## 改成 gin
整个现代一点的框架
`go get -u github.com/gin-gonic/gin`


```go
package main

import (
    "fmt"
    "github.com/gin-gonic/gin"
    "os/exec"
)

var allowedCommands = map[string]bool{
    "ls":   true,
    "date": true,
}

func main() {
    r := gin.Default()

    r.GET("/cmd", func(c *gin.Context) {
        command := c.Query("cmd")
        if command == "" {
            c.JSON(400, gin.H{"error": "Missing cmd parameter"})
            return
        }

        if !allowedCommands[command] {
            c.JSON(403, gin.H{"error": "Command not allowed"})
            return
        }

        out, err := exec.Command(command).Output()
        if err != nil {
            c.JSON(500, gin.H{"error": fmt.Sprintf("Error executing command: %s", err)})
            return
        }

        c.String(200, string(out))
    })

    r.Run(":8080") // 启动服务器并监听在 8080 端口
}
```

可以看得出来，格式上和 Python 的 Flask 基本上没啥区别了。

# 结语
至此，用来写业务的 go 算是勉强上手了，可以看得出来设计得非常简约。
但是更多的特性，比如 毕业之后就再没用过 **指针**， **Goroutines** 和 **Channels**，还有 和 JS 一样没用类，所以设计 **embedding** 的用法，如果有这个计划，前面的区域，以后再来探索吧！