import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
from plyer import notification
import praw

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
    team_names_tag = soup.find_all('span', {'class': 'sdc-site-match-header__team-name-block-target'})
    if len(team_names_tag) == 2:
        team_names = [tag.text.strip() for tag in team_names_tag]
        return team_names
    return [None, None]

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

def post_match_results_on_reddit(resultats):
    # Initialize PRAW with your credentials
    reddit = praw.Reddit(client_id='ORjfzbSg3Lwdda56vMIl2w',
                         client_secret='2qLaVCWTNhGWOGtCI6DqB6a27Ta6nQ',
                         user_agent='Matchs',
                         username="Nathes67",
                         password="Nathan1101/")
    
    # Specify the subreddit
    subreddit = reddit.subreddit('footballM1SE')
    
    # Title for the Reddit post
    title = "Résultats des matchs de football"
    
    # Formatting match results
    match_results = []
    for index, row in resultats.iterrows():
        match_result = f"{row['Teams']} : {row['Score Home']} - {row['Score Away']}"
        match_results.append(match_result)
        
    # Adding a comment for each match result
    match_comments = []
    for index, row in resultats.iterrows():
        winner = row['Teams'].split('vs')[0].strip() if row['Score Home'] > row['Score Away'] else row['Teams'].split('vs')[1].strip()
        comment = f"Et une belle victoire pour {winner} !"
        match_comments.append(comment)
    
    # Combining match results and comments
    formatted_results = [f"{match_results[i]} : {match_comments[i]}" for i in range(len(match_results))]
    results_text = "\n\n".join(formatted_results)
    
    # Submit the post
    subreddit.submit(title, selftext=results_text, flair_id='488ba704-eb95-11ee-8165-56a069b14437')

def check_for_new_data_and_post_on_reddit():
    # Specify the path to the existing Excel file
    file_path = "C:/Users/natha/OneDrive/Bureau/M1/resultats_matchs/match_stats.xlsx"

    # Scrape new match details
    new_match_data_list = []
    match_number = 482591
    while match_number <= 482881:
        match_url = base_url + f"{match_number}/"
        match_data = scrape_match_details(match_url)
        new_match_data_list.append(match_data)
        match_number += 1

    # Create DataFrame from the list of new match data
    new_df = pd.DataFrame(new_match_data_list)

    # Check if the Excel file already exists
    if os.path.exists(file_path):
        # Load the existing DataFrame from the Excel file
        existing_df = pd.read_excel(file_path)

        # Check if there are any new rows of data
        new_rows = new_df[~new_df.isin(existing_df)].dropna()
        if not new_rows.empty:
            # Send notification
            notification.notify(
                title="New data added",
                message="New match data has been added to the Excel file.",
                timeout=10
            )
            
            # Post match results on Reddit
            post_match_results_on_reddit(new_rows)
    else:
        # If the Excel file doesn't exist, create it
        new_df.to_excel(file_path, index=False)
        print(f"DataFrame created and saved to {file_path}")
        
# Execute the function to check for new data and post on Reddit
check_for_new_data_and_post_on_reddit()