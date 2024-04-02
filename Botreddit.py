#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 11:44:31 2024

@author: sarahmehiyddine
"""

import os
import re
import praw
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Base URL
base_url = 'https://www.skysports.com/football/burnley-vs-manchester-city/stats/'

# User agent header
user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}

# Function to get the HTML of the page
def get_page(urlpage):
    """
    Function to retrieve the HTML content of a webpage.

    Parameters:
    urlpage (str): The URL of the webpage.

    Returns:
    soup: The BeautifulSoup object containing the parsed HTML.
    """
    # Avoid getting banned
    # Get the HTML of the webpage
    print(f"Requesting {urlpage}")
    res = requests.get(urlpage, headers=user_agent)
    print(f"Response {res.status_code}")
    # Parse the HTML
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

# Function to scrape match details
def scrape_match_details(match_url):
    """
    Function to scrape match details from a given match URL.

    Parameters:
    match_url (str): The URL of the match.

    Returns:
    dict: A dictionary containing the scraped match details.
    """
    soup = get_page(match_url)

    # Extracting match details
    match_date = extract_match_date(soup)
    team_names = extract_team_names(soup)
    score_home, score_away = extract_scores(soup)
    attendance = extract_attendance(soup)

    home_stats_tag = soup.find_all('div', {'class': 'sdc-site-match-stats__stats-home'})
    away_stats_tag = soup.find_all('div', {'class': 'sdc-site-match-stats__stats-away'})

    home_stats = extract_team_stats(home_stats_tag, 'Home')
    away_stats = extract_team_stats(away_stats_tag, 'Away')

    # Create a dictionary with all the information
    match_data = {
        'Match Date': match_date,
        'Teams': f"{team_names[0]} vs {team_names[1]}",
        'Score Home': score_home,
        'Score Away': score_away,
        'Attendance': attendance,
        **home_stats,
        **away_stats
    }

    return match_data

# Function to extract match date
def extract_match_date(soup):
    """
    Function to extract the match date from the parsed HTML.

    Parameters:
    soup: The BeautifulSoup object containing the parsed HTML.

    Returns:
    str: The extracted match date.
    """
    match_date_tag = soup.find('time', {'class': 'sdc-site-match-header__detail-time'})
    return match_date_tag.get('aria-label').split(',')[1].strip() if match_date_tag else None

# Function to extract team names
def extract_team_names(soup):
    """
    Function to extract the team names from the parsed HTML.

    Parameters:
    soup: The BeautifulSoup object containing the parsed HTML.

    Returns:
    list: A list containing the extracted team names.
    """
    team_names_tag = soup.find_all('span', {'class': 'sdc-site-match-header__team-name-block-target'})
    if len(team_names_tag) == 2:
        team_names = [tag.text.strip() for tag in team_names_tag]
        return team_names
    return [None, None]

# Function to extract scores
def extract_scores(soup):
    """
    Function to extract the match scores from the parsed HTML.

    Parameters:
    soup: The BeautifulSoup object containing the parsed HTML.

    Returns:
    tuple: A tuple containing the extracted home and away scores.
    """
    score_home_tag = soup.find('span', {'data-update': 'score-home'})
    score_away_tag = soup.find('span', {'data-update': 'score-away'})
    return score_home_tag.text.strip() if score_home_tag else None, score_away_tag.text.strip() if score_away_tag else None

# Function to extract attendance
def extract_attendance(soup):
    """
    Function to extract the match attendance from the parsed HTML.

    Parameters:
    soup: The BeautifulSoup object containing the parsed HTML.

    Returns:
    str: The extracted attendance.
    """
    attendance_tag = soup.find('span', {'class': 'sdc-site-match-header__detail-attendance'})
    return attendance_tag.contents[-1].strip() if attendance_tag else None

def extract_team_stats(stats_tag, team_type):
    """
    Function to extract team statistics from the parsed HTML.

    Parameters:
    stats_tag: The BeautifulSoup object containing the parsed HTML for team statistics.
    team_type (str): The type of team ('Home' or 'Away').

    Returns:
    dict: A dictionary containing the extracted team statistics.
    """
    stats_labels = ['Possession', 'Tirs', 'Tirs Cadres', 'Tirs Non Cadres', 'Blocked Shots', 
                    'Completed Passes', 'Clear Cut', 'Corner', 'Offsides', 'Tackles Completed', 
                    'Aerial Duels', 'Saves', 'Fouls', 'Fouls Won', 'Yellow Cards', 'Red Cards']

    team_stats = {}
    for i, stat in enumerate(stats_tag):
        label = stats_labels[i] + ' ' + team_type
        value = re.search(r'\d+', stat.get_text(strip=True)).group() if stat else None
        team_stats[label] = value

    return team_stats

# Fonction pour récupérer le commentaire associé à l'équipe gagnante
def commentaire_equipe_gagnante(equipe):
    """
    Function to retrieve the comment associated with the winning team.

    Parameters:
    equipe (str): The name of the winning team.

    Returns:
    str: The comment associated with the winning team.
    """
    commentaires_gagnants = {
        'Arsenal': "Magnifique Victoire, ils ont dégainé l’artillerie !",
        'Aston Villa': "Martin vit dans une villa, assurément la victoire est à Aston !",
        'Bournemouth': "Soirée mousse pour fêter cette victoire !",
        'Brentford': "Aussi rapide et puissant qu’une bonne vieille Ford ! Bravo !",
        'Brighton and Hove Albion': "Encore une victoire brillante !",
        'Burnley': "Ils ont tout brulé sur leur passage ! Bravo !",
        'Chelsea': "Bravo ! De vrais guerriers en mer !",
        'Crystal Palace': "Une victoire aussi belle qu’un million de diamant !",
        'Everton': "Ils ont donné le ton sur ce match !",
        'Fulham': "Une belle âme de vainqueur ! Bravo !",
        'Liverpool': "Les reds ont passé le feu au rouge et ont décroché la victoire !",
        'Luton Town': "Aussi malicieux que des lutins !",
        'Manchester City': "Le ciel fut bleu et accueillant, belle victoire pour les skyblues",
        'Manchester United': "Ils se sont unis pour la victoire ! Bravo !",
        'Newcastle United': "Belle défense de leur château sur ce match !",
        'Nottingham Forest': "A croire qu’ils ont les clés de la forêt de la victoire !",
        'Sheffield United': "Des chefs ! Bravo pour leur Victoire !",
        'Tottenham Hotspur': "Tellement fort, on leur décernerait un totem pour cette victoire !",
        'West Ham United': "Le soleil s’est à l’ouest aujourd’hui ! Bravo !",
        'Wolverhampton': "Les loups sont de sortis ! Bravo !"
    }
    return commentaires_gagnants.get(equipe, "Équipe non trouvée !")

# Fonction pour récupérer le commentaire associé à l'équipe perdante
def commentaire_equipe_perdante(equipe):
    """
    Function to retrieve the comment associated with the losing team.

    Parameters:
    equipe (str): The name of the losing team.

    Returns:
    str: The comment associated with the losing team.
    """
    commentaires_perdants = {
        'Arsenal': "Ils n’avaient plus que des balles à blanc malheureusement !",
        'Aston Villa': "Martin a déménagé de la villa, emmenant avec lui la victoire d’Aston",
        'Bournemouth': "Trop dur à prononcer, défaite méritée …",
        'Brentford': "Le fordisme n’était pas très utile sur le terrain …",
        'Brighton and Hove Albion': "Aveuglés par le soleil, ils n’ont pas réussi à atteindre la victoire …",
        'Burnley': "Ils ont été brulés …",
        'Chelsea': "Malheureusement la houle fut tumultueuse …",
        'Crystal Palace': "Malgré un palace, le cristal reste une chose fragile … Dommage !",
        'Everton': "Ils ont chanté faux cette fois ci, dommage …",
        'Fulham': "Ils ont rendu l’âme …",
        'Liverpool': "Aïe aïe aïe, les reds ont vu rouge !",
        'Luton Town': "Les lutins farceurs n’ont pas été très malicieux …",
        'Manchester City': "Des nuages sont venus couvrir le ciel bleu … Dommage !",
        'Manchester United': "Défaite de Man chest er (ils n’étaient pas unis).",
        'Newcastle United': "Ils ont acheté un château en Espagne, pas de victoire en Angleterre !",
        'Nottingham Forest': "A croire que la balle s’est perdue au fond des bois …",
        'Tottenham': "Ils n’ont pas réussi à éperonner la victoire, dommage …",
        'West Ham United': "Dommage ! L’équipe était à l’ouest pendant ce match …",
        'Wolverhampton': "Trop dur à prononcer, défaite méritée …"
    }
    return commentaires_perdants.get(equipe, "Équipe non trouvée !")

def check_for_new_data_and_post_on_reddit():
    """
    Function to check for new match data and post on Reddit.
    """
    # Specify the path to the existing Excel file
    file_path = "/Users/zoesommer/Documents/FAC M1/S2/PP/Résultat_Match/match_stats.xlsx"

    # Scrape new match details
    new_match_data_list = []
    match_number = 482885
    while match_number <= 482886:
        match_url = base_url + f"{match_number}/"
        match_data = scrape_match_details(match_url)
        new_match_data_list.append(match_data)
        match_number += 1

    # Create DataFrame from the list of new match data
    new_df = pd.DataFrame(new_match_data_list)
    
    # Replace empty scores with a placeholder value
    new_df['Score Home'].replace('', 'N/A', inplace=True)
    new_df['Score Away'].replace('', 'N/A', inplace=True)

    # Check if the Excel file already exists
    if os.path.exists(file_path):
        # Load the existing DataFrame from the Excel file
        existing_df = pd.read_excel(file_path)

        # Check if there are any new rows of data
        new_rows = new_df[~new_df.isin(existing_df)]
        if not new_rows.empty:
            # Post match results on Reddit
            post_match_results_on_reddit(new_rows)
    else:
        # If the Excel file doesn't exist, create it
        new_df.to_excel(file_path, index=False)
        print(f"DataFrame created and saved to {file_path}")

def post_match_results_on_reddit(resultats):
    """
    Function to post match results on Reddit.

    Parameters:
    resultats (DataFrame): The DataFrame containing match results.
    """
    # Initialize PRAW with your credentials
    reddit = praw.Reddit(client_id='bQ3mcMhH90oqM4Amni93Yg',
                         client_secret='NZXa7P7qEkcHN4j0O8aJbp7v52Us6w',
                         user_agent='GigaFootM1PP',
                         username="zoepalacios47",
                         password="Petunia2024!!")
    
    # Specify the subreddit
    subreddit = reddit.subreddit('footballPROJECT')
    
    # Title for the Reddit post
    title = "Résultats des matchs de football"
    
    # Create a string to store the post content
    post_content = ""
    
    # Iterate through each row in the DataFrame
    for index, row in resultats.iterrows():
        # Extract the date of the match from the DataFrame
        match_date = row['Match Date']
        
        # Format the match date
        formatted_date = pd.to_datetime(match_date).strftime('%Y-%m-%d')
        
        # Format the match result
        match_result = f"{row['Teams']} : {row['Score Home']} - {row['Score Away']}"
        
        # Initialize winner variable
        winner = None
        
        # Determine the winner or if it's a draw
        if row['Score Home'] != "" and row['Score Away'] != "":
            if row['Score Home'] > row['Score Away']:
                winner = row['Teams'].split('vs')[0].strip()
                comment_winner = f"{winner} : {commentaire_equipe_gagnante(winner)}\n"
                loser = row['Teams'].split('vs')[1].strip()
                comment_loser = f"{loser} : {commentaire_equipe_perdante(loser)}\n"
            elif row['Score Home'] < row['Score Away']:
                winner = row['Teams'].split('vs')[1].strip()
                comment_winner = f"{winner} : {commentaire_equipe_gagnante(winner)}\n"
                loser = row['Teams'].split('vs')[0].strip()
                comment_loser = f"{loser} : {commentaire_equipe_perdante(loser)}\n"
            else:
                # Match nul
                comment_winner = "Match nul : Dommage les deux équipes n'ont pas su se départager, vraiment nul ce match !\n"
                comment_loser = ""
        else:
            # Match nul (scores non disponibles)
            comment_winner = "Match nul : Dommage les deux équipes n'ont pas su se départager, vraiment nul ce match\n"
            comment_loser = ""
        
        # Construct the match details
        match_details = f"Match du {formatted_date}\n{match_result}\n\n{comment_winner}\n{comment_loser}\n{'-'*30}\n\n"
        
        # Add the match details to the post content
        post_content += match_details
    
    # Submit the post
    subreddit.submit(title, selftext=post_content.strip(), flair_id=' fbd5a700-f0fa-11ee-b2fc-66ed8fc74fea')

# Execute the function to check for new data and post on Reddit
check_for_new_data_and_post_on_reddit()

