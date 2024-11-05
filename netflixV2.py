import tkinter as tk
from tkinter import ttk, messagebox

## DOTO:
# Précharger des cartes de crédit pour les clients Ligne 265
# Ajouter les interfaces pour l'ajout/modification des catégories
# Implémenter Employee (Date d'embauche, code utilisateur, password et type d'accès (Admin, Employé, Client))
# Voir comment intégrer Employee au login client déjà fonctionnel
# Faire les tests unitaires selon la vidéo

# Classe Personne
class Personne:
    def __init__(self, nom, prenom, sexe):
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe

# Classe Client qui hérite de la classe Personne
class Client(Personne): 
    def __init__(self, nom, prenom, sexe, date_inscription, courriel, password, cartes_credit=None):
        super().__init__(nom, prenom, sexe) #Hugues Ref: https://docs.python.org/2/library/functions.html#super + https://www.delftstack.com/fr/howto/python/python-super/
        self.date_inscription = date_inscription
        self.courriel = courriel
        self.password = password
        self.cartes_credit = cartes_credit if cartes_credit is not None else []
        #self.precharger_cartes_credit()

    def ajouter_carte_credit(self, carte_credit):
        self.cartes_credit.append(carte_credit)

    def afficher_cartes_credit(self):
        for carte in self.cartes_credit:
            print(f"Numéro: {carte.numeroCarte}, Expiration: {carte.dateExpiration}, Code: {carte.codeSecret}")
 
# Section Definition des classes pour les Acteurs qui hérite de la classe Personne
class Acteur(Personne):
    def __init__(self, nom, prenom, sexe, nom_personnage, cachet, Debut_emploi, Fin_emploi ):
        super().__init__(nom, prenom, sexe)
        self.nom_personnage = nom_personnage
        #self.cachet = cachet
        self.cachet = float(cachet)  # cachet est défini comme un nombre flottant
        self.Debut_emploi = Debut_emploi
        self.Fin_emploi = Fin_emploi
        self.films = []

    def ajouter_film(self, film):
        if film not in self.films:
            self.films.append(film)    
    
    def afficher_cachet_en_dollars(self):
        return f"${self.cachet:,.2f}"

# Section Definition des classes pour les FILMS
class Film:
    def __init__(self, titre, genre, annee, duree):
        self.titre = titre
        #self.genre = genre
        self.genres = genre if isinstance(genre, list) else [genre]
        self.annee = annee
        self.duree = duree

    def ajouter_genre(self, genre):
        if genre not in self.genres:
            self.genres.append(genre)

class Categorie(Film):
    def __init__(self, titre, genre, annee, duree, categorie, description):
        super().__init__(titre, genre, annee, duree)
        self.nom_categorie = categorie
        self.description_categorie = description
class AfficherFilmWindow:
    def __init__(self, root, film, acteurs):
        self.root = root
        self.film = film
        self.acteurs = acteurs
        self.root.title(f"Informations sur le film: {film.titre}")
        self.root.geometry("600x400")

        tk.Label(root, text="Titre:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(root, text=film.titre).grid(row=0, column=1, sticky=tk.W)

        tk.Label(root, text="Genres:").grid(row=1, column=0, sticky=tk.W)
        tk.Label(root, text=", ".join(film.genres)).grid(row=1, column=1, sticky=tk.W)

        tk.Label(root, text="Année:").grid(row=2, column=0, sticky=tk.W)
        tk.Label(root, text=film.annee).grid(row=2, column=1, sticky=tk.W)

        tk.Label(root, text="Durée:").grid(row=3, column=0, sticky=tk.W)
        tk.Label(root, text=film.duree).grid(row=3, column=1, sticky=tk.W)

        tk.Label(root, text="Listes des acteurs:").grid(row=4, column=0, sticky=tk.W)

        # Création de la Treeview pour afficher les acteurs
        self.tree = ttk.Treeview(root, columns=("Nom", "Sexe", "Personnage", "Cachet", "Début emploi", "Fin emploi"), show="headings")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Sexe", text="Sexe")
        self.tree.heading("Personnage", text="Personnage")
        self.tree.heading("Cachet", text="Cachet")
        self.tree.heading("Début emploi", text="Début emploi")
        self.tree.heading("Fin emploi", text="Fin emploi")
        
        # Définir la largeur des colonnes
        self.tree.column("Nom", width=100)
        self.tree.column("Sexe", width=50)
        self.tree.column("Personnage", width=100)
        self.tree.column("Cachet", width=80)
        self.tree.column("Début emploi", width=100)
        self.tree.column("Fin emploi", width=100)

        for acteur in acteurs:
            if film in acteur.films:
                self.tree.insert("", "end", values=(
                    f"{acteur.nom} {acteur.prenom}",
                    acteur.sexe,
                    acteur.nom_personnage,
                    acteur.afficher_cachet_en_dollars(),
                    acteur.Debut_emploi,
                    acteur.Fin_emploi
                ))

        self.tree.grid(row=5, column=0, columnspan=6, sticky="nsew")

        # Ajout des barres de défilement
        scrollbar_y = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=5, column=6, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(root, orient="horizontal", command=self.tree.xview)
        scrollbar_x.grid(row=6, column=0, columnspan=6, sticky="ew")
        self.tree.configure(xscrollcommand=scrollbar_x.set)

        tk.Button(root, text="Fermer", command=self.root.destroy).grid(row=7, column=1, sticky=tk.E)
        
# Section Carte de Crédit ____________________________________________________________________________________________________________________
class CarteCredit:
    def __init__(self, numero_carte, date_expiration, code_secret):
        self.numero_carte = numero_carte
        self.date_expiration = date_expiration
        self.code_secret = code_secret

class CarteCreditGestion:
    def __init__(self, root, client):
        self.root = root
        self.client = client
        self.root.title("Gérer Cartes de Crédit")
        self.root.geometry("400x300")

        tk.Label(root, text="Numéro de Carte").grid(row=0, column=0)
        tk.Label(root, text="Date d'Expiration").grid(row=1, column=0)
        tk.Label(root, text="Code Secret").grid(row=2, column=0)

        self.numero_carte = tk.Entry(root)
        self.date_expiration = tk.Entry(root)
        self.code_secret = tk.Entry(root, show="*")

        self.numero_carte.grid(row=0, column=1)
        self.date_expiration.grid(row=1, column=1)
        self.code_secret.grid(row=2, column=1)

        tk.Button(root, text="Ajouter Carte", command=self.ajouter_carte_credit).grid(row=0, column=2)
        tk.Button(root, text="Modifier Carte", command=self.modifier_carte_credit).grid(row=1, column=2)
        tk.Button(root, text="Supprimer Carte", command=self.supprimer_carte_credit).grid(row=2, column=2)
        tk.Button(root, text="Fermer", command=self.root.destroy).grid(row=3, column=2)

        self.cartes_listbox = tk.Listbox(root)
        self.cartes_listbox.grid(row=3, column=0, columnspan=2)

        # MAJ Listbox lors de la sélection d'une carte
        self.cartes_listbox.bind('<<ListboxSelect>>', self.afficher_carte_selectionnee)

        self.mettre_a_jour_cartes_listbox()

    def ajouter_carte_credit(self):
        numero_carte = self.numero_carte.get()
        date_expiration = self.date_expiration.get()
        code_secret = self.code_secret.get()

        if numero_carte and date_expiration and code_secret:
            carte = CarteCredit(numero_carte, date_expiration, code_secret)
            self.client.ajouter_carte_credit(carte)
            self.mettre_a_jour_cartes_listbox()
        # Effacer les champs de saisie
            self.numero_carte.delete(0, tk.END)
            self.date_expiration.delete(0, tk.END)
            self.code_secret.delete(0, tk.END)

        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")

    def modifier_carte_credit(self):
        selected_index = self.cartes_listbox.curselection()
        if selected_index:
            carte = self.client.cartes_credit[selected_index[0]]
            numero_carte = self.numero_carte.get()
            date_expiration = self.date_expiration.get()
            code_secret = self.code_secret.get()
            if numero_carte and date_expiration and code_secret:
                carte.numero_carte = numero_carte
                carte.date_expiration = date_expiration
                carte.code_secret = code_secret
                self.mettre_a_jour_cartes_listbox()
            # Effacer les champs de saisie
                self.numero_carte.delete(0, tk.END)
                self.date_expiration.delete(0, tk.END)
                self.code_secret.delete(0, tk.END)
            else:
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
        else:
            messagebox.showerror("Erreur", "Aucune carte sélectionnée.")

    def supprimer_carte_credit(self):
        selected_index = self.cartes_listbox.curselection()
        if selected_index:
            del self.client.cartes_credit[selected_index[0]]
            self.mettre_a_jour_cartes_listbox()
            # Effacer les champs de saisie
            self.numero_carte.delete(0, tk.END)
            self.date_expiration.delete(0, tk.END)
            self.code_secret.delete(0, tk.END)
        else:
            messagebox.showerror("Erreur", "Aucune carte sélectionnée.")

    def mettre_a_jour_cartes_listbox(self):
        self.cartes_listbox.delete(0, tk.END)
        for carte in self.client.cartes_credit:
            self.cartes_listbox.insert(tk.END, f"{carte.numero_carte} - {carte.date_expiration}")

    # Afficher les informations de la carte sélectionnée dans les champs de saisie pour la modification
    def afficher_carte_selectionnee(self, event):
        selected_index = self.cartes_listbox.curselection()
        if selected_index:
            carte = self.client.cartes_credit[selected_index[0]]
            self.numero_carte.delete(0, tk.END)
            self.date_expiration.delete(0, tk.END)
            self.code_secret.delete(0, tk.END)
            self.numero_carte.insert(0, carte.numero_carte)
            self.date_expiration.insert(0, carte.date_expiration)
            self.code_secret.insert(0, carte.code_secret)   
# FIN Section Carte de Crédit ____________________________________________________________________________________________________________________

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Ouverture de session")
        
        # Création de la liste des clients (Login avec les informations de connexion)
        self.clients = []

        # Définir la grandeur de la fenêtre (largeur x hauteur)
        self.root.geometry("300x150")

        tk.Label(root, text="Code Utilisateur").grid(row=0, column=0)
        tk.Label(root, text="Mot de Passe").grid(row=1, column=0)
        
        self.code_utilisateur = tk.Entry(root)
        self.mot_de_passe = tk.Entry(root, show="*")
        
        self.code_utilisateur.grid(row=0, column=1)
        self.mot_de_passe.grid(row=1, column=1)
        
        tk.Button(root, text="Login", command=self.login).grid(row=2, column=1)
    
        # Préchargement des données clients dans le LoginWindow pour avoir l'information lors de la connexion
        self.precharger_donnees_clients()
    
    def precharger_donnees_clients(self):
        #carte1 = CarteCredit("1234567890123456", "12/25", "123")
        #carte2 = CarteCredit("6543210987654321", "11/24", "456")
        #carte3 = CarteCredit("7543210987654321", "10/24", "789")
        #carte4 = CarteCredit("8543210987654321", "12/24", "741")
        #client1 = Client("Brisson", "Hugues", "M", "2023-01-01", "hugues@example.com", "password123", )
        client1 = Client("Brisson", "Hugues", "M", "2023-01-01", "q", "q" ) # pour faciliter le login pour les tests
        client2 = Client("Doré", "Sylvie", "F", "2022-05-15", "sylvie@example.com", "password456")
        client3 = Client("Brisson", "Grégory", "M", "2021-09-30", "greg@example.com", "password789")
        
        self.clients.extend([client1, client2, client3])
    
    def login(self):
        code = self.code_utilisateur.get()
        password = self.mot_de_passe.get()
        
        # Vérification des informations de connexion
        if self.verifier_informations(code, password):
            self.root.destroy()
            main_window = tk.Tk()
            MainWindow(main_window, self.clients)
        else:
            messagebox.showerror("Erreur", "Code utilisateur ou mot de passe incorrect")

    def verifier_informations(self, code, password):
        for client in self.clients:
            if client.courriel == code and client.password == password:
                return True
        return False

class MainWindow:
    def __init__(self, root, clients):
        self.root = root
        self.root.title("Fenêtre Principale")
        
        # Définir la grandeur de la fenêtre (largeur x hauteur)
        self.root.geometry("600x500")
       
        # Ancienne liste de clients et de films Sans Taille
        self.clients = clients
        self.films = []  # Liste pour stocker les films
        self.acteurs = [] # Liste pour stocker les acteurs
        self.categories = ["Action", "Comédie", "Drame", "Horreur", "Science-fiction"]  # Liste pour stocker les catégories

        # Préchargement des données clients, films et acteurs
        #self.precharger_donnees_clients() #Déplacer dans la class LoginWindow
        self.precharger_donnees_films()
        self.precharger_donnees_acteurs()
        self.precharger_associations()

        # Affichage des clients
        tk.Label(root, text="Clients").grid(row=0, column=0)
        self.clients_listbox = tk.Listbox(root)
        self.clients_listbox.grid(row=1, column=0)
        
        # Affichage des films
        tk.Label(root, text="Films").grid(row=0, column=1)
        self.films_listbox = tk.Listbox(root)
        self.films_listbox.grid(row=1, column=1)
        #self.films_listbox.bind('<<ListboxSelect>>', self.ouvrir_fenetre_afficher_film)

        #Affichage des Acteurs
        tk.Label(root, text="Acteurs/Personnages").grid(row=0, column=2)
        self.acteurs_listbox = tk.Listbox(root, width=50 )  # Modifier la taille ici)
        self.acteurs_listbox.grid(row=1, column=2)

        # Bouton de déconnexion
        tk.Button(root, text="Déconnexion", command=self.deconnexion).grid(row=6, column=1)

        # Boutons Clients
        tk.Button(root, text="Créer Client", command=self.ouvrir_fenetre_creation_client).grid(row=2, column=0)
        tk.Button(root, text="Modifier Client", command=self.ouvrir_fenetre_modification_client).grid(row=3, column=0)
        tk.Button(root, text="Supprimer Client", command=self.ouvrir_fenetre_suppression_client).grid(row=4, column=0)
        
        # Boutons Films
        tk.Button(root, text="Créer Films", command=self.ouvrir_fenetre_creation_films).grid(row=2, column=1)
        tk.Button(root, text="Modifier Films", command=self.ouvrir_fenetre_modification_films).grid(row=3, column=1)
        tk.Button(root, text="Supprimer Films", command=self.ouvrir_fenetre_suppression_films).grid(row=4, column=1)
        tk.Button(root, text="Informations sur le Film", command=self.ouvrir_fenetre_afficher_film).grid(row=5, column=1)

        # Bouton Gérer Cartes de Crédit
        tk.Button(root, text="Gérer Cartes de Crédit", command=self.ouvrir_fenetre_gestion_cartes).grid(row=5, column=0)

        # Buttons acteurs
        tk.Button(root, text="Créer Acteur/Personnage", command=self.ouvrir_fenetre_creation_acteur).grid(row=2, column=2)
        tk.Button(root, text="Modifier Acteur/Personnage", command=self.ouvrir_fenetre_modification_acteur).grid(row=3, column=2)
        tk.Button(root, text="Supprimer Acteur/Personnage", command=self.ouvrir_fenetre_suppression_acteur).grid(row=4, column=2)

        # Bouton Associer Acteurs et Catégories à un Film
        tk.Button(root, text="Gestion des Acteurs/Personnages et Catégories", command=self.ouvrir_fenetre_associer_acteur_film).grid(row=5, column=2)

        # Mise à jour de la Listbox avec les clients et les films préchargés
        self.mettre_a_jour_clients_listbox()
        self.mettre_a_jour_films_listbox()
        self.mettre_a_jour_acteurs_listbox()

    def ouvrir_fenetre_associer_acteur_film(self): # Bouton Gestion des Acteurs et Catégories
        associer_acteur_film_window = tk.Tk()
        GestionFilmWindow(associer_acteur_film_window, self)
        associer_acteur_film_window.mainloop()
    
    def ouvrir_fenetre_afficher_film(self):
        selection = self.films_listbox.curselection()
        if selection:
            index = selection[0]
            film = self.films[index]
            afficher_film_window = tk.Toplevel(self.root)
            AfficherFilmWindow(afficher_film_window, film, self.acteurs)
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un film pour afficher ces informations.")

    # Vérification si le courriel Existe (Méthode appelé dans la class CreerClientWindow:)
    def verifier_courriel_existant(self, courriel):
        for client in self.clients:
            if client.courriel == courriel:
                return True
        return False
    
    def supprimer_film(self, index):
        if 0 <= index < len(self.films):
            del self.films[index]
            # Mettre à jour l'interface utilisateur si nécessaire
            self.mettre_a_jour_interface()

    def mettre_a_jour_interface(self):
        # Code pour mettre à jour l'interface utilisateur après la suppression d'un film
        pass
    
    def precharger_donnees_films(self):
        film1 = Film("Inception", ["Science-fiction", "Action"], 2010, "2h28m")
        film2 = Film("The Matrix", ["Science-fiction", "Action"], 1999, "2h16m")
        film3 = Film("Titanic", ["Drame", "Romance"], 1997, "3h14m")
        film4 = Film("The Matrix Reloaded", ["Science-fiction", "Action"], 2003, "2h18m")
        film5 = Film("Mr. & Mrs. Smith", ["Action", "Comédie"], 2005, "2h0m")
        self.films.extend([film1, film2, film3, film4, film5])

    def precharger_donnees_acteurs(self):
        acteur1 = Acteur("DiCaprio", "Leonardo", "M", "Cobb", 20000000, "2009-05-15", "2010-07-16")
        acteur2 = Acteur("Pitt", "Brad", "M", "Tyler Durden", 15000000, "1999-10-15", "2000-12-16")
        acteur3 = Acteur("Reeves", "Keanu", "M", "Neo", 70000, "2023-01-01", "2023-12-31")
        acteur4 = Acteur("Smith", "John", "M", "Agent Smith", 50000, "2023-01-01", "2023-12-31")
        acteur5 = Acteur("Doe", "Jane", "F", "Trinity", 60000, "2023-01-01", "2023-12-31")
        acteur6 = Acteur("Kate", "Winslet", "F", "Rose DeWitt Bukater", 1000000, "1996-01-01", "1996-12-31")
        acteur7 = Acteur("levitt", "Joseph", "M", "Arthur", 1000000, "1996-01-01", "1996-12-31")
        acteur8 = Acteur("Angeline", "Jolie", "F", "Jane Smith", 1000000, "1996-01-01", "1996-12-31")
        acteur9 = Acteur("Pit", "Brad", "M", "John Smith", 1000000, "1996-01-01", "1996-12-31")
        self.acteurs.extend([acteur1, acteur2, acteur3, acteur4, acteur5, acteur6, acteur7, acteur8, acteur9])

    def precharger_associations(self):
        # Associer les acteurs aux films
        film1 = self.films[0]  # Inception
        film2 = self.films[1]  # The Matrix
        film3 = self.films[2]  # Titanic
        film4 = self.films[3]  # The Matrix Reloaded
        film5 = self.films[4]  # Mr. & Mrs. Smith
        
        acteur1 = self.acteurs[0]  # Leonardo DiCaprio
        acteur2 = self.acteurs[1]  # Brad Pitt
        acteur3 = self.acteurs[2]  # Keanu Reeves
        acteur4 = self.acteurs[3]  # John Smith
        acteur5 = self.acteurs[4]  # Jane Doe
        acteur6 = self.acteurs[5]  # Kate Winslet
        acteur7 = self.acteurs[6] # Joseph Levitt
        acteur8 = self.acteurs[7] # Angeline Jolie
        acteur9 = self.acteurs[8] # Brad Pit

        acteur1.ajouter_film(film1)  # Leonardo DiCaprio dans Inception
        acteur2.ajouter_film(film2)  # Brad Pitt dans The Matrix
        acteur3.ajouter_film(film2)  # Keanu Reeves dans The Matrix
        acteur4.ajouter_film(film2)  # John Smith dans The Matrix
        acteur5.ajouter_film(film2)  # Jane Doe dans The Matrix
        acteur1.ajouter_film(film3)  # Leonardo DiCaprio dans Titanic
        acteur6.ajouter_film(film3)  # Kate Winslet dans Titanic
        acteur7.ajouter_film(film1)  # Joseph Levitt dans Inception
        acteur7.ajouter_film(film4) # Joseph Levitt dans The Matrix Reloaded
        acteur3.ajouter_film(film4) # Keanu Reeves dans The Matrix Reloaded
        acteur4.ajouter_film(film4) # John Smith dans The Matrix Reloaded
        acteur8.ajouter_film(film5) # Angeline Jolie dans Mr. & Mrs. Smith
        acteur9.ajouter_film(film5) # Brad Pit dans Mr. & Mrs. Smith

    ### Volet Acteurs Création, Modification et Suppression
    def ouvrir_fenetre_creation_acteur(self):
        creer_acteur_window = tk.Tk()
        CreerActeurWindow(creer_acteur_window, self)
        creer_acteur_window.mainloop()
    
    def ouvrir_fenetre_modification_acteur(self):
        selected_index = self.acteurs_listbox.curselection()
        if selected_index:
            acteur = self.acteurs[selected_index[0]]
            modifier_acteur_window = tk.Tk()
            ModifierActeurWindow(modifier_acteur_window, self, acteur, selected_index[0])
            modifier_acteur_window.mainloop()
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un acteur à modifier.")   
    
    def ouvrir_fenetre_suppression_acteur(self):
        selected_index = self.acteurs_listbox.curselection()
        if selected_index:
            acteur = self.acteurs[selected_index[0]]
            confirmation_window = tk.Tk()
            ConfirmationSuppressionWindow_acteur(confirmation_window, self, acteur, selected_index[0])
            confirmation_window.mainloop()
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un acteur à supprimer.")

    def ajouter_acteur(self, acteur):
        self.acteurs.append(acteur)
        self.mettre_a_jour_acteurs_listbox()    

    def modifier_acteur(self, index, acteur_modifie):
        self.acteurs[index] = acteur_modifie
        self.mettre_a_jour_acteurs_listbox()    

    def supprimer_acteur(self, index):
        del self.acteurs[index]
        self.mettre_a_jour_acteurs_listbox()

    def mettre_a_jour_acteurs_listbox(self):
        self.acteurs_listbox.delete(0, tk.END)
        for acteur in self.acteurs:
            self.acteurs_listbox.insert(tk.END, f"||| {acteur.nom_personnage} ||| - {acteur.nom} {acteur.prenom}")
    ## Fin Volet Acteurs
    
    def ouvrir_fenetre_creation_films(self):
        creer_films_window = tk.Tk()
        CreerFilmsWindow(creer_films_window, self)
        creer_films_window.mainloop()

    def ouvrir_fenetre_modification_films(self):
        selected_index = self.films_listbox.curselection()
        if selected_index:
            film = self.films[selected_index[0]]
            modifier_films_window = tk.Tk()
            ModifierFilmsWindow(modifier_films_window, self, film, selected_index[0])
            modifier_films_window.mainloop()
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un film à modifier.")

    def ouvrir_fenetre_suppression_films(self):
        selected_index = self.films_listbox.curselection()
        # if selected_index:
        if selected_index and 0 <= selected_index[0] < len(self.films):
            film = self.films[selected_index[0]]
            confirmation_window = tk.Tk()
            ConfirmationSuppressionWindow_film(confirmation_window, self, film, selected_index[0])
            confirmation_window.mainloop()
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un film à supprimer.")
    
    def ouvrir_fenetre_creation_client(self):
        creer_client_window = tk.Tk()
        # Définir la fenêtre de création du client
        CreerClientWindow(creer_client_window, self)
        creer_client_window.mainloop()
    
    def ouvrir_fenetre_modification_client(self):
        selected_index = self.clients_listbox.curselection()
        if selected_index:
            client = self.clients[selected_index[0]]
            modifier_client_window = tk.Tk()
            # Définir la fenêtre de modification du client
            ModifierClientWindow(modifier_client_window, self, client, selected_index[0])
            modifier_client_window.mainloop()
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un client à modifier.")
    
    def ouvrir_fenetre_suppression_client(self):
        selected_index = self.clients_listbox.curselection()
        if selected_index:
            client = self.clients[selected_index[0]]
            confirmation_window = tk.Tk()
            ConfirmationSuppressionWindow(confirmation_window, self, client, selected_index[0])
            confirmation_window.mainloop()
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un client à supprimer.")
    
    def supprimer_client(self, index):
        del self.clients[index]
        self.mettre_a_jour_clients_listbox()
    
    def deconnexion(self):
        self.root.destroy()
        login_window = tk.Tk()
        LoginWindow(login_window)
    
    def ajouter_client(self, client):
        self.clients.append(client)
        self.mettre_a_jour_clients_listbox()
    
    def ajouter_film(self, film):
        self.films.append(film)
        self.mettre_a_jour_films_listbox()
    
    def supprimer_film(self, index):
        del self.films[index]
        self.mettre_a_jour_films_listbox()

    def mettre_a_jour_clients_listbox(self):
        self.clients_listbox.delete(0, tk.END)
        for client in self.clients:
            self.clients_listbox.insert(tk.END, f"{client.nom} {client.prenom} - {client.courriel}")
    
    def mettre_a_jour_films_listbox(self):
        self.films_listbox.delete(0, tk.END)
        for film in self.films:
            self.films_listbox.insert(tk.END, f"{film.titre} - ({film.annee})")
    
    def modifier_client(self, index, client_modifie):
        self.clients[index] = client_modifie
        self.mettre_a_jour_clients_listbox()

    def modifier_film(self, index, film_modifie):
        self.films[index] = film_modifie
        self.mettre_a_jour_films_listbox()

    def ouvrir_fenetre_gestion_cartes(self):
        selected_index = self.clients_listbox.curselection()
        if selected_index:
            client = self.clients[selected_index[0]]
            gestion_cartes_window = tk.Tk()
            CarteCreditGestion(gestion_cartes_window, client)
            gestion_cartes_window.mainloop()
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un client pour gérer ses cartes de crédit.")

class CreerActeurWindow:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window
        self.root.title("Créer Acteur/Personnage")
        self.root.geometry("300x200")
        tk.Label(root, text="Nom").grid(row=0, column=0)
        tk.Label(root, text="Prénom").grid(row=1, column=0)
        tk.Label(root, text="Sexe").grid(row=2, column=0)
        tk.Label(root, text="Nom Personnage").grid(row=3, column=0)
        tk.Label(root, text="Cachet").grid(row=4, column=0)
        tk.Label(root, text="Début Emploi").grid(row=5, column=0)
        tk.Label(root, text="Fin Emploi").grid(row=6, column=0)
        
        self.nom = tk.Entry(root)
        self.prenom = tk.Entry(root)
        self.sexe = tk.Entry(root)
        self.nom_personnage = tk.Entry(root)
        self.cachet = tk.Entry(root)
        self.Debut_emploi = tk.Entry(root)
        self.Fin_emploi = tk.Entry(root)
        
        self.nom.grid(row=0, column=1)
        self.prenom.grid(row=1, column=1)
        self.sexe.grid(row=2, column=1)
        self.nom_personnage.grid(row=3, column=1)
        self.cachet.grid(row=4, column=1)
        self.Debut_emploi.grid(row=5, column=1)
        self.Fin_emploi.grid(row=6, column=1)
        
        tk.Button(root, text="Créer", command=self.creer_acteur).grid(row=7, column=1)
    
    def creer_acteur(self):
       nom = self.nom.get()
       prenom = self.prenom.get()
       sexe = self.sexe.get()
       nom_personnage = self.nom_personnage.get()
       cachet = self.cachet.get()
       debut_emploi = self.Debut_emploi.get()
       fin_emploi = self.Fin_emploi.get()
    
        # validation des données    
       if not nom or not prenom or not sexe or not cachet or not debut_emploi or not fin_emploi:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
            return

       try:
            cachet = float(cachet)  # Convertir cachet en nombre flottant
       except ValueError:
            messagebox.showerror("Erreur", "Le cachet doit être un nombre")
            return
                   
        #création de l'acteur et ajout à la liste
       acteur = Acteur(nom, prenom, sexe, nom_personnage, cachet, debut_emploi, fin_emploi)
       self.main_window.ajouter_acteur(acteur)
       self.root.destroy() 

class ModifierActeurWindow:
    def __init__(self, root, main_window, acteur, index):
        self.root = root
        self.main_window = main_window
        self.acteur = acteur
        self.index = index
        self.root.title("Modifier Acteur/Personnage")
        self.root.geometry("300x200")
        tk.Label(root, text="Nom").grid(row=0, column=0)
        tk.Label(root, text="Prénom").grid(row=1, column=0)
        tk.Label(root, text="Sexe").grid(row=2, column=0)
        tk.Label(root, text="Nom Personnage").grid(row=3, column=0)
        tk.Label(root, text="Cachet").grid(row=4, column=0)
        tk.Label(root, text="Début Emploi").grid(row=5, column=0)
        tk.Label(root, text="Fin Emploi").grid(row=6, column=0)
        
        self.nom = tk.Entry(root)
        self.prenom = tk.Entry(root)
        self.sexe = tk.Entry(root)
        self.nom_personnage = tk.Entry(root)
        self.cachet = tk.Entry(root)
        self.Debut_emploi = tk.Entry(root)
        self.Fin_emploi = tk.Entry(root)
        
        self.nom.grid(row=0, column=1)
        self.prenom.grid(row=1, column=1)
        self.sexe.grid(row=2, column=1)
        self.nom_personnage.grid(row=3, column=1)
        self.cachet.grid(row=4, column=1)
        self.Debut_emploi.grid(row=5, column=1)
        self.Fin_emploi.grid(row=6, column=1)
        
        # Pré-remplir les champs avec les informations actuelles de l'acteur
        self.nom.insert(0, acteur.nom)
        self.prenom.insert(0, acteur.prenom)
        self.sexe.insert(0, acteur.sexe)
        self.nom_personnage.insert(0, acteur.nom_personnage)
        self.cachet.insert(0, acteur.cachet)
        self.Debut_emploi.insert(0, acteur.Debut_emploi)
        self.Fin_emploi.insert(0, acteur.Fin_emploi)
        
        tk.Button(root, text="Modifier", command=self.modifier_acteur).grid(row=7, column=1)
    
    def modifier_acteur(self):
        nom = self.nom.get()
        prenom = self.prenom.get()
        sexe = self.sexe.get()
        nom_personnage = self.nom_personnage.get()  
        cachet = self.cachet.get()  
        debut_emploi = self.Debut_emploi.get()
        fin_emploi = self.Fin_emploi.get()

        # Validation des données
        if  nom or  prenom or  nom_personnage or cachet or debut_emploi or fin_emploi:
         acteur = Acteur(nom, prenom, sexe, nom_personnage, cachet, debut_emploi, fin_emploi)
         self.main_window.modifier_acteur(self.index, acteur)
         self.root.destroy()
        else:    
         messagebox.showerror("Erreur", "Tous les champs doivent être remplis")

class ConfirmationSuppressionWindow_acteur:
    def __init__(self, root, main_window, acteur, index):
        self.root = root
        self.main_window = main_window
        self.acteur = acteur
        self.index = index
        self.root.title("Confirmer Suppression")
        
        tk.Label(root, text=f"Voulez-vous vraiment supprimer {acteur.nom_personnage} {acteur.nom} {acteur.prenom} ?").grid(row=0, column=0, columnspan=2)
        
        tk.Button(root, text="Oui", command=self.supprimer_acteur).grid(row=1, column=0)
        tk.Button(root, text="Non", command=self.annuler).grid(row=1, column=1)

    def supprimer_acteur(self):
        self.main_window.supprimer_acteur(self.index)
        self.root.destroy()
    
    def annuler(self):
        self.root.destroy() 

# Fenêtre Action Client
        
class CreerClientWindow:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window
        self.root.title("Créer Client")
        self.root.geometry("300x200")
        tk.Label(root, text="Nom").grid(row=0, column=0)
        tk.Label(root, text="Prénom").grid(row=1, column=0)
        tk.Label(root, text="Sexe").grid(row=2, column=0)
        tk.Label(root, text="Date d'inscription").grid(row=3, column=0)
        tk.Label(root, text="Courriel").grid(row=4, column=0)
        tk.Label(root, text="Mot de Passe").grid(row=5, column=0)
        
        self.nom = tk.Entry(root)
        self.prenom = tk.Entry(root)
        self.sexe = tk.Entry(root)
        self.date_inscription = tk.Entry(root)
        self.courriel = tk.Entry(root)
        self.mot_de_passe = tk.Entry(root, show="*")
        
        self.nom.grid(row=0, column=1)
        self.prenom.grid(row=1, column=1)
        self.sexe.grid(row=2, column=1)
        self.date_inscription.grid(row=3, column=1)
        self.courriel.grid(row=4, column=1)
        self.mot_de_passe.grid(row=5, column=1)
        
        tk.Button(root, text="Créer", command=self.creer_client).grid(row=6, column=1)
    
    def creer_client(self):
        nom = self.nom.get()
        prenom = self.prenom.get()
        sexe = self.sexe.get()
        date_inscription = self.date_inscription.get()
        courriel = self.courriel.get()
        mot_de_passe = self.mot_de_passe.get()
        
        # Validation des données
        if len(mot_de_passe) < 8:
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 8 caractères")
            return
        if not (nom and prenom and sexe and date_inscription and courriel and mot_de_passe):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
            return
        # Check if email already exists 
        if self.main_window.verifier_courriel_existant(courriel):
            messagebox.showerror("Erreur", "L'adresse courriel est déjà utilisée")
            return
        
        client = Client(nom, prenom, sexe, date_inscription, courriel, mot_de_passe)
        messagebox.showinfo("Succès", "Client créé avec succès")
        self.main_window.ajouter_client(client)
        self.root.destroy()

class ModifierClientWindow:
    def __init__(self, root, main_window, client, index):
        self.root = root
        self.main_window = main_window
        self.client = client
        self.index = index
        self.root.title("Modifier fiche d'un client")
        self.root.geometry("300x200")
        tk.Label(root, text="Nom").grid(row=0, column=0)
        tk.Label(root, text="Prénom").grid(row=1, column=0)
        tk.Label(root, text="Sexe").grid(row=2, column=0)
        tk.Label(root, text="Date d'inscription").grid(row=3, column=0)
        tk.Label(root, text="Courriel").grid(row=4, column=0)
        tk.Label(root, text="Mot de Passe").grid(row=5, column=0)
        
        self.nom = tk.Entry(root)
        self.prenom = tk.Entry(root)
        self.sexe = tk.Entry(root)
        self.date_inscription = tk.Entry(root)
        self.courriel = tk.Entry(root)
        self.mot_de_passe = tk.Entry(root, show="*")
        
        self.nom.grid(row=0, column=1)
        self.prenom.grid(row=1, column=1)
        self.sexe.grid(row=2, column=1)
        self.date_inscription.grid(row=3, column=1)
        self.courriel.grid(row=4, column=1)
        self.mot_de_passe.grid(row=5, column=1)
        
        # Pré-remplir les champs avec les informations actuelles du client
        self.nom.insert(0, client.nom)
        self.prenom.insert(0, client.prenom)
        self.sexe.insert(0, client.sexe)
        self.date_inscription.insert(0, client.date_inscription)   
        self.courriel.insert(0, client.courriel)
        self.mot_de_passe.insert(0, client.password)
        
        tk.Button(root, text="Modifier", command=self.modifier_client).grid(row=6, column=1)
    
    def modifier_client(self):
        nom = self.nom.get()
        prenom = self.prenom.get()
        sexe = self.sexe.get()
        date_inscription = self.date_inscription.get()
        courriel = self.courriel.get()
        mot_de_passe = self.mot_de_passe.get()
        
        # Validation des données
        if len(mot_de_passe) < 8:
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 8 caractères")
            return
        # Check if email already exists 
        if self.main_window.verifier_courriel_existant(courriel):
            messagebox.showerror("Erreur", "L'adresse courriel est déjà utilisée")
            return
        # Mise à jour des informations du client 
        try:
            client_modifie = Client(nom, prenom, sexe, date_inscription, courriel, mot_de_passe)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
        self.main_window.modifier_client(self.index, client_modifie)
        
        self.root.destroy()

# Classe ConfirmationSuppressionWindow : Cette classe gère la fenêtre de confirmation de suppression du client. Elle affiche un message de confirmation et des boutons pour confirmer ou annuler la suppression.
class ConfirmationSuppressionWindow:
    def __init__(self, root, main_window, client, index):
        self.root = root
        self.main_window = main_window
        self.client = client
        self.index = index
        self.root.title("Confirmer Suppression")
        
        tk.Label(root, text=f"Voulez-vous vraiment supprimer {client.nom} {client.prenom} ?").grid(row=0, column=0, columnspan=2)
        
        tk.Button(root, text="Oui", command=self.supprimer_client).grid(row=1, column=0)
        tk.Button(root, text="Non", command=self.annuler).grid(row=1, column=1)

 # Méthode supprimer_client : Cette méthode dans MainWindow supprime le client de la liste et met à jour la Listbox   
    def supprimer_client(self):
        self.main_window.supprimer_client(self.index)
        self.root.destroy()
    
    def annuler(self):
        self.root.destroy()

## Fin Fenêtre Action Client

# Classe CreerFilmsWindow : Cette classe gère la fenêtre de création de films. Elle affiche des champs pour saisir les informations du film et un bouton pour créer le film.
class CreerFilmsWindow:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window
        self.root.title("Créer Films")
        self.root.geometry("300x200")
        tk.Label(root, text="Titre").grid(row=0, column=0)
        #tk.Label(root, text="Genre").grid(row=1, column=0)
        tk.Label(root, text="Année").grid(row=2, column=0)
        tk.Label(root, text="Durée").grid(row=3, column=0)
        
        self.titre = tk.Entry(root)
        #self.genre = tk.Entry(root)
        self.annee = tk.Entry(root)
        self.duree = tk.Entry(root)
        
        self.titre.grid(row=0, column=1)
        #self.genre.grid(row=1, column=1)
        self.annee.grid(row=2, column=1)
        self.duree.grid(row=3, column=1)
        
        tk.Button(root, text="Créer", command=self.creer_film).grid(row=4, column=1)
    
    def creer_film(self):
        titre = self.titre.get()
        #genre = self.genre.get()
        annee = self.annee.get()
        duree = self.duree.get()
        
        # Validation des données
        if not titre or not annee or not duree:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
            return
        
        # Création du film et ajout à la liste
        film = Film(titre, annee, duree)
        self.main_window.ajouter_film(film)
        
        self.root.destroy()

class ModifierFilmsWindow:
    def __init__(self, root, main_window, film, index):
        self.root = root
        self.main_window = main_window
        self.film = film
        self.index = index
        self.root.title("Modifier Film")
        self.root.geometry("300x200")
        tk.Label(root, text="Titre").grid(row=0, column=0)
       # tk.Label(root, text="Genre").grid(row=1, column=0)
        tk.Label(root, text="Année").grid(row=2, column=0)
        tk.Label(root, text="Durée").grid(row=3, column=0)
        
        self.titre = tk.Entry(root)
        #self.genre = tk.Entry(root)
        self.annee = tk.Entry(root)
        self.duree = tk.Entry(root)
        
        self.titre.grid(row=0, column=1)
        #self.genre.grid(row=1, column=1)
        self.annee.grid(row=2, column=1)
        self.duree.grid(row=3, column=1)
        
        # Pré-remplir les champs avec les informations actuelles du film
        self.titre.insert(0, film.titre)
        #self.genre.insert(0, film.genre)
        self.annee.insert(0, film.annee)
        self.duree.insert(0, film.duree)
        
        tk.Button(root, text="Modifier", command=self.modifier_film).grid(row=4, column=1)
    
    def modifier_film(self):
        titre = self.titre.get()
        #genre = self.genre.get()
        annee = self.annee.get()
        duree = self.duree.get()
        
        # Validation des données
        if not titre or not annee or not duree:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis")
            return
        
        # Mise à jour des informations du film
        film_modifie = Film(titre, annee, duree)
        self.main_window.modifier_film(self.index, film_modifie)
        
        self.root.destroy()

# Classe ConfirmationSuppressionWindow_film : Cette classe gère la fenêtre de confirmation de suppression du film. Elle affiche un message de confirmation et des boutons pour confirmer ou annuler la suppression.   
class ConfirmationSuppressionWindow_film:
    def __init__(self, root, main_window, film, index):
        self.root = root
        self.main_window = main_window
        self.film = film
        self.index = index
        self.root.title("Confirmer Suppression")
        
        tk.Label(root, text=f"Voulez-vous vraiment supprimer {film.titre} ?").grid(row=0, column=0, columnspan=2)
        
        tk.Button(root, text="Oui", command=self.supprimer_film).grid(row=1, column=0)
        tk.Button(root, text="Non", command=self.annuler).grid(row=1, column=1)

    def supprimer_film(self):
        self.main_window.supprimer_film(self.index)
        self.root.destroy()
        self.mettre_a_jour_films_listbox()

    def annuler(self):
        self.root.destroy()
        
class GestionFilms:
    def __init__(self):
        self.films = []

    def ajouter_film(self, film):
        self.films.append(film)

    def modifier_film(self, titre, nouveau_titre=None, nouvelle_annee=None, nouvelle_duree=None):
        for film in self.films:
            if film.titre == titre:
                if nouveau_titre:
                    film.titre = nouveau_titre
                if nouvelle_annee:
                    film.annee = nouvelle_annee
                if nouvelle_duree:
                    film.duree = nouvelle_duree
                return True
        return False

    def supprimer_film(self, titre):
        for film in self.films:
            if film.titre == titre:
                self.films.remove(film)
                return True
        return False

    def ajouter_film(self, film):
        self.films.append(film)

class GestionFilmWindow:
    def __init__(self, root, main_window):
        self.root = root
        self.main_window = main_window
        self.root.title("Gestion Film pour associer des acteurs et des catégories à un Film")
        self.root.geometry("600x500")

        tk.Label(root, text="Sélectionner un Film").grid(row=0, column=0)
        tk.Label(root, text="Sélectionner des Acteurs").grid(row=1, column=0)
        tk.Label(root, text="Sélectionner des Catégories").grid(row=2, column=0)

        self.film_combobox = ttk.Combobox(root, values=[film.titre for film in main_window.films])
        self.acteurs_listbox = tk.Listbox(root, width=50, selectmode=tk.MULTIPLE, exportselection=0) # exportselection=0 to keep selection after losing focus
        self.categories_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, exportselection=0) # exportselection=0 to keep selection after losing focus
        
        for acteur in main_window.acteurs:
            self.acteurs_listbox.insert(tk.END, f"||| {acteur.nom_personnage} ||| - {acteur.nom} {acteur.prenom}")
        for categorie in main_window.categories:
            self.categories_listbox.insert(tk.END, categorie)

        self.film_combobox.grid(row=0, column=1)
        self.acteurs_listbox.grid(row=1, column=1)
        self.categories_listbox.grid(row=2, column=1)

        tk.Button(root, text="Associer", command=self.associer_acteur_et_categories).grid(row=3, column=1)

    def associer_acteur_et_categories(self):
        film_titre = self.film_combobox.get()
        acteurs_selectionnes = [self.acteurs_listbox.get(i) for i in self.acteurs_listbox.curselection()]
        categories_selectionnees = [self.categories_listbox.get(i) for i in self.categories_listbox.curselection()]
        if film_titre and acteurs_selectionnes or categories_selectionnees: # OR pour permettre la saisie d'un/des acteurs ou d'une/des catégories
            film = next((film for film in self.main_window.films if film.titre == film_titre), None)

            if film:
                for acteur_nom in acteurs_selectionnes:
                    acteur = next((acteur for acteur in self.main_window.acteurs if f"{acteur.nom} {acteur.prenom}" == acteur_nom), None)
                    if acteur:
                        acteur.ajouter_film(film)

                for categorie in categories_selectionnees:
                    film.ajouter_genre(categorie)

                messagebox.showinfo("Succès", f"Les modifications ont été associés à {film.titre}")
                self.root.destroy()
            else:
                messagebox.showerror("Erreur", "Film non trouvé")
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un film et une des sections (acteur ou catégorie")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()


