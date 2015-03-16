from Tkinter import *
import ConfigParser
import Tix
import os
import sys
import socket
from datetime import datetime

import logging
from git import GitCommandError, Repo
from gitdb import GitDB
import diva


logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(asctime)s:%(message)s')

# On part du principe que tous les fichier de review et sur les ue existent deja
class Questionaire(Frame):
    def get_file_content(self, filename):
        file_path = self.repo.working_dir + "/" + filename
        content = ""
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            fileStream = open(file_path, "r")
            for line in fileStream:
                if line != "\n":
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
            if mes_donnees[1] in self.les_review:
                p = mes_donnees[1]
                self.les_review[p].append(mes_donnees[2])
            else:
                self.les_review[mes_donnees[1]] = [mes_donnees[2]]
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
                2) + "|" + self.choix_ue_a_review.entry.get() + "|" + self.nom_usr + ": " + newReview + "\n"))

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

    # pour pull un usr, cette methode est utilisee par les sept boutons de pull,
    # le parametre usr sert a connaitre quel bouton est utilise
    def pull_un_usr(self, usr):
        try:
            executeResult = self.repo.git.execute(["git", "pull", usr, "master"])
            logging.info("pull from " + usr + ": " + executeResult.replace("\n", ";"))
        except GitCommandError as e:
            logging.error(e)

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


    def createTabs(self, master):
        # definition des onglets
        self.notebook = Tix.NoteBook(master, width=630)
        self.notebook.add("ue", label="UE")
        self.notebook.add("review", label="Review")
        self.notebook.grid(column=0, row=0)

        # onglet ue
        self.ue = self.notebook.subwidget_list["ue"]
        #contient tous les widget de l'onglet question
        self.onglet_ue = Frame(self.ue)
        self.onglet_ue.grid(column=0, row=0)

        #onglet review
        self.review = self.notebook.subwidget_list["review"]
        #contient tous les widget de l'onglet commentaire
        self.onglet_review = Frame(self.review)
        self.onglet_review.grid(column=0, row=0)

    def createWidgetsInUE(self):

        # bouton qui sert a faire un commit
        self.envoyer = Button(self.onglet_ue, text="Envoyer", width=5, height=20, command=self.envoyer_mon_ue)
        self.envoyer.grid(column=5, row=3)

        self.label_mon_ue = Label(self.onglet_ue, text="Description " + self.mon_ue).grid(column=1, row=0, columnspan=1)

        # scroll barre pour la zone de texte editable + zone de texte editable pour l'ue
        self.scroll_texte_mon_ue_V = Scrollbar(self.onglet_ue, orient=VERTICAL)
        self.texte_mon_ue = Text(self.onglet_ue, width=75, height=20, wrap=WORD)
        self.texte_mon_ue.config(yscrollcommand=self.scroll_texte_mon_ue_V.set, background="#FFFFFF", foreground="Black")
        self.texte_mon_ue.insert(END, self.charger_texte(self.mon_ue))
        self.scroll_texte_mon_ue_V.config(command=self.texte_mon_ue.yview)
        self.scroll_texte_mon_ue_V.grid(column=4, row=1, rowspan=5, sticky=S + N)
        self.texte_mon_ue.grid(column=0, row=1, columnspan=3, rowspan=5)

        #zone review
        self.label_review_mon_ue = Label(self.onglet_ue, text="Les review de mon UE").grid(column=1, row=6,
                                                                                           columnspan=1)
        self.scroll_review_mon_ue_V = Scrollbar(self.onglet_ue, orient=VERTICAL)
        self.review_mon_ue = Text(self.onglet_ue, width=75, height=20, wrap=WORD)
        self.review_mon_ue.insert(END, self.string_review(self.mon_ue))
        self.review_mon_ue.config(state=DISABLED, yscrollcommand=self.scroll_review_mon_ue_V.set, background="#DBDBDB", foreground="Black")
        self.scroll_review_mon_ue_V.config(command=self.review_mon_ue.yview)
        self.scroll_review_mon_ue_V.grid(column=4, row=7, rowspan=8, sticky=S + N)
        self.review_mon_ue.grid(column=0, row=7, columnspan=3, rowspan=8)

        #boutons de maj
        self.label_maj_review_mon_ue = Label(self.onglet_ue, text="Maj de").grid(column=5, row=7, columnspan=1)

        i = 0

        for usr in sorted(self.liste_usr):
            self.boutons_maj = Button(self.onglet_ue, text= self.config.get(usr,"name"), width=5, height=1,
                                      command=lambda x=usr : self.pull_un_usr(x))
            self.boutons_maj.grid(column=5, row= (8+i))
            i += 1

    def createWidgetsInReview(self):

        # liste deroulant pour choisir une ue (pas la meme que la precedente, on utilisera pas la meme fontion
        self.choix_ue_a_review = Tix.ComboBox(self.onglet_review)
        self.choix_ue_a_review.slistbox.listbox.bind('<ButtonRelease-1>', self.changer_UE)
        self.choix_ue_a_review.entry.config(width=45, state='readonly')
        for a, b in self.liste_usr.iteritems():
            self.choix_ue_a_review.insert(0,b)

        self.choix_ue_a_review.pick(0)

        self.choix_ue_a_review.grid(column=1, row=0, columnspan=2, sticky=W)

        # affichage de la reponse dans une zone de texte non editable
        self.label_reponse = Label(self.onglet_review, text="Reponse: ", font=30).grid(column=0, row=2)
        self.scroll_reponse_ue_V = Scrollbar(self.onglet_review, orient=VERTICAL)
        self.reponse_ue = Text(self.onglet_review, width=65, height=18, wrap=WORD)
        self.reponse_ue.insert(END, self.charger_texte(self.choix_ue_a_review.entry.get()))
        self.reponse_ue.config(state=DISABLED, yscrollcommand=self.scroll_reponse_ue_V.set, background="#DBDBDB", foreground="Black")

        self.scroll_reponse_ue_V.config(command=self.reponse_ue.yview)
        self.scroll_reponse_ue_V.grid(column=3, row=1, rowspan=3, sticky=S + N)
        self.reponse_ue.grid(column=1, row=1, columnspan=2, rowspan=3, sticky=W)

        #affichage des review dans une zone de texte non editable
        self.lable_review = Label(self.onglet_review, text="Review: ", font=30).grid(column=0, row=5)
        self.scroll_review_V = Scrollbar(self.onglet_review, orient=VERTICAL)
        self.review = Text(self.onglet_review, width=65, height=20, wrap=WORD)
        self.review.insert(END, self.string_review(self.choix_ue_a_review.entry.get()))
        self.review.config(state=DISABLED, yscrollcommand=self.scroll_review_V.set, background="#DBDBDB", foreground="Black")
        self.scroll_review_V.config(command=self.review.yview)
        self.scroll_review_V.grid(column=3, row=4, rowspan=4, sticky=S + N)
        self.review.grid(column=1, row=4, columnspan=2, rowspan=4, sticky=W)

        #bouton qui sert a faire un pull
        self.lable_review = Label(self.onglet_review, text="MAJ de ", font=30).grid(column=4, row=0)

        i = 1
        for usr in sorted(self.liste_usr):
            self.recuperer = Button(self.onglet_review, text= self.config.get(usr,"name"), width=5, height=1,
                                    command=lambda x=usr : self.pull_un_usr(x))
            self.recuperer.grid(column=4, row=i)
            i += 1

        #bouton pour poster un commentaire
        self.post = Button(self.onglet_review, text="Post", width=5, height=1, command=self.poster_commentaire)
        self.post.grid(column=4, row=9)

        #zone de texte editable pour ecrire un commentaire
        self.label_mon_review = Label(self.onglet_review, text="Votre\nreview: ", font=30).grid(column=0, row=9)
        #self.scroll_mon_review_V = Scrollbar(self.onglet_review, orient = VERTICAL)
        self.texte_mon_review = Entry(self.onglet_review, width=56, background="#FFFFFF", foreground="Black")
        #self.scroll_mon_review_V.config(command = self.texte_mon_review.yview)
        #self.scroll_mon_review_V.grid(column = 3, row = 9, sticky = S + N)
        self.texte_mon_review.grid(column=1, row=9, columnspan=2)

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


    def __init__(self, master=None):
        Frame.__init__(self, master)
        master.title("Interface Tkinter")
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

        branchUsr = []
        for branch in self.liste_usr:
            branchUsr.append(branch+"/master")

        diva_root = Tix.Toplevel(master)
        self.diva = diva.DivaWidget(listBranch=branchUsr, master=diva_root)
        self.diva.launch()
        screen_width = self.diva.winfo_screenwidth()
        screen_height = self.diva.winfo_screenheight()
        Xpos = str(screen_width-150)
        self.diva.master.title('diva')
        self.diva.master.geometry('500x500+'+Xpos+'+50')
        #self.diva.master.overrideredirect(self.diva.always_ontop)
        self.diva.master.wm_iconbitmap(bitmap = "@diva.xbm")



root = Tix.Tk()
app = Questionaire(master=root)
app.mainloop()
