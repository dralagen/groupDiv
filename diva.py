#!/usr/bin/env python2.7
import Tkinter as tk   
import ttk
from git import *
import Image, ImageTk
import ConfigParser
import threading, time
import sys

class Application(tk.Frame):              
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)   
        self.read_conf()
        self.init_git()
        self.run_thread()
        self.grid()
        self.createWidgets()
        self.master.protocol("WM_DELETE_WINDOW", self.quitAction)
    
    def read_conf(self):
		config = ConfigParser.RawConfigParser()
		config.read('diva.cfg')
		self.my_repo=config.get("git","my_repo")
		self.my_branch=config.get("git","my_branch")
	
		self.friends_repo=config.get("git","friends_repo")
		self.friends_repo=self.friends_repo.split(" ")
	
		self.friends_branch=config.get("git","friends_branch")
		self.friends_branch=self.friends_branch.split(" ")
	
		##############################################################
		self.mes_amis = {}
		for branch in self.friends_branch:
			temp=tk.IntVar()
	  		temp.set(0)
			self.mes_amis[branch] = temp
		##############################################################
	
		self.refresh_rate=int(config.get("diva","refresh_rate"))
		self.sync_limit=int(config.get("diva","sync_limit"))
		self.always_ontop=int(config.get("diva","always_ontop"))
      
    def init_git(self):
		repo = Repo(self.my_repo, odbt=GitDB)
		assert repo.bare ==False
		self.git = repo.git
	
    def run_thread(self):
		self.update_stop=threading.Event()
		self.thread=threading.Thread(target=self.threadUpdateRepo)
		self.thread.start()
	
    def threadUpdateRepo(self):
		while(not self.update_stop.is_set()):
		  self.git.remote("update")
		  self.calculateGDtot()
		  self.update_stop.wait(self.refresh_rate)
		pass
    
    def createWidgets(self):    
        self.controlVarGDtot=tk.IntVar()

        self.h1=tk.IntVar()

        self.controlVarDelta=tk.IntVar()
        self.controlVarState=tk.StringVar()

        self.Label1 = tk.Label(self, text="GDtot=")
        self.Label1.grid(column=0,row=0,sticky='WE',padx=2,pady=2)
        self.GDtotLabel = tk.Label(self, textvariable=self.controlVarGDtot)
        self.GDtotLabel.grid(column=1,row=0,sticky='W',padx=2,pady=2)
#########################################
        z = 4
        mes_h={}
        for i, j in self.mes_amis.iteritems():
        	self.Label22 = tk.Label(self, text=i)
        	self.Label22.grid(column=0,row=z,sticky='WE',padx=2,pady=2)
        	mes_h[i] = tk.Label(self, textvariable=self.mes_amis[i])
        	mes_h[i].grid(column=1,row=z,sticky='W',padx=2,pady=2)
        	z=z+1
##########################################
        
        self.Label2 = tk.Label(self, text="Distance=")
        self.Label2.grid(column=0,row=2,sticky='WE',padx=2,pady=2)
        self.DeltaLabel = tk.Label(self, textvariable=self.controlVarDelta)
        self.DeltaLabel.grid(column=1,row=2,sticky='W',padx=2,pady=2)
        
        self.quitButton = tk.Button(self, text='Quit', command=self.quitAction)            
        self.quitButton.grid(sticky='WE',columnspan=2,padx=5,pady=5)
                   
        self.can1 = tk.Canvas(self , width = 50 , height = 50)

        self.img = Image.open('xwing.gif')
       # self.img = ImageTk.PhotoImage(self.img) 
        self.photo = ImageTk.PhotoImage(self.img)
        self.item = self.can1.create_image(0, 0, image = self.photo)
        self.can1.grid(row=z+1 , column=0)



    def quitAction(self):
      self.update_stop.set()
      if self.thread.isAlive():
	self.thread.join()
      self.master.quit()

    def calculateGDtot(self):
	H1=self.git.log(self.my_branch,format="oneline")
	if (H1 != ""):
	    H1=set(H1.split('\n'))
	
	sumHi=len(H1)
	Hmax=H1
	i = 1
	for branch in self.friends_branch:
	  log=self.git.log(branch,format="oneline")
	  if (log != ""):
	      Hi=set(log.split('\n'))
#######################################################
	  temp = tk.IntVar()
	  temp.set(len(Hi))
	  self.mes_amis[branch].set(len(Hi))
#################################################################
	  sumHi=sumHi+len(Hi)
	  Hmax=Hmax|Hi
	  i=i+1
	
	self.controlVarGDtot.set((len(self.friends_branch)+1)*len(Hmax)-sumHi)

	self.controlVarDelta.set(len(Hmax)-len(H1))
	
	    
app = Application() 
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight() 
Xpos = str(screen_width-150)
app.master.title('diva')
app.master.geometry('150x350+'+Xpos+'+50')
app.master.overrideredirect(app.always_ontop)
app.master.wm_iconbitmap(bitmap = "@diva.xbm")
app.mainloop()
