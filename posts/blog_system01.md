---
title: 关于博客系统二三事（一）
sub_title: 这期我们来谈谈关于博客系统建设的一些思考
date: 2024-05-31+0800
category: 博客
id: d8f2433b-0f7d-423d-9a3a-a7e6ebffd92c
tags: [ "博客建设", "优化", "日常", "长期更新" ]
---

在刚开始写下这篇文章的时候我正在苦苦思考如何优雅的进行文章的更新（又或者说整个博客系统的结构？），而且整个系统还是跑在localhost上的那种极简测试版。正苦于没思路之时突然想起我好像已经一个月没有写文章了，遂来水之（

那么这篇文章就来聊一聊那些关于建设这个网站的一些有意思的问题，和一些思考吧。大概率会长期更新哦（

## 为什么要自己写博客和CMS？

~~别问，问就是手痒~~

### 关于博客和CMS

关于自己建立自己的站点这个企划我在小学的时候就有了，限于当时的设计能力和技术水平，在当时服务器挂掉不在维护之前最高的技术力就是从`codepen.io`
上复制粘贴代码下来拼凑出一个网页。怎么说呢...就像一份乐高玩具一样，她从远处看起来还有个样子，但是实际上细心看看就会发现她就是各个零件东拼西凑出来的，一个活生生的赛博Frankenstein。既不美观，有没有创新性（但是还是很可惜存档好像丢失了，不论如何仍然是我小时候努力的痕迹）。

好在最近高中毕业了，时间有一点小小的富足，而且在经过几年的时间之后技术力有所上涨，那么是时候完成小时候的梦想之一啦，我如是想到，于是就开始轰轰烈烈的基建计划了。

首先是前端，为了不让自己显得千篇一律，我的计划是直接自己手搓一套界面，使用现代的技术（指`React`
这些框架），也算是一种对小时候的自己的一种别样致敬吧。（碎碎念：这几年都在玩一些比较偏向服务器的东西，没怎么接触网页开发了，手感都生疏了嗷）

关于CMS...实际上市面上有大量的成熟的CMS，而且其中不乏有活跃的社区支持的佼佼者，包括不限于`Wordpress`
这种老牌选手，以及[其他大量](https://jamstack.org/headless-cms/)的headless-cms。

他们都实现了非常丰富的功能，远高于我的预期，而这对于我来说带来了额外的性能开销（至少`Wordpress`
这种东西对于我的那个轻量级服务器有点过于重量了）。一些精简的CMS又显得有点不成熟（社区上），毕竟谁也不想自己的博客后端出了问题没人修吧（

还有就是一些个人~~的精神洁癖~~
问题，相比之下我更喜欢将自己的数据保留在自己手中，或者说我不是非常喜欢那些第三方的介入（比如说一些专门的博客平台，他们会出现各种各样的问题，期中就包括广告，审核，以及其他平台本身对你的影响），尽管有些时候你不得不这样，但这些都是后话了。

最后一点，先不说自己使用自己写的软件听起来就非常炫酷 ~~（什么小学生心态啊）~~
，重要的是我可以完全自由的设计自己的系统，完全符合我个人的操作习惯（这点我稍后会聊聊）。比如说，API的调用逻辑，更加优雅的更新方式，还有好多好多我这里没想到的...

### 这么做值得嘛？

值得一提的是，自建CMS实际上是非常不理智的行为，特别是从时间利用效率上来讲，在你只考虑成品的情况下。这是一个非常耗时费力的过程，你需要考虑你的需求，和你“可能"
会出现的需求。你需要一直去考虑综合的系统框架，同时你也会由于自己一开始的各种考虑不周导致连续狂敲键盘几天的工作成果付之东流。这无疑是一件非常沮丧的事，你将会在不断重构中度过接下来的几个星期，直到你的土制CMS满足了你的需求，或者自暴自弃的跑回去使用`Wordpress`。

假如你只是想自建一个个人网站，那么类似`Hugo`，`Hexo`
之类的静态网页生成器是你的好伙伴，她们完全可以满足大多数你对个人网站的期望，同时不用花大量心思去设计，搓css。静态网站更快，性能更好，建站更方便，甚至不需要服务器都可以。不论是从时间成本还是经济成本她们都是不二之选。

但是假如一个这样的站点对于你来说有着特别的意义，就像对于我来说这里是专属于我的王国，是一个独属于自己的社交媒体，是一种日记本，是一面面向自己的镜子，那么你就会自发的去建设，维护，发展这篇土地。你会发现可能现有的产品和工具无法满足你的需求，或者说就是没办法作出你想要的效果，那么从零开始也许是一个不错的选择，它不一定总是最佳的方案，但是也许和尝试理解、修改各种现有的源码，这个方案是最有可能达成你的目标的，尽管他对个人要求相对较高。而且这个过程中你也会收获许多，比如说新的技术小知识，一些静下心思考、与内心交流的机会，
~~和一个独一无二的网站~~，这些不那么起眼的事物，或许在这个娱乐致死的时代反而是更为珍贵的呢...

## 现阶段的项目构成？

### 前端

- Next.js

目前的方法非常的暴力