import threading
from tkinter import E
import JSF_sj
from bs4 import BeautifulSoup
import nmap_1
import requests
import socket
import click
import re
import sys
import getopt
import time 
import os
import platform
from urllib.parse import urlparse
requests.packages.urllib3.disable_warnings()
import random

list1 = ["(*￣︿￣)\n", "凸(艹皿艹 )\n", "(＃￣～￣＃)\n", "づ￣ 3￣)づ\n", "(=￣ω￣=)\n",
         "(＠￣ー￣＠)\n", "╮(￣▽ ￣)╭\n", "(￣▽￣)～■干杯□～(￣▽￣)\n", "^(*￣(oo)￣)^\n"]

def req_url(url):   #url请求函数
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"
    }
    try:
        response = requests.get(url,headers=headers,timeout=3,verify=False)
    except requests.exceptions.ReadTimeout:
        #print(url+"  | 请求url超时！")
        return False
    except requests.exceptions.ConnectionError:
        #print(url+"  | 连接出错！")
        return False
    return response

def mu_split(file_or_url): # 将获取的url进行每一级目录拆分，并生成每一级目录的url，保存到url_list_max列表中，然后再去重
    Fingerprint_query = []
    url_list_max = []
    url_list_max2 = []   
    for url in file_or_url:       #遍历传入的url，URL_raw = urlparse(URL)
        url  = url.strip()
        if re.findall("http://",url):         #对url的请求进行判断，是http还是https，之前我一律以http发出请求，踩坑，一直报错，排查半天
            url=re.sub(r"http://",'',url)     
            catalogue = url.split("/")
            url =  "http://"+ catalogue[0]
            if url not in Fingerprint_query:
                Fingerprint_query.append(url)
            url_list_max.append(url)
            for i in range(1,len(catalogue)):     
                url += "/" + catalogue[i]
                url_list_max.append(url)
                # if url not in url_list_max:        在这里写去重不知道为什么这么写不生效，我不理解
                #     url_list_max.append(url)

        if re.findall("https://",url):
            url=re.sub(r"https://",'',url)   
            catalogue = url.split("/")
            url =  "https://"+ catalogue[0]
            if url not in Fingerprint_query:
                Fingerprint_query.append(url)    
            url_list_max.append(url)
            for i in range(1,len(catalogue)):     
                url += "/" + catalogue[i]
                url_list_max.append(url)

    for i in url_list_max:       #列表去重，会生成很多重复的url
        if i[-1] == "/":
            continue
        if i not in url_list_max2:
            url_list_max2.append(i)
    return[url_list_max2,Fingerprint_query]


def port_detection(url_list):  #端口探测
    port_die = []   #存储未开放端口
    port_survival = []  #存储存活端口
    dir_scan_list = []   #存活端口url存储
    for url in url_list:
        URL_raw = urlparse(url)
        if URL_raw.scheme+URL_raw.netloc not in port_survival and URL_raw.scheme+URL_raw.netloc not in port_die: #判断是否检测过端口存活
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                if re.findall(":",URL_raw.netloc):                #对url的端口和ip进行判断，进行存活探测
                    ip_port = URL_raw.netloc.split(":")
                    result = sock.connect_ex((ip_port[0],int(ip_port[1])))

                elif URL_raw.scheme == "https":
                    result = sock.connect_ex((URL_raw.netloc,443))

                elif URL_raw.scheme == "http":
                    result = sock.connect_ex((URL_raw.netloc,80))
            except :
                continue

            if 0 == result:                 
                dir_scan_list.append(url)
                port_survival.append(URL_raw.scheme+URL_raw.netloc)
            else:
                port_die.append(URL_raw.scheme+URL_raw.netloc)

        elif URL_raw.scheme+URL_raw.netloc in port_survival: #对检测过并存活的端口的url直接保存
            dir_scan_list.append(url)

    return dir_scan_list


def url_division(url_file,u_judge):     #判断传入的是文件还是url，然后对url分割

    if u_judge == 0:
        with open(url_file,encoding='utf-8') as url_list:
            url = mu_split(url_list)
            return [url[0],url[1]]
    elif u_judge == 1:
        url = [url_file]
        url = mu_split(url)
        return [url[0],url[1]]
  
def url_screen(dirsearch,time,dirsearch_path):  #这个函数主要是对存活主机的url进行一下筛选，将后面是文件的url去掉，只留下目录
    for url in dirsearch: 
        url2 = url
        url=re.sub(r"http://",'',url)
        url=re.sub(r"https://",'',url)   
        catalogue = url.split("/")
        if len(catalogue) == 1:    #判断最后一层目录，是文件还是目录，文件就直接舍弃，目录就直接保存到dirsearch目录下
            with open(dirsearch_path+ "urls/" +time+ ".txt", "a",encoding="utf-8") as f:
                f.write(url2+"\n")
                
        else:
            if "." not in catalogue[len(catalogue)-1] and "?" not in catalogue[len(catalogue)-1] and  "=" not in catalogue[len(catalogue)-1]:
                with open(dirsearch_path+ "urls/" +time+ ".txt", "a",encoding="utf-8") as f:
                    f.write(url2+"\n")
                    

def js_screen(page_200,time_1,js_crawling):#js爬取模块
    ji_shu = 0
    list_ltt = []
    for url in page_200:
            list_p =[]
            res = req_url(url)
            if res == False:
                continue
            html_raw = res.content.decode("utf-8", "ignore")
            html = BeautifulSoup(html_raw, "html.parser")
            if html.findAll("script"):
                if js_crawling == 1:
                    JSF_sj_r = JSF_sj.find_by_url(url)
                    js_url_p = JSF_sj_r[0]
                elif js_crawling ==2:
                    JSF_sj_r = JSF_sj.find_by_url_deep(url)
                    js_url_p = JSF_sj_r[0]
                if js_url_p:
                    for urlq in js_url_p:
                        res = req_url(urlq)
                        if res == False:
                            continue
                        if res.status_code == 200 or  res.status_code == 302 or res.status_code == 403:
                            if urlq not in list_ltt:
                                list_ltt.append(urlq)
                                ji_shu += 1
                                urlq = urlq + "         | "+str(res.status_code)+"  | 页面返回包大小"+str(len(res.content.decode("utf-8", "ignore")))
                                list_p.append(urlq)
            if list_p:
                print("\n\n================================================\n"+url + "   | 页面js爬取的内容：\n================================================")
                with open(time_1+".txt", "a",encoding="utf-8") as f:
                    f.write("\n\n================================================\n"+url + "   | 页面js爬取的内容：\n================================================\n")
                    for text in list_p:
                        print(text)
                        f.write(text+"\n")
                    if JSF_sj_r[1]:
                        f.write("\njs中爬取到的ip：\n------------------------------------------------\n")
                        print("\njs中爬取到的ip：\n------------------------------------------------\n")
                        for ip in JSF_sj_r[1]:
                            print(ip)
                            f.write(ip + "\n")
            if JSF_sj_r[1]:
                ji_shu += 1
                print("\n\n================================================\n"+url + "   | 页面js爬取的内容：\n================================================")
                with open(time_1+".txt", "a",encoding="utf-8") as f:
                    f.write("\n\n================================================\n"+url + "   | 页面js爬取的内容：\n================================================\n")
                    for ip in JSF_sj_r[1]:
                            print(ip)
                            f.write(ip + "\n")
                            
    return ji_shu

def res_title(html):  #获取title
    html = BeautifulSoup(html, "html.parser")
    html_title = html.findAll("title")
    if  html_title:
        title_text = re.findall('<title>(.+)</title>',str(html_title[0]))
        if title_text:
            return title_text[0]
        else:
            return "null"
    else:
        title_text = "null"
        return title_text

port_survival = []  #存储存活端口
port_survival_2 =[]
def survival_judgment(url):  #端口扫描主程序
    url = url.strip()
        # print(url)
    URL_raw = urlparse(url)
    # print(URL_raw)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if re.findall(":",URL_raw.netloc):                #对url的端口和ip进行判断，进行存活探测
            ip_port = URL_raw.netloc.split(":")
            if  URL_raw.scheme+"://"+URL_raw.netloc not in port_survival_2:
                port_survival_2.append(URL_raw.scheme+"://"+URL_raw.netloc)
                result = sock.connect_ex((ip_port[0],int(ip_port[1])))
                if result == 0:
                    port_survival.append(URL_raw.scheme+"://"+URL_raw.netloc)

        elif URL_raw.scheme == "https":
            if  URL_raw.scheme+"://"+URL_raw.netloc not in port_survival_2:
                port_survival_2.append(URL_raw.scheme+"://"+URL_raw.netloc)
                result = sock.connect_ex((URL_raw.netloc,443))
                if result == 0:
                    port_survival.append(URL_raw.scheme+"://"+URL_raw.netloc)


        elif URL_raw.scheme == "http":
            if  URL_raw.scheme+"://"+URL_raw.netloc not in port_survival_2:
                port_survival_2.append(URL_raw.scheme+"://"+URL_raw.netloc)
                result = sock.connect_ex((URL_raw.netloc,80))
                if result == 0:
                    port_survival.append(URL_raw.scheme+"://"+URL_raw.netloc)
                
        elif URL_raw.scheme != '' and URL_raw.path != '' :
            if URL_raw.scheme+":"+URL_raw.path not in port_survival_2:
                port_survival_2.append(URL_raw.scheme+":"+URL_raw.path)
                result = sock.connect_ex((URL_raw.scheme,int(URL_raw.path)))
                if 0 == result:               
                    port_survival.append(URL_raw.scheme+":"+URL_raw.path)
        
        elif URL_raw.path != '':
            result = 1
    except :
        pass

def survival_judgment_thread(url_list,switch):  #端口扫描30线程
    url_list_1 =[] 
    for ip in url_list:
        url_list_1.append(ip.strip())
    count = len(url_list_1)//30        #30线程跑多少次
    remainder = len(url_list_1)%30     #30的余数
    threads = []
    start = 0
    end = 30
    if count > 0:
        while count > 0:        
            for i in range(start,end):  #三十线程跑ip
            #    创建线程
                t = threading.Thread(target=survival_judgment, args=(url_list_1[i],))
                threads.append(t)
                t.start()
            [thread.join() for thread in threads]
            start += 30
            end += 30
            count -= 1
            click.secho("\n正在拼命的跑！ "+ random.choice(list1),fg='blue')
        if remainder != 0:                      #全部的ip30的余数，就不开三十个线程，最后多少个一起跑
            start =  30*count
            end = remainder + 30*count
            for i in range(start,end):
            #    创建线程
                t = threading.Thread(target=survival_judgment, args=(url_list_1[i],))
                threads.append(t)
                t.start()
            [thread.join() for thread in threads]
            click.secho("\n收工收工！ "+ random.choice(list1),fg='blue')
    else:   #当ip数量不够三十，直接有多少ip就开多少线程跑
        for ip in url_list_1:
            #    创建线程
            t = threading.Thread(target=survival_judgment, args=(ip,))
            threads.append(t)
            t.start()
        [thread.join() for thread in threads]
        click.secho("\n收工收工！ "+ random.choice(list1),fg='blue') 

    if port_survival:
        click.secho("\n\n---------------存活的端口---------------\n", fg='green')
        for ip_p in port_survival:
            click.secho(ip_p, fg='green')
    else:
        click.secho("\n------------------------------------------------\n云龙兄，咱们端口全体阵亡了!ಠ╭╮ಠ!\n------------------------------------------------\n",fg='red')

    if switch:
        if port_survival:
            click.secho("\n\n---------------加请求协议---------------\n", fg='green')
            for ip_p in port_survival:
                if re.findall("http",ip_p):
                    click.secho(ip_p, fg='green')
                else:
                    click.secho("http://"+ip_p, fg='green')

def get_scan_ip(url_list,host_detection):  #url中获取主机ip，和主机存活扫描
    host1 = []  
    for url in url_list:
        url = url.strip()
        URL_raw = urlparse(url)
        try:
            if re.findall(":",URL_raw.netloc):              
                ip_port = URL_raw.netloc.split(":")
                if ip_port[0] not in host1:
                    host1.append(ip_port[0])

            elif re.findall("http",URL_raw.scheme):
                if URL_raw.netloc not in host1:
                    host1.append(URL_raw.netloc)
            
            elif URL_raw.scheme != '' and URL_raw.path != '' :
                if URL_raw.scheme not in host1:             
                    host1.append(URL_raw.scheme)
            
            elif URL_raw.path != '':
                if URL_raw.path not in host1:
                    host1.append(URL_raw.path)
        except :
            continue
    
    if host1:
        click.secho("\n\n---------------主机ip---------------\n", fg='green')
        for ip in host1:
            click.secho(ip, fg='green')
        click.secho("\n------------------------------------\n", fg='green')
    else:
        click.secho("\n------------------------------------------------\n粗心！文件都是空的!ಠ╭╮ಠ!\n------------------------------------------------\n",fg='red')
        return

    if host_detection:
        nmap_1.nmap_host(host1)

def main():     #主函数
    click.secho('''
             _                 _
  __ _ _ __ | |_      ___ ___ | | ___  _ __  _   _   
 / _` | '_ \| __|_ _ / __/ _ \| |/ _ \| '_ \| |_| |
| (_| | | | | |_ _ _| (_| (_) | | (_) | | | |\_  /
 \__,_|_| |_|\__|    \___\___/|_|\___/|_| |_|_| |
                                            \__/
Version：1.4.0/202205220131      大雾四起\n
            ''', fg='green')

    opts, args = getopt.getopt(sys.argv[1:], "-h-t:-j-s-d-c-u:-n-o:-z-r:-p")   #传入参数
    dir_switch = 0   #dirseach
    js_crawling = 0  #js爬取
    fingerprint = 0  #指纹识别
    u_judge = 0      #单个url扫描
    nmap_switch = 0  #nmap
    ip_port_file =0  #纯端口存活探测
    http_add = 0     #增加http协议
    get_scan_ip1 = 0 #url中ip获取
    host_detection = 0 #主机存活探测是否开启


    for opt_name,opt_value in opts:
        if opt_name == "-u":
            u_judge = 1
            url_file = opt_value
            js_crawling= 2
            fingerprint = 1 
            dir_switch = 1
        if opt_name == "-n":
            nmap_switch = 1
        if opt_name == "-z":
            http_add = 1
        if opt_name == "-j":
            js_crawling = 1
        if opt_name == "-c":
            fingerprint = 1  
        if opt_name == "-s":
            js_crawling= 2
        if opt_name == "-r":
            get_scan_ip1 = opt_value
        if opt_name == "-p":
            host_detection = 1
        if opt_name == "-o":
            ip_port_file = opt_value
        if opt_name == "-t":
            url_file = opt_value
        if opt_name == "-d":
            dir_switch = 1
        if opt_name == "-h":
            print("--------------------------help--------------------------\n\n\
单个url扫描：\n\n\
    -u ： 指定url进行扫描(开启指纹探测，js深度爬取，dirsearch每层目录扫描)\n\n\
    -n ： 开启nmap扫描，暂时只支持和-u一起用，使用前需要安装nmap(使用的nmap参数为 -A -n -v)\n\n\
批量url扫描：\n\n\
    -t ： 指定存放url需要扫描的txt文件\n\n\
    -d ： 启用dirsearch扫描生成的每一层目录\n\n\
    -j ： 启用从js中爬取url和ip，会对爬取到url进行访问，如果无法连接和404会被舍弃(相比于深度爬取时间较快，看需求选择)\n\n\
    -s ： js深度爬取url和ip(-j和-s一起用的话，启用的为深度爬取)\n\n\
    -c ： 开启cms指纹扫描\n\n\
端口存活探测：\n\n\
    -o ： 指定存放ip:端口或url的文件，进行端口存活探测\n\n\
    -z ： 只可以和-o联用，可以为存活的端口增加http://,看需求选择\n\n\
主机存活探测：\n\n\
    -i ： 指定存放url的文件，可以从url中获取域名/ip并去重(主要作用为多资产为url形式，需要端口扫描，可以通过这样直接获取ip)\n\n\
    -p ： 使用nmap进行主机存活探测，只可和-i联用(但是有的主机可能会阻止我们的ping探测)\n\n\
常用命令介绍：\n\n\
    python Ant_colony.py -u https://xxx.xx/ -n    --单个url检测使用的命令，不开端口扫描就不需要-n \n\n\
    python Ant_colony.py -t url.txt               --对每个url的每一层目录进行访问，对重复返回的页面进行去重，返回页面的状态码，title和页面大小等信息 \n\n\
    python Ant_colony.py -t url.txt -s -c -d      --批量扫描，对每个url开启js深度爬取(想快一点替换为-j)，指纹识别和每层目录扫描  \n\n\
    python Ant_colony.py -o url.txt -z            --端口探测，并在存活的端口前加上http://(没有这个需求可以不加)\n\n\
    python Ant_colony.py -r url.txt               --从url中获取ip或者域名(当多资产需要端口探测时)    \n\n\
    python Ant_colony.py -r url.txt -p            --主机存活扫描(但是有的主机可能会阻止我们的ping探测)\n\n\
        ")

                

            return

    if ip_port_file:
        with open(ip_port_file,encoding='utf-8') as url_list:
            survival_judgment_thread(url_list,http_add)
        return 


    if get_scan_ip1:
        with open(get_scan_ip1,encoding='utf-8') as url_list:
            get_scan_ip(url_list,host_detection)
        return 

    url_list_return = url_division(url_file,u_judge)   #读取url，并生成
    url_list = url_list_return[0]

    # dirsearch = []    #存活主机需要dirsearch扫描的url（初筛）
    page_200 = []               #需要查看的url
    page_200_max = []           #存放200页面加数据包大小信息
    content_404_403_500 = []   #存在中间件版本泄露的url        
    page_500 = []                   #500页面的url
    page_302 = []
    page_size = {}

    for url in url_list:
        url = url.strip()    
        img_determine = ""   #截取url后缀，判定是否为图片地址
        for n in range(len(url)-1,-1,-1):
            if url[n] != "." and url[n] != "/":
                img_determine += url[n]
            else:
                break

        format_list = ["gnp","fig","gpj","oci","ssc"]    #常见图片格式和css
        if img_determine in format_list:
            print(url+"  | 图片或css地址")
            print("------------------------------------------------")
            continue


        res = req_url(url)
        if res ==False:
            continue
        res.encoding = "UTF-8"
        content = res.content.decode("utf-8", "ignore")
        statuscode = res.status_code

        if statuscode != 302  and content == "":   #除了状态码为302
                print(url+"  | "+str(statuscode) +"  | 页面返回为空")
                print("------------------------------------------------")

        elif statuscode == 404  or statuscode == 403:                #404和403页面判断是否有中间件泄露
            if re.findall("\w{1,12}/\d{1,2}\.",content):
                content_404_403_500.append(url+"  | "+str(statuscode)+"  | 可能存在中间件版本泄露！")
            else:
                print(url+"  |  "+str(statuscode) +"  | 403/404页面")
                print("------------------------------------------------")
        
        elif statuscode >= 500:          #状态码为500及其以上的，首先判断是否存在中间件版本泄露，如没有就放入列表中，后面可以在生成文件中查看
            if re.findall("\w{1,12}/\d{1,2}\.",content):
                content_404_403_500.append(url+"  | "+str(statuscode)+"  | 可能存在中间件版本泄露！")
            else:
                title_name= res_title(content)
                page_500.append(url)
                print(url+"  |  "+str(statuscode) +"  | 500页面" + "|  "+title_name)
                print("------------------------------------------------")

        elif statuscode == 302:                               
            page_302.append(url)
            print(url+"  | "+str(statuscode) +"  | 302跳转")
            # print(content)
            print("------------------------------------------------")

        elif statuscode == 200:       #存储200url并去掉同ip的回显                          
            URL_raw = urlparse(url).netloc
            try:
                qwe = page_size[URL_raw]
                list = qwe.split(",")
                st = str(len(content))
                if st not in list:
                    page_200.append(url)
                    title_name= res_title(content)
                    page_200_max.append(url+"           |  返回包大小" + str(len(content)) + "  |  "+title_name )
                    page_size[URL_raw] = qwe + ","+ st
                    print(url+"  |  "+str(statuscode) +"   |  返回包大小" + str(len(content)) + "  |  "+title_name)
                    print("------------------------------------------------")
                else:
                    print(url+"  |  "+str(statuscode) +"   |  返回包大小" + str(len(content)))
                    print("------------------------------------------------")
            except KeyError:
                title_name= res_title(content)
                page_size[URL_raw] = str(len(content))
                page_200.append(url)
                page_200_max.append(url+"           |  返回包大小" + str(len(content))  + "  |  "+title_name)
                print(url+"  |  "+str(statuscode) +"   |  返回包大小" + str(len(content)) + "  |  "+title_name)
                print("------------------------------------------------")

    time_1 = str(time.time()).split(".")[0]  #获取时间戳，生成文件,并将扫描结果保存在文件中
    time_2 = "report/"+time_1 
    if content_404_403_500:
        with open(time_2+".txt", "a",encoding="utf-8") as f:
            f.write("\n以下是404、403、500等页面可能存在中间件版本泄露：\n------------------------------------------------\n")
            for text in content_404_403_500:
                f.write(text+"\n")
            f.write("------------------------------------------------\n")

    if page_200:
        with open(time_2+".txt", "a", encoding="utf-8") as f:
            f.write("\n状态码为200的url：\n================================================\n")
            for text in page_200_max:
                f.write(text+"\n")
            f.write("================================================\n")

    
    if page_302:
        with open(time_2+".txt", "a",encoding="utf-8") as f:
            f.write("\n状态码为302的url：\n------------------------------------------------\n")
            for text in page_302:
                f.write(text+"\n")
            f.write("------------------------------------------------\n")

    if page_500:             
        with open(time_2+".txt", "a",encoding="utf-8") as f:
            f.write("\n状态码为500的url：\n------------------------------------------------\n")
            for text in page_500:
                f.write(text+"\n")
            f.write("------------------------------------------------\n\n\n\n\n")
    
    if page_200 or content_404_403_500 or page_500 or page_302:   #判断扫描结果，如果啥都没发现就不生成文件，打印下面这句话
        pass
    else:
        print("\n------------------------------------------------\n扫了个寂寞，啥都没有发现!ಠ╭╮ಠ\n------------------------------------------------\n")
    #js中的url扫描
    if js_crawling :    #开启js扫描
        print("\n\n开始js爬取：")
        with open(time_2+".txt", "a",encoding="utf-8") as f:
                    f.write("\n\njs爬取结果：")
        if js_screen(page_200,time_2,js_crawling) == 0:
            print("\n------------------------------------------------\nJS翻烂了都没看到东西!唉！ಠ╭╮ಠ\n------------------------------------------------\n")
            with open(time_2+".txt", "a",encoding="utf-8") as f:
                    f.write("\n------------------------------------------------\nJS翻烂了都没看到东西!唉!\n------------------------------------------------\n")
    
    if nmap_switch:      #开启端口探测
        print("\n\n开始端口扫描：\n")
        ip_scan = url_list_return[1]
        if len(ip_scan) == 1:
            URL_raw = urlparse(ip_scan[0]).netloc
            nmap_1.nmap_A_scan(URL_raw,time_2)
        if len(ip_scan) > 1: 
            print("目前只支持单ip端口扫描，多ip段开口扫描太过缓慢！")     
            # for ip in ip_scan:
            #     URL_raw = urlparse(ip).netloc
            #     nmap_1.nmap_A_scan(URL_raw,time_2)

    if os.path.isfile(sys.path[0]+"\\report\\"+time_1+".txt"):
        click.secho("\n\n扫描结果保存在："+sys.path[0]+"\\report\\"+time_1+".txt中\n", fg='green')
    #开启指纹探测
    if fingerprint == 1:
        print("\n\n开始指纹识别：\n")
        ip_scan = url_list_return[1]
        if len(ip_scan) > 1:  
            with open("dismap/ip/"+time_1+".txt", "a",encoding="utf-8") as f:
                for text in ip_scan:
                    f.write(text+"\n")
            os.chdir("dismap")
            if (platform.system()=='Windows'):
                os.system(r"dismap-0.3-windows-amd64.exe -f ip/"+time_1+".txt")
            elif (platform.system()=='Linux'):
                os.system(r"./dismap-0.3-linux-amd64 -f ip/"+time_1+".txt")
            else:
                os.system(r"./dismap-0.3-darwin-amd64 -f ip/"+time_1+".txt")
            os.chdir("../")
            
        elif len(ip_scan) == 1:
            os.chdir("dismap")
            if (platform.system()=='Windows'):
                os.system(r"dismap-0.3-windows-amd64.exe -u "+ ip_scan[0])
            elif (platform.system()=='Linux'):
                os.system(r"./dismap-0.3-linux-amd64  -u "+ ip_scan[0])
            else:
                os.system(r"./dismap-0.3-darwin-amd64 -u "+time_1+".txt")
            os.chdir("../")
            
        else:
            print("无可指纹探测的ip！野熊吧！")

    #调用dirsearch对生成的目录进行扫描
    if dir_switch :
        print("\n\n开始目录扫描：\n")
        dirsearch_path = "dirsearch-master/"
        url_list = port_detection(url_list)
        url_screen(url_list,time_1,dirsearch_path)     
        if  os.system(r"python "+dirsearch_path+"dirsearch.py -l " + dirsearch_path+ "urls/" +time_1+ ".txt") == 0:
            pass
        else:
            os.system(r"python3 "+dirsearch_path+"dirsearch.py -l " + dirsearch_path+ "urls/" +time_1+ ".txt")
        

if __name__ == "__main__":
    try:
        main()
    except getopt.GetoptError:
        print("传入参数错误！-h查看参数帮助！(￣(工)￣)")
    except UnboundLocalError:
        print("未输入读取文件！传入文件参数为-t！╮(￣▽ ￣)╭ 	")
    except  FileNotFoundError:
        print("有亿点小错误，文件名错误或文件内容为空！づ￣ 3￣)づ")
    except OSError:
        print("有亿点小错误，你是不是把url当文件了!(￣(工)￣)")
    except TypeError:
        print("拜拜了您嘞!⊙︿⊙")
    except KeyboardInterrupt:
        print("拜拜了您嘞!⊙︿⊙")