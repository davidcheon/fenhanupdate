#!/usr/bin/python
#!_*_ coding:utf-8 _*_
import wx
from wx.lib.pubsub import Publisher
import cookielib
import urllib2
import threading
import time
import test3
class mygui(wx.Frame):
	def __init__(self,headers,img):
		wx.Frame.__init__(self,None,title='奋韩')
		self.item=None
		self.headers=headers
		self.tmp=img.ConvertToBitmap()
		self.SetSizeHintsSz((500,400),(500,400))
		panel=wx.Panel(self)
		self.panel=panel
		self.sitename_label=wx.StaticText(panel,label='website')
		self.sitename=wx.TextCtrl(panel,value='http://bbs.icnkr.com/forum.php?mobile=1',style=wx.TE_READONLY)
		self.username_label=wx.StaticText(panel,label='username')
		self.username=wx.TextCtrl(panel)
		self.password_label=wx.StaticText(panel,label='password')
		self.password=wx.TextCtrl(panel,style=wx.TE_PASSWORD)
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
		self.vbox1=wx.BoxSizer(wx.VERTICAL)
		self.vbox1.Add(self.hbox1,border=5)
		self.vbox1.Add(self.hbox2,border=5)
		self.vbox1.Add(self.hbox3,border=5)
		self.vbox1.Add(self.hbox4,border=5)
		self.vbox1.Add(self.hbox5,border=5)
		self.vbox1.Add(self.hbox6,proportion=1,border=5)
		self.vbox1.Add(self.hbox7,border=5)
		panel.SetSizer(self.vbox1)
		
		#wx.StaticBitmap(parent=panel,bitmap=self.tmp)
	def selectbankuai(self,evt):
		self.item=evt.GetSelection()
		self.diyu_choice.Clear()
		if self.item==0:
			test=[f for f in xrange(192,209)]
			test.append(291)
			self.values=['其他','首尔','仁川','釜山','大邱','大田','光州','京畿','忠北','忠南','全北','全南','江原','庆北','庆南','济州','蔚山','经验分享']
		elif self.item==1:
			test=[f for f in xrange(50,57)]
			test.append(646)
			self.values=['韩国聚会','其他相关','老乡交流','交朋结友','聚会总结','非诚勿扰','兴趣小组','晒照片大赛']
		elif self.item==2:
			test=[f for f in xrange(57,62)]
			test.append(277)
			self.values=['其他相关','婚姻相关','孕儿育儿','妈妈卖场','幸福生活照','婆媳关系']
		self.diyu_choice.AppendItems(self.values)
		self.diyu_choice.SetSelection(0)
		Publisher().subscribe(self.updatedisplay,"update")
	def selectdiyu(self,evt):
		self.diyuitem=evt.GetSelection()
	def sendaction(self,evt):
		username=self.username.GetValue()
		password=self.password.GetValue()
		subject=self.subject.GetValue()
		sitename=self.sitename.GetValue()
		content=self.content.GetValue()
		bankuai_choice=self.bankuai_choice.GetSelection()
		diyu_choice=self.diyu_choice.GetSelection()
		if username=='' or password=='' or sitename=='' or content=='' or subject=='' or bankuai_choice<0 or diyu_choice<0:
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
			
			req_url=test3.get_request_url(sitename,self.headers)
			cj=cookielib.CookieJar()
			opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			#test3.autosend(req_url,opener,username,password,self.diyuname,subject,content,self.headers,
#sitename,self.bankuainame)
			t=mythread(req_url,opener,username,password,self.diyuname,subject,content,self.headers,
sitename,self.bankuainame,self.panel)
			t.setDaemon(True)
			t.start()
			self.btn=evt.GetEventObject()
			self.btn.Disable()
			#t.join()
	def updatedisplay(self,msg):
		dlg=wx.MessageDialog(self.panel,msg.data,caption='Message',style=wx.OK)
		if dlg.ShowModal()==wx.ID_OK:
			self.btn.Enable()
		dlg.Destroy()
		
class mythread(threading.Thread):
	def __init__(self,req_url,opener,username,password,diyuname,subject,content,headers,
sitename,bankuainame,panel):
		threading.Thread.__init__(self)
		self.panel=panel
		self.req_url=req_url
		self.opener=opener
		self.username=username
		self.password=password
		self.diyuname=diyuname
		self.subject=subject
		self.content=content
		self.sitename=sitename
		self.bankuainame=bankuainame
		self.headers=headers
	def run(self):
		result=test3.autosend(self.req_url,self.opener,self.username,self.password,self.diyuname,self.subject,self.content,self.headers,self.sitename,self.bankuainame)
		wx.CallAfter(self.postdata,result)
	def postdata(self,msg):
		Publisher().sendMessage(topic='update',data=msg)
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
