# D-Mur-Jeu---421
Programme d'un (futur) jeu de 421 mural.

import random

# === CONSTANTES ===
NB_POSITIONS_JOUEUR = 5
POINTS_PAR_JOUEUR = 5

# === VARIABLES ===
phase = 'intro'   #'intro', 'charge', 'décharge'

# === CLASSES ===
class Joueur:
    def __init__(self, position):
        self.position = position
        self.points = 0
        self.etat = 'joueur'  # 'joueur', 'waiting...' ou 'spectateur'
        self.score = []
        self.lancers = 0

    def __str__(self):
        return f"J{self.position}(pts={self.points}, etat={self.etat}, score={self.score}, lancers={self.lancers})"


# === FONCTIONS ===
def inserer_pieces():
    # Simule les joueurs ayant mis une piece : positions 1 à 12, booléen aléatoire
    actifs = [random.choice([True, True]) for _ in range(NB_POSITIONS_JOUEUR)]
    joueurs = [Joueur(i + 1) for i, actif in enumerate(actifs) if actif]
    print(f"{len(joueurs)} joueurs en jeu : {[j.position for j in joueurs]}")
    return joueurs

def lancer_des(nb):
    return sorted([random.randint(1, 6) for _ in range(nb)], reverse=True)

def score_value(score):
    if phase == 'intro':
        return score
    # Évalue le score et attribue un score de force afin de hiérarchiser les scores du tour
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

def jeton_par_score(score, pot, points, phase):
    # Évalue le score et attribue un nombre de jeton associé au score
    if phase == 'charge':
        a = pot
    else:
        a = points
    if score == [4, 2, 1]:
        if phase == 'charge':
            return min(10, a)  # Score max : 421
        elif phase == 'décharge' and len(temp_joueurs) > 2:
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

def jouer_tour(joueur, max_lancers):
    if phase == 'intro':
        nb_des = 1
    else:
        nb_des = 3
    print(f"\n-- Joueur {joueur.position} --")
    des = lancer_des(nb_des)
    print(f"Lancer 1/{max_lancers}:", des)
    joueur.lancers = 1
    while joueur.lancers < max_lancers:
        choix = input("Voulez-vous relancer ? (y/n) ").lower()
        if choix == 'n':
            break
        garder = [input(f"Relancer le dé {d} ? (y/n): ").lower() == 'n' for d in des]
        for i in range(nb_des):
            if not garder[i]:
                des[i] = random.randint(1, 6)
        des.sort(reverse=True)
        joueur.lancers += 1
        print(f"Lancer {joueur.lancers}/{max_lancers}: {des}")

    joueur.score = des
    print(f"Score final: {des}\n      Validé en {joueur.lancers} lancer(s)\n-----------------")

def resoudre_tour(joueurs, pot, phase):
    perdants = []
    gagnants = []
    if phase == 'intro':
        scores = [(j.score, j) for j in joueurs if j.etat == 'joueur']
        scores.sort(key=lambda x: x[0])  # Score le plus bas en premier
        n = 0
        for j in joueurs:
            if j.score == scores[-1][0]:
                gagnants.append(j)
        while len(gagnants) > 1:
            n += 1
            print("\nc'est l'heure du-du-du-du-du DUEL! (ça commence bien...)")
            print(f"=== Duel gagnant : {len(gagnants)} joueurs ===")
            gagnants = duel_gagnant(gagnants)
        gagnant = gagnants[0]
        gagnant.score = scores[-1][0]
        print(f"\nLe premier joueur à commencer est le joueur {gagnants[0].position} avec {gagnants[0].score}")
        phase = 'charge'
        print("----------------------------------")
        return 0, gagnant
    else:
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

def comparer_nb_lancers(joueurs, a): # merci GPT...y'avait plus de boucles itératives dans ma fonction que dans des cheveux crépus.
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
    joueurs_filtrés = [j for j in joueurs if j.lancers == reference]

    # Affichage du résultat
    print(f"\nNombre de lancers retenu : {reference}")
    print("Joueurs retenus :", [j.position for j in joueurs_filtrés])

    return joueurs_filtrés

def duel_perdant(joueurs):
    score_temp = joueurs[0].score
    joueurs = comparer_nb_lancers(joueurs, True)

    if len(joueurs) > 1:
        for j in joueurs:
            print(f"Joueur {j.position}")
            j.score = lancer_des(3)
            print(j.score)
        scores_duel = [(score_value(j.score), j.score, j) for j in joueurs]
        scores_duel.sort(key=lambda x: x[0])  # Score le plus bas en premier
        perdants = []
        for j in joueurs:
            if j.score == scores_duel[0][1]:
                perdants.append(j)
        for j in joueurs:
            j.score = score_temp
    if len(joueurs) == 1:
        perdants = joueurs
    return perdants
def duel_gagnant(joueurs):
    score_temp = joueurs[0].score
    joueurs = comparer_nb_lancers(joueurs, False)
    if len(joueurs) > 1:
        for j in joueurs:
            print(f"Joueur {j.position}, à ton tour.")
            j.score = lancer_des(1 if phase == 'intro' else 3)
            print(j.score)
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

def passer_en_spectateur(joueurs):
    for j in joueurs:
        if j.points <= 0:
            j.etat = 'spectateur'

def passer_en_attente(joueurs):
    for j in joueurs:
        j.etat = 'waiting...'

def passer_en_joueur(joueurs):
    for j in joueurs:
        j.etat = 'joueur'

def afficher_etat(joueurs):
    for j in joueurs:
        print(j)

def changer_phase(x):
    phase = x
    return phase

def repartition_points(pot, gagnant, perdant, phase):
    jetons = jeton_par_score(gagnant.score, pot, gagnant.points, phase)
    if phase == 'décharge':
        perdant.points += min(jetons, gagnant.points)
        gagnant.points -= min(jetons, gagnant.points)
        if gagnant.points == 0:
            gagnant.etat = 'spectateur'
            print(f"le joueur {gagnant.position} est sauvé")
            print(f"\n=== TABLEAU DES POINTS ===")
        for j in joueurs:
            if j.etat == 'joueur':
                print(f"Joueur {j.position} : {j.points} jetons")
    if phase == 'charge':
        perdant.points += jetons
        pot -= jetons
        if pot > 0:
            print(f"\n=== TABLEAU DES POINTS ===\n===  POT : {pot} jetons   ===")
            for j in joueurs:
                if j.points > 0:
                    print(f"Joueur {j.position} : {j.points} jetons")
        if pot == 0:
            print(f"\n=== TABLEAU DES POINTS ===\n===  POT : {pot} jetons   ===")
            for j in joueurs:
                if j.points > 0:
                    print(f"Joueur {j.position} : {j.points} jetons")
            input("\n ./!\ /!\ /!\ LA BANQUE SAUTE /!\ /!\ /!\. ")
            for x in joueurs:
                if x.points == 0:
                    x.etat = 'spectateur'
                    print(f"le joueur {x.position} est sauvé")
            print("\n=== PHASE DECHARGE ===\nCette phase se jouera avec les joueurs suivants:\n")
            for x in joueurs:
                if x.etat == 'joueur':
                    print(f"Joueur {x.position} : {x.points} jetons")
            phase = changer_phase('décharge')
    return pot, phase

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


def phase_intro(joueurs):
    print("\n        BIENVENUE POUR CETTE PARTIE DE\n")
    print("        =============================\n"
          "        =      ##     ###     ##    =\n"
          "        =     # #    #   #   # #    =\n"
          "        =    #  #       #   #  #    =\n"
          "        =   #######    #       #    =\n"
          "        =       #     #        #    =\n"
          "        =       #    #####   ####   =\n"
          "        =============================\n")
    print(f"        NOMBRE DE JOUEURS : {len(joueurs)}")
    print(f"        NOMBRE DE JETONS DANS LE POT : {pot}\n")
    print("=== PHASE PRÉLIMINAIRE ===")
    print("Veuillez lancer 1 dé à tour de rôle pour déterminer le premier joueur")
    for j in joueurs:
        jouer_tour(j, 1)
    nb_tour, gagnant = resoudre_tour(joueurs, pot, phase)
    joueurs = ordre_passage(joueurs, gagnant.position)
    return joueurs

# === PROGRAMME PRINCIPAL ===
# init
joueurs = inserer_pieces()
pot = POINTS_PAR_JOUEUR * len(joueurs) + 1
nb_tour = 0
# Phase préliminaire
joueurs = phase_intro(joueurs)

# Phase CHARGE
phase = 'charge'
while phase == 'charge':
    nb_tour += 1
    print(f"\n=== PHASE {phase.upper()} === TOUR {nb_tour} ===")
    for j in joueurs:
        jouer_tour(j, 3 if phase == 'décharge' else 1)
    perdant, gagnant = resoudre_tour(joueurs, pot, phase)
    pot, phase = repartition_points(pot, gagnant, perdant, phase)
    print(f"\n----------------------------------\n")
    joueurs = ordre_passage(joueurs, perdant.position)

# Phase DECHARGE
phase = 'décharge'
temp_joueurs = []
for j in joueurs:
    if j.etat == 'joueur':
        temp_joueurs.append(j)
while len(temp_joueurs) > 1:
    nb_tour += 1
    print(f"\n=== PHASE {phase.upper()} === TOUR {nb_tour} ===")
    jouer_tour(temp_joueurs[0], 3)
    for j in temp_joueurs[1:]:
        jouer_tour(j, temp_joueurs[0].lancers)

    perdant, gagnant = resoudre_tour(joueurs, pot, phase)
    pot, phase = repartition_points(pot, gagnant, perdant, phase)
    print(f"\n----------------------------------")
    temp_joueurs = []
    for j in joueurs:
        if j.etat == 'joueur':
            temp_joueurs.append(j)
    temp_joueurs = ordre_passage(temp_joueurs, perdant.position)
    ### PROBLEME LORS DE LA DECHARGE, LE PREMIER JOUEUR DU TOUR N'EST PAS FORCEMENT LE PERDANT DU TOUR PRECEDENT...

# FIN
print(f"NOUS AVONS UN GRAND PERDANT\n BRAVO AU JOUEUR {perdant.position} D'AVOIR ÉTÉ SI NUL")
print("Merci les nazes d'avoir joué\n\n                                       - Superc3be")

# A CORRIGER :
# Ligne 361 - généralement le perdant du tour n gagne (lot de compensation) un avantage lors du tour suivant et commence le tour (donc définit le nombre de lancers maximal, mais. mais. mais. lors de la décharge (uniquement) ce n'est pas le cas...et je n'identifie pas l'origine de l'erreur bien que ca ne doit être qu'un souci d'organisation de l'architecture du programme. dick me.
# Global : beaucoup trop de répétitions/boucles itératives, beaucoup d'appel a fonction superflus, condensation possible du programme avec une meilleure synthaxe
# In fine : Lorsqu'un joueur perd il devient "mortel" et ne doit pas perdre une deuxième fois. Le jeu s'arrête lorsqu'un joueur devenu mortel perd.

# SUITE :
# 1 - Créer une interface très simple (qui servira d'émulateur/debug du jeu physique).
# 2 - Acheter un raspberry-pi, cerveaux-moteurs, LED, petit écran,... coupler le bazar pour que ça émule le programme.
# 3 - Modéliser en 3D les pièces du boitier ---> Contacter Yv pour le fer forgé ---> Biot pour le verre souflé ---> Trouver menuisier chouette
# 4 - Assemblage et test resistances des matériaux, robustesse du programme, Modding, Personnalisation
