#!/usr/bin/env python
# coding=utf-8
from inc import run, init, output, config
import argparse, sys, time
import requests
requests.packages.urllib3.disable_warnings()

# POC bomber 控制台        参数处理和程序调用
def pocbomber_console(url_list,time_filename):  
    poc_modole_list = init.get_poc_modole_list() # 调用此函数获取 /pocs 下的全部 路径
    #[<module 'pocs.framework.flask.flask_ssti' from 'd:\\tools\.....k\\flask\\flask_ssti.py'>,...]

    # output.status_print('检测到 {0} 个目标, 已加载 {1} 条POC'.format(len(target_list), len(poc_modole_list)), 0)
    if run.verify(url_list, poc_modole_list, time_filename):   #target_list要检测的url列表，poc_modole_list所以poc列表， config.output_path输出文件路径
        pass
    else:
        output.status_print('程序异常终止', 3)
        sys.exit()
