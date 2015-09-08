#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import wx
from wx.lib.pubsub import Publisher
import cookielib
import urllib2
import threading
import time,sys
import test3
import mygauge
class mygui(wx.Frame):
	def __init__(self,headers,img):
		wx.Frame.__init__(self,None,title='奋韩')
		self.tiezi_selection=0
		self.item=None
		self.headers=headers
		self.tmp=img.ConvertToBitmap()
		self.SetSizeHintsSz((500,600),(500,600))
		panel=wx.Panel(self)
		self.panel=panel
		self.Bind(wx.EVT_CLOSE,self.closeaction)
		self.status_label=wx.StaticText(panel,label='status')
		self.gaua=wx.Gauge(panel,-1,20,pos=(220,85),size=(250,20))
		self.sitename_label=wx.StaticText(panel,label='website')
		self.sitename=wx.TextCtrl(panel,value='http://bbs.icnkr.com/forum.php?mobile=1',style=wx.TE_READONLY)
		self.username_label=wx.StaticText(panel,label='username')
		self.username=wx.TextCtrl(panel)
		self.username.SetFocus()
		self.password_label=wx.StaticText(panel,label='password')
		self.password=wx.TextCtrl(panel,style=wx.TE_PASSWORD)
		self.loginbutton=wx.Button(panel,label='login')
		self.loginbutton.Bind(wx.EVT_BUTTON,self.loginaction)
		self.exitbutton=wx.Button(panel,label='exit')
		self.exitbutton.Bind(wx.EVT_BUTTON,self.exitaction)
		self.bankuai=['招聘求职','交友频道-친구','美丽人生|婚姻|育儿']
		self.bankuai_label=wx.StaticText(panel,label='bankuai:')
		self.bankuai_choice=wx.ComboBox(panel,-1,"Default Value",(15,30),wx.DefaultSize,self.bankuai,wx.CB_DROPDOWN)
		self.bankuai_choice.Bind(wx.EVT_COMBOBOX,self.selectbankuai)
		diyu=[]
		self.diyu_label=wx.StaticText(panel,label='diyu:')
		self.diyu_choice=wx.ComboBox(panel,-1,"Default Value",(15,30),wx.DefaultSize,diyu,wx.CB_DROPDOWN)
		self.diyu_choice.Bind(wx.EVT_COMBOBOX,self.selectdiyu)
		self.subject_label=wx.StaticText(panel,label='subject')
		self.subject=wx.TextCtrl(panel)
		self.content_label=wx.StaticText(panel,label='content')
		self.content=wx.TextCtrl(panel,style=wx.TE_MULTILINE|wx.VSCROLL)
		self.sendbutton=wx.BitmapButton(panel,id=-1,bitmap=self.tmp,name='send',size=(250,50),style=0)
		self.sendbutton.SetDefault()
		self.sendbutton.Bind(wx.EVT_BUTTON,self.sendaction)
		self.sendbutton.Disable()
		self.tiezilist=wx.ListBox(panel,26,size=(150,100),pos=wx.DefaultPosition,choices=[],style=wx.LB_SINGLE)
		self.tiezilist.Bind(wx.EVT_LISTBOX,self.tieziselection)
		self.tiezicontent=wx.TextCtrl(panel,style=wx.TE_MULTILINE|wx.VSCROLL|wx.HSCROLL)
		self.tiezireply=wx.TextCtrl(panel,style=wx.TE_MULTILINE|wx.VSCROLL)
		self.tiezideletebutton=wx.Button(panel,label='refresh')
		self.tiezideletebutton.Bind(wx.EVT_BUTTON,self.refreshtiezi)
		self.tiezideletebutton.Disable()
		self.tiezireplybutton=wx.Button(panel,label='send')
		self.tiezireplybutton.Bind(wx.EVT_BUTTON,self.sendreply)
		self.tiezireplybutton.Disable()
		self.hbox1=wx.BoxSizer()
		self.hbox1.Add(self.sitename_label,proportion=1,flag=wx.EXPAND|wx.ALL,border=0)
		self.hbox1.Add(self.sitename,proportion=7,flag=wx.EXPAND|wx.ALL,border=0)
		self.hbox2=wx.BoxSizer()
		self.hbox2.Add(self.username_label,proportion=1,flag=wx.EXPAND|wx.ALL,border=0)
		self.hbox2.Add(self.username,proportion=5,flag=wx.EXPAND|wx.ALL,border=0)
		self.hbox3=wx.BoxSizer()
		self.hbox3.Add(self.password_label,proportion=1,flag=wx.EXPAND|wx.ALL,border=0)
		self.hbox3.Add(self.password,proportion=6,flag=wx.EXPAND|wx.ALL,border=0)
		self.hbox4=wx.BoxSizer()
		self.hbox4.Add(self.bankuai_label,proportion=0,flag=wx.EXPAND,border=0)
		self.hbox4.Add(self.bankuai_choice,proportion=2,flag=wx.EXPAND,border=0)
		self.hbox4.Add(self.diyu_label,proportion=0,flag=wx.EXPAND,border=0)
		self.hbox4.Add(self.diyu_choice,proportion=2,flag=wx.EXPAND,border=0)
		self.hbox5=wx.BoxSizer()
		self.hbox5.Add(self.subject_label,proportion=1,border=0)
		self.hbox5.Add(self.subject,proportion=8,flag=wx.ALL|wx.EXPAND|wx.RIGHT,border=0)
		self.hbox6=wx.BoxSizer()
		self.hbox6.Add(self.content_label,proportion=1,border=0)
		self.hbox6.Add(self.content,proportion=7,flag=wx.EXPAND|wx.ALL|wx.ALIGN_CENTER,border=0)
		self.hbox7=wx.BoxSizer()
		self.tmp=img.ConvertToBitmap()
		self.hbox7.Add(self.sendbutton,proportion=5,flag=wx.EXPAND|wx.ALL,border=0)
		self.hbox8=wx.BoxSizer()
		self.tiezilist_label=wx.StaticText(panel,label='tiezis')
		self.hbox8.Add(self.tiezilist_label,proportion=1)
		self.hbox8.Add(self.tiezilist,proportion=5,flag=wx.EXPAND|wx.ALL,border=0)
		self.hbox9=wx.BoxSizer()
		self.tiezicontent_label=wx.StaticText(panel,label='content')
		self.hbox9.Add(self.tiezicontent_label,proportion=1)
		self.hbox9.Add(self.tiezicontent,proportion=5,flag=wx.EXPAND|wx.ALL,border=0)
		self.hbox10=wx.BoxSizer()
		self.tiezireply_label=wx.StaticText(panel,label='reply')
		self.hbox10.Add(self.tiezireply_label,proportion=1)
		self.hbox10.Add(self.tiezireply,proportion=5,flag=wx.EXPAND|wx.ALL,border=0)
		self.hbox11=wx.BoxSizer()
		self.hbox11.Add(self.tiezideletebutton)
		self.hbox11.Add(self.tiezireplybutton)
		self.vbox1=wx.BoxSizer(wx.VERTICAL)
		self.vbox1.Add(self.hbox1,border=5)
		self.vbox1.Add(self.hbox2,border=5)
		self.vbox1.Add(self.hbox3,border=5)
		self.hboxext1=wx.BoxSizer()
		self.hboxext1.Add(self.loginbutton,proportion=1,border=0)
		self.hboxext1.Add(self.exitbutton,proportion=1,border=0)
		self.hboxext1.Add(self.status_label,proportion=1,border=0)
		self.vbox1.Add(self.hboxext1,border=5)
		self.vbox1.Add(self.hbox4,border=5)
		self.vbox1.Add(self.hbox5,border=5)
		self.vbox1.Add(self.hbox6,proportion=1,border=5)
		self.vbox1.Add(self.hbox7,border=5)
		self.vbox1.Add(self.hbox8,border=5)
		self.vbox1.Add(self.hbox9,border=5)
		self.vbox1.Add(self.hbox10,border=5)
		self.vbox1.Add(self.hbox11,border=5)
		panel.SetSizer(self.vbox1)
		cj=cookielib.CookieJar()
		opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		self.connector=test3.connector(opener=opener,headers=headers,home_url=self.sitename.GetValue())
		Publisher().subscribe(self.sendnewtieziresultdisplay,"sendnewtiezi")
		Publisher().subscribe(self.loginresultdisplay,'login result')
		Publisher().subscribe(self.mytiezilistdisplay,'mytiezilist')
		Publisher().subscribe(self.tiezicontentdisplay,'tiezicontent')
		Publisher().subscribe(self.sendtiezireplydisplay,'sendtiezireply')
		Publisher().subscribe(self.sendstatuscountdisplay,'sendstatuscount')
		#wx.StaticBitmap(parent=panel,bitmap=self.tmp)
	def tieziselection(self,evt):
		self.ust_tieziselection=updatestatusthread()
		self.ust_tieziselection.start()
		if evt.GetSelection()!=-1:
			self.tiezi_selection=evt.GetSelection()
		select_url=self.tiezis[self.tiezi_selection][0]
		t=tiezicontentthread(self.connector,select_url)
		t.setDaemon(True)
		t.start()
	def closeaction(self,evt):
		ret=wx.MessageBox('exit?','confirm',wx.OK|wx.CANCEL)
		if ret==wx.OK:
			sys.exit(0)
			#evt.Skip()
	def refreshtiezi(self,evt):
		self.ust_refresh2=updatestatusthread()
		self.ust_refresh2.start()
		t=getmytiezilistthread(self.connector)
		t.setDaemon(1)
		t.start()
	def sendreply(self,evt):
		reply=str(self.tiezireply.GetValue()).strip()
		if reply=='':
			dlg=wx.MessageDialog(self.panel,'reply content can not be empty',caption='Message',style=wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
		else:
			self.ust_sendreply=updatestatusthread()
			self.ust_sendreply.start()
			current_url=self.tiezis[self.tiezilist.GetSelection()][0]
			message=str(self.tiezireply.GetValue()).strip()
			t=sendreplythread(self.connector,current_url,message)
			t.setDaemon(1)
			t.start()
	def loginaction(self,evt):
		username=self.username.GetValue()
		password=self.password.GetValue()
		if username==''or password=='':
			dlg=wx.MessageDialog(self.panel,'please fill username or password',caption='Message',style=wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
		self.ust_login=updatestatusthread()
		self.ust_login.start()
		lt=loginthread(self.connector,username,password)
		lt.setDaemon(True)
		lt.start()
		self.loginbt=evt.GetEventObject()
		self.loginbt.Disable()
	def exitaction(self,evt):
		self.closeaction(self)
	
	def selectbankuai(self,evt):
		self.item=evt.GetSelection()
		self.diyu_choice.Clear()
		if self.item==0:
#			test=[f for f in xrange(192,209)]
#			test.append(291)
			self.values=['其他','首尔','仁川','釜山','大邱','大田','光州','京畿','忠北','忠南','全北','全南','江原','庆北','庆南','济州','蔚山','经验分享']
		elif self.item==1:
#			test=[f for f in xrange(50,57)]
#			test.append(646)
			self.values=['韩国聚会','其他相关','老乡交流','交朋结友','聚会总结','非诚勿扰','兴趣小组','晒照片大赛']
		elif self.item==2:
#			test=[f for f in xrange(57,62)]
#			test.append(277)
			self.values=['其他相关','婚姻相关','孕儿育儿','妈妈卖场','幸福生活照','婆媳关系']
		self.diyu_choice.AppendItems(self.values)
		self.diyu_choice.SetSelection(0)
#		Publisher().subscribe(self.updatedisplay,"update")
	def selectdiyu(self,evt):
		self.diyuitem=evt.GetSelection()
	def sendaction(self,evt):
		
		subject=self.subject.GetValue()
		sitename=self.sitename.GetValue()
		content=self.content.GetValue()
		bankuai_choice=self.bankuai_choice.GetSelection()
		diyu_choice=self.diyu_choice.GetSelection()
		if sitename=='' or content=='' or subject=='' or bankuai_choice<0 or diyu_choice<0:
			dlg=wx.MessageDialog(self.panel,'please fill input',caption='Message',style=wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
		else:
		
			if self.item==0:
				test=[f for f in xrange(192,209)]
				test.append(291)
							
			elif self.item==1:
				test=[f for f in xrange(50,57)]
				test.append(646)
			elif self.item==2:
				test=[f for f in xrange(57,62)]
				test.append(277)
			self.bankuainame=self.bankuai[self.item]
			self.diyuname=test[self.diyu_choice.GetSelection()]
			
			
			#test3.autosend(req_url,opener,username,password,self.diyuname,subject,content,self.headers,
#sitename,self.bankuainame)
			self.ust_sendnewtiezi=updatestatusthread()
			self.ust_sendnewtiezi.start()
			t=sendnewtiezithread(self.connector,self.diyuname,subject,content,self.bankuainame)
			t.setDaemon(True)
			t.start()
			
			self.btn=evt.GetEventObject()
			self.btn.Disable()
			#t.join()
	def sendstatuscountdisplay(self,msg):
		self.gaua.SetValue(int(msg.data))
	def sendtiezireplydisplay(self,msg):
		self.ust_sendreply.stop()
		self.gaua.SetValue(0)
		if msg.data=='reply succeed':
			showline='我 at now 说:\n\t%s\n---------------\n'%(self.tiezireply.GetValue())
			self.tiezicontent.AppendText(showline)
		dlg=wx.MessageDialog(self.panel,str(msg.data) if msg.data!=None else 'html code changed',caption='sendreply result',style=wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
	
	def tiezicontentdisplay(self,msg):
		self.ust_tieziselection2.stop()
		if self.__dict__.has_key('ust_tieziselection'):
			self.ust_tieziselection.stop()
		if self.__dict__.has_key('ust_refresh1'):
			self.ust_refresh1.stop()
		if self.__dict__.has_key('ust_refresh2'):
			self.ust_refresh2.stop()
		if self.__dict__.has_key('ust'):
			self.ust.stop()
		self.gaua.SetValue(0)
		
		content=msg.data['content']
		title=msg.data['title']
		self.tiezicontent.Clear()
		self.tiezicontent.AppendText('---------------%s-----------\n'%title)
		for n in content:
			showline='%s at %s 说:\n\t%s\n---------------\n'%('我' if n[0]==self.username.GetValue() else n[0],n[1].replace('&nbsp;',''),n[2].replace('<br />','').replace('\n','\n\t'))
			self.tiezicontent.AppendText(showline)
	def mytiezilistdisplay(self,msg):
		if self.__dict__.has_key('ust_refresh1'):
			self.ust_refresh1.stop()
		if self.__dict__.has_key('ust_refresh2'):
			self.ust_refresh2.stop()
		self.gaua.SetValue(0)
		self.tiezis=msg.data
		self.tiezilist.Clear()
		
		for n in  msg.data:
			showline='%s\t%s'%(n[1],n[2].replace('\n','\n\t'))
			self.tiezilist.Append(showline)
		self.tiezilist.SetSelection(self.tiezi_selection)
		self.ust_tieziselection2=updatestatusthread()
		self.ust_tieziselection2.start()
		t=tiezicontentthread(self.connector,self.tiezis[self.tiezi_selection][0])
		t.setDaemon(1)
		t.start()
	def loginresultdisplay(self,msg):
		self.ust_login.stop()
		self.gaua.SetValue(0)
		if msg.data[0]:
			self.loginbutton.Disable()
			self.ust_refresh1=updatestatusthread()
			self.ust_refresh1.start()
			t=getmytiezilistthread(self.connector)
			t.setDaemon(True)
			t.start()
			self.sendbutton.Enable()
			self.tiezireplybutton.Enable()
			self.tiezideletebutton.Enable()
			
		dlg=wx.MessageDialog(self.panel,str(msg.data[1]),caption='login result',style=wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
		self.loginbt.Enable()
		
	def sendnewtieziresultdisplay(self,msg):
		self.ust_sendnewtiezi.stop()
		self.gaua.SetValue(0)
		if msg.data[0]:
			self.tiezis.insert(0,[msg.data[2],self.subject.GetValue(),'now'])
			showline='%s\t'%(self.tiezis[0][1])
			self.tiezilist.InsertItems([showline],0)
		dlg=wx.MessageDialog(self.panel,msg.data[1],caption='Message',style=wx.OK)
		dlg.ShowModal()
		self.btn.Enable()
		dlg.Destroy()
class updatestatusthread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.flag=True
		self.count=0
	def run(self):
		while self.flag:
			self.count+=1
			time.sleep(.2)
			if self.count==20:
				self.count=0
			if self.flag:
				wx.CallAfter(self.postdata,self.count)
	def stop(self):
		self.flag=False
	
	def postdata(self,count):
		Publisher.sendMessage(topic='sendstatuscount',data=count)
class sendreplythread(threading.Thread)	:
	def __init__(self,connector,current_url,message):
		threading.Thread.__init__(self)
		self.connector=connector
		self.current_url=current_url
		self.message=message
	def run(self):
		contents=self.connector.sendreply(self.current_url,self.message)
		wx.CallAfter(self.postdata,contents)
	def postdata(self,result):
		Publisher.sendMessage(topic='sendtiezireply',data=result)
class tiezicontentthread(threading.Thread):
	def __init__(self,connector,url):
		threading.Thread.__init__(self)
		self.connector=connector
		self.url=url
	def run(self):
		contents=self.connector.gettiezicontent(self.url)
		wx.CallAfter(self.postdata,contents)
	def postdata(self,result):
		Publisher.sendMessage(topic='tiezicontent',data=result)
class getmytiezilistthread(threading.Thread):
	def __init__(self,connector):
		threading.Thread.__init__(self)
		self.connector=connector
	def run(self):
		mytiezilist=self.connector.getmytiezilist()
		wx.CallAfter(self.postdata,mytiezilist)
	def postdata(self,result):
		Publisher.sendMessage(topic='mytiezilist',data=result)
class loginthread(threading.Thread):
	def __init__(self,connector,username,password):
		threading.Thread.__init__(self)
		self.connector=connector
		self.username=username
		self.password=password
	def run(self):
		result=self.connector.login(self.username,self.password)
		wx.CallAfter(self.postdata,result)		
	def postdata(self,result):
		Publisher.sendMessage(topic='login result',data=result)
class sendnewtiezithread(threading.Thread):
	def __init__(self,connector,diyuname,subject,content,bankuainame):
		threading.Thread.__init__(self)
		self.connector=connector
		self.diyuname=diyuname
		self.subject=subject
		self.content=content
		self.bankuainame=bankuainame
	def run(self):
		result=self.connector.sendnewtiezi(self.diyuname,self.subject,self.content,self.bankuainame)
		wx.CallAfter(self.postdata,result)
	def postdata(self,msg):
		Publisher().sendMessage(topic='sendnewtiezi',data=msg)
if __name__=='__main__':
	app=wx.App()
	headers={'User-Agent':'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13',
	'Content-Type':'multipart/form-data',
	'Cache-Control':'no-cache',
	'Connection':'keep-alive',
	'Accept':'*/*',}
	img=wx.Image('logo.png',wx.BITMAP_TYPE_PNG)
	mg=mygui(headers,img)
	mg.Show()
	app.MainLoop()

