---
title: hard 4. Median of Two Sorted Arrays -- 第一道Hard，做了5年。
date: 2022-05-29 08:48:59
tags: 
  - Hard
  - OJ
categories: Leetcode
---

# 背景
我最重要的一道题，第一次遇到看题解也无法理解的题，想起了以前高中去竞赛划水的日子，想起了在大学划水地没有去竞赛的日子。

第一次看到这个题的时候，我还不知道做工程分前端和后端，我还可能只有170斤，我还看着Java代码觉得太丑陋看不懂；

后来小付快速的把这题理解并做出来了，我还是没有足够的行动力，后来就开始了一系列的迷茫的日子；

这么多年过去了，只有山东大哥的红轴Cherry键盘一直陪着我，他拿这键盘打Dota，考研；我拿这把键盘打Lol，假装考研；又在磨子桥的电脑城被我的老乡阵修理+魔改；然后在成都摸鱼，在深圳打字。

有很多变化了，又有很多没有变，不过看样子我的行动力确实螺旋上升了。

<!--more-->
# 题干
https://leetcode.com/problems/median-of-two-sorted-arrays/

There are two sorted arrays nums1 and nums2 of size m and n respectively.

Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

You may assume nums1 and nums2 cannot be both empty.

Example 1:

nums1 = [1, 3]
nums2 = [2]

The median is 2.0
Example 2:

nums1 = [1, 2]
nums2 = [3, 4]

The median is (2 + 3)/2 = 2.5

# 思路
## 保底算法
先排序再找中位数，由于python的sort()使用的是快排，所以o(n)=log(n)，不过揣摩出题人意图，肯定不是想考察这个知识点。
## 分析类型
分析之后不难得出，本题的目的是找出2个有规律的数组中的一个有特征的值，稍微思考之后能够得出可以用分治法；

原因为： 中位数实际上只与整个数组中位置最中间的两个数有关系，因此2个数组的共同中位数也只会与最多2数组中各取2个数（共计4个数）有关系，而其他部分都可以剪枝。

# 分治法
```python
from typing import List
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        nums1_small = nums2_small = 0
        nums1_big = len(nums1) - 1
        nums2_big = len(nums2) - 1

        while nums1_big - nums1_small + nums2_big - nums2_small > 2:
            break  # TODO 一头一尾一个个删除

        # 只剩下其中一个列表
        if nums1_small > nums1_big:
            return (nums2[nums2_small] + nums2[nums2_big]) / 2
        if nums2_small > nums2_big:
            return (nums1[nums1_small] + nums1[nums1_big]) / 2

        return (max(nums1[nums1_small], nums2[nums2_small]) + min(nums1[nums1_big], nums2[nums2_big])) / 2

```
有了上述思路之后不难写出最初版本的伪代码：既找出分治原子，然后不断缩小问题规模；  
体现在本题中就是：每次判断2数组两端4个数字，淘汰掉其中最大和最小的2数；然后当其中一个数组无法再淘汰数时
## 分治原子有问题
跑了几个用例之后发现不正确，因为按照上述算法只有把其中一个数组中的数全部淘汰完了才是分治原子，这是不符合中位数定义的，因为每一个数组的最中间的2个数都是有成为“共同中位数”的可能的，因此分治原子条件应当是任意一个数字的长度小于2；
```python
from typing import List
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        def get_mid(nums):
            if not nums:
                return 0
            else:
                len_nums = len(nums)
                left = (len_nums - 1) // 2
                right = len_nums // 2
                return (nums[left] + nums[right]) / 2

        len1 = len(nums1)
        len2 = len(nums2)
        while len1 > 2 and len2 > 2:
            pass  # TODO 一头一尾一个个删除
        if len1 == 0:
            return get_mid(nums2)
        if len2 == 0:
            return get_mid(nums1)
        
        # TODO 解决其他分治原子问题

        return get_mid(nums1)
```
中间其实经过了长达一个星期的思考和尝试，在这里意义不大就不展开了，毕竟距离我第一次看这个题已经过去5年；

主要解决以下问题：
1. 摒弃中学时代的“下标处理数组模式”，都做了这么多年工程了，还是要明白可读性是远比”性能“重要的，且最后的时间表也看得出来并没有多少损耗；
2. 优先处理特殊情况，这个从OJ到工程都是很重要的，这个都忘了那就没啥可说的了；
3. 分治原子找错了，当其中任意一个数组只剩小于2个数的时候就可以结束分治进入决赛圈了；

## 分治原子的优化 & O(n)的思辨
在本来的做法中，进入决赛圈后，我是拿其中小的那个数组中剩下的数去和大的数字的两边，中间各个数字进行比较；

为此还总结了3种情况： 包含在大的中，分离在大的外，与大的交叉，然后又根据这三种情况进一步的分类，试图找出通用的比较规则；

实际上非常的蠢，是属于自己给自己找麻烦，且实际上的刷题过程中，经常由于这种case过多的情况进行放弃。

在连续想了一个星期之后，突然发现，对于分治原子来说，最后这一步使用的方法是不会影响到整体的时间复杂度的，且做了这么多年工程，熟练使用轮子的意义远大于反复的抠这几个下标，于是果断使用先合并、排序再找中位数的方法；

且由于最后决赛圈的中位数说白了还是在小于4个数之间出现，因此这一步O(n)=1；

实际上很多时候思维是会被自己局限的。
```python
# TODO 解决其他分治原子问题 code
nums1.extend(nums2)
nums1.sort()

return get_mid(nums1)
```

## 分治策略的优化
跑几个case之后就会发现，实际上对一个数组来说，除了“中间”一点的位置可能产生中位数，其他部位其实都是炮灰；

再发现数组边上其实很多时候都是在重复淘汰同一边的数，在继续观察之后发现规律：

先比较两个数组的中位数，同时将2个数组平均分成两份，考虑一下，中位数只可能诞生在两个数组相对“中间”的位置，因此一次性淘汰掉2个数组的两边的部分；

最后再注意一下边界取值等，代码如下
```python
# TODO 一头一尾一个个删除
len1 = len(nums1)
len2 = len(nums2)
while len1 > 2 and len2 > 2:
    if len(nums1) == 1 or len(nums2) == 1:
        break

    mid_1 = get_mid(nums1)
    mid_2 = get_mid(nums2)
    if mid_1 == mid_2:
        return mid_1
    elif mid_1 < mid_2:  # 砍掉nums1小的和nums2大的部分
        cut = min((len(nums1) - 1) // 2, (len(nums2) - 1) // 2)
        nums1 = nums1[cut:]
        nums2 = nums2[:len2 - cut]
    else:  # 砍掉nums1大的和nums2小的部分
        cut = min((len(nums2) - 1) // 2, (len(nums1) - 1) // 2)
        nums1 = nums1[:len1 - cut]
        nums2 = nums2[cut:]
    len1 = len(nums1)
    len2 = len(nums2)

```
