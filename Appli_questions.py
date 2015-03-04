from Tkinter import *
import Tix, ttk


class Application(Frame):


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
		self.envoyer = Button(self.onglet_ue, text = "Envoyer", width = 5, height = 20)
		self.envoyer.grid(column = 5, row = 3)

		self.label_mon_ue = Label(self.onglet_ue, text="Description Web and cloud ").grid(column=1, row=0, columnspan = 1)


		#scroll barre pour la zone de texte editable + zone de texte editable pour l'ue
		self.scroll_texte_mon_ue_V = Scrollbar(self.onglet_ue, orient = VERTICAL) 
		self.texte_mon_ue = Text(self.onglet_ue, width = 75, height = 20, wrap = WORD)  
		self.texte_mon_ue.config(yscrollcommand = self.scroll_texte_mon_ue_V.set) 
		self.scroll_texte_mon_ue_V.config(command = self.texte_mon_ue.yview)
		self.scroll_texte_mon_ue_V.grid(column = 4, row = 1, rowspan = 5, sticky = S + N)
		self.texte_mon_ue.grid(column = 0, row = 1, columnspan = 3, rowspan = 5)

		#zone review
		self.label_review_mon_ue = Label(self.onglet_ue, text="Les review de mon UE").grid(column = 1, row = 6, columnspan = 1)

		self.scroll_review_mon_ue_V = Scrollbar(self.onglet_ue, orient = VERTICAL) 
		self.review_mon_ue = Text(self.onglet_ue, width = 75, height = 20, wrap = WORD)  
		self.review_mon_ue.config(yscrollcommand = self.scroll_review_mon_ue_V.set) 
		self.scroll_review_mon_ue_V.config(command = self.review_mon_ue.yview)
		self.scroll_review_mon_ue_V.grid(column = 4, row = 7, rowspan = 8, sticky = S + N)
		self.review_mon_ue.grid(column = 0, row = 7, columnspan = 3, rowspan = 8)

		#boutons de maj
		self.label_maj_review_mon_ue = Label(self.onglet_ue, text="Maj de").grid(column=5, row=7, columnspan = 1)

		self.usr1 = Button(self.onglet_ue, text = "USR 1", width = 5, height = 1)
		self.usr1.grid(column = 5, row = 8)

		self.usr2 = Button(self.onglet_ue, text = "USR 2", width = 5, height = 1)
		self.usr2.grid(column = 5, row = 9)

		self.usr3 = Button(self.onglet_ue, text = "USR 3", width = 5, height = 1)
		self.usr3.grid(column = 5, row = 10)


		self.usr4 = Button(self.onglet_ue, text = "USR 4", width = 5, height = 1)
		self.usr4.grid(column = 5, row = 11)


		self.usr5 = Button(self.onglet_ue, text = "USR 5", width = 5, height = 1)
		self.usr5.grid(column = 5, row = 12)


		self.usr6 = Button(self.onglet_ue, text = "USR 6", width = 5, height = 1)
		self.usr6.grid(column = 5, row = 13)


		self.usr7 = Button(self.onglet_ue, text = "USR 7", width = 5, height = 1)
		self.usr7.grid(column = 5, row = 14)




	def createWidgetsInReview(self, master):

		#liste deroulant pour choisir une ue (pas la meme que la precedente, on utilisera pas la meme fontion
		self.choix_ue_a_review = Tix.ComboBox(self.onglet_review,  listwidth = 30)
		self.choix_ue_a_review.entry.config(width = 10,state = 'readonly')
		for i in range(0, len(self.liste_ue)-2):
			self.choix_ue_a_review.insert(0, i)
		self.choix_ue_a_review.grid(column = 0, row = 0, sticky = E)

		#zone de texte pour afficher l'ue (meme principe que pour l'onglet ue)

		self.ue_choisie = Text(self.onglet_review, width = 55, height = 3, wrap = WORD)
		self.ue_choisie.config(state = DISABLED)
		self.ue_choisie.grid(column = 1, row = 0,  columnspan = 2, sticky = W)

		#affichage de la reponse dans une zone de texte non editable
		self.label_reponse = Label(self.onglet_review, text="Reponse: ").grid(column=0, row=1)
		self.scroll_reponse_ue_V = Scrollbar(self.onglet_review, orient = VERTICAL) 
		self.reponse_ue = Text(self.onglet_review, width = 55, height = 6, wrap = WORD)
		self.reponse_ue.config(state = DISABLED, yscrollcommand = self.scroll_reponse_ue_V.set)
		self.scroll_reponse_ue_V.config(command = self.reponse_ue.yview)
		self.scroll_reponse_ue_V.grid(column = 3, row = 1, sticky = S + N)
		self.reponse_ue.grid(column = 1, row = 1,  columnspan = 2, sticky = W)

		#affichage des commentaire dans une zone de texte non editable
		self.lable_review = Label(self.onglet_review, text="review: ").grid(column=0, row=2)
		self.scroll_review_V = Scrollbar(self.onglet_review, orient = VERTICAL) 
		self.review = Text(self.onglet_review, width = 55, height = 6, wrap = WORD)
		self.review.insert(INSERT, "Quel est le nom de la princesse dans la seie de jeux video The legend of Zelda ?")
		self.review.config(state = DISABLED, yscrollcommand = self.scroll_review_V.set)
		self.scroll_review_V.config(command = self.review.yview)
		self.scroll_review_V.grid(column = 3, row = 2, sticky = S + N)
		self.review.grid(column = 1, row = 2,  columnspan = 2, sticky = W)

		#bouton qui sert a faire un pull
		self.recuperer = Button(self.onglet_review, text = "Mise a jour\nreponse &\nreview", width = 10, height = 12)
		self.recuperer.grid(column = 4, row = 1, rowspan=2)

		#bouton pour poster un commentaire
		self.post = Button(self.onglet_review, text = "Post", width = 10, height = 7)
		self.post.grid(column = 4, row = 3)

		#zone de texte editable pour ecrire un commentaire
		self.label_mon_review = Label(self.onglet_review, text="Votre\nreview: ").grid(column=0, row=3)
		self.scroll_mon_review_V = Scrollbar(self.onglet_review, orient = VERTICAL) 
		self.texte_mon_review = Text(self.onglet_review, width = 55, height = 7, wrap = WORD)  
		self.texte_mon_review.config(yscrollcommand = self.scroll_mon_review_V.set) 
		self.scroll_mon_review_V.config(command = self.texte_mon_review.yview)
		self.scroll_mon_review_V.grid(column = 3, row = 3, rowspan = 5, sticky = S + N)
		self.texte_mon_review.grid(column = 1, row = 3, columnspan = 2)

    	def __init__(self, master=None):
		Frame.__init__(self, master)
		master.title("Interface Tkinter")
		self.liste_ue = []

		self.createTabs(master)
		self.createWidgetsInUE(master)
		self.createWidgetsInReview(master)


root = Tix.Tk()
app = Application(master=root)
app.mainloop()
