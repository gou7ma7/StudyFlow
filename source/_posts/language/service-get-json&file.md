---
title: Web Service同时json字符串和文件，编码该如何设置
date: 2022-05-29 18:38:17
tags: Python, HTTP
categories: Language
---

# 需求
现在有一个Web Service的api，请求的时候有json字符串、文件，或者两者都有，应该怎样设置接口协议。（以Flask为例）

# 背景
在 HTTP 协议消息头中，使用 Content-Type 来表示请求和响应中的媒体类型信息。
<!--more-->

Content-Type: application/json;charset:utf-8;

> JSON 是一种轻量级的数据格式，以 “键 - 值” 对的方式组织的数据。这个使用这个类型，需要参数本身就是 json 格式的数据，参数会被直接放到请求实体里，不进行任何处理。服务端 / 客户端会按 json 格式解析数据（约定好的情况下）。

Content-Type: multipart/form-data
> 这是一个多部分多媒体类型。首先生成了一个 boundary 用于分割不同的字段，在请求实体里每个参数以 ------boundary 开始，然后是附加信息和参数名，然后是空行，最后是参数内容。多个参数将会有多个 boundary 块。如果参数是文件会有特别的文件域。最后以 ------boundary–为结束标识。multipart/form-data 支持文件上传的格式，一般需要上传文件的表单则用该类型。

# 请求参数构造
此处以python的Web api框架 flask与HTTP 请求库requests进行演示，其他框架、语言的构造解析均可参照下表中的Content-Type

|请求类型|  Content-Type   | requests.post参数  | flask.request取值对象 | flask.request取值结果| 备注 |
|  ----  | ----  |  ----  | ----  | --- | --- |
| 参数  | application/json  | json=data | request.get_json(), request.json| 均有，dict | Content-Type自动: application/json|
| 文件  | multipart/form-data; boundary= |files=files|request.files|有，ImmutableMultiDict| 见**解释*1**|
| 参数  | application/x-www-form-urlencoded  | data={'json': data} | request.form| 有，ImmutableMultiDict | 按照表单编码|
| 参数 文件  | multipart/form-data; boundary= |data={'json': data}, files=files|request.form，request.files|有，分开取| 混合编码，抓包信息见**解释*2**|

>解释*：
> 1. 使用requests构造HTTP请求的话，**不要显示的设置headers={'Content-Type': 'multipart/form-data'}**，因为不能给定boundary具体的值，接口解析会失败
> 2. 请求体body中同时有json字符串和文件的抓包，raw格式（原始格式）的结构类似如下，可以看到键值对是按照表单编码，文件是按照二进制格式编码之后，再组成键值对进行表单编码
> ![raw格式的请求体](/images/http_upload_01.png)
> 更加直观的webForms格式查看该请求的结构如下![webForms格式的请求体](/images/http_upload_02.png)
> **如果使用其他语言或者HTTP请求请求库，请自行按照上述方法进行请求的构造**
>


# 原因剖析
先进的HTTP请求库如requests在构造请求的时候会根据post的不同参数自行构造Content-Type，因此平时根本没有注意；  
在写业务时遇到该问题，也没能沉下心好好试验一下，总想网上找篇文章一抄了之解决问题。