#!/usr/bin/env python2.7
import Tkinter as tk
import ConfigParser
import threading
import logging

from git import *

class DivaWidget(tk.Frame):

    def __init__(self, friends_branch=None, my_repo=None, my_branch=None, master=None):
        tk.Frame.__init__(self, master)
        self.read_conf()

        if not my_repo is None:
            self.my_repo = my_repo

        if not my_branch is None:
            self.my_branch = my_branch

        if not friends_branch is None:
            self.friends_branch = friends_branch

        ##############################################################
        self.mes_amis = {}
        for branch in sorted(self.friends_branch):
            temp=tk.IntVar()
            temp.set(0)
            self.mes_amis[branch] = temp

        ##############################################################

        ############################################################
    def myfunction(self, event):
        self.canvasDistances.configure(scrollregion=self.canvasDistances.bbox("all"),width=140,height=100)
        ###############################################################

    def placerXwing(self, yedlm):
        self.photoXwing = tk.PhotoImage(file = "xwing.gif")
        self.photoXwingU = tk.PhotoImage(file = "xwingUSER.gif")
	place = False
	place_min = 300 - self.photoEdlm.height()-self.photoXwing.height()

        j = 5
        k = 0

        for i in sorted(self.mes_amis.values()):
		if k == 0:
                	j = j+5
			if j == 10:
				j = -5
		if self.controlVarDelta.get() < i.get() and (not(self.controlVarDelta.get() >= i.get()) and place==False):
			self.canvasAnimation.create_image(20+k + self.photoXwingU.width()/2 + j, place_min - (place_min*self.controlVarDelta.get())/self.echelle + self.photoXwingU.height()/2, image = self.photoXwingU)
			place = True
			k = (k+40)%120
               	self.canvasAnimation.create_image(20+k + self.photoXwing.width()/2 + j, place_min - (place_min*i.get())/self.echelle + self.photoXwing.height()/2, image = self.photoXwing)
            	k = (k+40)%120
	if(not(place)):
		self.canvasAnimation.create_image(20+k + self.photoXwingU.width()/2 + j, place_min - (place_min*self.controlVarDelta.get())/self.echelle + self.photoXwingU.height()/2, image = self.photoXwingU)


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
            try:
                self.git.remote("update")
                self.calculateGDtot()
            except GitCommandError as e:
                logging.debug(e)
                pass

            self.update_stop.wait(self.refresh_rate)
        pass

    def createWidgets(self):
        self.controlVarGDtot=tk.IntVar()

        self.h1=tk.IntVar()

        self.controlVarDelta=tk.IntVar()
        self.controlVarState=tk.StringVar()

        self.Label1 = tk.Label(self, text="GDtot=")
        self.Label1.grid(column=0,row=0, sticky='WE',padx=2,pady=2)
        self.GDtotLabel = tk.Label(self, textvariable=self.controlVarGDtot)
        self.GDtotLabel.grid(column=1,row=0,sticky='W',padx=2,pady=2)

        self.Label2 = tk.Label(self, text="Distance=")
        self.Label2.grid(column=0,row=1, sticky='WE',padx=2,pady=2)
        self.DeltaLabel = tk.Label(self, textvariable=self.controlVarDelta)
        self.DeltaLabel.grid(column=1,row=1,sticky='W',padx=2,pady=2)
###############################################################
############Affichage de toutes les distances##################
###############################################################
        self.frameDistances = tk.Frame(self, relief = tk.GROOVE, width = 30, height = 30, bd = 1)
        self.frameDistances.grid(column = 0, row = 2, columnspan=2)

        self.canvasDistances = tk.Canvas(self.frameDistances, width = 50)
        self.frameCanvasDistance = tk.Frame(self.canvasDistances,  width = 50)

        self.scrollbarDistances = tk.Scrollbar(self.frameDistances, orient="vertical", command=self.canvasDistances.yview)
        self.canvasDistances.configure(yscrollcommand=self.scrollbarDistances.set)

        self.scrollbarDistances.pack(side="right",fill="y")
        self.canvasDistances.pack(side="left")
        self.canvasDistances.create_window((0,0), window=self.frameCanvasDistance, anchor='nw')
        self.frameCanvasDistance.bind("<Configure>", self.myfunction)

        z = 3
        incr = 0

        for i, j in sorted(self.mes_amis.iteritems()):
            tk.Label(self.frameCanvasDistance, text=i).grid(row=incr,column=0)
            tk.Label(self.frameCanvasDistance,textvariable = j).grid(column=1, row=incr)
            incr += 1

    #################################################################
    ######################Affichage des Xwing########################
    #################################################################
        self.canvasAnimation = tk.Canvas(self, width = 150, height = 300)
	self.echelle = 20
        self.photoXwing = tk.PhotoImage(file = "xwing.gif")
        self.photoEdlm = tk.PhotoImage(file = "edlm.gif")
        self.canvasAnimation.create_image(self.photoEdlm.width()/2+50, 300 - self.photoEdlm.height()/2, image = self.photoEdlm)
        self.placerXwing(0)
        self.canvasAnimation.grid(column=0, row = z, columnspan=2)

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
	self.echelle = len(H1)
        for branch in self.friends_branch:
            try:
                git_log=self.git.log(branch.strip(),format="oneline")
                if git_log != "":
                    Hi=set(git_log.split('\n'))
 #######################################################
                    distancesAmis[branch]=len(Hi)
                    sumHi += len(Hi)
                    Hmax=Hmax|Hi
                    #################################################################
            except GitCommandError as e:
                logging.debug(e)
                distancesAmis[branch] = 0

        haveNewDistance = False

        for branch in self.friends_branch:
            newFriendDistance = len(Hmax)-distancesAmis[branch]

            if newFriendDistance>self.echelle:
            	self.echelle = newFriendDistance

            if self.mes_amis[branch].get() != newFriendDistance:
                haveNewDistance = True
            self.mes_amis[branch].set(newFriendDistance)

        self.placerXwing((len(self.friends_branch)+1)*len(Hmax)-sumHi)
	if self.echelle<20:
		self.echelle = 20
        newGDtot = (len(self.friends_branch)+1)*len(Hmax)-sumHi
        if self.controlVarGDtot.get() != newGDtot:
            haveNewDistance = True
        self.controlVarGDtot.set(newGDtot)

        newDelta = len(Hmax)-len(H1)
        if self.controlVarDelta.get() != newDelta:
            haveNewDistance = True

        self.controlVarDelta.set(newDelta)

        if haveNewDistance:
            if logging.getLogger().getEffectiveLevel() == logging.INFO \
                    or logging.getLogger().getEffectiveLevel() == logging.DEBUG:
                logUsr=[]
                for branch, value in self.mes_amis.iteritems():
                    logUsr.append(str(branch)+"="+str(value.get()))

                logging.info("GDtot="+str(self.controlVarGDtot.get())+";"+
                     "delta="+str(self.controlVarDelta.get())+";"+
                     ";".join(logUsr))


def main():
    app = DivaWidget()
    app.launch()
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    Xpos = str(screen_width-160)
    app.master.title('diva')
    app.master.geometry('170x460+'+Xpos+'+50')
    app.master.overrideredirect(app.always_ontop)
    app.master.wm_iconbitmap(bitmap = "@diva.xbm")
    app.mainloop()

if __name__ == "__main__":
    main()
