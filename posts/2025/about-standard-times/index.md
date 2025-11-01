---
title: 关于标准时间的一些事
date: 2025-4-04
category: 碎碎念
id: 0af91143-d9fe-4740-b2ef-d89fc6fdd8ec
subtitle: 偶然间发现似乎 UTC 与 GMT 之间存在不小的区别，于是稍微展开探索一下...
tags: [ "日常", "时区", "时间", "冷知识" ]
---

前段时间偶然在聊天的时候发觉到了关于标准时间有些有意思的冷知识，稍微整理一下...

事先声明，这篇文章是基于大量在线资料，包括但不限于维基百科等不可置信源（incredible source）整理的，这意味着下面所有的文字将构建在 “源文章可信” 的假设，以及大量所谓 “俺寻思” 的逻辑上，遂无法确定此篇文章事实上的准确性，仅供参考。例如在编写的时候不同维基词条之间出现了定义与逻辑上的冲突，所以这篇文章所表达的现象与观点都应被理解为存在性的阐述，而不是准确性的定义。若有不同的观点和理解，欢迎联系沟通交流。

## UT0，UT1 与 UT2

首先要指出的提出的是，虽然 UT (or UT1) (Universal Time) 和 UTC (Coordinated Universal Time) 字面上相差不大，但实际上两者相差甚远，前者是在天文上定义的，后者是由国际原子时确定的。同时两者之间有个名为 DUT1 的时间差，大致在 $\plusmn 0.9s$ 的区间内摆动，由两者之间的闰秒机制保证范围。

以下是 UT0, UT1, UT2 的定义：
> $\text{UT0:}$ Unadjusted measure of Universal Time obtained directly from astronomical observations of the Earth’s rotation.
>
> $\text{UT1} = \text{UT0} + (\text{polar motion correction})$
>
> $\text{UT2} = \text{UT1} + (\text{correction on seasonal variations in the Earth’s rotation rate})$

根据定义，UT0 的结果是地域性的；UT1 基于此加入了极移的考量，所以这是一个全球统一的值，这也是在一般语境下 $\text{UT} \equiv \text{UT1}$ 的原因；UT2 在此基础上加入了季节性的因素的矫正，但随着 UTC 锚定点的改变，（曾在 1961 到 1971 期间锚定 UTC2，之后才更改为 UTC1），逐渐和 UT0 一起退出了历史舞台。

尽管现代生活中人们口中的 GMT 一般指的是 UT1（按照维基的说法），但实际上日常生活中人们似乎总是混着使用 GMT 和 UTC 这两个东西，举个例子，有些时候人们在信件里表达时区的时候（以及口语化的场景和部分司法系统下）会使用诸如 GMT-5 的写法来表达 UTC-5 时区。但基于两者间存在事实上的区别，仍然应该在高精度场合统一标准。

## 在 POSIX timezone format 下，\<TZ>+\<offset> 表示 \<TZ>-\<offset>

根据[这篇 StackExchange 文章](https://unix.stackexchange.com/questions/104088/why-does-tz-utc-8-produce-dates-that-are-utc8)的说法，后面的 offset 所表达的意思是 `x hours beind timezone`，所以在这种逻辑下，`TZ=UTC-8` 所表达的实际上是 `UTC+8` 这个时区。

基于这种历史性原因，`tzdb` 为了兼容性，所有以 `Etc/GMT` 开头的时区其 offset 的符号都是和 ISO 8061 相反的（也就是遵从了上述 POSIX 格式）。

## What's more: Falsehoods programmers believe about time

有人收集了一些关于时间的谎言（~~有点不太确定如何翻译这个词，也许伪命题更合适~~），原文链接在[这里](https://gist.github.com/timvisee/fcda9bbdff88d45cc9061606b4b923ca)，推荐去看看，这里稍微截取一些我觉得有意思的，以及个人给出的可能解释。

- Time zones always differ by a whole hour.

  其实并不是，举个例子，尼泊尔时区是 UTC+5:45，印度的时区是 UTC+5:30

- If you have a date in a correct YYYY-MM-DD format, the year consists of four characters.

  若是遵循 ISO 8601，`YYYY-MM-DD` 实际上指代的是 Extended Format（与之相对的是 `YYYYMMDD` 的 Basic Format），实际上它允许年份超过 [0000, 9999], 实际上，我们甚至可以写出如下两个时间：`+012345-06-07`（超过四位数，包括非数字字符），`-000010-06-07`（甚至支持公元前）。

  顺带一提，在 ISO 8601-2:2019 中时间的表示会更加复杂和灵活，Extended Date/Time Format (EDTF) 的加入使得（包括但不限于）如下表达成为了可能，解释器将按照支持性分级为 Level 0, 1, 2，具体参考[文档](https://www.loc.gov/standards/datetime/)。

  - EDTF Level 0
    - 基本的日期解析
    - Time Interval: 允许通过 `/` 来表达一段时间，比如 `2004-02-01/2005`，其含义为“从 2004 年 2 月 1 日的某个时间开始，到 2005 年的某个时间的区间”。
  - EDTF Level 1
    - Seasons: 21, 22, 23, 24 这四个数字分别表示春夏秋冬，比如 `2025-23` 表示 2025 年秋季
    - Qualification of a date: `?` 表达不确定时间（`2025?`: 可能 2025 年），`~`表达大致时间（`2025-11~`: 大致 2025 年 11 月），`%` 表达不确定的大致时间（`2025-11-01%`）
    - Unspecified digit(s) from the right: 形如 `20XX` 不确定时间
    - Open start/end time interval: `1985-04-12/..`
    - Time interval with unknown start/end: `1985-04-12/`
    - Negative calendar year: `-1985`
  - EDTF Level 2
    - Exponential year: 年份的科学计数法支持（`Y-17E7`: -170000000 年）
    - Sub-year groupings: 在季节的基础上扩展了季度，南北半球等
    - Set representation: `[]`（其中一个时间）, `{}`（所有时间）支持

- Months have either 28, 29, 30, or 31 days.
  
  公历（Gregorian calendar） 1582 年的 10 月 只有 21 天，从 4 号直接到了 15 号。公历以外的日历系统有一般着独特的计量，比如金星历法（Venus calendar）一年有 19 月，其中有 18 个月有 20 天，而第 19 个月有 5 天 3 时 45 分 48 秒。

- The day before Saturday is always Friday.

    在公历下，这种事件一般发生在国家或地区切换时区的时候，如萨摩亚在 2011 年 12 月 29, 星期四的时候将时区从 UTC-11 调到了 UTC+13，使得这个地方跳过了周五，直接来到了 2011 年 12 月 31，星期六。其他历法可能对一个星期内每一天的叫法都不一样（或者说对星期的定义有所不同），所以这里不纳入讨论范围。

---

碎碎念：怎么会有人附件写的比正文长啊喂（