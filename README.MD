
## 首次运行：
- pip install -r requirements.txt        
- 详细使用看 python Ant_colony.py -h

## 部分代码来源：
-https://github.com/maurosoria/dirsearch
-https://github.com/tr0uble-mAker/POC-bomber
-https://github.com/Threezh1/JSFinder
-https://github.com/yunemse48/403bypasser
根据需求对以上的项目的部分功能进行摘取和修改。


## 1.7 Update content

- 优化了输出格式
- 增加了常见漏洞扫描

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

