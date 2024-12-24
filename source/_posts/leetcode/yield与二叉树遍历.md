---
title: 从二叉树遍历到yield # TODO
date: 2022-05-29 08:48:59
tags: 
  - python
  - computer
categories: Leetcode
---



# yield的作用
首先yield就是return，不要想多了，所以搭配`yield from func()`能够递归，就是这么简单；

只是说普通的函数返回的是一个value或者obj，而yield返回的是一个生成器对象。
## 生成器的定义&同迭代器的区别
在python中实现了__iter__和__next__方法，可以迭代操作的对象就叫迭代器；  
构建迭代器的时候，并不一次性加载所有元素到内存，只有调用next方法的时候才会**返回**需要的该元素；

<!--more-->

生成器就是一种迭代器，由生成器函数返回；  
生成器函数就是上文中的 return -> yield的函数；  
# 用法
学以致用，看文档的时候自然说：都懂，都懂，结果自己不仅写不来还看不懂。  
尤其是再遇到几个yield并排就不会了？
## 当一个生成器函数中多个yield并排

```python
import sys

def func():  # 普通函数
    return 1
    return 2
    return 3

def gen():  # 生成器函数
    yield 1
    yield 2
    yield 3

# 遍历一个生成器
it = gen()
while True:
    try:
        print(next(it))
    except StopIteration:
        sys.exit()
```
要遍历一个生成器，自然需要调用next方法到报错为止，实际上行为和遍历序列的时候下标越界同理，只是现代编译器做好了没意识到而已。  
>普通函数func调用：  
>`print(func())  # 1`  
>`print(func())  # 1`

  

>生成器函数调用：  
>`it = gen();  # 获得一个生成器`  
>`print(next(it))  # 1`  
>`print(next(it))  # 2`  

## 为啥要用生成器
从上文中可以看到生成器函数一个巨大的优势就是函数写出来是分块的，可以直接剪掉很多的选择分支，让代码更加的整洁接近算法描述。  
尤其是当需要递归的时候，使用yield的代码写出来简直就像是伪代码，曾一度让我无法理解其中的逻辑分支和递归基是如何运行的。

比如使用普通函数实现中序遍历一个BST的伪代码如下
```python
global_res = []

class TreeNode(object):  # 定义一个二叉树
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def in_order_visit(node: TreeNode):
    if node is None:  # 递归基
        return None
    in_order_visit(node.left)
    global_res.append(node.value)
    in_order_visit(node.right)

in_order_visit(root)  # root为需要遍历的BST的根节点
print(global_res)
```
### 递归参数只能是对象本身，遍历出来的值无法收集
可以明显的看得出来，遍历函数本身在递归的过程中**参数只能是node or None**，同时**node = None作为递归基**；  
那么问题来了，我**遍历出来的值**如何返回给上层呢？  
我当时的函数设计的无比复杂，进入函数的时候先进行一个**逻辑判断**，再选择进入node.left还是返回node.value，因此一个函数就可能**接受2种数据结构**，  
再根据自己的下面的调用结果判断是该继续往下递归还是往上return。
### 需要的值放到递归参数中会导致逻辑十分混乱
代码无比丑陋，逻辑无比复杂。  
不得已，只得引入**全局变量**（不引入也可以，可以让遍历函数返回一个元组(node, node.value: list[int])，但本质没变，就是把列表当成指针来用，还是全局，这不pythonic）  
让遍历函数只专心访问node，我用一个全局变量来储存访问结果（也就是网上教材都只让你print出来的操作）  
问题是全局变量应该少用，这是破坏结构性的，不管是封装成对象还是闭包还是什么玩意儿；
或者不用递归，用循环 + 堆栈来访问这个树，这与本文无关。

### 必须将所有节点全部访问到内存
迭代器可以每次调回的时候再到下一个节点，在有些情况（比如求前n个数），就不用像普通函数这样需要先遍历（排序）整个树，然后再截取需求的部分。

### 试图yield实现递归
使用生成器函数遍历一个BST的代码如下
```python
def in_order_visit_gen(node: TreeNode):
    if node is None:
        return None
    yield visit_bst(node.left)
    yield node.val
    yield visit_bst(node.right)

it = visit_bst(root_node)
print(next(it))
```
结果非常意外`<generator object visit_bst at 'addr in mem'>`  
为什么呢？  
其实很简单，因为yield是懒狗，它只会返回一个it（迭代器/生成器)，还记得之前的“生成器函数调用”的方法么。
每次需要先调用生成器函数，得到一个it，相当于把无产阶级请过来了`it = gen()`
然后在调用这个迭代器，才能调用，相当于任务分配下去了`print(it)`


因此如果yeild接自己想递归的话，第一次下去的时候，就会直接返回一个visit_bst(node.left)，还记得吗，这是一个生成器函数，现在调用它自然只会得到一个迭代器，还需要在外面像“遍历一个生成器”一样不断地用next去调用才能启动。

### yield from = return -> 递归
python好就好在他有足够多的语法糖，在本文中只要粗暴的记得以下等价关系就行  
yield obj = yield from func() = return obj/func()  # 递归过程  
相当于yield from就是先调用这个func得到一个it，然后马上就调用这个it一次，因此就得到了递归；
```python
def in_order_visit_gen(node: TreeNode):
    if node is None:
        return None
    yield from visit_bst(node.left)
    yield node.val
    yield from visit_bst(node.right)

it = visit_bst(root_node)
print(next(it))
```

### 并排yield -> 递归表达式

# TODO 有空再写吧。