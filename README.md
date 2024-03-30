# Automatisation de la Publication des Résultats de la Premier League sur Reddit

MEHIYDINNE Sarah, SCHILD Nathan & SOMMER Zoé

Master APE 1ère année

UE Techniques de programmation
 
## Introduction

Ce document accompagne le projet réalisé dans le cadre de l'UE Techniques de Programmation. L'objectif principal de ce projet est d'automatiser la collecte et la publication des résultats des matchs de football de la Premier League pour la saison 2023-2024. Cela permettra aux passionnés de football de suivre facilement les derniers résultats et de participer à des discussions sur Reddit. En utilisant des techniques de scraping et d'interaction avec l'API Reddit, nous avons développé un système qui récupère automatiquement les résultats des matchs et les publie sur un subreddit dédié.

## Etapes du code

L'objectif principal de ce projet est de créer un système automatisé qui récupère les scores des matchs de football de la Premier League à partir du site Web de Skysports, puis les publie régulièrement sur le réseau social Reddit. Plus précisément, le projet est divisé en trois étapes principales :

i) Dans un premier temps, le but est de scrapper sur la page de Skysports (https://www.skysports.com/premier-league) les scores des matchs de football en Premier League pour la saison 2023-2024. Cette partie du code est lié au document Scrapping.py sur le github.

ii) Dans un second temps, le but a été de créer une application sur Reddit afin de poster régulièrement les résultats des matchs de la saison. Pour cela, il suffit de se rendre sur le site suivant : https://www.reddit.com/prefs/apps. Il convient de noter qu'il faut créer un compte Reddit avant de réaliser cette étape. Par la suite, nous avons dû créer un subreddit se nommant footballM1SE et pouvant être retrouvé à l'adresse suivante : https://www.reddit.com/r/footballM1SE. 

iii) Enfin, le but final était d'automatiser l'application afin que le bot reddit puisse publier automatiquement les résultats dès lors que des matchs sont joués avec un petit commentaire associé. Le code concernant cette partie se nomme Botreddit.py

iv) Une extension supplémentaire à envisager est de faire en sorte qu'avant les matchs, le bot puisse réaliser des prévisions.

## Comment exécuter le code ?

Pour exécuter le code, veuillez suivre les instructions fournies dans chaque script. Assurez-vous également de créer une application sur Reddit et de configurer les informations d'authentification dans le script Botreddit.py. Quelques pistes afin de vous aider :

i) Dans un premier temps, veuillez lancer le code `Scrapping.py` présent sur la github. Il convient de changer l'user agent, vous pourrez trouver le vôtre ici : https://www.whatismybrowser.com/detect/what-is-my-user-agent/. Pensez à changer le chemin du fichier excel créé.

ii) Par la suite, il faudra lancer le code `Botreddit.py`, cela générera automatiquement un post sur votre subreddit. Pensez à créer un subreddit et une application reddit.

iii) N'oubliez pas d'installer toutes les bibliothèques nécessaires : vous pouvez le faire en utilisant `pip install`.

## Bibliothèques et logiciels utilisés

Le projet utilise les bibliothèques suivantes :
- `requests`
- `BeautifulSoup` (pour le scrapping)
- `re`
- `pandas`
- `os`
- `time`
- `schedule`
- `plyer.notification`
- `praw` (Python Reddit API Wrapper, pour interagir avec l'API Reddit)

Pour toute question ou suggestion, n'hésitez pas à nous contacter.

