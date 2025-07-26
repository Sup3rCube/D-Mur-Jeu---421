# version 4. Adaptation suivant conseils Zgg
# On commence par récupérer/revérifier chaque fonction de la v3 avant de l'ajouter à la v4

import random

################################################################################################################
# === PARAMETRES DE LA PARTIE ===
POINTS_PAR_JOUEUR = 5

################################################################################################################
# === INPUTs ===
NB_PIECES_JOUEURS = 5

################################################################################################################
# === CLASSE JOUEUR ===
class Joueur:
    def __init__(self, position):
        self.position = position
        self.points = 0
        self.etat = 'joueur'  # 'joueur', 'waiting...' ou 'spectateur'
        self.score = []
        self.lancers = 0

# === CLASSES DES PHASES ===
class PhaseIntro:
    def jouer_tour(joueur):
        # la logique de jouer_tour pour la phase d'intro
        jouer_tour(joueur, max_lancers=1, nb_des=1)

    def run_phase(joueurs):
        for j in joueurs:
            self.jouer_tour(j)

        nb_tour, gagnant = self.resoudre_tour(joueurs, pot)
        return self.ordre_passage(joueurs, gagnant.position)

class PhaseCharge:
    def jouer_tour(joueur):
        # la logique de jouer tour pour la phase de charge
        jouer_tour(joueur, max_lancers=3, nb_des=3)

    def run_phase(joueurs):
        return joueurs

class PhaseDecharge:
    def jouer_tour(joueur):
        # la logique de jouer tour pour la phase de decharge, pareil que la charge mais pas grave
        jouer_tour(joueur, max_lancers=3, nb_des=3)

    def run_phase(joueurs):
        return joueurs

################################################################################################################
# === FONCTIONS ===
def inserer_pieces():
    # Simule les joueurs ayant mis une piece : positions 1 à 12, booléen aléatoire
    actifs = [True for _ in range(NB_PIECES_JOUEURS)]
    joueurs = [Joueur(i + 1) for i, actif in enumerate(actifs) if actif]
    print(f"{len(joueurs)} joueurs en jeu : {[j.position for j in joueurs]}")
    return joueurs

def jouer_tour(joueur, max_lancers, nb_des):
    # # # GPIO IN # # # Input du levier à actionner par le joueur
    print(f"\n-- Joueur {joueur.position} --")
    # # # GPIO IN # # # Détection des résultats des dés + Tri + Affichage
    des = sorted([random.randint(1, 6) for _ in range(nb_des)], reverse=True)
    # # # GPIO OUT # # # Affichage du résultat traduit en 421 (croissant) vers servomoteur
    # # # Faire fonction pour ° de rotation souhaité ---> servomoteur ---> Affichage flipboard
    # des = input(lancer_des(nb_des))
    print(f"Lancer 1/{max_lancers}:", des)
    joueur.lancers = 1
    while joueur.lancers < max_lancers:
        choix = input("Voulez-vous relancer ? (y/n) ").lower()
        # # # A REMPLACER PAR UN "VALIDER" APRES SELECTION DES BOUTONS
        # # # GPIO IN # # # Input d'un bouton ou d'une action du levier pour valider la relance et relancer les dés
        if choix == 'n':
            break
        garder = [input(f"Relancer le dé {d} ? (y/n): ").lower() == 'n' for d in des]
        # # # GPIO IN # # # Intput des boutons poussoirs sélectionnables indépendamment les uns des autres
        for i in range(nb_des):
            if not garder[i]:
                # # # GPIO OUT # # # Output pour relancer le dé dans l'ampoule dont est issu le résultat
                des[i] = random.randint(1, 6)
                # # # GPIO IN # # # Détection des résultats des dés + Tri + Affichage
        des.sort(reverse=True)
        # # # GPIO OUT # # # Affichage du résultat traduit en 421 (croissant) vers servomoteur
        joueur.lancers += 1
        # # # GPIO OUT # # # Met à jour l'affichage du nombre de lancers
        print(f"Lancer {joueur.lancers}/{max_lancers}: {des}")
    joueur.score = des
    # # # GPIO OUT # # # Met à jour l'affichage du score associé au joueur dans l'interface secondaire
    # # # GPIO OUT # # # Met à jour l'affichage du nombre de lancers associé au joueur dans l'interface secondaire
    print(f"Score final: {des}\n      Validé en {joueur.lancers} lancer(s)\n-----------------")










################################################################################################################
###########################################  PROGRAMME PRINCIPAL  ##############################################
################################################################################################################
# le jeu commence!
joueurs = inserer_pieces()

intro = PhaseIntro()
joueurs = intro.run_phase()

charge = PhaseCharge()
joueurs = charge.run_phase(joueurs)

decharge = PhaseDecharge()
joueurs = decharge.run_phase(joueurs)
