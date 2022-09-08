from bs4 import BeautifulSoup
import requests
import ssl
import urllib.request, urllib.parse, urllib.error
import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.utils import response

from lxml import html
from lxml import etree as ET

from selenium import webdriver

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


def export_last_3_results(team_name, team_number):
    team = team_name.lower()
    team = team.replace(" ", "-")

    results = []
    url = "https://www.livescore.com/en/football/team/" + f"{team}" + f"/{team_number}/" + "overview/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    scraped_home_team_names = soup.find_all('div', class_='Ij', id="undefined__home-team-name")
    scraped_away_team_names = soup.find_all('div', class_='Ij', id="undefined__away-team-name")
    scraped_home_team_goals = soup.find_all('div', class_='Nj')
    scraped_away_team_goals = soup.find_all('div', class_='Oj')

    home_team_names = []
    for home_team in scraped_home_team_names:
        home_team_names.append(home_team.text)

    away_team_names = []
    for away_team in scraped_away_team_names:
        away_team_names.append(away_team.text)

    home_team_goals = []
    for home_goals in scraped_home_team_goals:
        home_team_goals.append(home_goals.text)

    away_team_goals = []
    for away_goals in scraped_away_team_goals:
        away_team_goals.append(away_goals.text)

    for each_game in range(len(home_team_names)):
        results.append({home_team_names[each_game]: home_team_goals[each_game],
                        away_team_names[each_game]: away_team_goals[each_game]})

    return results


def export_team_location(team_name):
    WEBSITE_URL = 'https://int.soccerway.com'

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    agent = {
        "User-Agent": 'Mozilla/5.0'}

    league_url = "https://int.soccerway.com/national/bulgaria/a-pfg/20222023/regular-season/r70062/"
    page = requests.get(league_url, headers=agent)
    soup = BeautifulSoup(page.content, 'html.parser')

    football_clubs = []

    scraped_team_info = soup.find_all('td', class_='text team large-link')

    for el in scraped_team_info:
        scraped_team_url = el.contents[0].attrs['href']
        scraped_team_name = el.contents[0].attrs['title']
        # football_clubs.append({scraped_team_name: scraped_team_url})
        football_clubs.append({scraped_team_url: scraped_team_name})

    teams = export_team_names()

    replace_team_names = []

    for t_name in teams.values():
        replace_team_names.append(t_name)

    counter = 0

    while len(football_clubs) > len(replace_team_names):
        football_clubs.pop()

    for team in range(len(football_clubs)):
        for key, value in football_clubs[team].items():
            football_clubs[team][key] = replace_team_names[counter]
            counter += 1

    desired_url = ""
    for team in range(len(football_clubs)):
        for key, value in football_clubs[team].items():
            if value == team_name:
                desired_url = WEBSITE_URL + key
                break
        else:
            continue
        break
    page = requests.get(desired_url, headers=agent)
    soup = BeautifulSoup(page.content, 'html.parser')
    team = soup.find_all('dd')
    location_info = ''
    unedited_location = team[1].text
    first_edit_location = unedited_location.replace("\n ", "")
    second_edit_location = first_edit_location.replace("  ", "")

    location_info = second_edit_location

    return location_info


def load_bing_maps(location_name):
    bing_constant = 'https://www.bing.com/maps?q=+'
    # target_url = 'https://www.bing.com/maps?q=+bul.+Dragan+Tzankov+3%2C+Borisova+Gradina+1164+Sofia'

    location_url = location_name.replace(" ", "+")
    location_url = location_url.replace(",", "%2C")
    bing_address = bing_constant + location_url
    return bing_address


def estimated_distance(location_name):
    # Using Selenium

    PATH = "C:\Program Files (x86)\chromedriver.exe"
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(PATH, options=op)
    driver.get("https://www.bing.com/maps?q=+bul.+Dragan+Tzankov+3%2C+Borisova+Gradina+1164+Sofia")
    s = driver.find_element_by_class_name('geochainModuleLatLong').text
    print(s)


estimated_distance('bul. Rozhen 26 1220 Sofia')
