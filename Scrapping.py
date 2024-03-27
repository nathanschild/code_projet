# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 12:27:31 2024

@author: nathan , zoé et sarah M
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
    match_date_tag = soup.find('time', {'class': 'sdc-site-match-header__detail-time'})
    return match_date_tag.get('aria-label').split(',')[1].strip() if match_date_tag else None

# Function to extract team names
def extract_team_names(soup):
    team_names_tag = soup.find('p', {'class': 'sdc-site-match-header__detail-fixture'})
    return team_names_tag.text.split(' vs ') if team_names_tag else [None, None]

# Function to extract scores
def extract_scores(soup):
    score_home_tag = soup.find('span', {'data-update': 'score-home'})
    score_away_tag = soup.find('span', {'data-update': 'score-away'})
    return score_home_tag.text.strip() if score_home_tag else None, score_away_tag.text.strip() if score_away_tag else None

# Function to extract attendance
def extract_attendance(soup):
    attendance_tag = soup.find('span', {'class': 'sdc-site-match-header__detail-attendance'})
    return attendance_tag.contents[-1].strip() if attendance_tag else None

def extract_team_stats(stats_tag, team_type):
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
    # Initial match number
    match_number = 482591
    
    match_data_list = []

    # Scrape match details from each match
    while match_number <= 482971:
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