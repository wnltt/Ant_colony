# Ant Colony 蚁群

![python3.x](https://img.shields.io/badge/language-python3-brightgreen.svg?style=plastic)
![Tools-AntColony](https://img.shields.io/badge/Tools-AntColony-brightgreen.svg?style=plastic)

![](./6.ico)

基于特殊场景下的路由爆破工具，具体应用场景需拿到大量资产，针对该系统资产下多个路由批量跑字典，`Ant Colony`应运而生。

## 首次运行：
- `pip install -r requirements.txt`
- 详细使用看 `python Ant_colony.py -h`:

```bash

             _                 _
  __ _ _ __ | |_      ___ ___ | | ___  _ __  _   _
 / _` | '_ \| __|_ _ / __/ _ \| |/ _ \| '_ \| |_| |
| (_| | | | | |_ _ _| (_| (_) | | (_) | | | |\_  /
 \__,_|_| |_|\__|    \___\___/|_|\___/|_| |_|_| |
                                            \__/
Version：1.7.0/202206080512      大雾四起


--------------------------help--------------------------

单个url扫描：

    -u ： 指定url进行扫描(js深度爬取，dirsearch每层目录扫描,403bypass,漏洞扫描)

批量url扫描：

    -t ： 指定存放url需要扫描的txt文件

    -d ： 启用dirsearch扫描生成的每一层目录

    -j ： 启用从js中爬取url和ip(相比于深度爬取时间较快)

    -s ： js深度爬取url和ip

    -p ： 常见漏洞扫描

端口存活探测：

    -o ： 指定存放ip:端口或url的文件，进行端口存活探测

    -z ： 只可以和-o联用，可以为存活的端口增加http://,看需求选择

主机存活探测：

    -i ： 指定存放url的文件，可以从url中获取域名/ip并去重(主要作用为多资产为url形式，需要端口扫描)

403bypass:

    -b ： -u和-t默认开启对403bypass(js爬取到的403页面也会进行bypass尝试)，当-u和-t与-b特殊指定则只开启403bypass不进行其他操作

常用命令介绍：

    python Ant_colony.py -u https://xxx.xx/       --单个url检测使用的命令

    python Ant_colony.py -t url.txt               --对每个url的每一层目录进行访问，对重复返回的页面进行去重，返回页面的状态码，title和页面大小等信息

    python Ant_colony.py -t url.txt -s -d -p      --批量扫描，对每个url开启js深度爬取(想快一点替换为-j)，漏洞扫描和每层目录扫描(每个参数均可单独使用)

    python Ant_colony.py -o url.txt -z            --端口探测，并在存活的端口前加上http://(没有这个需求可以不加)

    python Ant_colony.py -r url.txt               --从url中获取ip或者域名(当多资产需要端口探测时)

    python Ant_colony.py -u https://xxx.xx/ -b    --对403页面进行bypass，只进行该操作

    python Ant_colony.py -t url.txt -b            --对文件中的403页面进行bypass，只进行该操作
```

## 部分代码来源：
- https://github.com/maurosoria/dirsearch
- https://github.com/tr0uble-mAker/POC-bomber
- https://github.com/Threezh1/JSFinder
- https://github.com/yunemse48/403bypasser
- 根据需求对以上的项目的部分功能进行摘取和修改。

## 主要功能：
- 批量对资产进行访问，返回可以正常访问的页面的大小，状态码，title等信息
- 批量对资产的，每层目录进行目录探测
- 批量对资产进行js中url爬取并访问，返回可以访问的url和页面大小信息，403页面的bypass，常见漏洞扫描
- 以上功能也支持-u单个检测

## 1.7 Update content

- 优化了输出格式
- 增加了常见漏洞扫描
- 更新poc库可以直接去[POC-bomber](https://github.com/tr0uble-mAker/POC-bomber)，将最新的poc文件夹，覆盖进来

## 1.6 Update content

- 修复js爬取爬到外站的ip格式
- 取消了-t的不必要输出
- 增加403bypass，对输入的403页面和js爬取到的403页面，进行bypass尝试，也可单独使用该功能

## 1.5 Update content

- 修复js爬取为空报错
- 增加js爬取到ip的js文件的url显示


## Completed

- 取消`-c`，探测中访问request超时会导致脚本错误，实际错误为运行目录不正确；
- python3环境判断；
  - mac
  - linux
  - windows
- 探测超时；优化探测存活思路；


## TODO List

- 后续会增加常见通用漏洞的漏洞检测
- [ ] 减少仓库占用
  - [x] `pocs/framework/shiro` 下jar包删除；
  - [ ] `.git`文件夹
