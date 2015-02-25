from Tkinter import *
import Tix, ttk


class Application(Frame):

	def importer_questions(self, master):
		fichier_question = open("questions.txt")
		contenu = fichier_question.read()
		self.liste_questions = contenu.split("\n")
		fichier_question.close()

	def changer_question(self, t):

		self.question.config(state = NORMAL)

		self.question.config(state = DISABLED)

	def changer_question_com(self, t):
		print t
		self.question2.config(state = NORMAL)
		x = int(t)
		self.question2.delete(1.0, END)
		self.question2.insert(INSERT, self.liste_questions[x])
		self.question2.config(state = DISABLED)
	
	def createTabs(self, master):
		#definition des onglets
		self.notebook = Tix.NoteBook(master, width = 630);
		self.notebook.add("questions", label = "Questions")
		self.notebook.add("commentaires", label = "Commentaires")
		self.notebook.grid(column = 0, row = 0)

		#onglet questions
		self.questions = self.notebook.subwidget_list["questions"]
		#contient tous les widget de l'onglet question
		self.onglet_question = Frame(self.questions)
		self.onglet_question.grid(column = 0, row = 0)

		#onglet commentaires
		self.commentaires = self.notebook.subwidget_list["commentaires"]
		#contient tous les widget de l'onglet commentaire
		self.onglet_commentaires = Frame(self.commentaires)
		self.onglet_commentaires.grid(column = 0, row = 0)

	def createWidgetsInQuestion(self, master):

		#bouton qui sert a faire un commit
		self.envoyer = Button(self.onglet_question, text = "envoyer", width = 5, height = 20)
		self.envoyer.grid(column = 5, row = 3)

		#zone de texte non editable qui contient la question choisie
		self.question = Text(self.onglet_question, width = 60, height = 3, wrap = WORD)
		#pour editer la zone de texte il faut la rendre editable avant, puis la remettre non editable
		self.question.insert(INSERT, "Quel est le nom de la princesse dans la seie de jeux video The legend of Zelda ?")
		self.question.config(state = DISABLED)
		self.question.grid(column = 1, row = 0,  columnspan = 2, sticky = W)

		#scroll barre pour la zone de texte editable + zone de texte editable pour repondre a la question
		self.scroll_texte_V = Scrollbar(self.onglet_question, orient = VERTICAL) 
		self.texte = Text(self.onglet_question, width = 75, height = 20, wrap = WORD)  
		self.texte.config(yscrollcommand = self.scroll_texte_V.set) 
		self.scroll_texte_V.config(command = self.texte.yview)
		self.scroll_texte_V.grid(column = 4, row = 1, rowspan = 5, sticky = S + N)
		self.texte.grid(column = 0, row = 1, columnspan = 3, rowspan = 5)

		#liste deroulant pour choisir une question
		self.choix_question = Tix.ComboBox(self.onglet_question,  listwidth = 30, command=self.changer_question)
		self.choix_question.entry.config(width = 10,state = 'readonly')
		self.choix_question.insert(0, "Question 1")
		self.choix_question.insert(1, "Question 2")
		self.choix_question.insert(2, "Question 3")
		self.choix_question.grid(column = 0, row = 0, sticky = E)


	def createWidgetsInCommentaire(self, master):

		#liste deroulant pour choisir une question (pas la meme que la precedente, on utilisera pas la meme fontion
		self.choix_question_a_com = Tix.ComboBox(self.onglet_commentaires,  listwidth = 30, command=self.changer_question_com)
		self.choix_question_a_com.entry.config(width = 10,state = 'readonly')
		for i in range(0, len(self.liste_questions)-2):
			self.choix_question_a_com.insert(0, i)
		self.choix_question_a_com.grid(column = 0, row = 0, sticky = E)

		#zone de texte pour afficher la question (meme principe que pour l'onglet question)

		self.question2 = Text(self.onglet_commentaires, width = 55, height = 3, wrap = WORD)
		self.question2.config(state = DISABLED)
		self.question2.grid(column = 1, row = 0,  columnspan = 2, sticky = W)

		#affichage de la reponse dans une zone de texte non editable
		self.l=Label(self.onglet_commentaires, text="Reponse: ").grid(column=0, row=1)
		self.scroll_reponse_question_V = Scrollbar(self.onglet_commentaires, orient = VERTICAL) 
		self.reponse_question = Text(self.onglet_commentaires, width = 55, height = 6, wrap = WORD)
		self.reponse_question.config(state = DISABLED, yscrollcommand = self.scroll_reponse_question_V.set)
		self.scroll_reponse_question_V.config(command = self.reponse_question.yview)
		self.scroll_reponse_question_V.grid(column = 3, row = 1, sticky = S + N)
		self.reponse_question.grid(column = 1, row = 1,  columnspan = 2, sticky = W)

		#affichage des commentaire dans une zone de texte non editable
		self.l2=Label(self.onglet_commentaires, text="Commentaires: ").grid(column=0, row=2)
		self.scroll_coms_V = Scrollbar(self.onglet_commentaires, orient = VERTICAL) 
		self.coms = Text(self.onglet_commentaires, width = 55, height = 6, wrap = WORD)
		self.coms.insert(INSERT, "Quel est le nom de la princesse dans la seie de jeux video The legend of Zelda ?")
		self.coms.config(state = DISABLED, yscrollcommand = self.scroll_coms_V.set)
		self.scroll_coms_V.config(command = self.coms.yview)
		self.scroll_coms_V.grid(column = 3, row = 2, sticky = S + N)
		self.coms.grid(column = 1, row = 2,  columnspan = 2, sticky = W)

		#bouton qui sert a faire un pull
		self.recuperer = Button(self.onglet_commentaires, text = "Mise a jour\nreponse &\ncommentaires", width = 10, height = 12)
		self.recuperer.grid(column = 4, row = 1, rowspan=2)

		#bouton pour poster un commentaire
		self.post = Button(self.onglet_commentaires, text = "Post", width = 10, height = 7)
		self.post.grid(column = 4, row = 3)

		#zone de texte editable pour ecrire un commentaire
		self.l3=Label(self.onglet_commentaires, text="Votre\ncommentaire: ").grid(column=0, row=3)
		self.scroll_texte_commentaire_V = Scrollbar(self.onglet_commentaires, orient = VERTICAL) 
		self.texte_commentaire = Text(self.onglet_commentaires, width = 55, height = 7, wrap = WORD)  
		self.texte_commentaire.config(yscrollcommand = self.scroll_texte_commentaire_V.set) 
		self.scroll_texte_commentaire_V.config(command = self.texte.yview)
		self.scroll_texte_commentaire_V.grid(column = 3, row = 3, rowspan = 5, sticky = S + N)
		self.texte_commentaire.grid(column = 1, row = 3, columnspan = 2)

    	def __init__(self, master=None):
		Frame.__init__(self, master)
		master.title("Interface Tkinter")
		self.liste_questions = []
		self.importer_questions(master)
		self.createTabs(master)
		self.createWidgetsInQuestion(master)
		self.createWidgetsInCommentaire(master)


root = Tix.Tk()
app = Application(master=root)
app.mainloop()
