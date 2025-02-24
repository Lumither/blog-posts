---
title: 关于博客系统二三事（二）：自动化部署
date: 2024-12-5-0800
last_update: 2025-2-20-0800
category: 博客建设
# header_img: https://oss.lumither.com/blog/pictures/gothic_kiriyama_lolita.webp
id: a5df0869-879b-45a2-94b4-7eea0e294c8f
sub_title: 每一次版本大更新的时候都要手动部署，实在是太麻烦了，不如让它自动化吧（笑）
tags: [ "博客建设", "日常", "Docker", "Docker Compose" ]
---

上回书说道，彼时的 Nocturne，由多个部件组成，场面之混乱当属一绝。脑部一下每次大版本更新的时候都会出现各种各样奇怪的小情况（什么一不小心忘记更新依赖导致 `npm build` 完之后出现 hash mismatch (Next.js SSR 部分客户端报错（忘记 `npm update` 了），一不小心少了个环境变量导致哪个服务启动失败啊之类的)。考虑到其实每一次的操作并没有太大的区别，其实一切都可以通过自动化的流程来解决，于是便有了这篇文章。

当然，由于这篇文章并不是一次性写完的，比如说第一次落笔的日期是2024年12月5日，第二次完善（或者说完成？）的时间已经来到了25年的2月20日，所以说可能阅读体验会有所割裂 ~~（什么，你问中间那段时间干什么去了？问就是摸鱼去了（笑））~~，我会努力将逻辑调整清楚的。

## Docker，启动！

> [!NOTE]
> 初次书写时的方案并不是最终的解决方案，相比之下后者移除了 `docker compose` 的使用，转而采用了一个类似网关之类的机制，从而实现一定程度上的不停机的自动更新，我将会在后面解释这一变化。

项目组成非常简单，三个部分，前端，后端，数据库。为了方便维护（个人喜好），我将 `compose.yaml` 分割了一下，大致结构展示如下：

```text
nocturne
├── .env                            
├── frontend
│   │── .dockerignore
│   └── ... // 源码
├── backend
│   │── .dockerignore
│   └── ... // 源码
├── container
│   │── dev
│   │   ├── backend.containerfile
│   │   └── frontend.containerfile
│   └── release
│       ├── backend.containerfile
│       └── frontend.containerfile
├── dev.compose.yaml
├── prod.compose.yaml
└── Makefile
```

从上往下的逻辑舒徐开始介绍：

- `.env`: 这个文件包含一大堆环境变量，相当与是我的项目的配置文件，大致内容如下：

    ```sh
    # database settings
    DB_HOST=localhost
    DB_PORT=5432
    
    # database & backend settings
    POSTGRES_PASSWORD=passwd
    POSTGRES_USER=nocturne
    POSTGRES_DB=nocturne
    POSTGRES_HOST=postgres

    # backend settings
    BLOG_GIT_URL=https://github.com/Lumither/blog-posts.git
    WORK_DIR=/nocturne

    # frontend settings
    API_LOCAL_URL=http://backend:3001
    API_REMOTE_URL=https://lumither.com/api
    ```

- `frontend`: 前端源码文件夹，包含一个 `.dockerignore` 用来排除不希望放入容器的东西（不必要或者影响构建），示例如下（其实和 `.gitignore` 内容没有太大区别的样子）：

    ```sh
    /node_modules
    /.next
    /out
    /build

    .DS_Store

    *.pem
    .env*.local
    ```

- `backend`: 如上，这是它的 `.dockerignore`:

    ```sh
    /target
    /Cargo.lock
    ```

    其实这一部分的处理非常粗糙，但是在后面不影响结果，所以嘛....(开摆)
- `container`: 一个用来存放 dockerfile 的目录，分开dev和 production 方便管理，待会我会详细谈谈 production 部分（dev 的部分不会涉及 CI/CD，而且也只在开发环境起作用，此时不需要 docker 反而更方便调试，所以不多进行说明）
- `dev.compose.yaml`: 由名字可得，dev 环境的 `Docker Compose` 配置文件，不做过多解释。
- `prod.compose.yaml`: 生产环境的 comopsefile，内容如下：

    ```dockerfile
    services:
        frontend:
            build:
            context: ./frontend
            dockerfile: ../container/release/frontend.containerfile
            restart: always
            ports:
                - "3000:3000"
            env_file:
                - ./.env

        backend:
            build:
            context: ./backend
            dockerfile: ../container/release/backend.containerfile
            args:
                ARCH: ${ARCH}
            restart: always
            ports:
                - "3001:3001"
            env_file:
                - ./.env
            dns:
                - 1.1.1.1

        postgres:
            image: postgres:16.3
            ports:
                - "5432:5432"
            env_file:
                - ./.env
    ```

    唯一值得一提的是我在 backend 那一部分添加了一个 `ARCH`，详细作用我会在后面体积。
- `Makefile`: 就是用来构建的啦:

    ```makefile
    ARCH := $(shell uname -m)
    ifeq ($(ARCH), arm64)
        ARCH := aarch64
    endif

    all: release

    release:
        docker compose -f prod.compose.yaml build --build-arg ARCH=$(ARCH)

    dev:
        docker-compose -f dev.compose.yaml up --build

    clean:
        docker-compose -f prod.compose.yaml -f dev.compose.yaml rm -fsv
    ```

    同上，我稍候会提起为什么会有一个 if block 在这里。

由于在正真开始写这一团东西之前我还没有完全决定使用 Docker，毕竟还有  等其它的容器化方案。所以一开始创建文件的时候使用了 `.containerfile` 这种 unopinionated 的文件扩展名。

## 迭代

在一开始，我直接按照我平时部署服务的流程写了一遍 dockerfile，大概是这个样子的：

- `frontend.containerfile`:

    ```dockerfile
    FROM node:latest
    WORKDIR /app
    ENV NEXT_TELEMETRY_DISABLED=1
    COPY package*.json ./
    RUN npm install
    COPY . .
    RUN npm run build
    CMD npm start
    ```

- `backend.containerfile`:

    ```dockerfile
    FROM rust:latest
    WORKDIR /app
    COPY . .
    RUN cargo build -r
    CMD cargo r -r
    ```

总而言之就是简单粗暴，但是可以跑。但是这里有个巨大的问题，那就是容器的体积:

<div align="center">

| Name              |   Size   |
| ----------------- | :------: |
| postgres          | 630.85MB |
| nocturne-frontend |  3.59GB  |
| nocturne-backend  |  3.61GB  |

</div>

Hummm.. 对于一个普普通通的服务来说，这个大小有点难以接受，优化，必须优化。经过小小的资料查询，我发现了一个有意思的东西，既[来自谷歌的 distroless 方案](https://github.com/GoogleContainerTools/distroless)。
> "Distroless" images contain only your application and its runtime dependencies. They do not contain package managers, shells or any other programs you would expect to find in a standard Linux distribution.

对于 nodejs 服务，它提供了 `gcr.io/distroless/nodejs22`，而一般的“mostly-statically compiled“可执行提供了 `gcr.io/distroless/cc`。

### `frontend.containerfile`

对前端配置稍加修改，配合 Multi-stage builds，便获得了如下 `frontend.containerfile`：

```dockerfile
FROM node:22 AS builder
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM gcr.io/distroless/nodejs22 AS production
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=builder /app/next.config.mjs ./
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
ENV HOSTNAME="0.0.0.0"
CMD ["./server.js"]
```

> [!NOTE]
> 除 `gcr.io/distroless/cc`，`gcr.io/distroless/base` 和 `gcr.io/distroless/static` 以外，其它带特定语言支持的 `distroless` 都自带默认的 ENTRYPOINT，所以应使用
>
> ```dockerfile
> CMD ["./server.js"]
> ```
>
> 而不是
>
> ```dockerfile
> ENTRYPOINT ["./server.js"]
> ```

这个版本去除了没必要的 `node_modules`，同时将 Next.js 设置为了 standalone 构建方案，这样的话它就会自动抽取依赖以获得最小的打包体积。有一点需要注意的是 `COPY --from=builder /app/.next/static ./.next/static` 这一步非常重要，各种 CSS 都被单独提了出来，需要将其拷贝至对应位置，否则样式就会完全失效。

### `backend.containerfile`

我对 `backend.containerfile` 做了较大的改变，现在是这个样子的：

```dockerfile
FROM rust:latest AS builder
WORKDIR /app
COPY . .
RUN ["cargo", "build", "-r"]

FROM gcr.io/distroless/cc AS production
ARG ARCH
COPY --from=builder /app/target/release/api_server ./api_server
COPY --from=builder /usr/lib/${ARCH}-linux-gnu/libz.so.1 /usr/lib/${ARCH}-linux-gnu/
ENTRYPOINT ["./api_server"]
```

> [!NOTE]
> 注意：`gcr.io/distroless/cc`里面由于缺少内置的 shell，所以你需要以 vector form 来写入 ENTRYPOINT。
>
> ```dockerfile
> # this is valid
> ENTRYPOINT ["./api_server"]
>
> # these are not
> ENTRYPOINT "./api_server"
> ENTRYPOINT ./api_server
> ```

这个 dockerfile 里面有一个参数 `ARCH`，用来表示当前计算机的 CPU 架构，（一般）POSIX 系统下可以通过 `uname -m` 获得（至少 IBM 的机子不是[^2]）。由于 `gcr.io/distroless/cc` 中没有提供 `zlib`支持，而我的 `nocturne` 动态连接了它，其中一种解决方法就是直接将 builder 中的直接复制过去。`libz.so.1` 的路径不是固定的，它会根据计算机架构而变化，所以我们需要获得当前（生产环境）的架构而确定 `libz.so.1` 的位置。这里我们通过外部 `Makefile` 自动获取。

```makefile
ARCH := $(shell uname -m)
ifeq ($(ARCH), arm64)
    ARCH := aarch64
endif
```

由于 MacOS 系统特性会返回 "arm64"，而 Linux 社区一般使用 "aarch64"（至少在动态库路径上），所以这里需要做一个小转换提高通用性。关于两者之间的区别可以参考[这篇 Stack Overflow](https://stackoverflow.com/questions/31851611/differences-between-arm64-and-aarch64)。

至此，nocturne 容器化完成，可以通过一下命令构建并启动：

```sh
# 构建 release 版本
make

# 启动
docker compose -f prod.compose.yaml up
```

<div align="center">

| Name                   |       Size       |
| ---------------------- | :--------------: |
| postgres (unoptimized) |     630.85MB     |
| nocturne-frontend      | 3.59GB -> 361MB  |
| nocturne-backend       | 3.61GB -> 61.7MB |

*最终的 image 大小，感觉 frontend 还是有较大的优化空间的（碎碎念）

</div>

> [!NOTE]
> 顺带一提，`distroless` 并不是唯一的方案，另一个常用的方案是 `Alpine`。
>
> > A minimal Docker image based on Alpine Linux with a complete package index and only 5 MB in size!
>
> 听起来不错，但是有个小问题，它是一个基于 Alpine Linux 的方案，而 Alpine Linux 是使用的是 `musl libc`。先不说现在已知 Rust 在 musl 上有[性能](https://andygrove.io/2020/05/why-musl-extremely-slow/)和[兼容性](https://wiki.musl-libc.org/functional-differences-from-glibc.html)问题[^1]，市面上相当一部分的组件在设计的时候好像就没有这方面太多的考虑，所以为了兼容性，使用经典的 `glibc` 自然就是最稳妥的选择了。

## CI/CD

~~<正在研究方案中...>~~ *时间又向后拨几个月

从结果上来看

[^1]: <https://superuser.com/a/1820423/2021323>
[^2]: <https://en.wikipedia.org/wiki/Uname#Examples>
