'''
Shodan Url
https://www.shodan.io/search?query=title%3A%22Key%22+country%3A%22Cn%22&page=1
python shodan_key.py -u shodanUser -p shodanPasswd 
'''
import re
import urllib
import urllib2
import cookielib
import sys
import os
import string
import Queue
import ssl
import getopt
import threading
import socket
import requests
import time

p=Queue.Queue() 
c=Queue.Queue() 

def cnlist(): 
	 names=open('cnlist.txt','r') 
	 for name in names: 
		 name=name.rstrip() 
		 c.put(name) 
	
def pagelist(): 
	 passwds=open('pagelist.txt','r') 
	 for passwd in passwds: 
		 passwd=passwd.rstrip() 
		 p.put(passwd) 

k=Queue.Queue() 
cn = ["AD","AE","AF","AG","AI","AL","AM","AO","AR","AT","AU","AZ","BB","BD","BE","BF","BG","BH","BI","BJ","BL","BM","BN","BO","BR","BS","BW","BY","BZ","CA","CF","CG","CH","CK","CL","CM","CN","CO","CR","CS","CU","CY","CZ","DE","DJ","DK","DO","DZ","EC","EE","EG","ES","ET","FI","FJ","FR","GA","GB","GD","GE","GF","GH","GI","GM","GN","GR","GT","GU","GY","HK","HN","HT","HU","ID","IE","IL","IN","IQ","IR","IS","IT","JM","JO","JP","KE","KG","KH","KP","KR","KT","KW","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","MG","ML","MM","MN","MO","MS","MT","MU","MV","MW","MX","MY","MZ","NA","NE","NG","NI","NL","NO","NP","NR","NZ","OM","PA","PE","PF","PG","PH","PK","PL","PR","PT","PY","QA","RO","RU","SA","SB","SC","SD","SE","SG","SI","SK","SL","SM","SN","SO","SR","ST","SV","SY","SZ","TD","TG","TH","TJ","TM","TN","TO","TR","TT","TW","TZ","UA","UG","US","UY","UZ","VC","VE","VN","YE","YU","ZA","ZM","ZR","ZW","end"]

def scrape(text, start_trig, end_trig):
        return text.split(start_trig, 1)[-1].split(end_trig, 1)[0]
		
def getHtml(url):    
	try:           
		request_score = urllib2.Request(url, headers=headers)
		response_score = opener.open(request_score)
		b = response_score.read().decode("gb2312", 'ignore').encode("utf8")
		a = scrape(b, '<div class=\"msg alert alert-info\">', '</div>')
		if a == 'No results found':
			print a
			return None
		return b
	except urllib2.URLError, e:
		if hasattr(e, "reason"):
			string = "erry" +  str(e.reason)
			print string.encode(charaterset)
			return None

def caiji():
	try:
		#keys= "tomcat"
		content = None
		for keys in open('key.txt').read().split('\n'): 
			if keys == "end":
				return
			for c in cn:
				if c == "end":
					break
				for i in range(1,6):
					i_url="https://www.shodan.io/search?query="+keys+"+country%3A\""+ c +"\"&page="+str(i)
					try:
						request_score = urllib2.Request(i_url, headers=headers)
						response_score = opener.open(request_score)
						b = response_score.read().decode("gb2312", 'ignore').encode("utf8")
						content = getHtml(i_url)
						if not content:
							print i_url + "----erry1"
							break
						print i_url
						urls=re.findall(r"<div class=\"ip\"><a.*?href=\"(.*?)\">",b,re.I)
						for a in urls:
							f = open('netgore_url.txt','a+')
							f.write(a + '\n')
							f.close()
						time.sleep(0.1)
						
					except urllib2.URLError, e:
						time.sleep(10)
						print e.reason
						
					except:
						print "logout!"
						time.sleep(10)
						url = "https://account.shodan.io/login"
						socket.setdefaulttimeout(30)
						postData = {"username":user, "password":passwd}
						data = urllib.urlencode(postData)
						ssl._create_default_https_context = ssl._create_unverified_context
						request_new = urllib2.Request(url, headers=headers)
						response = opener.open(request_new, data)
						
	except:
			return
			
def thread():
    queue=Queue.Queue()
    netgoreurl="key.txt"
    for i in open(netgoreurl):
        queue.put(i.replace('\n',''))
    th=[]
    for hi in queue.get(block=False):
        h = threading.Thread(target=caiji,args=(queue,))
        th.append(h)
    for i in th:
        i.start()
        i.join(1)
    queue.queue.clear()
                
string = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
headers = {'User-Agent' : string}
cookie = cookielib.CookieJar()
hander = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(hander)

options,args=getopt.getopt(sys.argv[1:],'u:p:')

for name,value in options:
	if name=='-u':
		user=value
	if name=='-p':
		passwd=value

url = "https://account.shodan.io/login"
socket.setdefaulttimeout(30)
postData = {"username":user, "password":passwd}
data = urllib.urlencode(postData)
ssl._create_default_https_context = ssl._create_unverified_context
request_new = urllib2.Request(url, headers=headers)
response = opener.open(request_new, data)


caiji()
#thread()
