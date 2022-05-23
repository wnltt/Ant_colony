import threading
import click
import nmap
import random

list1 = ["(*￣︿￣)\n", "凸(艹皿艹 )\n", "(＃￣～￣＃)\n", "づ￣ 3￣)づ\n", "(=￣ω￣=)\n",
         "(＠￣ー￣＠)\n", "╮(￣▽ ￣)╭\n", "(￣▽￣)～■干杯□～(￣▽￣)\n", "^(*￣(oo)￣)^\n"]

def nmap_A_scan(network_prefix,time2):
    try:
        nm = nmap.PortScanner()
        # 配置nmap扫描参数
        scan_raw_result = nm.scan(hosts=network_prefix, arguments='-v -n -A ')
        # 分析扫描结果
        with open(time2+".txt", "a",encoding="utf-8") as f:
            f.write("\n\nnmap扫描结果：\n")
        for host, result in scan_raw_result['scan'].items():
            if result['status']['state'] == 'up':
                print('#' * 17 + 'Host:' + host + '#' * 17)
                print('-' * 20 + '操作系统猜测' + '-' * 20)
                with open(time2+".txt", "a",encoding="utf-8") as f:
                    f.write('\n'+'#' * 17 + 'Host:' + host + '#' * 17+'\n'+'-' * 20 + '操作系统猜测' + '-' * 20)
                    
        for os in result['osmatch']:
            print('操作系统为：' + os['name'] + ' ' * 3 + '准确度为：' + os['accuracy'])
            with open(time2+".txt", "a",encoding="utf-8") as f:
                f.write('\n操作系统为：' + os['name'] + ' ' * 3 + '准确度为：' + os['accuracy'])
            idno = 1    
        try:
            for port in result['tcp']:
                try:
                    print('-' * 17 + 'TCP服务器详细信息' + '[' + str(idno) + ']' + '-' * 17)
                    idno += 1
                    print('TCP端口号：' + str(port))
                    with open(time2+".txt", "a",encoding="utf-8") as f:
                        f.write('\n'+'-' * 17 + 'TCP服务器详细信息' + '[' + str(idno) + ']' + '-' * 17+'\nTCP端口号：' + str(port))
                    try:
                        print('状态：' + result['tcp'][port]['state'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n状态：' + result['tcp'][port]['state'])
                    except:
                        pass
                    try:
                        print('额外信息：' + result['tcp'][port]['extrainfo'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n额外信息：' + result['tcp'][port]['extrainfo'])
                    except:
                        pass
                    try:
                        print('名字：' + result['tcp'][port]['name'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n名字：' + result['tcp'][port]['name'])
                    except:
                        pass
                    try:
                        print('版本：' + result['tcp'][port]['version'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n版本：' + result['tcp'][port]['version'])
                    except:
                        pass
                    try:
                        print('产品：' + result['tcp'][port]['product'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n产品：' + result['tcp'][port]['product'])
                    except:
                        pass
                    try:
                        print('脚本：' + result['tcp'][port]['script'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n脚本：' + result['tcp'][port]['script'])
                    except:
                        pass
                except:
                    pass
        except:
            pass

        idno = 1
        try:
            for port in result['udp']:
                try:
                    print('-' * 17 + 'UDP服务器详细信息' + '[' + str(idno) + ']' + '-' * 17)
                    idno += 1
                    print('UDP端口号：' + str(port))
                    with open(time2+".txt", "a",encoding="utf-8") as f:
                        f.write('\n'+'-' * 17 + 'UDP服务器详细信息' + '[' + str(idno) + ']' + '-' * 17+'\nUDP端口号：' + str(port))
                    try:
                        print('状态：' + result['udp'][port]['state'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n状态：' + result['udp'][port]['state'])
                    except:
                        pass
                    try:
                        print('额外信息：' + result['udp'][port]['extrainfo'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n额外信息：' + result['udp'][port]['extrainfo'])
                    except:
                        pass
                    try:
                        print('名字：' + result['udp'][port]['name'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n名字：' + result['udp'][port]['name'])
                    except:
                        pass
                    try:
                        print('版本：' + result['udp'][port]['version'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n版本：' + result['udp'][port]['version'])
                    except:
                        pass
                    try:
                        print('产品：' + result['udp'][port]['product'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n产品：' + result['udp'][port]['product'])
                    except:
                        pass
                    try:
                        print('脚本：' + result['udp'][port]['script'])
                        with open(time2+".txt", "a",encoding="utf-8") as f:
                            f.write('\n脚本：' + result['udp'][port]['script'])
                    except:
                        pass
                except:
                    pass
        except:
                    pass
    except KeyboardInterrupt:
        print("拜拜了您嘞!⊙︿⊙")


list_ip_report = []   #主机存活的主程序
def host_survival(host):
    try:
        nm = nmap.PortScanner()
        # 配置nmap扫描参数
        scan_raw_result = nm.scan(hosts=host, arguments='-sn')
        if scan_raw_result['scan'] == {}:
            pass
        for ip in scan_raw_result['scan']:
            if  (scan_raw_result['scan'][ip]["status"]["state"]) == "up":
                list_ip_report.append(host)
            else:
                pass
            break
    except KeyboardInterrupt:
        print("拜拜了您嘞!⊙︿⊙")


def nmap_host(ip_scan):   #主机存活探测多线程
    count = len(ip_scan)//30        #30线程跑多少次
    remainder = len(ip_scan)%30     #30的余数
    threads = []
    start = 0
    end = 30
    if count > 0:
        while count > 0:        
            for i in range(start,end):  #三十线程跑ip
            #    创建线程
                t = threading.Thread(target=host_survival, args=(ip_scan[i],))
                threads.append(t)
                t.start()
            [thread.join() for thread in threads]
            start += 30
            end += 30
            count -= 1
            click.secho("\n正在拼命的跑！ "+ random.choice(list1),fg='blue')
        if remainder != 0:                      #全部的ip30的余数，就不开三十个线程，最后多少个一起跑
            start = 30*count
            end = remainder + 30*count
            for i in range(start,end):
            #    创建线程
                t = threading.Thread(target=host_survival, args=(ip_scan[i],))
                threads.append(t)
                t.start()
            [thread.join() for thread in threads]
            click.secho("\n收工收工！ "+ random.choice(list1),fg='blue')
    else:   #当ip数量不够三十，直接有多少ip就开多少线程跑
        for ip in ip_scan:
            #    创建线程
            t = threading.Thread(target=host_survival, args=(ip,))
            threads.append(t)
            t.start()
        [thread.join() for thread in threads]
        click.secho("\n收工收工！ "+ random.choice(list1),fg='blue')
    

    if list_ip_report:   #结果输出
        click.secho("\n---------------存活的主机---------------\n", fg='green')
        for ip in list_ip_report:
            click.secho(ip, fg='green')
    else:
        click.secho("\n------------------------------------------------\n一个能打的都没有!ಠ╭╮ಠ!\n------------------------------------------------\n",fg='red')


