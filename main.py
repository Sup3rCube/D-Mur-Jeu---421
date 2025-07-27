# version 4. Adaptation suivant conseils Zgg
# On commence par récupérer/revérifier chaque fonction de la v3 avant de l'ajouter à la v4

import random

################################################################################################################
# === PARAMETRES DE LA PARTIE ===
POINTS_PAR_JOUEUR = 5
PHASE = 'Zzz...Zzz...Zzz...'
POT = 0

################################################################################################################
# === INPUTs ===
NB_PIECES_JOUEURS = 5

################################################################################################################
# === CLASSE JOUEUR ===
class Joueur:
    def __init__(self, position):
        self.position = position    #GPIO - déterminé par le nombre de pîèces insérées
        self.points = 0             #GPIO - affiche : nombre de points
        self.etat = 'joueur'        #GPIO - affiche : 'joueur', 'waiting...' ou 'spectateur'
        self.score = []             #GPIO - affiche : score
        self.lancers = 0            #GPIO - affiche : nombre de lancers restants

# === CLASSES DES PHASES ===
class PhaseIntro:
    def run_phase(self):
        for j in joueurs:
            jouer_tour(j, max_lancers=1, nb_des=1)
        nb_tour, gagnant = resoudre_tour(joueurs, POT)
        return ordre_passage(joueurs, gagnant.position)

class PhaseCharge:
    def run_phase(self):
        for j in joueurs:
            jouer_tour(j, max_lancers=3, nb_des=3)
        nb_tour, gagnant = resoudre_tour(joueurs, POT)
        return ordre_passage(joueurs, gagnant.position)

class PhaseDecharge:
    def run_phase(self):
        for j in joueurs:
            jouer_tour(j, max_lancers=3, nb_des=3)
        nb_tour, gagnant = resoudre_tour(joueurs, POT)
        return ordre_passage(joueurs, gagnant.position)

################################################################################################################
# === FONCTIONS ===
def inserer_pieces():
    # Simule les joueurs ayant mis une piece : positions 1 à 12, booléen aléatoire
    # # # GPIO IN # # # Input incrémentation fonction du nb de pièces
    actifs = [True for _ in range(NB_PIECES_JOUEURS)]
    # # # GPIO OUT # # # Output allumage led et interface secondaire associé au cardinal
    joueurs = [Joueur(i + 1) for i, actif in enumerate(actifs) if actif]
    print(f"{len(joueurs)} joueurs en jeu : {[j.position for j in joueurs]}")
    return joueurs
    # # # GPIO IN # # # Input levier si nombre de pièces > 0
    # # # GPIO OUT # # # Output affichage nombre de points dans le pot
    # Lancement de la partie

def jouer_tour(joueur, max_lancers, nb_des):
    # # # GPIO IN # # # Input du levier à actionner par le joueur
    print(f"\n-- Joueur {joueur.position} --")
    # # # GPIO IN # # # Détection des résultats des dés + Tri + Affichage
    des = sorted([random.randint(1, 6) for _ in range(nb_des)], reverse=True)
    # # # GPIO OUT # # # Affichage du résultat traduit en 421 (croissant) vers servomoteur
    # # # Faire fonction pour ° de rotation souhaité → servomoteur → Affichage flipboard
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

def resoudre_tour(joueurs, POT):
    gagnants = []
    perdants = []
    if PHASE == 'intro':
        scores = [(j.score, j) for j in joueurs if j.etat == 'joueur']
        scores.sort(key=lambda x: x[0])  # Score le plus bas en premier
        for j in joueurs:
            if j.score == scores[-1][0]:
                gagnants.append(j)
        while len(gagnants) > 1:
            print(f"DUEL POUR : ÊTRE LE PREMIER JOUEUR ENTRE JOUEURS {gagnants}")
            # a corriger après premier test
            gagnants = duel_intro(gagnants)
        gagnants[0].score = scores[-1][0]
        print(f"\nLe premier joueur à commencer est le joueur {gagnants[0].position} avec {gagnants[0].score}")
        print("----------------------------------")
        return 0, gagnants[0]
    if PHASE == 'charge':
        scores = [(j.score, j) for j in joueurs]
        scores.sort(key=lambda x: x[0])  # Score le plus bas en premier
        for j in joueurs:
            if j.score == scores[0][0]:
                perdants.append(j)
        while len(perdants) > 1:
            print(f"DUEL POUR : NE PAS PRENDRE {jeton_par_score(scores[-1][0], POT, None, PHASE)} JETONS")
            perdants = duel_charge(perdants)
        perdants[0].score = scores[0][0]
        print(f"\nLe premier joueur à commencer est le joueur {gagnants[0].position} avec {gagnants[0].score}")
        print("----------------------------------")
        return 0, gagnants[0]


    if PHASE == 'intro':
        scores = [(score_value(j.score), j.score, j, j.lancers) for j in joueurs if j.etat == 'joueur']
        scores.sort(key=lambda x: x[0])  # Score le plus bas en premier
        for j in joueurs:
            if j.score == scores[0][1]:
                perdants.append(j)
        n = 0
        while len(perdants) > 1:
            n += 1
            print("\nc'est l'heure du-du-du-du-du DUEL! (des nuls)")
            input(f"=== Duel perdant : {len(perdants)} joueurs ===")
            perdants = duel_perdant(perdants)
        perdant = perdants[0]
        perdant.score = scores[0][1]
        print(f"\nPERDANT DU TOUR {nb_tour}:\n     Joueur {perdants[0].position} avec {perdants[0].score}\n")
        if phase == 'charge':
            gagnant = scores[-1][2]
            gagnants.append(gagnant)
        elif phase == 'décharge':
            for j in joueurs:
                if j.score == scores[-1][1]:
                    gagnants.append(j)
            n = 0
            while len(gagnants) > 1:
                n += 1
                print("\nc'est l'heure du-du-du-du-du DUEL! (des boss)")
                input(f"=== Duel gagnant : {len(gagnants)} joueurs ===")
                gagnants = duel_gagnant(gagnants)
            gagnant = gagnants[0]
        gagnant.score = scores[-1][1]
        print(f"GAGNANT DU TOUR {nb_tour}:\n     Joueur {gagnants[0].position} avec {gagnants[0].score}")

        if phase == 'décharge':
            print(f"\n>> Le joueur {gagnant.position} donne {jeton_par_score(gagnant.score, pot, gagnant.points, phase)} jeton(s)")
            print(f"au joueur {perdant.position}")
        if phase == 'charge':
            print(f"\n>> Attribution de {jeton_par_score(gagnant.score, pot, gagnant.points, phase)} jeton(s)")
            print(f"au joueur {perdant.position}")
        return perdant, gagnant














def duel_intro(joueurs):
    score_temp = joueurs[0].score
    joueurs = comparer_nb_lancers(joueurs, False)
    if len(joueurs) > 1:
        # # # GPIO OUT # # # Output des LEDS/guichet d'état par joueur : signale le duel
        for j in joueurs:
            print(f"Joueur {j.position}, à ton tour.")
            # # # GPIO IN # # # Input du levier à actionner par le joueur
            # # # GPIO IN # # # Détection des résultats des dés + Tri + Affichage
            j.score = random.randint(1, 6)
            # # # GPIO OUT # # # Affichage du résultat traduit en 421 (croissant) vers servomoteur (ici 1 dé)
            # # # Faire fonction pour ° de rotation souhaité → servomoteur → Affichage flipboard secondaire
            print(f"score : {j.score}")
        scores_duel = [(score_value(j.score), j.score, j) for j in joueurs]
        scores_duel.sort(key=lambda x: x[0])  # Score le plus haut en premier
        gagnants = []
        for j in joueurs:
            if j.score == scores_duel[-1][1]:
                gagnants.append(j)
        for j in joueurs:
            j.score = score_temp
    elif len(joueurs) == 1:
        gagnants = joueurs
    return gagnants
def duel_charge(joueurs):
    score_temp = joueurs[0].score
    joueurs = comparer_nb_lancers(joueurs, True)
    perdants = []
    if len(joueurs) > 1:
        # # # GPIO OUT # # # Output des LEDS/guichet d'état par joueur : signale le duel
        for j in joueurs:
            j.etat = 'duel'
            print(f"Joueur {j.position}, à ton tour.")
            # # # GPIO IN # # # Input du levier à actionner par le joueur
            # # # GPIO IN # # # Détection des résultats des dés + Tri + Affichage
            j.score = sorted([random.randint(1, 6) for _ in range(3)], reverse=True)
            # # # GPIO OUT # # # Affichage du résultat traduit en 421 (croissant) vers servomoteur (ici 1 dé)
            # # # Faire fonction pour ° de rotation souhaité → servomoteur → Affichage flipboard secondaire
            print(f"score : {j.score}")
        scores_duel = [(score_value(j.score), j.score, j) for j in joueurs]
        scores_duel.sort(key=lambda x: x[0])  # Score le plus haut en premier
        for j in joueurs:
            if j.score == scores_duel[0][1]:
                perdants.append(j)
        for j in joueurs:
            j.score = score_temp
            j.etat = 'joueur'
    elif len(joueurs) == 1:
        perdants = joueurs
    return perdants
def duel_decharge(joueurs):
    score_temp = joueurs[0].score
    joueurs = comparer_nb_lancers(joueurs, True)
    gagnants = []
    if len(joueurs) > 1:
        # # # GPIO OUT # # # Output des LEDS/guichet d'état par joueur : signale le duel
        for j in joueurs:
            print(f"Joueur {j.position}, à ton tour.")
            # # # GPIO IN # # # Input du levier à actionner par le joueur
            # # # GPIO IN # # # Détection des résultats des dés + Tri + Affichage
            j.score = sorted([random.randint(1, 6) for _ in range(3)], reverse=True)
            # # # GPIO OUT # # # Affichage du résultat traduit en 421 (croissant) vers servomoteur (ici 1 dé)
            # # # Faire fonction pour ° de rotation souhaité → servomoteur → Affichage flipboard secondaire
            print(f"score : {j.score}")
        scores_duel = [(score_value(j.score), j.score, j) for j in joueurs]
        scores_duel.sort(key=lambda x: x[0])  # Score le plus haut en premier
        for j in joueurs:
            if j.score == scores_duel[-1][1]:
                gagnants.append(j)
        for j in joueurs:
            j.score = score_temp
    elif len(joueurs) == 1:
        gagnants = joueurs
    return gagnants
def ordre_passage(joueurs, position):
    ordre = []
    for j in joueurs:
        if j.etat == 'joueur':
            ordre.append(j)
    ordre.sort(key=lambda x: x.position)
    nouvel_ordre = []
    d = [(j.position-1) for j in ordre if j.position == position]
    nouvel_ordre.append(ordre[d[0]:])
    nouvel_ordre.append(ordre[:d[0]])
    nouvel_ordre = [x for xs in nouvel_ordre for x in xs]
    return nouvel_ordre
def comparer_nb_lancers(joueurs, a):
    if not joueurs:
        print("Aucun joueur à comparer.")
        return []
    # On récupère tous les nombres de lancers
    lancers_possibles = [j.lancers for j in joueurs]
    # On détermine le nombre de lancers à conserver
    if a:  # cas "perdant" : on garde ceux qui ont lancé le plus de fois
        reference = max(lancers_possibles)
    else:  # cas "gagnant" : on garde ceux qui ont lancé le moins de fois
        reference = min(lancers_possibles)
    # On filtre la liste des joueurs
    joueurs_filtres = [j for j in joueurs if j.lancers == reference]
    # Affichage du résultat
    #print(f"\nNombre de lancers retenu : {reference}")
    #print("Joueurs retenus :", [j.position for j in joueurs_filtrés])
    return joueurs_filtres
def score_value(score):
    if PHASE == 'intro':
        return score
    # Évalue le score et attribue un score de force afin de hiérarchiser les scores du tour. bordel.
    else:
        if score == [4, 2, 1]:
            return 10000  # Score max : 421
        elif score[0] == score[1] == score[2] == 1:
            return 7000   # Mac 1
        elif score[0] != 1 and score[1] == score[2] == 1:
            return score[0] * 1000  # Mac n
        elif score[0] == score[1] == score[2] != 1:
            return (score[0] * 1000) - 1   # Zanzi
        elif score in ([3, 2, 1], [4, 3, 2], [5, 4, 3], [6, 5, 4]):
            return 2000 + score[2]  # Suite
        else:
            return int(score[0] * 100 + score[1] * 10 + score[2])  # rien

def jeton_par_score(score, pot, points, PHASE):
    # Évalue le score et attribue un nombre de jeton associé au score
    if PHASE == 'charge':
        a = pot
    else:
        a = points
    if score == [4, 2, 1]:
        if PHASE == 'charge':
            return min(10, a)  # Score max : 421
        elif PHASE == 'décharge' and len(joueurs) > 2: # A VERIFIER SI 1V1 DECHARGE
            return min(10, a)  # Si décharge avec nb joueurs > 2
        else:
            print('EXECUTION!')
            return a # tous les jetons du gagnant en 1v1
    elif score[0] == score[1] == score[2] == 1:
        return min(7, a)   # Mac 1
    elif score[0] != 1 and score[1] == score[2] == 1:
        return min(score[0], a)   # Mac n
    elif score[0] == score[1] == score[2] != 1:
        return min(score[0], a)   # Zanzi
    elif score in ([3, 2, 1], [4, 3, 2], [5, 4, 3], [6, 5, 4]):
        return min(2, a)  # Suite
    else:
        return min(1, a)  # rien

################################################################################################################
###########################################  PROGRAMME PRINCIPAL  ##############################################
################################################################################################################
# le jeu commence!
joueurs = inserer_pieces()
POT = POINTS_PAR_JOUEUR * len(joueurs) + 1

# # # GPIO OUT # # # Affichage de la phase 'OUVERTURE'
PHASE = "intro"
intro = PhaseIntro()
joueurs = intro.run_phase()

# # # GPIO OUT # # # Affichage de la phase 'CHARGE'
PHASE = 'charge'
charge = PhaseCharge()
joueurs = charge.run_phase()

# # # GPIO OUT # # # Affichage de la phase 'DECHARGE'
PHASE = 'décharge'
decharge = PhaseDecharge()
joueurs = decharge.run_phase(joueurs)
