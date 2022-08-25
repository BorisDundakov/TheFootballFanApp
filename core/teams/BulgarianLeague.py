import requests


new_url = "https://prod-public-api.livescore.com/v1/api/app/stage/soccer/bulgaria/parva-liga/3?MD=1"
old_url = "https://www.livescore.com/en/football/bulgaria/parva-liga/table/"


def export_team_names():
    url = "https://prod-public-api.livescore.com/v1/api/app/stage/soccer/bulgaria/parva-liga/3?MD=1"

    football_clubs = []

    response = requests.get(url)
    # soup = BeautifulSoup(page.content, 'html.parser')
    json_file = (response.json())
    teams = (json_file['Stages'][0]['LeagueTable']['L'][0]['Tables'][0]['team'])

    for index in teams:
        team_name = index['Tnm']
        team_name.capitalize()
        football_clubs.append(team_name)

    return football_clubs


