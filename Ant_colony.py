import JSF_sj
from bs4 import BeautifulSoup
import requests
import re
import sys
import getopt
import time
import os
from urllib.parse import urlparse

requests.packages.urllib3.disable_warnings()


def req_url(url):  # url请求函数
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=3, verify=False)
    except requests.exceptions.ReadTimeout:
        # print(url+"  | 请求url超时！")
        return False
    except requests.exceptions.ConnectionError:
        # print(url+"  | 连接出错！")
        return False
    return response


def mu_split(file_or_url):
    Fingerprint_query = []
    url_list_max = []
    url_list_max2 = []
    for url in file_or_url:  # 遍历传入的url
        url = url.strip()
        if re.findall("http://", url):  # 对url的请求进行判断，是http还是https，之前我一律以http发出请求，踩坑，一直报错，排查半天
            url = re.sub(r"http://", '', url)
            catalogue = url.split("/")
            url = "http://" + catalogue[0]
            if url not in Fingerprint_query:
                Fingerprint_query.append(url)
            url_list_max.append(url)
            for i in range(1, len(catalogue)):
                url += "/" + catalogue[i]
                url_list_max.append(url)
                # if url not in url_list_max:        在这里写去重不知道为什么这么写不生效，我不理解
                #     url_list_max.append(url)

        if re.findall("https://", url):
            url = re.sub(r"https://", '', url)
            catalogue = url.split("/")
            url = "https://" + catalogue[0]
            if url not in Fingerprint_query:
                Fingerprint_query.append(url)
            url_list_max.append(url)
            for i in range(1, len(catalogue)):
                url += "/" + catalogue[i]
                url_list_max.append(url)

    for i in url_list_max:  # 列表去重，会生成很多重复的url
        if i[-1] == "/":
            continue
        if i not in url_list_max2:
            url_list_max2.append(i)
    return [url_list_max2, Fingerprint_query]


def url_division(url_file, u_judge):  # 将获取的url进行每一级目录拆分，并生成每一级目录的url，保存到url_list_max列表中，然后再去重

    if u_judge == 0:
        with open(url_file, encoding='utf-8') as url_list:
            url = mu_split(url_list)
            return [url[0], url[1]]
    elif u_judge == 1:
        url = [url_file]
        url = mu_split(url)
        return [url[0], url[1]]


def url_screen(dirsearch, time, dirsearch_path):
    # 这个函数主要是对存活主机的url进行一下筛选，将后面是文件的url去掉，只留下目录
    for url in dirsearch:
        url2 = url
        url = re.sub(r"http://", '', url)
        url = re.sub(r"https://", '', url)
        catalogue = url.split("/")
        if len(catalogue) == 1:  # 判断最后一层目录，是文件还是目录，文件就直接舍弃，目录就直接保存到dirsearch目录下
            with open(dirsearch_path + "urls/" + time + ".txt", "a", encoding="utf-8") as f:
                f.write(url2 + "\n")

        else:
            if "." not in catalogue[len(catalogue) - 1] and "?" not in catalogue[len(catalogue) - 1] and "=" not in \
                    catalogue[len(catalogue) - 1]:
                with open(dirsearch_path + "urls/" + time + ".txt", "a", encoding="utf-8") as f:
                    f.write(url2 + "\n")


def js_screen(page_200, time_1, js_crawling):
    ji_shu = 0
    list_ltt = []
    for url in page_200:
        list_p = []
        res = req_url(url)
        if res == False:
            continue
        html_raw = res.content.decode("utf-8", "ignore")
        html = BeautifulSoup(html_raw, "html.parser")
        if html.findAll("script"):
            if js_crawling == 1:
                js_url_p = JSF_sj.find_by_url(url)
            elif js_crawling == 2:
                js_url_p = JSF_sj.find_by_url_deep(url)
            if js_url_p:
                for urlq in js_url_p:
                    res = req_url(urlq)
                    if res == False:
                        continue
                    if res.status_code == 200 or res.status_code == 302 or res.status_code == 403:
                        if urlq not in list_ltt:
                            list_ltt.append(urlq)
                            ji_shu += 1
                            urlq = urlq + "         | " + str(res.status_code) + "  | 页面返回包大小" + str(
                                len(res.content.decode("utf-8", "ignore")))
                            list_p.append(urlq)
        if list_p:
            print(
                "\n\n-----------------------------------------------------\n" + url + "   | 页面js爬取的内容：\n-----------------------------------------------------")
            with open(time_1 + ".txt", "a", encoding="utf-8") as f:
                f.write(
                    "\n\n-----------------------------------------------------\n" + url + "   | 页面js爬取的内容：\n-----------------------------------------------------\n")
                for text in list_p:
                    print(text)
                    f.write(text + "\n")
    return ji_shu


def main():  # 主函数
    print('''
             _                 _
  __ _ _ __ | |_      ___ ___ | | ___  _ __  _   _   
 / _` | '_ \| __|_ _ / __/ _ \| |/ _ \| '_ \| |_| |
| (_| | | | | |_ _ _| (_| (_) | | (_) | | | |\_  /
 \__,_|_| |_|\__|    \___\___/|_|\___/|_| |_|_| |
                                            \__/
Version：1.3.0/st\n       
            ''')

    opts, args = getopt.getopt(sys.argv[1:], "-h-t:-j-s-d-c-u:")  # 传入参数
    dir_switch = 0
    js_crawling = 0
    fingerprint = 0
    u_judge = 0

    for opt_name, opt_value in opts:
        if opt_name == "-u":
            u_judge = 1
            url_file = opt_value
            js_crawling = 2
            fingerprint = 1
            dir_switch = 1
        if opt_name == "-j":
            js_crawling = 1
        if opt_name == "-c":
            fingerprint = 1
        if opt_name == "-s":
            js_crawling = 2
        if opt_name == "-t":
            url_file = opt_value
        if opt_name == "-d":
            dir_switch = 1
        if opt_name == "-h":
            print(
                "--------------------------help--------------------------\n\n-t ： 指定存放url需要扫描的txt文件\n\n-u ： 指定url进行扫描(开启指纹探测，js深度爬取，dirsearch扫描)\n\n-d ： 启用dirsearch扫描生成的目录(无需参数，默认不启动)\n\n-j ： 启用从js中爬取url\n\n-s ： js深度爬取url(-j和-s一起用的话，启用的为深度爬取)\n\n-c ： 开启cms指纹扫描\n")
            return

    url_list_return = url_division(url_file, u_judge)  # 读取url，并生成
    url_list = url_list_return[0]

    dirsearch = []  # 存活主机需要dirsearch扫描的url（初筛）
    page_200 = []  # 需要查看的url
    page_200_max = []  # 存放200页面加数据包大小信息
    content_404_403_500 = []  # 存在中间件版本泄露的url
    page_500 = []  # 500页面的url
    page_302 = []
    page_size = {}
    for url in url_list:
        url = url.strip()
        img_determine = ""  # 截取url后缀，判定是否为图片地址，如果是就视为正常，css也视为正常
        for n in range(len(url) - 1, -1, -1):
            if url[n] != "." and url[n] != "/":
                img_determine += url[n]
            else:
                break

        format_list = ["gnp", "fig", "gpj", "oci", "ssc"]  # 常见图片格式和css
        if img_determine in format_list:
            print(url + "  | 正常")
            print("------------------------------------------------")
            continue

        res = req_url(url)
        if res == False:
            continue
        res.encoding = "UTF-8"
        content = res.content.decode("utf-8", "ignore")
        statuscode = res.status_code
        dirsearch.append(url)

        if statuscode != 302 and content == "":  # 除了状态码为302，的其余返回页面为空的视为正常
            print(url + "  | " + str(statuscode) + "  | 页面返回为空")
            print("------------------------------------------------")

        elif statuscode == 404 or statuscode == 403:  # 404和403页面判断是否有中间件泄露的风险，无的话视为安全，若有存入content_404列表，最后保存进文件
            if re.findall("\w{1,12}/\d{1,2}\.", content):
                content_404_403_500.append(url + "  | " + str(statuscode) + "  | 存在中间件信息泄露！")
            else:
                print(url + "  | " + str(statuscode) + "  | 403/404页面")
                print("------------------------------------------------")

        elif statuscode >= 500:  # 状态码为500及其以上的，首先判断是否存在中间件版本泄露，如没有就放入列表中，后面可以在生成文件中查看
            if re.findall("\w{1,12}/\d{1,2}\.", content):
                content_404_403_500.append(url + "  | " + str(statuscode) + "  | 存在中间件信息泄露！")
            else:
                page_500.append(url)
                print(url + "  | " + str(statuscode) + "  | 500页面")
                print("------------------------------------------------")

        elif statuscode == 302:
            page_302.append(url)
            print(url + "  | " + str(statuscode) + "  | 302跳转")
            # print(content)
            print("------------------------------------------------")

        elif statuscode == 200:
            URL_raw = urlparse(url).netloc
            try:
                qwe = page_size[URL_raw]
                list = qwe.split(",")
                st = str(len(content))
                if st not in list:
                    page_200.append(url)
                    page_200_max.append(url + "           | 返回包大小" + str(len(content)))
                    page_size[URL_raw] = qwe + "," + st
                    print(url + "  | " + str(statuscode) + "    | 返回包大小" + str(len(content)))
                    print("------------------------------------------------")
                else:
                    print(url + "  | " + str(statuscode) + "    | 返回包大小" + str(len(content)))
                    print("------------------------------------------------")
            except KeyError:
                page_size[URL_raw] = str(len(content))
                page_200.append(url)
                page_200_max.append(url + "           | 返回包大小" + str(len(content)))
                print(url + "  | " + str(statuscode) + "    | 返回包大小" + str(len(content)))
                print("------------------------------------------------")

    time_1 = str(time.time()).split(".")[0]  # 获取时间戳，生成文件,并将扫描结果保存在文件中
    time_2 = "report/" + time_1
    if content_404_403_500:
        with open(time_2 + ".txt", "a", encoding="utf-8") as f:
            f.write("\n以下是404、403、500等页面存在中间件版本泄露：\n------------------------------------------------\n")
            for text in content_404_403_500:
                f.write(text + "\n")
            f.write("------------------------------------------------\n")

    if page_200:
        with open(time_2 + ".txt", "a", encoding="utf-8") as f:
            f.write("\n状态码为200的url：\n================================================\n快速查看(含返回包大小等信息)：\n")
            for text in page_200_max:
                f.write(text + "\n")
            f.write("================================================\n")

    if page_302:
        with open(time_2 + ".txt", "a", encoding="utf-8") as f:
            f.write("\n状态码为200的url：\n------------------------------------------------\n")
            for text in page_302:
                f.write(text + "\n")
            f.write("------------------------------------------------\n")

    if page_500:
        with open(time_2 + ".txt", "a", encoding="utf-8") as f:
            f.write("\n状态码为500的url：\n------------------------------------------------\n")
            for text in page_500:
                f.write(text + "\n")
            f.write("------------------------------------------------\n\n\n\n\n")

    if page_200 or content_404_403_500 or page_500 or page_302:  # 判断扫描结果，如果啥都没发现就不生成文件，打印下面这句话
        pass
    else:
        print(
            "\n------------------------------------------------\n扫了个寂寞，啥都没有发现!ಠ╭╮ಠ\n------------------------------------------------\n")
    # js中的url扫描
    if js_crawling:  # 开启js扫描
        print("\n\n开始js爬取：")
        with open(time_2 + ".txt", "a", encoding="utf-8") as f:
            f.write("\n\njs爬取结果：")
        if js_screen(page_200, time_2, js_crawling) == 0:
            print(
                "\n------------------------------------------------\nJS翻烂了都没看到东西!唉！ಠ╭╮ಠ\n------------------------------------------------\n")
            with open(time_2 + ".txt", "a", encoding="utf-8") as f:
                f.write(
                    "\n------------------------------------------------\nJS翻烂了都没看到东西!唉!\n------------------------------------------------\n")

    # 开启指纹探测
    if fingerprint == 1:
        ip_scan = url_list_return[1]
        if len(ip_scan) > 1:
            with open("dismap/ip/" + time_1 + ".txt", "a", encoding="utf-8") as f:
                for text in ip_scan:
                    f.write(text + "\n")
            os.chdir("dismap")
            #os.system(r"dismap-0.3-windows-amd64.exe -f ip/" + time_1 + ".txt")
            os.system(r"./dismap-0.3-linux-amd64 -f "+time_1+".txt")
        elif len(ip_scan) == 1:
            os.chdir("dismap")
            # os.system(r"dismap-0.3-windows-amd64.exe -u " + ip_scan[0])
            os.system(r"./dismap-0.3-linux-amd64  -u "+ ip_scan[0])
        else:
            print("无可指纹探测的ip！野熊吧！")

    # 调用dirsearch对生成的目录进行扫描
    if dir_switch:
        os.chdir("../")
        dirsearch_path = "dirsearch-master/"
        url_screen(dirsearch, time_1, dirsearch_path)
        print("python3 " + dirsearch_path + "dirsearch.py -l " + dirsearch_path + "urls/" + time_1 + ".txt")
        # os.system(r"python3 "+dirsearch_path+"dirsearch.py -l " + dirsearch_path+ "urls/" +time_1+ ".txt")      #调用dirsearch对筛选出来的url进行目录扫描


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
    except KeyboardInterrupt:
        print("拜拜了您嘞!⊙︿⊙")
