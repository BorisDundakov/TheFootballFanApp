from bs4 import BeautifulSoup
import requests

new_url = "https://prod-public-api.livescore.com/v1/api/app/stage/soccer/bulgaria/parva-liga/3?MD=1"
old_url = "https://www.livescore.com/en/football/bulgaria/parva-liga/table/"


def export_team_names():
    url = "https://prod-public-api.livescore.com/v1/api/app/stage/soccer/bulgaria/parva-liga/3?MD=1"

    football_clubs = {}

    response = requests.get(url)
    # soup = BeautifulSoup(page.content, 'html.parser')
    json_file = (response.json())
    teams = (json_file['Stages'][0]['LeagueTable']['L'][0]['Tables'][0]['team'])

    for index in teams:
        team_name = index['Tnm']
        team_number = index['Tid']
        team_name.capitalize()
        football_clubs[team_number] = team_name

    return football_clubs


def export_next_fixture(team_name, team_number):
    team = team_name.lower()
    team = team.replace(" ", "-")
    # https://www.livescore.com/en/football/team/levski-sofia/6552/overview/
    # https://www.livescore.com/en/football/team/team-name/1111/overview/
    result = {"home": 0, "away": 0}
    url = "https://www.livescore.com/en/football/team/" + f"{team}" + f"/{team_number}/" + "overview/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    team_names = soup.find_all('span', class_='li')
    for team_name in range(len(team_names)):
        if team_name == 0:
            result['home'] = team_names[team_name].text
        else:
            result['away'] = team_names[team_name].text

    return result

