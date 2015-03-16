#!/usr/bin/env python2.7
import Tkinter as tk
import ConfigParser
import threading
import logging

from git import *

class DivaWidget(tk.Frame):
    
    def __init__(self, listBranch=None, my_repo=None, my_branch=None, master=None):
        tk.Frame.__init__(self, master)
        self.read_conf()

        if not my_repo is None:
            self.my_repo = my_repo

        if not my_branch is None:
            self.my_branch = my_branch

        if not listBranch is None:
            self.friends_branch = listBranch

        ##############################################################
        self.toutesLesDistances = []
        self.mes_amis = {}
        for branch in sorted(self.friends_branch):
            self.toutesLesDistances.append(0)
            temp=tk.IntVar()
            temp.set(0)
            self.mes_amis[branch] = temp
            
        ##############################################################
        
        ############################################################
    def myfunction(self, event):
        self.canvasDistances.configure(scrollregion=self.canvasDistances.bbox("all"),width=200,height=200)
        ###############################################################

    def placerXwing(self):
        self.photoXwing = tk.PhotoImage(file = "xwing.gif")
        #self.photoEdlm = tk.PhotoImage(file = "xwing.gif")
        j = 1
        k = 0
        for i in sorted(self.toutesLesDistances):
            if k == 0:
                j = -j
            if i >60:
                self.canvasAnimation.create_image(k + self.photoXwing.width()/2 + j, 5*60 + self.photoXwing.height()/2, image = self.photoXwing)
            else:
                self.canvasAnimation.create_image(k + self.photoXwing.width()/2 + j, 5*i + self.photoXwing.height()/2, image = self.photoXwing)
            k = (k+40)%120
    	
    def launch(self):
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

        self.friends_branch=config.get("git","friends_branch")
        self.friends_branch=self.friends_branch.split(" ")

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
        while not self.update_stop.is_set():
            self.git.remote("update")
            self.calculateGDtot()

            if logging.getLogger().getEffectiveLevel() == logging.INFO \
                    or logging.getLogger().getEffectiveLevel() == logging.DEBUG:
                logUsr=[]
                for branch, value in self.mes_amis.iteritems():
                    logUsr.append(str(branch)+"="+str(value.get()))

                logging.info("GDtot="+str(self.controlVarGDtot.get())+";"+
                             "delta="+str(self.controlVarDelta.get())+";"+
                             ";".join(logUsr))
            self.update_stop.wait(self.refresh_rate)
        pass
    
    def createWidgets(self):    
        self.controlVarGDtot=tk.IntVar()

        self.h1=tk.IntVar()

        self.controlVarDelta=tk.IntVar()
        self.controlVarState=tk.StringVar()

        self.Label1 = tk.Label(self, text="GDtot=")
        self.Label1.grid(column=0,row=0, columnspan="7", sticky='WE',padx=2,pady=2)
        self.GDtotLabel = tk.Label(self, textvariable=self.controlVarGDtot)
        self.GDtotLabel.grid(column=8,row=0,sticky='W',padx=2,pady=2)

        self.Label2 = tk.Label(self, text="Distance=")
        self.Label2.grid(column=0,row=2, columnspan="7",sticky='WE',padx=2,pady=2)
        self.DeltaLabel = tk.Label(self, textvariable=self.controlVarDelta)
        self.DeltaLabel.grid(column=8,row=1,sticky='W',padx=2,pady=2)
###############################################################
############Affichage de toutes les distances##################
###############################################################
        self.frameDistances = tk.Frame(self, relief = tk.GROOVE, width = 40, height = 50, bd = 1)
        self.frameDistances.grid(column = 0, row = 2, columnspan=8)

        self.canvasDistances = tk.Canvas(self.frameDistances)
        self.frameCanvasDistance = tk.Frame(self.canvasDistances)

        self.scrollbarDistances = tk.Scrollbar(self.frameDistances, orient="vertical", command=self.canvasDistances.yview)
        self.canvasDistances.configure(yscrollcommand=self.scrollbarDistances.set)

        self.scrollbarDistances.pack(side="right",fill="y")
        self.canvasDistances.pack(side="left")
        self.canvasDistances.create_window((0,0), window=self.frameCanvasDistance, anchor='nw')
        self.frameCanvasDistance.bind("<Configure>", self.myfunction)

        z = 3
        i = 0

        for i, j in sorted(self.mes_amis.iteritems()):
            tk.Label(self.frameCanvasDistance, text=i).grid(row=i,column=0)
            tk.Label(self.frameCanvasDistance,textvariable = j).grid(column=1, row=i)
            i += 1
            
	##########################################
        self.quitButton = tk.Button(self, text='Quit', command=self.quitAction)            
        self.quitButton.grid(sticky='WE',columnspan=8,row=z, padx=5,pady=5)
        z += 1
        
	#################################################################
	######################Affichage des Xwing########################
	#################################################################
        self.canvasAnimation = tk.Canvas(self, width = 200, height = 250)
        self.placerXwing()
        self.canvasAnimation.grid(column=0, row = z)

    def quitAction(self):
        self.update_stop.set()
        if self.thread.isAlive():
            self.thread.join()
            self.master.quit()

    def calculateGDtot(self):
        try:
            H1=self.git.log(self.my_branch,format="oneline")
        except GitCommandError:
            H1 = ""

        if H1 != "":
            H1=set(H1.split('\n'))

        sumHi=len(H1)
        
        Hmax=set(H1)
        distancesAmis = {}

        for branch in self.friends_branch:

            try:
                git_log=self.git.log(branch.strip(),format="oneline")
            except GitCommandError as e:
                logging.error(e)
                git_log=""
            if git_log != "":
                Hi=set(git_log.split('\n'))
                #######################################################
                distancesAmis[branch]=len(Hi)
                sumHi += len(Hi)
                Hmax=Hmax|Hi
                #################################################################
        self.toutesLesDistances = []
        for branch in self.friends_branch:
            self.toutesLesDistances.append(len(Hmax)-distancesAmis[branch])
            self.mes_amis[branch].set(len(Hmax)-distancesAmis[branch])
        
        self.placerXwing()

        self.controlVarGDtot.set((len(self.friends_branch)+1)*len(Hmax)-sumHi)

        self.controlVarDelta.set(len(Hmax)-len(H1))


def main():
    app = DivaWidget()
    app.launch()
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    Xpos = str(screen_width-150)
    app.master.title('diva')
    app.master.geometry('500x500+'+Xpos+'+50')
    app.master.overrideredirect(app.always_ontop)
    app.master.wm_iconbitmap(bitmap = "@diva.xbm")
    app.mainloop()

if __name__ == "__main__":
    main()
