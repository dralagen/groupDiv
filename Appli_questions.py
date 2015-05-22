# coding=utf-8
from Tkinter import *
import ConfigParser
import Tix
import os
import sys
import socket
from datetime import datetime

import logging
import threading
from git import GitCommandError, Repo
from gitdb import GitDB
import diva

logDirectory = os.environ["HOME"]+"/.groupDiv"
if not os.path.exists(logDirectory):
    os.mkdir(logDirectory)
logPath = logDirectory+"/"+socket.gethostname()+".log"
logging.basicConfig(filename=logPath,level=logging.INFO, format='%(levelname)s:%(asctime)s:%(message)s')

# On part du principe que tous les fichier de review et sur les ue existent deja
class Questionaire(Frame):
    def get_file_content(self, filename):
        file_path = self.repo.working_dir + "/" + filename
        content = ""
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            fileStream = open(file_path, "r")
            for line in fileStream:
                content += line
            fileStream.close()
        return content

    def charger_review(self):
        self.les_review.clear()
        temp = {}
        content = self.get_file_content("review_" + self.nom_usr + ".txt")
        if content != "":
            temp[self.mon_ue] = content.split('\n')
            temp[self.mon_ue].remove('')

        for usr in self.liste_usr:
            content = self.get_file_content("review_" + usr + ".txt")
            if content != "":
                temp[usr] = content.split('\n')
                temp[usr].remove('')

        # ici temp contient les contenu de chaque fichier de chaque usr
        while temp != {}:
            maxi = sys.maxint
            k = ""
            for key in temp:
                nombre = temp[key][0][0:6]
                if int(nombre) < maxi:
                    maxi = int(nombre)
                    k = key
            v = temp[k][0]
            mes_donnees = v.split("|")
            p = mes_donnees[1].decode("UTF-8")
            if p in self.les_review:
                self.les_review[p].append(mes_donnees[2])
            else:
                self.les_review[p] = [mes_donnees[2]]
            temp[k].remove(v)
            if not temp[k]:
                del temp[k]

    def string_review(self, ue):
        mes_review = ""
        if ue in self.les_review:
            for value in self.les_review[ue]:
                mes_review += value + "\n"
        return mes_review

    def envoyer_mon_ue(self):
        nom_fichier = "texte_" + self.mon_ue + ".txt"
        oldContent = self.get_file_content(nom_fichier).strip()
        newContent = self.texte_mon_ue.get(1.0, END).encode("UTF-8").strip()
        if oldContent == newContent:
            return

        fichier = open(self.repo.working_dir+"/"+nom_fichier, "w")
        fichier.write(newContent)
        fichier.close()

        self.repo.index.add([nom_fichier])
        hashCommit = self.repo.index.commit("update ue " + self.mon_ue)
        logging.info("commit update ue :" + str(hashCommit))

    def charger_texte(self, nom_ue):
        return self.get_file_content("texte_" + nom_ue + ".txt")

    def poster_commentaire(self):
        newReview = str(self.texte_mon_review.get().encode("UTF-8")).replace("\n", " ").strip()
        if not newReview:
            return

        nom_fichier = "review_" + self.nom_usr + ".txt"
        fichier = open(self.repo.working_dir+"/" + nom_fichier, "a")
        maintenant = datetime.now()
        fichier.write((
            str(maintenant.hour).zfill(2) + str(maintenant.minute).zfill(2) + str(maintenant.second).zfill(
                2) + "|" + self.choix_ue_a_review.entry.get().encode("UTF-8") + "|" + self.nom_usr + ": " + newReview + "\n"))

        self.review.config(state=NORMAL)
        self.review.insert(END, self.nom_usr + ": " + newReview + "\n")
        self.review.config(state=DISABLED)

        if self.choix_ue_a_review.entry.get() == self.mon_ue:
            self.review_mon_ue.config(state=NORMAL)
            self.review_mon_ue.insert(END, self.nom_usr + ": " + newReview + "\n")
            self.review_mon_ue.config(state=DISABLED)

        self.texte_mon_review.delete(0, END)
        fichier.close()

        # commit change
        self.repo.index.add([nom_fichier], False)
        hashCommit = self.repo.index.commit("add review by " + self.nom_usr)
        logging.info("commit new review :"+str(hashCommit))

        # reload review
        self.charger_review()

    # pour pull un usr, cette methode est utilisee par les sept boutons de pull,
    # le parametre usr sert a connaitre quel bouton est utilise
    def pull_un_usr(self, usr):
        try:
            executeResult = self.repo.git.execute(["git", "pull", usr, "master"])
            logging.info("pull from " + usr + ": " + executeResult.replace("\n", ";"))
        except GitCommandError as e:
            logging.error(e)

        self.commit_usr[usr] = 0
        self.charger_review()
        self.ui_update(self.choix_ue_a_review.entry.get())

    # methode a utiliser pour afficher les infos liees a une ue
    def changer_UE(self, event):
        self.ui_update(self.choix_ue_a_review.entry.get())

    # FIN METHODES ACTION

    def ui_update(self, ue_review):
        self.reponse_ue.config(state=NORMAL)
        self.reponse_ue.delete(1.0, END)
        self.reponse_ue.insert(END, self.charger_texte(ue_review))
        self.reponse_ue.config(state=DISABLED)

        self.review.config(state=NORMAL)
        self.review.delete(1.0, END)
        self.review.insert(END, self.string_review(ue_review))
        self.review.config(state=DISABLED)

        self.review_mon_ue.config(state=NORMAL)
        self.review_mon_ue.delete(1.0, END)
        self.review_mon_ue.insert(END, self.string_review(self.mon_ue))
        self.review_mon_ue.config(state=DISABLED)
    
    def consultation_des_log(self):
        #TODO ajouter log consultation de l'historique
        print "log histo OK"

    def arret_consultation_des_log(self):
        #TODO ajouter log arret consultation de l'historique
        print "log histo ARRET"

    def createTabs(self, master):


        # definition des onglets
        self.notebook = Tix.NoteBook(master, width=660)
        self.notebook.add("ue", label="UE", raisecmd=self.arret_consultation_des_log)
        self.notebook.add("review", label="Review", raisecmd=self.arret_consultation_des_log)
        self.notebook.add("historique", label = "Historique des commits", raisecmd=self.consultation_des_log)
        self.notebook.grid(column=0, row=1, columnspan = 8)

        # onglet ue
        self.ue = self.notebook.subwidget_list["ue"]
        #contient tous les widget de l'onglet question
        self.onglet_ue = Frame(self.ue)
        self.onglet_ue.grid(column=0, row=1)

        #onglet review
        self.review = self.notebook.subwidget_list["review"]
        #contient tous les widget de l'onglet commentaire
        self.onglet_review = Frame(self.review)
        self.onglet_review.grid(column=0, row=1)

        #onglet messages
        self.historiqueCommit = self.notebook.subwidget_list["historique"]
        self.onglet_historique = Frame(self.historiqueCommit)
        self.onglet_historique.grid(column = 0, row = 1)

    def createWidgetsInUE(self):

        # bouton qui sert a faire un commit
        self.envoyer = Button(self.onglet_ue, text="Envoyer", width=5, height=20, command=self.envoyer_mon_ue)
        self.envoyer.grid(column=5, row=3)

        self.label_mon_ue = Label(self.onglet_ue, text="Description " + self.mon_ue).grid(column=1, row=0, columnspan=1)

        # scroll barre pour la zone de texte editable + zone de texte editable pour l'ue
        self.scroll_texte_mon_ue_V = Scrollbar(self.onglet_ue, orient=VERTICAL)
        self.texte_mon_ue = Text(self.onglet_ue, width=80, height=20, wrap=WORD)
        init_text_ue = self.charger_texte(self.mon_ue)
        if not init_text_ue:
            init_text_ue = "Pre-requis:\n\n\n\nCompetences acquises:\n\n\n\nProgramme:\n\n\n\nAmeliorations a apporter:\n\n\n\n"
        self.texte_mon_ue.insert(END, init_text_ue)
        self.texte_mon_ue.config(yscrollcommand=self.scroll_texte_mon_ue_V.set, background="#FFFFFF", foreground="Black")
        self.scroll_texte_mon_ue_V.config(command=self.texte_mon_ue.yview)
        self.scroll_texte_mon_ue_V.grid(column=4, row=1, rowspan=5, sticky=S + N)
        self.texte_mon_ue.grid(column=0, row=1, columnspan=3, rowspan=5)

        #zone review
        self.label_review_mon_ue = Label(self.onglet_ue, text="Les review de mon UE").grid(column=1, row=6,
                                                                                           columnspan=1)
        self.scroll_review_mon_ue_V = Scrollbar(self.onglet_ue, orient=VERTICAL)
        self.review_mon_ue = Text(self.onglet_ue, width=80, height=20, wrap=WORD)
        self.review_mon_ue.insert(END, self.string_review(self.mon_ue))
        self.review_mon_ue.config(state=DISABLED, yscrollcommand=self.scroll_review_mon_ue_V.set, background="#DBDBDB", foreground="Black")
        self.scroll_review_mon_ue_V.config(command=self.review_mon_ue.yview)
        self.scroll_review_mon_ue_V.grid(column=4, row=7, rowspan=8, sticky=S + N)
        self.review_mon_ue.grid(column=0, row=7, columnspan=3, rowspan=8)

    def createWidgetsInReview(self):

        # liste deroulant pour choisir une ue (pas la meme que la precedente, on utilisera pas la meme fontion
        self.choix_ue_a_review = Tix.ComboBox(self.onglet_review)
        self.choix_ue_a_review.slistbox.listbox.bind('<ButtonRelease-1>', self.changer_UE)
        self.choix_ue_a_review.entry.config(width=45, state='readonly')
        for a, b in self.liste_usr.iteritems():
            self.choix_ue_a_review.insert(0,b)

        self.choix_ue_a_review.pick(0)

        self.choix_ue_a_review.grid(column=1, row=0, columnspan=3, sticky=W)

        # affichage de la reponse dans une zone de texte non editable
        self.label_reponse = Label(self.onglet_review, text="Texte: ", font=30).grid(column=0, row=2)
        self.scroll_reponse_ue_V = Scrollbar(self.onglet_review, orient=VERTICAL)
        self.reponse_ue = Text(self.onglet_review, width=78, height=18, wrap=WORD)
        self.reponse_ue.insert(END, self.charger_texte(self.choix_ue_a_review.entry.get()))
        self.reponse_ue.config(state=DISABLED, yscrollcommand=self.scroll_reponse_ue_V.set, background="#DBDBDB", foreground="Black")

        self.scroll_reponse_ue_V.config(command=self.reponse_ue.yview)
        self.scroll_reponse_ue_V.grid(column=4, row=1, rowspan=3, sticky=S + N)
        self.reponse_ue.grid(column=1, row=1, columnspan=4, rowspan=3, sticky=W)

        #affichage des review dans une zone de texte non editable
        self.lable_review = Label(self.onglet_review, text="Review: ", font=30).grid(column=0, row=5)
        self.scroll_review_V = Scrollbar(self.onglet_review, orient=VERTICAL)
        self.review = Text(self.onglet_review, width=78, height=20, wrap=WORD)
        self.review.insert(END, self.string_review(self.choix_ue_a_review.entry.get()))
        self.review.config(state=DISABLED, yscrollcommand=self.scroll_review_V.set, background="#DBDBDB", foreground="Black")
        self.scroll_review_V.config(command=self.review.yview)
        self.scroll_review_V.grid(column=4, row=4, rowspan=4, sticky=S + N)
        self.review.grid(column=1, row=4, columnspan=3, rowspan=4, sticky=W)

        #bouton pour poster un commentaire
        self.post = Button(self.onglet_review, text="Post", width=5, height=1, command=self.poster_commentaire)
        self.post.grid(column=3, row=9)

        #zone de texte editable pour ecrire un commentaire
        self.label_mon_review = Label(self.onglet_review, text="Votre\nreview: ", font=30).grid(column=0, row=9)
        #self.scroll_mon_review_V = Scrollbar(self.onglet_review, orient = VERTICAL)
        self.texte_mon_review = Entry(self.onglet_review, width=56, background="#FFFFFF", foreground="Black")
        #self.scroll_mon_review_V.config(command = self.texte_mon_review.yview)
        #self.scroll_mon_review_V.grid(column = 3, row = 9, sticky = S + N)
        self.texte_mon_review.grid(column=1, row=9, columnspan=2)

    def createWidgetsInHistoriqueCommit(self):
        self.scroll_review_historique_V = Scrollbar(self.onglet_historique, orient=VERTICAL)
        self.texte_historique_commit = Text(self.onglet_historique, width=90, height=43, wrap=WORD)
        self.texte_historique_commit.config(state=DISABLED, yscrollcommand=self.scroll_review_historique_V.set, background="#DBDBDB", foreground="Black")
        self.scroll_review_historique_V.config(command=self.texte_historique_commit.yview)
        self.scroll_review_historique_V.grid(column=1, row=0, sticky=S + N)
        self.texte_historique_commit.grid(column=0, row=0)

    def get_usr_ue_name(self, filename):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(filename)

        user_computer = socket.gethostname()

        for section in self.config.sections():
            hostname = self.config.get(section, "hostname")
            if hostname == user_computer:
                self.mon_ue = self.config.get(section, "ue")
                self.nom_usr = section
            else:
                self.liste_usr[section] = self.config.get(section, "ue")

                try:
                    self.repo.delete_remote(section)
                except GitCommandError:
                    pass

                self.repo.create_remote(section, "git://" + self.config.get(section, "hostname").strip() + "/")

    def threadHistoryCommit(self):
        while not self.update_stop.is_set():
            try:
                self.repo.remote("update")
                try:
                    myCommit = len(str(self.repo.git.log("master", format="oneline")).split('\n'))
                except GitCommandError:
                    myCommit = 0

                for usr in sorted(self.commit_usr, reverse=True):
                    try:
                        if myCommit == 0:
                            usrCommit = len(str(self.repo.git.log(usr+"/master", format="oneline")).split('\n'))
                        else:
                            usrCommit = len(str(self.repo.git.execute(["git", "log", "HEAD.." + usr + "/master", "--oneline"])).split('\n'))

                        if usrCommit > self.commit_usr[usr]:
                            nbCommit = usrCommit - self.commit_usr[usr]
                            logCommit = usr + " à fait "
                            logCommit += str(nbCommit)
                            logCommit += " commit"
                            if nbCommit > 1:
                                logCommit +="s"
                            logCommit += "\n"

                            self.texte_historique_commit.config(state=NORMAL)
                            self.texte_historique_commit.insert('0.0', logCommit)
                            self.texte_historique_commit.config(state=DISABLED)
                            self.commit_usr[usr] = usrCommit
                    except GitCommandError:
                        pass

            except GitCommandError:
                pass

            # wait 5 secondes
            self.update_stop.wait(5)
        pass

    def onKeyPress(self, event):
        if repr(event.keysym) == self.konami_code['keymap'][self.konami_code['indice']]:
            self.konami_code['indice'] += 1
        else:
            self.konami_code['indice'] = 0

        print self.konami_code['indice']
        print len(self.konami_code['keymap'])

        if self.konami_code['indice'] >= len(self.konami_code['keymap']):
            self.konami_code['indice'] = 0
            self.konami_code['cmd']()

    def toogleDiva(self):
        self.hide = not self.hide
        if self.hide:
            self.diva_root.withdraw()
        else:
            self.diva_root.deiconify()


    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("Interface Tkinter")
        master.protocol("WM_DELETE_WINDOW", self.quitAction)
        self.konami_code = { 'indice' : 0,
                             'keymap' : ("'Up'", "'Up'", "'Down'", "'Down'", "'Left'", "'Right'", "'Left'", "'Right'", "'b'", "'a'"),
                             'cmd': self.toogleDiva }
        self.hide = False
        #Detection code konami
        master.bind("<KeyPress>", self.onKeyPress)


        self.repo = Repo(os.environ["DIVA_REPO_DIR"], odbt=GitDB)
        assert not self.repo.bare
        os.environ["GIT_MERGE_AUTOEDIT"] = "no"
        self.mon_ue = ""
        self.nom_usr = ""

        #liste[usr1] = matiere
        self.liste_usr = {}
        self.get_usr_ue_name(sys.argv[1])

        self.les_review = {}
        self.charger_review()
        self.createTabs(master)
        self.createWidgetsInUE()
        self.createWidgetsInReview()
        self.createWidgetsInHistoriqueCommit()
        #bouton qui sert a faire un pull
        self.lable_review = Label(master, text="Se mettre a jour avec:", font=12).grid(column=0, row=0)

        i = 1

        for usr in sorted(self.liste_usr):
            self.boutons_maj = Button(master, text= self.config.get(usr,"name"), width=5, height=1,
                                      command=lambda x=usr : self.pull_un_usr(x))
            self.boutons_maj.grid(column=i, row= 0)
            i += 1

        branchUsr = []
        self.commit_usr = {}
        for branch in self.liste_usr:
            branchUsr.append(branch+"/master")
            self.commit_usr[branch] = 0

        self.update_stop=threading.Event()
        self.thread=threading.Thread(target=self.threadHistoryCommit)
        self.thread.start()

        self.diva_root = Tix.Toplevel(master)
        self.diva = diva.DivaWidget(my_repo=os.environ["DIVA_REPO_DIR"], friends_branch=branchUsr, master=self.diva_root)
        self.diva.launch()
        if len(sys.argv) == 3 and sys.argv[2] == "1":
            self.diva_root.withdraw()
            self.hide = True

        screen_width = self.diva.winfo_screenwidth()
        Xpos = str(screen_width-160)
        self.master.title(self.nom_usr +" " +self.mon_ue)
        self.diva.master.title('diva')
        self.diva.master.geometry('170x500+'+Xpos+'+50')
        self.diva.master.overrideredirect(self.diva.always_ontop)
        self.diva.master.wm_iconbitmap(bitmap = "@diva.xbm")

    def quitAction(self):
        self.update_stop.set()
        if self.thread.isAlive():
            self.thread.join()
            self.master.quit()
        self.diva.quitAction()



root = Tix.Tk()
app = Questionaire(master=root)
app.mainloop()
