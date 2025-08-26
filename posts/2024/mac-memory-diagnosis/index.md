---
title: 一次失败的故障排查（待續）
date: 2024-10-05
category: 备忘录
id: 44cb00dc-4b57-445f-8735-663c41840383
subtitle: 这是一个关于Mac操作系统崩溃的小故事
tags: [ "Mac", "macOS", "故障排查", "WIP" ]
---

从很长一段时间开始（大概是两年以前），我手上的一台Mac就开始间歇性出一些些小问题。一开始是报`宗卷哈希值不匹配`，大概报错信息是这个样子的
```text
Volume hash mismatch: Hash mismatch detected on disk1s1. Mac OS should be reinstalled on this volume.
```
但是当时好像唯一的现象只有这个来自macOS的报警，没有任何其它问题的出现，所以我就逐渐忽略了这个问题，毕竟谁会闲着没事干去重装系统呢（笑）。然后嘛，过一段时间我就重装了（逃），主要是由于我手头上各种奇妙的设置逐渐将操作系统配置得和蜘蛛网一样，环境逐渐开始崩坏，而解决这种问题最简单的方法自然就是重新fresh install一下啦。

但是这个问题还是复线了，就在重装系统之后的不久。由于当时这是我的主要工作机，所以我直接扛着她去了Genius Bar，毕竟吃饭的家伙可不能出问题。然而通过`Apple Diagnostics`检测并没有出现任何问题，工作人员直接和我说可能是系统问题，重装一下就好了（明明是刚刚重装的怎么会出问题嘛），但是由于考虑到这是“Apple专家”给出的方案，所以嘛...我照做了，然而并没有什么作用。

我和这个Hash Mismatch就这么相安无事的共处了几年，直到最近，她决定给我搞一波大的。这是一天，我早上从被窝里爬起来，正打算开始我的日常摸鱼时，电脑启动失败了。大概率是晚上在进行自动更新的时候内核挂了（顺带一提，正好从前段时间开始，部分软件开始随机崩溃），进而导致引导损坏。不得不日常重装系统，但是从这次开始，一切变得有意思了起来。

现在所有的软价都开始奔溃，从`idea`到`loginwindow`，可以想到的全都有（当然包括`Kernel`在内）（顺便偶然间发现macOS自带的`Console`应用的搜索filter好像会自动过滤掉`Kernel`的记录）~~（但是`Firfox`好像只出现了标签页层面的奔溃，并没有出现软件上的全局奔溃）~~（更新：现已无法打开任何标签页，启动既崩溃），所以嘛这下不得不开始尝试修复这个问题了。

## 排障记录

> MemTest86 and Memtest86+ are memory test software programs designed to test and stress test an x86 architecture computer's random-access memory (RAM) for errors, by writing test patterns to most memory addresses, reading back the data, and comparing for errors. Each tries to verify that the RAM will accept and correctly retain arbitrary patterns of data written to it, that there are no errors where different bits of memory interact, and that there are no conflicts between memory addresses. (Wikipedia)

正如上所言，`MemTest86`和`MemTest86+`是一款用来跑内存测试的软件，但其实从某种角度上来讲也不太像是的感觉，毕竟它们不是跑在任何操作系统上的，而是直接通过BIOS/UEFI裸金属上启动。这两款软件是非常成熟的解决方案，而且都有漫长的历史（`MemTest86+`作为前者的fork，已经有22年的维护历史），所以我直接采用它们作为测试工具。

### 计划

1. 内存测试 
2. 找到错误内存
3. 按[照这](https://github.com/0nelight/macOS-Disable-RAM-Areas)里的指导尝试修复
4. 解决问题


### 测试

第一次跑`MemTest86+`的时候给了我巨大的惊喜，短短五分钟左右扫出的问题大概就出现了350个，在4小时的测试之后数量进一步涨到了580左右，这系统不崩溃才怪嘞。

（待续）
