---
title: 关于在Linux上安装ComfyUI的那档事
date: 2024-08-20+0800
category: 备忘录
id: 5b029257-0ca0-42e5-a04d-0ce84d11d724
sub_title: 记录一下
summary: 略
tags: [ "日常", "Linux", "ComfyUI" ]
---

好一段时间没有关注AI图片生成的内容了，近日了解了一下，发现好像和之前我刚开始玩`Stable Diffusion web UI`的时候的那种呢力相比...简直是跨时代的进步。于是呢我决定升级一下自己的"玩具盒"，看看由节点逻辑构成的`ComfyUI`能给我带来怎么样的惊喜。

~~其实就是想水一篇文章啦~~

## LT;DR

没什么技术含量啦，就是使用`python venv`而已（叉腰）。

## 坐和放宽，让我们开始吧（笑）

一般情况直接参考官方[安装指南](https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#manual-install-windows-linux)，以下是个人建议的安装步骤（基本上就是翻译啦）。

1. 克隆仓库
    ```bash
    cd ~ # 先给ComfyUI安个家
    git clone https://github.com/comfyanonymous/ComfyUI.git comfyui # 顺便按照自己的使用习惯重命名
    cd comfyui
    ```
2. 创建`python venv`（建议，可选）

    对于大部分操作系统来说这一步是没有必要的，不过鉴于有可能会污染环境（谁都不想碰到依赖地狱的吧（笑）），而且部分发行版可能会有特殊要求（比如说在`Arch Linux`上pip直接被禁用掉了），使用虚拟的python环境在个人看来是最佳的解决方法。

    观察`.gitignore`可发现官方使用虚拟环境使用的是`/venv`目录而不是`.venv`，所以通过以下命令创建并激活环境
    ```bash
    python -m venv venv
    source venv/bin/activate # 根据你使用的shell选用合适的脚本
    ```
3. 依赖安装

    首先根据你的GPU型号选择合适的依赖安装命令

    - AMD
        ```bash
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm6.0
        ```
    - AMD (Nightly版本，可能提供格外的性能提升)
        ```bash
        pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.1
        ```
    - NVIDIA
        ```bash
        pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu121
        ```
    - NVIDIA (Nightly版本，可能提供格外的性能提升)
        ```bash
        pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124
        ```
    - Others
        
        对于Intel显卡和Apple silicon，参考[这里](https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#others)。

    注：鉴于文章时效性问题，请查看官网，使用最新的依赖安装

    然后再安装一下`requirements.txt`里面的依赖
    ```bash
    pip install -r requirements.txt
    ```

    *大功告成*

## 使用方法

和官方操作指南相比，我们多了一步，激活虚拟环境
```bash
#!/bin/bash
source ./venv/bin/activate
python main.py
```
建议制成shell脚本，方便后期使用。

## 參考列表
- https://github.com/HAMM3REXTREME/ComfyUI-Installer
- https://github.com/comfyanonymous/ComfyUI

