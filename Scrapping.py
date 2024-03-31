# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 12:27:31 2024

@author: nathan, zoé, et sarah M
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

# Base URL
base_url = 'https://www.skysports.com/football/burnley-vs-manchester-city/stats/'

# User agent header
user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}

# Function to get the HTML of the page
def get_page(urlpage):
    """
    Function to get the HTML of a webpage.

    Parameters:
    urlpage (str): The URL of the webpage.

    Returns:
    BeautifulSoup: Parsed HTML of the webpage.
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
    Function to scrape match details from a given URL.

    Parameters:
    match_url (str): The URL of the match.

    Returns:
    dict: Match details.
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
    Function to extract the match date from HTML.

    Parameters:
    soup (BeautifulSoup): Parsed HTML of the webpage.

    Returns:
    str: Match date.
    """
    match_date_tag = soup.find('time', {'class': 'sdc-site-match-header__detail-time'})
    return match_date_tag.get('aria-label').split(',')[1].strip() if match_date_tag else None

# Function to extract team names
def extract_team_names(soup):
    """
    Function to extract team names from HTML.

    Parameters:
    soup (BeautifulSoup): Parsed HTML of the webpage.

    Returns:
    list: List containing team names.
    """
    team_names_tag = soup.find_all('span', {'class': 'sdc-site-match-header__team-name-block-target'})
    if len(team_names_tag) == 2:
        team_names = [tag.text.strip() for tag in team_names_tag]
        return team_names
    return [None, None]

# Function to extract scores
def extract_scores(soup):
    """
    Function to extract scores from HTML.

    Parameters:
    soup (BeautifulSoup): Parsed HTML of the webpage.

    Returns:
    tuple: Scores for home and away teams.
    """
    score_home_tag = soup.find('span', {'data-update': 'score-home'})
    score_away_tag = soup.find('span', {'data-update': 'score-away'})
    return score_home_tag.text.strip() if score_home_tag else None, score_away_tag.text.strip() if score_away_tag else None

# Function to extract attendance
def extract_attendance(soup):
    """
    Function to extract attendance from HTML.

    Parameters:
    soup (BeautifulSoup): Parsed HTML of the webpage.

    Returns:
    str: Attendance.
    """
    attendance_tag = soup.find('span', {'class': 'sdc-site-match-header__detail-attendance'})
    return attendance_tag.contents[-1].strip() if attendance_tag else None

# Function to extract team stats
def extract_team_stats(stats_tag, team_type):
    """
    Function to extract team statistics from HTML.

    Parameters:
    stats_tag (list): List of HTML tags containing team statistics.
    team_type (str): Type of team ('Home' or 'Away').

    Returns:
    dict: Dictionary containing team statistics.
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

# Function to main
def main():
    """
    Main function to scrape match details and save them to Excel.
    """
    # Initial match number
    match_number = 482591
    
    match_data_list = []

    # Scrape match details from each match
    while match_number <= 482880:
        match_url = base_url + f"{match_number}/"
        match_data = scrape_match_details(match_url)
        match_data_list.append(match_data)

        match_number += 1

    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(match_data_list)

    # Specify the new path with .xlsx extension
    directory_path = "C:/Users/natha/OneDrive/Bureau/M1/resultats_matchs"
    file_path = os.path.join(directory_path, "match_stats.xlsx")

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Save DataFrame to Excel file
    df.to_excel(file_path, index=False)

    print(f"DataFrame created and saved to {file_path}")

if __name__ == "__main__":
    main()
