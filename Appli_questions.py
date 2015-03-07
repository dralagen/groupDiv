from Tkinter import *
import Tix, ttk
from datetime import datetime

# On part du principe que tous les fichier de review et sur les ue existent deja

class Application(Frame):

	def charger_review(self):
		self.les_review.clear()
		temp = {}
		for usr in self.liste_usr:
			nom_fichier = "review_" +usr+".txt"
			fichier = open(nom_fichier, "r")
			contenu_fichier = fichier.readlines()
			temp[usr] = contenu_fichier				
			fichier.close()
		#ici temp contient les contenu de chaque fichier de chaque usr
		while temp != {}:
			maxi = 999999
			k = ""
			v = ""
			for key in temp:
				nombre = temp[key][0][0:6]
				if int(nombre) < maxi:
					maxi = int(nombre)
					k = key
			v = temp[k][0]
			mes_donnees = v.split("|")
			if self.les_review.has_key(mes_donnees[1]):
				p = mes_donnees[1]
				self.les_review[p].append(mes_donnees[2])
			else:
				self.les_review[mes_donnees[1]] = [mes_donnees[2]]
			temp[k].remove(v)
			if temp[k] == []:
				del temp[k]

	
	def string_review(self, ue):
		mes_review = ""
		for value in self.les_review[ue]:
			mes_review += value 
		return mes_review


	def envoyer_mon_ue(self):
		nom_fichier = "texte_" + self.mon_ue + ".txt"
		fichier = open(nom_fichier, "w")
		fichier.write(self.texte_mon_ue.get(1.0, END))
		fichier.close()
		self.commit()
	
	def charger_texte(self, nom_ue):
		nom_fichier = "texte_" + nom_ue + ".txt"
		fichier = open(nom_fichier, "r")
		contenu_fichier = fichier.readlines()
		fichier.close()
		retour = ""
		for ligne in contenu_fichier:
			retour += ligne
		return retour

	def poster_commentaire(self):
		nom_fichier = "review_" + self.nom_usr + ".txt"
		fichier = open(nom_fichier, "a")
		maintenant = datetime.now()
		fichier.write(str(maintenant.hour) + str(maintenant.minute) + str(maintenant.second) +" " + self.choix_ue_a_review.entry.get() + " " +  self.texte_mon_review.get(1.0, END))
		self.texte_mon_review.delete(1.0, END)
		fichier.close()
		self.commit()

	def commit(self):
		print("je commit")

	#pour pull un usr, cette methode est utilisee par les sept boutons de pull, le parametre usr sert a connaitre quel bouton est utilise
	def pull_un_usr(self, usr):
		print(usr)

	#methode a utiliser pour afficher les infos liees a une ue
	def changer_UE(self, evt):
		self.reponse_ue.config(state = NORMAL)
		self.reponse_ue.delete(1.0, END)
		self.reponse_ue.insert(END, self.charger_texte(self.choix_ue_a_review.entry.get()))
		self.reponse_ue.config(state = DISABLED)

		self.review.config(state = NORMAL)
		self.review.delete(1.0, END)
		self.review.insert(END, self.string_review(self.choix_ue_a_review.entry.get()))
		self.review.config(state = DISABLED)


	#FIN METHODES ACTION


	def createTabs(self, master):
		#definition des onglets
		self.notebook = Tix.NoteBook(master, width = 630);
		self.notebook.add("ue", label = "UE")
		self.notebook.add("review", label = "Review")
		self.notebook.grid(column = 0, row = 0)

		#onglet ue
		self.ue = self.notebook.subwidget_list["ue"]
		#contient tous les widget de l'onglet question
		self.onglet_ue = Frame(self.ue)
		self.onglet_ue.grid(column = 0, row = 0)

		#onglet review
		self.review = self.notebook.subwidget_list["review"]
		#contient tous les widget de l'onglet commentaire
		self.onglet_review = Frame(self.review)
		self.onglet_review.grid(column = 0, row = 0)

	def createWidgetsInUE(self, master):

		#bouton qui sert a faire un commit
		self.envoyer = Button(self.onglet_ue, text = "Envoyer", width = 5, height = 20, command=self.envoyer_mon_ue)
		self.envoyer.grid(column = 5, row = 3)

		self.label_mon_ue = Label(self.onglet_ue, text="Description " + self.mon_ue).grid(column=1, row=0, columnspan = 1)


		#scroll barre pour la zone de texte editable + zone de texte editable pour l'ue
		self.scroll_texte_mon_ue_V = Scrollbar(self.onglet_ue, orient = VERTICAL) 
		self.texte_mon_ue = Text(self.onglet_ue, width = 75, height = 20, wrap = WORD)  
		self.texte_mon_ue.config(yscrollcommand = self.scroll_texte_mon_ue_V.set) 
		self.texte_mon_ue.insert(END, self.charger_texte(self.mon_ue))
		self.scroll_texte_mon_ue_V.config(command = self.texte_mon_ue.yview)
		self.scroll_texte_mon_ue_V.grid(column = 4, row = 1, rowspan = 5, sticky = S + N)
		self.texte_mon_ue.grid(column = 0, row = 1, columnspan = 3, rowspan = 5)

		#zone review
		self.label_review_mon_ue = Label(self.onglet_ue, text="Les review de mon UE").grid(column = 1, row = 6, columnspan = 1)

		self.scroll_review_mon_ue_V = Scrollbar(self.onglet_ue, orient = VERTICAL) 
		self.review_mon_ue = Text(self.onglet_ue, width = 75, height = 20, wrap = WORD)  
		self.review_mon_ue.insert(END, self.string_review(self.mon_ue))
		self.review_mon_ue.config(state = DISABLED, yscrollcommand = self.scroll_review_mon_ue_V.set) 
		self.scroll_review_mon_ue_V.config(command = self.review_mon_ue.yview)
		self.scroll_review_mon_ue_V.grid(column = 4, row = 7, rowspan = 8, sticky = S + N)
		self.review_mon_ue.grid(column = 0, row = 7, columnspan = 3, rowspan = 8)

		#boutons de maj
		self.label_maj_review_mon_ue = Label(self.onglet_ue, text="Maj de").grid(column=5, row=7, columnspan = 1)

		self.usr1 = Button(self.onglet_ue, text = "USR 1", width = 5, height = 1)
		self.usr1.config(command = lambda x="usr1":self.pull_un_usr(x))
		self.usr1.grid(column = 5, row = 8)

		self.usr2 = Button(self.onglet_ue, text = "USR 2", width = 5, height = 1)
		self.usr2.config(command = lambda x="usr2":self.pull_un_usr(x))
		self.usr2.grid(column = 5, row = 9)

		self.usr3 = Button(self.onglet_ue, text = "USR 3", width = 5, height = 1)
		self.usr3.config(command = lambda x="usr3":self.pull_un_usr(x))		
		self.usr3.grid(column = 5, row = 10)


		self.usr4 = Button(self.onglet_ue, text = "USR 4", width = 5, height = 1)
		self.usr4.config(command = lambda x="usr4":self.pull_un_usr(x))		
		self.usr4.grid(column = 5, row = 11)


		self.usr5 = Button(self.onglet_ue, text = "USR 5", width = 5, height = 1)
		self.usr5.config(command = lambda x="usr5":self.pull_un_usr(x))		
		self.usr5.grid(column = 5, row = 12)


		self.usr6 = Button(self.onglet_ue, text = "USR 6", width = 5, height = 1)
		self.usr6.config(command = lambda x="usr6":self.pull_un_usr(x))		
		self.usr6.grid(column = 5, row = 13)


		self.usr7 = Button(self.onglet_ue, text = "USR 7", width = 5, height = 1)
		self.usr7.config(command = lambda x="usr7":self.pull_un_usr(x))		
		self.usr7.grid(column = 5, row = 14)




	def createWidgetsInReview(self, master):

		#liste deroulant pour choisir une ue (pas la meme que la precedente, on utilisera pas la meme fontion
		self.choix_ue_a_review = Tix.ComboBox(self.onglet_review,  listwidth = 150)
		self.choix_ue_a_review.slistbox.listbox.bind('<ButtonRelease-1>', self.changer_UE)
		self.choix_ue_a_review.entry.config(width = 45,state = 'readonly')

		self.choix_ue_a_review.insert(0, "Web and cloud")
		self.choix_ue_a_review.insert(0, "Web semantique")
		self.choix_ue_a_review.insert(0, "Verification et test")
		self.choix_ue_a_review.insert(0, "Concepts et outils de developpement")
		self.choix_ue_a_review.insert(0, "Anglais 1 & 2")
		self.choix_ue_a_review.insert(0, "Techniques de communication & Connaissances de l'entreprise")
		self.choix_ue_a_review.insert(0, "Temps reel")
		self.choix_ue_a_review.insert(0, "SGBD")
		self.choix_ue_a_review.insert(0, "Genie logiciel")

		self.choix_ue_a_review.insert(0, "IHM")
		self.choix_ue_a_review.insert(0, "Conception de logiciel extensible")
		self.choix_ue_a_review.insert(0, "Structure de donnee & Complexitee")
		self.choix_ue_a_review.insert(0, "Constraint programming & Multicore programming")
		self.choix_ue_a_review.insert(0, "Recherche")
		self.choix_ue_a_review.insert(0, "Compilation")
		self.choix_ue_a_review.insert(0, "Reseaux")
	
		self.choix_ue_a_review.pick(0)

		self.choix_ue_a_review.grid(column = 1, row = 0, columnspan=2, sticky = W)


		#affichage de la reponse dans une zone de texte non editable
		self.label_reponse = Label(self.onglet_review, text="Reponse: ", font=(30)).grid(column=0, row=2)
		self.scroll_reponse_ue_V = Scrollbar(self.onglet_review, orient = VERTICAL) 
		self.reponse_ue = Text(self.onglet_review, width = 65, height = 15, wrap = WORD)
		self.reponse_ue.insert(END, self.charger_texte(self.choix_ue_a_review.entry.get()))
		self.reponse_ue.config(state = DISABLED, yscrollcommand = self.scroll_reponse_ue_V.set)

		self.scroll_reponse_ue_V.config(command = self.reponse_ue.yview)
		self.scroll_reponse_ue_V.grid(column = 3, row = 1, rowspan=3, sticky = S + N)
		self.reponse_ue.grid(column = 1, row = 1,  columnspan = 2, rowspan=3, sticky = W)

		#affichage des review dans une zone de texte non editable
		self.lable_review = Label(self.onglet_review, text="Review: ", font=(30)).grid(column=0, row=5)
		self.scroll_review_V = Scrollbar(self.onglet_review, orient = VERTICAL) 
		self.review = Text(self.onglet_review, width = 65, height = 20, wrap = WORD)
		self.review.insert(END, self.string_review(self.choix_ue_a_review.entry.get()))
		self.review.config(state = DISABLED, yscrollcommand = self.scroll_review_V.set)
		self.scroll_review_V.config(command = self.review.yview)
		self.scroll_review_V.grid(column = 3, row = 4, rowspan=4 , sticky = S + N)
		self.review.grid(column = 1, row = 4,  columnspan = 2, rowspan=4, sticky = W)

		#bouton qui sert a faire un pull
		self.lable_review = Label(self.onglet_review, text="MAJ de ", font=(30)).grid(column=4, row=0)


		self.recuperer = Button(self.onglet_review, text = "USR 1", width = 5, height = 1, command = lambda x="usr1":self.pull_un_usr(x))
		self.recuperer.grid(column = 4, row = 1)

		self.recuperer = Button(self.onglet_review, text = "USR 2", width = 5, height = 1, command = lambda x="usr2":self.pull_un_usr(x))
		self.recuperer.grid(column = 4, row = 2)

		self.recuperer = Button(self.onglet_review, text = "USR 3", width = 5, height = 1, command = lambda x="usr3":self.pull_un_usr(x))
		self.recuperer.grid(column = 4, row = 3)

		self.recuperer = Button(self.onglet_review, text = "USR 4", width = 5, height = 1, command = lambda x="usr4":self.pull_un_usr(x))
		self.recuperer.grid(column = 4, row = 4)

		self.recuperer = Button(self.onglet_review, text = "USR 5", width = 5, height = 1, command = lambda x="usr5":self.pull_un_usr(x))
		self.recuperer.grid(column = 4, row = 5)

		self.recuperer = Button(self.onglet_review, text = "USR 6", width = 5, height = 1, command = lambda x="usr6":self.pull_un_usr(x))
		self.recuperer.grid(column = 4, row = 6)

		self.recuperer = Button(self.onglet_review, text = "USR 7", width = 5, height = 1, command = lambda x="usr7":self.pull_un_usr(x))
		self.recuperer.grid(column = 4, row = 7)



		#bouton pour poster un commentaire
		self.post = Button(self.onglet_review, text = "Post", width = 5, height = 5, command = self.poster_commentaire)
		self.post.grid(column = 4, row = 9)

		#zone de texte editable pour ecrire un commentaire
		self.label_mon_review = Label(self.onglet_review, text="Votre\nreview: ", font=(30)).grid(column=0, row=9)
		self.scroll_mon_review_V = Scrollbar(self.onglet_review, orient = VERTICAL) 
		self.texte_mon_review = Text(self.onglet_review, width = 65, height = 5, wrap = WORD)  
		self.texte_mon_review.config(yscrollcommand = self.scroll_mon_review_V.set) 
		self.scroll_mon_review_V.config(command = self.texte_mon_review.yview)
		self.scroll_mon_review_V.grid(column = 3, row = 9, sticky = S + N)
		self.texte_mon_review.grid(column = 1, row = 9, columnspan = 2)

    	def __init__(self, master=None):
		Frame.__init__(self, master)
		master.title("Interface Tkinter")
		self.nom_usr = "usr8"
		self.liste_usr = ["usr1", "usr2"]

		self.liste_ue = ["Web and cloud", "Reseaux"]
		self.les_review = {}
		self.mon_ue = "Web and cloud"
		self.charger_review()
		self.createTabs(master)
		self.createWidgetsInUE(master)
		self.createWidgetsInReview(master)


root = Tix.Tk()
app = Application(master=root)
app.mainloop()
