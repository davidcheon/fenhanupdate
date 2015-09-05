#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import urllib,urllib2,cookielib,re
import random,time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
#cj=cookielib.CookieJar()
#opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
#urllib2.install_opener(opener)
class connector(object):
	def __init__(self,opener,headers,home_url):
		self.opener=opener
		self.headers=headers
		self.loginstatus=False
		self.home_url=home_url
	def login(self,username,password):
		self.username=username
		self.password=password
		login_url=self.get_request_url()
		c=urllib2.urlopen(login_url).read()
		pat1=re.compile(r'name="formhash".*value=\'(.*?)\'')
		formhash=pat1.findall(c)[0]
		pat2=re.compile(r'action="(.*?)" ')
		act=pat2.findall(c)[0]
		act=act.replace('amp;','')
		act='http://bbs.icnkr.com/'+act
		para=urllib.urlencode({'username':self.username,
			'password':self.password,
			'formhash':formhash,
			'referer':'http://bbs.icnkr.com/forum.php?mobile=1',
			'questionid':0,
			'cookietime':2592000,
			'questionid':'0',
			'submit':'登录',
			'fastloginfield':'username',})
		req=urllib2.Request(act,para)
		reap=self.opener.open(req)
		checkpat=re.compile('messagetext.*\n<p>(.*?)</p>')
		
		mes=str(checkpat.findall(reap.read())[0])
		if mes.startswith('欢迎'):
			self.loginstatus=True
			return (True,mes)
		else:

			return (False,mes)
	def sendnewtiezi(self,typeid,subject,message,bankuaimingzi):
		if self.loginstatus:
			self.typeid=typeid
			self.subject=subject
			self.message=message
			self.bankuaimingzi=bankuaimingzi
			post_base=self.get_post_url(self.home_url,self.headers,self.opener,self.bankuaimingzi)
			result=self.opener.open(post_base)
			content=result.read()
			pat3=re.compile('action="(.*?)"')
			pub_url='http://bbs.icnkr.com/'+pat3.findall(content)[0].replace('amp;','')
			pat3=re.compile(r'name="formhash".*value="(.*?)"')
			formhash2=pat3.findall(content)[0]
			pat4=re.compile(r'name="hash" value="(.*?)"')
			hashcode=pat4.findall(content)[0]
			pat5=re.compile(r'name="uid" value="(.*?)"')
			uid=pat5.findall(content)[0]
			
			data=urllib.urlencode({'posttime':r'1440649853','typeid':r'%s'%self.typeid,'subject':r'%s'%self.subject,'formhash':r'%s'%formhash2,'message':r'%s'%self.message,'topicsubmit':r'发表帖子','uid':r'%s'%uid,'hash':r'%s'%hashcode,'type':r'image'})
			
			req2=urllib2.Request(pub_url,data)
			res2=self.opener.open(req2)
			checkpat=re.compile('messagetext.*\n<p>(.*?)</p>')
			mes=checkpat.findall(res2.read())
			if mes!=[]:
				mes=str(mes[0])
				result='%s'%mes
				self.opener.close()
				return result
			else:
				result='%s send succeed'%self.username
				self.opener.close()
				return result
			#print res2.read()
		else:
			result='%s login failed:%s'%(str(self.username),str(mes))
			self.opener.close()
			return result

	def get_request_url(self):
		opener=urllib2.build_opener()
		req=urllib2.Request(self.home_url,headers=self.headers)
		content=opener.open(req).read()
		pat=re.compile(r'<a\s*href="(.*?)"\s*title="登录"')
		url=self.home_url[:self.home_url.find('com/')+len('com/')]+pat.findall(content)[0].replace('amp;','')
		opener.close()
		return url
	def get_post_url(self,url,headers,opener,bankuaimingzi):
		req=urllib2.Request(url,headers=headers)
		content=opener.open(req).read()
		st='<a\s*href="(.*?)"\s*>%s'%bankuaimingzi
		pat=re.compile(st)
		url=url[:url.find('com/')+len('com/')]+pat.findall(content)[0].replace('amp;','')
		req=urllib2.Request(url,headers=headers)
		content=opener.open(req).read()
		
		pat2=re.compile(r'<a\s*href="(.*?)"\s*title="发帖"')
		url=url[:url.find('com/')+len('com/')]+pat2.findall(content)[0].replace('amp;','')
	
		return url
if __name__=='__main__':
	#choice=source[random.randint(0,len(source)-1)]
	#data['subject']='this is a test from %s'%choice
	#data['message']='this is just a test from %s,forgive it,sorry'%choice
	#req2=urllib2.Request(pub_url,urllib.urlencode(data))
	#res2=opener.open(req2)
	#print dir(res2)
	#res2.close()
	#time.sleep(3)
	

	headers={'User-Agent':'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
	'Content-Type':'multipart/form-data',
	'Cache-Control':'no-cache',
	'Connection':'keep-alive',
	'Accept':'*/*',}
	base_url='http://bbs.icnkr.com/forum.php?mobile=1'
	url_request=get_request_url(base_url,headers)
	#post_base='http://bbs.icnkr.com/forum.php?mod=post&action=newthread&fid=137&mobile=yes'
	users=['testuser','1960772215']
	passwords=['******','*****']
	messages=['发表帖子1','发表帖子2','我想要找工作']
	subjects=['发表帖子1','发表帖子2','求职男']

	for n in xrange(1):
		cj=cookielib.CookieJar()
		opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		index=random.randint(0,len(users)-1)
		#typeid=random.randint(193,291)
		typeid=53
		sindex=random.randint(0,len(messages)-1)
		autosend(url_request,opener,users[1],passwords[1],typeid,subjects[sindex],messages[sindex],headers,base_url,'交友频道-친구')
		time.sleep(10)
