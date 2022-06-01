import requests, re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from yarl import URL
requests.packages.urllib3.disable_warnings()

def Extract_html(URL):    #请求函数
	header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36"}
	try:
		raw = requests.get(URL, headers = header, timeout=3, verify=False)
		raw0 = raw.content.decode("utf-8", "ignore")
		raw1 = raw.status_code
		return [raw0,raw1]
	except KeyboardInterrupt:
		pass
	except:
		return ["flase","flase"]

def extract_URL(JS):   #正则匹配函数
	pattern_raw = r"""
	  (?:"|')                               # Start newline delimiter
	  (
	    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
	    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
	    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path
	    |
	    ((?:/|\.\./|\./)                    # Start with /,../,./
	    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
	    [^"'><,;|()]{1,})                   # Rest of the characters can't be
	    |
	    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
	    [a-zA-Z0-9_\-/]{1,}                 # Resource name
	    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
	    (?:[\?|/][^"|']{0,}|))              # ? mark with parameters
	    |
	    ([a-zA-Z0-9_\-]{1,}                 # filename
	    \.(?:php|asp|aspx|jsp|json|
	         action|html|js|txt|xml)             # . + extension
	    (?:\?[^"|']{0,}|))                  # ? mark with parameters
	  )
	  (?:"|')                               # End newline delimiter
	"""
	pattern = re.compile(pattern_raw, re.VERBOSE)
	result = re.finditer(pattern, str(JS))
	if result == None:
		return None
	js_url = []
	return [match.group().strip('"').strip("'") for match in result
		if match.group() not in js_url]

list_ip = []
url_ip_list={}
def ip_crawling(js,url2):
    ip_r = re.findall("(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)(:[0-9]{1,5}){0,1}",js)
    if ip_r:
        url = re.split("!@xkeyx@!",js)[1]
        for ip in ip_r:
            if ip[4] != '':
                ip = ip[0]+"."+ip[1]+"."+ip[2]+"."+ip[3]+ip[4]
                if re.findall(list_ip[0],ip):
                    pass
                else:
                    if ip not in list_ip:
                        list_ip.append(ip)
                        if dns_judge([url],url2):
                            try:
                                d_value = url_ip_list[url] 
                                d_value = d_value+","+ip
                                url_ip_list[url] = d_value
                            except KeyError:
                                url_ip_list[url] = ip
	
            else:
                ip = ip[0]+"."+ip[1]+"."+ip[2]+"."+ip[3] 
                if re.findall(list_ip[0],ip):
                    pass
                else:                           
                    if ip not in list_ip:
                        list_ip.append(ip)
                        if dns_judge([url],url2):
                            try:
                                d_value = url_ip_list[url] 
                                d_value = d_value+","+ip
                                url_ip_list[url] = d_value
                            except KeyError:
                                url_ip_list[url] = ip


def find_last(string,str):     #匹配域名中点的位置并保存成一个列表返回
	positions = []
	last_position=-1
	while True:
		# position = string.find(str,last_position+1)
		position = string.find(str,last_position+1)
		if position == -1:break
		last_position = position
		positions.append(position)
	return positions

def process_url(URL, re_URL):   #对从页面获取的src信息，进行加工，生成完整的可访问的地址

	black_url = ["javascript:"]	# Add some keyword for filter url.
	URL_raw = urlparse(URL)

	ab_URL = URL_raw.netloc   #(scheme='https', netloc='www.baidu.com', path='/adsdsda/index.html', params='user', query='id=5', fragment='comment') 获取域名信息
									#获取域名信息  将获取的url获取域名
	host_URL = URL_raw.scheme    #获取请求协议

	if re_URL[0:2] == "//":     #判断是否有请求协议如果没有请求协议加上请求协议
		result = host_URL  + ":" + re_URL
	elif re_URL[0:7] == "http://": 
		result = re_URL
	elif re_URL[0:8] == "https://": 
		result = re_URL
	elif re_URL[0:2] != "//" and re_URL not in black_url:  #排除//和javascript:，判断单/,那么判断是域名后面的目录，进行拼接生成url
		if re_URL[0:1] == "/":
			result = host_URL + "://" + ab_URL + re_URL
		else:
			if re_URL[0:1] == ".":
				if re_URL[0:2] == "..":
					result = host_URL + "://" + ab_URL + re_URL[2:]
				else:
					result = host_URL + "://" + ab_URL + re_URL[1:]
			else:
				result = host_URL + "://" + ab_URL + "/" + re_URL
	else:
		result = URL
	return result

def dns_judge(allurls,url):   #判断是不是所属域名
    result = []
    for singerurl in allurls:  #对获取并二次加工的url进行遍历
        url_raw = urlparse(url)  
        domain = url_raw.netloc   #获取最开始访问的域名

        positions = find_last(domain, ".")   #调用函数，匹配域名中点的位置并保存成一个列表返回

        miandomain = domain
        if len(positions) > 1:    #获取顶级域名
            miandomain = domain[positions[-2] + 1:]
            if re.findall(":",miandomain):
                miandomain = miandomain.split(":")[0]
        suburl = urlparse(singerurl)
        subdomain = suburl.netloc
        #print(singerurl)
        if miandomain in subdomain or subdomain.strip() == "":  
            if singerurl.strip() not in result:
                result.append(singerurl)
    	
    return result

def find_by_url(url,js_crawling):
    if js_crawling ==1:
        global list_ip
        list_ip = []
        global url_ip_list
        url_ip_list={}
    if js_crawling == 1:
        Native_IP = urlparse(url)
        ip = Native_IP.netloc
        if re.findall(':',ip):
            ip = re.split(":",ip)[0]
        list_ip.append(ip)
    html_raw = Extract_html(url)[0]    #获取页面的html文本信息

    if html_raw == "flase" and  html_raw:         #如果页面没有东西为空返回none
        return None
        
    #print(html_raw)
    html = BeautifulSoup(html_raw, "html.parser") #使用bs4.BeautifulSoup()方法，解析Response 对象
    html_scripts = html.findAll("script")    #获取所有script标签和文本内容,并分割成列表
    script_array = {}
    script_temp = ""
    for html_script in html_scripts:
        script_src = html_script.get("src")   #获取src的标签值
        if script_src == None:         
            script_temp += html_script.get_text() + "\n" #如果src没有值，去除html所有html标签获取文本信息
        else:
            purl = process_url(url, script_src)    #对获取的url二次加工，生成可使用的地址
            st = Extract_html(purl)[0] 
            if st  != "flase" and  st:
                script_array[purl] = Extract_html(purl)[0]+"!@xkeyx@!"+purl #对处理的url，进行请求获取页面 ,保存在字典中，对应的url保存对应请求返回的文本
    script_array[url] = script_temp+"!@xkeyx@!"+ url  

    allurls = []
    for script in script_array:   #script是字典的键
        #print(script)
        temp_urls = extract_URL(script_array[script])   #将对应url的内容传入，进行正则匹配
        ip_crawling(script_array[script],url)
        if len(temp_urls) == 0: continue    #如果没有匹配到东西直接跳过本轮循环

        for temp_url in temp_urls:     #对从js文件里面匹配到的url进行遍历保存，保存前还是对获取的url进行加工，并保存到 allurls = []
            allurls.append(process_url(script, temp_url)) 

    a = dns_judge(allurls,url)
    return  [a,url_ip_list]


def find_by_url_deep(url,js_crawling): #深度爬取,从这开始入手
	global list_ip
	list_ip = []
	global url_ip_list
	url_ip_list={}
	if js_crawling == 2:
		Native_IP = urlparse(url)
		ip = Native_IP.netloc
		if re.findall(':',ip):
			ip = re.split(":",ip)[0]
		list_ip.append(ip)
	res = find_by_url(url,js_crawling)
	if res != None:
		result_main = res
	else:
		return None
	html_raw = Extract_html(url)[0]  #请求url
	if html_raw == "flase" and html_raw :  
		return None
	html = BeautifulSoup(html_raw, "html.parser") 
	html_as = html.findAll("a") #获取所有a标签和文本内容,并分割成列表
	if html_as == []:
		return result_main
	links = []    
	for html_a in html_as: 
		src = html_a.get("href") #获取超链接标签值
		if src == "" or src == None: continue
		link = process_url(url, src) #对获取的url进行加工
		if link not in links: #获取链接去重
			links.append(link)
	if links == []: return result_main
	
	urls = []
	# i = len(links)
	for link in links:
		link1 = [link]
		if  dns_judge(link1,url):
			pass
		else:
			continue
		temp_urls = find_by_url(link,js_crawling)
		if temp_urls == None: continue
		if temp_urls[0] == []: continue
		# print("Remaining " + str(i) + " | Find " + str(len(temp_urls)) + " URL in " + link)
		for temp_url in temp_urls[0]:
			if temp_url[-1] == "/":
				temp_url = temp_url[::-1].replace('/','', 1)[::-1]
			if temp_url not in urls:
				urls.append(temp_url)
		# i -= 1
	for url12 in result_main[0]:
		if url12: 
			if url12[-1] == "/":
				url12 = url12[::-1].replace('/','', 1)[::-1]
			if url12 not in urls:
				urls.append(url12)

	return [urls,url_ip_list]
	