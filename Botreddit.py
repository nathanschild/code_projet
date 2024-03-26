# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 17:52:02 2024

@author: natha
"""

import praw
import pandas as pd

# Initialiser PRAW avec vos informations d'identification
reddit = praw.Reddit(client_id='ORjfzbSg3Lwdda56vMIl2w',
                     client_secret='2qLaVCWTNhGWOGtCI6DqB6a27Ta6nQ',
                     user_agent='Matchs',
                     username="Nathes67",
                     password="Nathan1101/")

# Créer une fonction pour poster sur Reddit
def poster_resultats_sur_reddit(resultats):
    subreddit = reddit.subreddit('footballM1SE')  # Remplacez 'NomDuSubreddit' par le nom du subreddit où vous voulez publier
    title = "Résultats des matchs de football"
    subreddit.submit(title, selftext=resultats, flair_id='488ba704-eb95-11ee-8165-56a069b14437')

# Résultat simplifié pour le test
resultat_test = """
Match 1:
Equipe A 2 - 1 Equipe B

Match 2:
Equipe C 0 - 0 Equipe D
"""

# Publier sur Reddit si l'authentification a réussi
if reddit.user.me():
    poster_resultats_sur_reddit(resultat_test)
else:
    print("L'authentification avec Reddit a échoué. Impossible de publier sur Reddit.")