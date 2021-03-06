from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

# GLOBAL MENUS
CHOIX_MENU_PRINCIPAL = {
    1: "Gestion des Joueurs (ajouter/supprimer)",
    2: "Gestion du Tournoi",
    3: "Rapports",
    4: "Sauvegarde / Chargement des données",
    0: "Quitter le programme",
}

CHOIX_MENU_JOUEURS = {
    1: "Afficher la liste des Joueurs",
    2: "Ajouter un nouveau Joueur",
    3: "Supprimer un Joueur",
    4: "Mettre à jour le classement d'un Joueur",
    0: "Quitter",
}

CHOIX_MENU_TOURNOI = {
    1: "Créer un nouveau Tournoi",
    2: "Démarrer nouveau Round",
    3: "Entrer/Modifier les résultats",
    4: "Mettre à jour le classement des Joueurs du Tournoi",
    5: "Terminer le tournoi",
    0: "Quitter",
}

CHOIX_MENU_RAPPORTS = {
    1: "Liste de tous les Acteurs par ordre alphabétique",
    2: "Liste de tous les Acteurs par classement",
    3: "Liste de tous les Joueurs d'un Tournoi par ordre alphabétique",
    4: "Liste de tous les Joueurs d'un Tournoi par classement",
    5: "Liste de tous les Tournois",
    6: "Liste de tous les Tours d'un Tournoi",
    7: "Liste de tous les Matchs d'un Tournoi",
    0: "Quitter",
}

CHOIX_MENU_SAUVEGARDE_CHARGEMENT = {
    1: "Sauvegarder l'état du programme",
    2: "Charger l'état du programme",
    3: "Réinitialiser la base de donnée",
    0: "Quitter",
}

# INITIALIZATION CONSTANTS
# Number of Rounds per tournament
NOMBRE_DE_TOURS = 4

# Number of players per tournament
NOMBRE_DE_JOUEURS = 8


# Class describing the Joueur
class Sex(Enum):
    """Sex Enum Class"""
    MALE = 'm'
    FEMALE = 'f'


@dataclass
class Joueur:
    """Class describing a player"""
    nom_de_famille: str
    prenom: str
    date_de_naissance: datetime
    sexe: Sex
    classement: int

    def to_json(self) -> Dict[str, Any]:
        """Function to serialize a Joueur to JSON format"""
        self_as_dict = asdict(self)
        self_as_dict['date_de_naissance'] = self.date_de_naissance.isoformat()
        self_as_dict['sexe'] = self.sexe.value

        return self_as_dict

    @classmethod
    def from_json(cls, json_value: Dict[str, Any]) -> 'Joueur':
        """Class Method to deserialize a JSON into a Joueur instance"""
        joueur = Joueur(**json_value)
        joueur.date_de_naissance = datetime.fromisoformat(json_value['date_de_naissance'])
        joueur.sexe = Sex(json_value['sexe'])

        return joueur


# Class describing the Match
class Score(Enum):
    """Point System Enum Class"""
    GAGNANT = 1
    PERDANT = 0
    MATCH_NUL = 1 / 2


# Classes describing the Round
class RoundName(Enum):
    """Enum class describing the names of Rounds used"""
    ROUND1 = 'Round 1'
    ROUND2 = 'Round 2'
    ROUND3 = 'Round 3'
    ROUND4 = 'Round 4'


# Type alias for Match
Match = Tuple[Tuple[Joueur, Optional[Score]], Tuple[Joueur, Optional[Score]]]


@dataclass
class Round:
    nom: Optional[RoundName]
    match_liste: List[Match]
    date_debut: datetime
    date_fin: datetime

    # for instance comparison in testing
    def __eq__(self, other):
        if isinstance(other, Round):
            return self.nom == other.nom \
                   and self.match_liste == other.match_liste \
                   and self.date_debut.date() == other.date_debut.date() \
                   and self.date_fin.date() == other.date_fin.date()
        else:
            return False

    def to_json(self) -> Dict[str, Any]:
        """Function to serialize a Round to JSON format"""
        self_as_dict = asdict(self)
        self_as_dict['nom'] = self.nom.value
        self_as_dict['match_liste'] = [
            [[joueur1.to_json(), score_joueur1.value], [joueur2.to_json(), score_joueur2.value]] for
            ((joueur1, score_joueur1), (joueur2, score_joueur2)) in self.match_liste]
        self_as_dict['date_debut'] = self.date_debut.isoformat()
        self_as_dict['date_fin'] = self.date_fin.isoformat()

        return self_as_dict

    @classmethod
    def from_json(cls, json_value: Dict[str, Any]) -> 'Round':
        """Class Method to deserialize a JSON into a Round instance"""
        round_instance = Round(**json_value)
        round_instance.nom = RoundName(json_value['nom'])
        round_instance.match_liste = [
            ((Joueur.from_json(joueur1_json), Score(score_joueur1_json)),
             (Joueur.from_json(joueur2_json), Score(score_joueur2_json)))
            for [[joueur1_json, score_joueur1_json], [joueur2_json, score_joueur2_json]] in json_value['match_liste']]
        round_instance.date_debut = datetime.fromisoformat(json_value['date_debut'])
        round_instance.date_fin = datetime.fromisoformat(json_value['date_fin'])

        return round_instance


# Class describing the Tournament
class ControleDuTemps(Enum):
    """Time Control Enum Class"""
    BULLET = 'bullet'
    BLITZ = 'blitz'
    COUP_RAPIDE = 'coup rapide'


@dataclass
class Tournoi:
    """Class describing a Tournament"""
    nom: str
    lieu: str
    date_debut: datetime
    date_fin: datetime
    controle_du_temps: ControleDuTemps
    description: str
    rounds: List[Round]
    joueurs_du_tournoi: Optional[List[Joueur]] = None
    joueurs_en_jeux: Optional[List[Joueur]] = None
    nombre_tours: int = NOMBRE_DE_TOURS

    def to_json(self) -> Dict[str, Any]:
        """Function to serialize a Tournament to JSON format"""
        self_as_dict = asdict(self)
        self_as_dict['date_debut'] = self.date_debut.isoformat()
        self_as_dict['date_fin'] = self.date_fin.isoformat()
        self_as_dict['controle_du_temps'] = self.controle_du_temps.value
        self_as_dict['rounds'] = [round_object.to_json() for round_object in self.rounds]
        self_as_dict['joueurs_du_tournoi'] = [joueur.to_json() for joueur in self.joueurs_du_tournoi]
        self_as_dict['joueurs_en_jeux'] = [joueur.to_json() for joueur in self.joueurs_en_jeux]

        return self_as_dict

    @classmethod
    def from_json(cls, json_value: Dict[str, Any]) -> 'Tournoi':
        """Class Method to deserialize a JSON into a Tournament instance"""
        tournoi = Tournoi(**json_value)
        tournoi.date_debut = datetime.fromisoformat(json_value['date_debut'])
        tournoi.date_fin = datetime.fromisoformat(json_value['date_fin'])
        tournoi.controle_du_temps = ControleDuTemps(json_value['controle_du_temps'])
        tournoi.rounds = [Round.from_json(round_json) for round_json in json_value['rounds']]
        tournoi.joueurs_du_tournoi = [Joueur.from_json(joueur_json) for joueur_json in
                                      json_value['joueurs_du_tournoi']]
        tournoi.joueurs_en_jeux = [Joueur.from_json(joueur_json) for joueur_json in json_value['joueurs_en_jeux']]

        return tournoi

    # for instance comparison in testing
    def __eq__(self, other):
        if isinstance(other, Tournoi):
            return self.nom == other.nom \
                   and self.lieu == other.lieu \
                   and self.date_debut.date() == other.date_debut.date() \
                   and self.date_fin.date() == other.date_fin.date() \
                   and self.controle_du_temps == other.controle_du_temps \
                   and self.description == other.description \
                   and self.joueurs_du_tournoi == other.joueurs_du_tournoi \
                   and self.joueurs_en_jeux == other.joueurs_en_jeux \
                   and self.nombre_tours == other.nombre_tours
        else:
            return False


class State:
    def __init__(self, acteurs: Optional[Dict[int, Joueur]] = None,
                 tournois: Optional[List[Tournoi]] = None,
                 tournoi: Optional[Tournoi] = None):
        self.acteurs: Dict[int, Joueur] = acteurs or {}
        self.tournois: List[Tournoi] = tournois or []
        self.tournoi: Optional[Tournoi] = tournoi

    # for instance comparison in testing
    def __eq__(self, other):
        if isinstance(other, State):
            return self.acteurs == other.acteurs \
                   and self.tournoi == other.tournoi \
                   and self.tournois == other.tournois
        else:
            return False

    def creer_nouveau_tournoi(self, nouveau_tournoi: Tournoi):
        self.tournoi = nouveau_tournoi

    def nombre_joueurs(self):
        return len(self.tournoi.joueurs_du_tournoi)

    def ajouter_nouveau_joueur(self, nouveaux_joueurs: List[Joueur]):
        for joueur in nouveaux_joueurs:
            # When acteurs is empty
            if not self.acteurs:
                nouvel_indice = 1
            else:
                nouvel_indice = list(self.acteurs.keys())[-1] + 1
            self.acteurs[nouvel_indice] = joueur

    def supprimer_joueur(self, joueur_a_supprimer: Joueur):
        """Function to delete joueur_a_supprimer from self.acteurs"""
        key_to_delete = list(self.acteurs.keys())[list(self.acteurs.values()).index(joueur_a_supprimer)]
        del self.acteurs[key_to_delete]

    def creer_nouveau_round(self, nouveau_round: Round):
        self.tournoi.rounds.append(nouveau_round)

    def generer_paires_joueurs(self, joueurs_paires: List[Tuple[Joueur, Joueur]]):
        """Function generate player pairs in the suisse tournament way"""

        # Generating pairs into match_liste
        for [joueur_1, joueur_2] in joueurs_paires:
            self.tournoi.rounds[-1].match_liste.append(((joueur_1, None), (joueur_2, None)))

    def entrer_scores(self, scores: List[Match]):
        self.tournoi.rounds[-1].match_liste = scores

    def modifier_classement_tournoi(self, joueurs_classement: List[Joueur]):
        self.tournoi.joueurs_du_tournoi = joueurs_classement

    def modifier_classement(self, joueurs_ancien_classement: List[Joueur], joueurs_nouveau_classement: List[Joueur]):
        """Function to update players ranking"""
        for joueur in joueurs_ancien_classement:
            key_to_update_ranking = list(self.acteurs.keys())[list(self.acteurs.values()).index(joueur)]
            self.acteurs[key_to_update_ranking] = joueurs_nouveau_classement[joueurs_ancien_classement.index(joueur)]

    def terminer_tournoi(self):
        """Function to update tourmanent list and clean state.tournoi"""
        self.tournois.append(self.tournoi)
        self.tournoi = None
