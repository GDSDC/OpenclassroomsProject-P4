from typing import List
from datetime import date, datetime
import parse_validate_tools as pvt
import model

# Constantes Globales
CHOIX_MENU_PRINCIPAL = {1: 'Créer un nouveau tournoi',
                        2: 'Ajouter huit joueurs',
                        3: 'Démarrer nouveau Round',
                        4: 'Entrer les résultats',
                        5: 'Terminer le tournoi',
                        6: 'Quitter'}


class Vue:
    """Classe qui gère l'interface/menu du programme."""

    def menu_principal(self) -> int:
        """Affichage du menu principal et récupération du choix de l'utilisateur."""

        # Affichage de l'entête
        affichage_menu_principal = """
==============================
Menu Principal
==============================
"""
        print(affichage_menu_principal)

        # Affichage des différents choix
        for choix in CHOIX_MENU_PRINCIPAL.keys():
            print(choix, '--', CHOIX_MENU_PRINCIPAL[choix])

        # Choix du menu
        choix_du_menu_texte = '\nRenseignez votre choix parmis les propositions ci-dessus (1 à ' + str(
            len(CHOIX_MENU_PRINCIPAL)) + ') : '
        choix_utilisateur_menu_principal = pvt.parse_and_validate(explanation=choix_du_menu_texte, parse=pvt.parse_int,
                                                                  validate=pvt.validate_integer_interval)

        return choix_utilisateur_menu_principal

    def menu_creer_nouveau_tournoi(self) -> model.Tournoi:
        """Création d'un nouveau tournoi en renseignant toutes les informations demandées."""

        # Initialisation
        nouveau_tournoi = {
            'nom': '',
            'lieu': '',
            'date_debut': '',
            'date_fin': '',
            'nombre_tours': '',
            'controle_du_temps': '',
            'description': '',
            'rounds': ''
        }

        # Affichage de l'entête
        affichage_menu_creer_nouveau_tournoi = """
==============================
Créer un nouveau Tournoi
==============================
"""
        print(affichage_menu_creer_nouveau_tournoi)

        # Définition du nom du tournoi
        nouveau_tournoi_texte_nom = '\nRenseignez le Nom du tournoi : '
        nouveau_tournoi['nom'] = pvt.parse_and_validate(explanation=nouveau_tournoi_texte_nom,
                                                        parse=pvt.parse_string_not_empty, validate=pvt.no_validation)

        # Définition du le lieu du tournoi
        nouveau_tournoi_texte_lieu = '\nRenseignez le Lieu du tournoi : '
        nouveau_tournoi['lieu'] = pvt.parse_and_validate(explanation=nouveau_tournoi_texte_lieu,
                                                         parse=pvt.parse_string_not_empty, validate=pvt.no_validation)

        # Définition date de début de tournoi
        nouveau_tournoi['date_debut'] = date.today()

        # Définition date de fin de tournoi par defaut
        # nouveau_tournoi['date_fin'] = date.today()

        # Définition le contrôle du temps
        nouveau_tournoi_texte_controle_du_temps = '\nRenseignez le contrôle du temps ("bullet", "blitz" ou "coup rapide") : '
        nouveau_tournoi['controle_du_temps'] = pvt.parse_and_validate(
            explanation=nouveau_tournoi_texte_controle_du_temps, parse=pvt.parse_string_not_empty,
            validate=pvt.validate_controle_du_temps)

        # Description
        nouveau_tournoi_texte_description = '\nRensignez les remarques générales du directeur du tournoi : '
        nouveau_tournoi['description'] = pvt.parse_and_validate(explanation=nouveau_tournoi_texte_description,
                                                                parse=pvt.parse_string_not_empty,
                                                                validate=pvt.no_validation)

        # Formatage du resultat au format model.Tournoi
        nouveau_tournoi = model.Tournoi(**nouveau_tournoi)

        return nouveau_tournoi

    def ajouter_joueurs(self) -> List[model.Joueur]:
        """AJout des informations de huit joueurs dans une liste de dictionnaires à destination du Controller."""

        # Initialisation
        # liste retournée contenant les informations des huit joueurs
        nouveaux_joueurs = []

        # Affichage de l'entête
        affichage_menu_ajouter_joueurs = """
==============================
Ajouter 8 joueurs
==============================
"""
        print(affichage_menu_ajouter_joueurs)

        # Boucle sur les huits joueurs
        for joueur in range(1, model.NOMBRE_DE_JOUEURS + 1):
            # dictionnaire type contenant les informations d'un joueur
            information_nouveau_joueur = {
                'nom_de_famille': '',
                'prenom': '',
                'date_de_naissance': '',
                'sexe': '',
                'classement': ''
            }

            # ajout du dictionnaire type à la liste de nouveaux joueurs
            nouveaux_joueurs.append(information_nouveau_joueur)

            # Affichage de l'entête pour chaque nouveau joueur
            affichage_nouveau_joueur = """
    Renseigner les informations du joueur n°""" + str(joueur) + """
    ==========================================
            """
            print(affichage_nouveau_joueur)

            # Définition du nom de famille
            nouveau_joueur_texte_nom = '\nRenseignez le Nom de famille du joueur n°' + str(joueur) + ' : '
            nouveaux_joueurs[joueur - 1]['nom_de_famille'] = pvt.parse_and_validate(
                explanation=nouveau_joueur_texte_nom, parse=pvt.parse_string_not_empty, validate=pvt.no_validation)

            # Définition le prénom
            nouveau_joueur_texte_prenom = '\nRenseignez le Prénom du joueur n°' + str(joueur) + ' : '
            nouveaux_joueurs[joueur - 1]['prenom'] = pvt.parse_and_validate(explanation=nouveau_joueur_texte_prenom,
                                                                            parse=pvt.parse_string_not_empty,
                                                                            validate=pvt.no_validation)

            # Définition de la date de naissance
            nouveau_joueur_texte_date_naissance = '\nRenseignez la Date de naissance du joueur n°' + str(
                joueur) + ' au format "jj/mm/aaaa" : '
            nouveaux_joueurs[joueur - 1]['date_de_naissance'] = pvt.parse_and_validate(
                explanation=nouveau_joueur_texte_date_naissance, parse=pvt.parse_date,
                validate=pvt.validate_date_format)

            # Définition du sexe
            nouveau_joueur_texte_sexe = '\nRenseignez le sexe du joueur n°' + str(joueur) + ' ("m"/"f") :'
            nouveaux_joueurs[joueur - 1]['sexe'] = pvt.parse_and_validate(explanation=nouveau_joueur_texte_sexe,
                                                                          parse=pvt.parse_string_not_empty,
                                                                          validate=pvt.validate_sexe)

            # Définition du classement
            nouveau_joueur_texte_classement = '\nRenseignez le classement du joueur n°' + str(joueur) + ' : '
            nouveaux_joueurs[joueur - 1]['classement'] = pvt.parse_and_validate(
                explanation=nouveau_joueur_texte_classement, parse=pvt.parse_int,
                validate=pvt.validate_integer_positive)

            # Formatage des informations de joueurs au format model.Joueur
            nouveaux_joueurs[joueur - 1] = model.Joueur(**nouveaux_joueurs[joueur - 1])

        return nouveaux_joueurs

    def afficher_paires_joueurs(self, round: model.Round):

        nombre_de_paires = len(round.match_liste)

        # Affichage de l'entête
        affichage_paires_joueurs_entete = """
==========================================================
""" + str(nombre_de_paires) + """ nouvelles paires de joueurs générées avec succès !
==========================================================
"""
        print(affichage_paires_joueurs_entete)

        # Boucle pour afficher toutes les paires de joueurs
        for paires in range(1, nombre_de_paires + 1):
            print('Paire n°' + str(paires) + ' : ' + str(
                round.match_liste[paires - 1].resultat_1.joueur.prenom) + ' ' + str(
                round.match_liste[paires - 1].resultat_1.joueur.nom_de_famille) + ' / ' + str(
                round.match_liste[paires - 1].resultat_2.joueur.prenom) + ' ' + str(
                round.match_liste[paires - 1].resultat_2.joueur.nom_de_famille))

    def creer_nouveau_round(self, numero_round: int) -> model.Round:
        """Affichage menu creer_nouveau_round"""

        # Initialisation
        nouveau_round = {
            'nom': '',
            'match_liste': [],
            'date_debut': '',
            'date_fin': ''
        }

        # Définition du nom du Round
        nouveau_round['nom'] = model.RoundName('Round ' + str(numero_round))

        # Affichage
        affichage_creer_nouveau_round = '''
==============================
Création du ''' + nouveau_round['nom'].value + ''' avec succès !
==============================
'''
        print(affichage_creer_nouveau_round)

        # Définition date de début de round
        nouveau_round['date_debut'] = datetime.today()

        # Formatage du resultat au format model.Round
        nouveau_round = model.Round(**nouveau_round)

        return nouveau_round

    def entrer_scores(self, round: model.Round) -> List[model.Match]:

        # Initialisation
        match_liste_scores = round.match_liste
        nombre_de_paires = len(match_liste_scores)

        # Affichage menu entrer scores
        affichage_menu_entrer_scores = '''
==========================================================
Entrez les scores des ''' + str(nombre_de_paires) + ''' matchs :  
==========================================================        
'''
        print(affichage_menu_entrer_scores)

        # Boucle sur les matchs
        for paires in range(1, nombre_de_paires + 1):
            print('Match ' + str(paires) + ' : ')
            # Boucle sur les résultats du match
            for result_field in list(match_liste_scores[paires - 1].__dict__.keys()):
                resultat = getattr(match_liste_scores[paires - 1], result_field)
                match_texte = ' Veuillez renseigner le score du joueur ' + str(resultat.joueur.prenom) + ' ' + str(
                    resultat.joueur.nom_de_famille) + ' : '
                score = pvt.parse_and_validate(explanation=match_texte, parse=pvt.parse_float,
                                               validate=pvt.validate_score)
                resultat.score = model.Score(score)

        return match_liste_scores


if __name__ == '__main__':
    pass