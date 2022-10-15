from bs4 import BeautifulSoup
import requests
import ssl
import geocoder
import time
from time import strptime
import asyncio

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# TODO: Put these addresses into constants file and reference them from there
new_url = "https://prod-public-api.livescore.com/v1/api/app/stage/soccer/bulgaria/parva-liga/3?MD=1"
old_url = "https://www.livescore.com/en/football/bulgaria/parva-liga/table/"


def export_team_names():
    URL = "https://prod-public-api.livescore.com/v1/api/app/stage/soccer/bulgaria/parva-liga/3?MD=1"
    football_clubs = {}
    response = requests.get(URL)
    json_file = (response.json())
    teams = (json_file['Stages'][0]['LeagueTable']['L'][0]['Tables'][0]['team'])

    for index in teams:
        team_name = index['Tnm']
        team_number = index['Tid']
        team_name.capitalize()
        football_clubs[team_number] = team_name

    return football_clubs


def export_matchday_results():
    LEAGUE_URL = "https://www.flashscore.com/football/bulgaria/parva-liga/"
    PATH = "C:\Program Files (x86)\chromedriver.exe"  # PATH TO THE chromedriver.exe downloaded (check requirements.txt)
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    op.add_argument('--blink-settings=imagesEnabled=false')  # blocking images load to increase program speed
    driver = webdriver.Chrome(PATH, options=op)
    driver.get(LEAGUE_URL)

    # ACCEPTING COOKIES
    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

    gameweek = driver.find_element_by_class_name("event__round.event__round--static").text

    gameweek_results = []

    home_teams = driver.find_elements_by_class_name("event__participant.event__participant--home")
    home_goals = driver.find_elements_by_class_name("event__score.event__score--home")
    away_teams = driver.find_elements_by_class_name("event__participant.event__participant--away")
    away_goals = driver.find_elements_by_class_name("event__score.event__score--away")

    for el in range(len(home_teams)):
        if el == 8:
            return gameweek, gameweek_results

        gameweek_results.append(

            [{home_teams[el].text: home_goals[el].text}, {away_teams[el].text: away_goals[el].text}])

    driver.quit()


def export_next_fixture(team_name, team_number):
    team = team_name.lower()
    team = team.replace(" ", "-")
    result = {"home": 0, "away": 0, "home_badge": '', "away_badge": ''}
    url = "https://www.livescore.com/en/football/team/" + f"{team}" + f"/{team_number}/" + "overview/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    team_names = soup.find_all('span', class_='Pi')
    for team_name in range(len(team_names)):
        if team_name == 0:
            result['home'] = team_names[team_name].text
        else:
            result['away'] = team_names[team_name].text

    last_game_info = soup.find_all('div', class_='Oi')

    for el in last_game_info:
        badges = el.find_all_next("img")
        result["away_badge"] = badges[2]['src']
        result["home_badge"] = badges[5]['src']

    PATH = "C:\Program Files (x86)\chromedriver.exe"  # PATH TO THE chromedriver.exe downloaded (check requirements.txt)
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(PATH, options=op)
    driver.get(url)

    match_info = driver.find_element_by_class_name("Ui").text
    game_details = list(match_info.split("\n"))

    game_time = game_details[0]
    game_date = game_details[1]

    result['weekday'] = game_date
    result['game_time'] = game_time
    driver.quit()
    return result


def export_last_game_badges(team_name, team_number):
    team = team_name.lower()
    team = team.replace(" ", "-")
    url = "https://www.livescore.com/en/football/team/" + f"{team}" + f"/{team_number}/" + "overview/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    badges = {}
    last_game_badges = soup.find('div', class_='Sj')

    for el in last_game_badges:
        x = el.find_all_next("img")
        badges["home"] = x[2]['src']
        badges["away"] = x[5]['src']
        break

    return badges


def export_last_3_results(team_name, team_number):
    start = time.time()

    team = team_name.lower()
    team = team.replace(" ", "-")

    results = []
    url = "https://www.livescore.com/en/football/team/" + f"{team}" + f"/{team_number}/" + "overview/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    scraped_home_team_names = soup.find_all('div', class_='Jj', id="undefined__home-team-name")
    scraped_away_team_names = soup.find_all('div', class_='Jj', id="undefined__away-team-name")
    scraped_home_team_goals = soup.find_all('div', class_='Oj')
    scraped_away_team_goals = soup.find_all('div', class_='Pj')

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

    end = time.time()

    # print("Export_last_3_results is :",
    #       (end - start) * 10 ** 3, "ms")

    return results


def export_team_location(team_name):
    # TODO: Reduce function complexity (count of for loops)

    start = time.time()

    WEBSITE_URL = 'https://int.soccerway.com'

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    AGENT = {
        "User-Agent": 'Mozilla/5.0'}

    LEAGUE_URL = "https://int.soccerway.com/national/bulgaria/a-pfg/20222023/regular-season/r70062/"
    page = requests.get(LEAGUE_URL, headers=AGENT)
    soup = BeautifulSoup(page.content, 'html.parser')

    football_clubs = []

    scraped_team_info = soup.find_all('td', class_='text team large-link')

    teams = export_team_names()

    for el in scraped_team_info:
        scraped_team_url = el.contents[0].attrs['href']
        scraped_team_name = el.contents[0].attrs['title']
        football_clubs.append({scraped_team_url: scraped_team_name})
        if len(football_clubs) == len(teams):
            break

    replace_team_names = []

    for t_name in teams.values():
        replace_team_names.append(t_name)

    counter = 0
    desired_url = ""
    for team in range(len(football_clubs)):
        for key, value in football_clubs[team].items():
            football_clubs[team][key] = replace_team_names[counter]
            counter += 1
            if football_clubs[team][key] == team_name:
                desired_url = WEBSITE_URL + key
                break
        else:
            continue
        break

    page = requests.get(desired_url, headers=AGENT)
    soup = BeautifulSoup(page.content, 'html.parser')
    team = soup.find_all('dd')

    if team[0].text.isdigit():
        unedited_location = team[1].text
        unedited_location = unedited_location.strip()
        unedited_location = unedited_location.replace("\n          ", "0")
        count_new_lines = unedited_location.count("0")

        for i in range(count_new_lines - 1):
            unedited_location = unedited_location.replace("0", "", 1)
        if count_new_lines:
            unedited_location = unedited_location.replace("0", ", ")

        unedited_location = unedited_location.replace("\n ", "")
        unedited_location = unedited_location.replace("  ", "")

        if unedited_location == 'Sofia' or unedited_location == 'Pazardzhik':
            if team_name == 'CSKA 1948':
                unedited_location = 'Stadion Bistritsa, 1 ulitsa Sportist, Pancharevo, Bulgaria'
            else:
                unedited_location = 'Stadion Vasil Levski, Sredets, Bulgaria'

    else:
        unedited_location = team[0].text
        unedited_location = unedited_location.strip()
        unedited_location = unedited_location.replace("\n ", "")
        unedited_location = unedited_location.replace("  ", "")

    location_info = unedited_location

    end = time.time()

    # print("Export_location is :",
    #       (end - start) * 10 ** 3, "ms")

    return location_info


def load_bing_maps(location_name):
    bing_constant = 'https://www.bing.com/maps?q=+'

    location_url = location_name.replace(" ", "+")
    location_url = location_url.replace(",", "%2C")
    bing_address = bing_constant + location_url

    return bing_address


# noinspection DuplicatedCode
def get_my_location():
    myloc = geocoder.ip('me')
    current_loc = myloc.latlng
    return current_loc


def locate_nearest_trainstation(current_loc):
    x = current_loc[0]
    y = current_loc[1]

    bing_constant = 'https://www.bing.com/maps?q=+'
    # https://www.bing.com/maps?q=+42.69775,+23.3241
    bing_address = bing_constant + f'{x},+'f'{y}'
    driver = chromedriver_setup(bing_address)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#bnp_btn_accept"))).click()
    near_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".nearbyBtn .ibs_btn"))).click()

    search_bar = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#maps_sb")))

    ActionChains(driver).move_to_element(search_bar)
    search_bar.send_keys('train station')
    search_icon = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".searchIcon"))).click()
    time.sleep(5)
    # .nameContainer
    try:
        station = driver.find_element_by_class_name('eh_text_outer')
    except selenium.common.exceptions.NoSuchElementException:
        station = driver.find_element_by_css_selector('li:nth-child(1) .b_vPanel div:nth-child(1) .b_factrow')

    nearest_station = station.text
    driver.quit()
    return nearest_station


def locate_departure_trainstation(bing_address):
    driver = chromedriver_setup(bing_address)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#bnp_btn_accept"))).click()
    near_btn = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".nearbyBtn .ibs_btn"))).click()

    search_bar = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#maps_sb")))

    ActionChains(driver).move_to_element(search_bar)
    search_bar.send_keys('train station')
    search_icon = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".searchIcon"))).click()
    time.sleep(5)
    # .nameContainer
    try:
        station = driver.find_element_by_class_name('eh_text_outer')
    except selenium.common.exceptions.NoSuchElementException:
        station = driver.find_element_by_css_selector('li:nth-child(1) .b_vPanel div:nth-child(1) .b_factrow')

    departure_station = station.text
    driver.quit()
    return departure_station


def generate_railways_website_link(starting_station, departure_station, weekday, game_time):
    pass
    bulgarian_railways_website = 'https://www.bdz.bg/bg'
    # #from, #to
    # 'Централна Железопътна гара - Пловдив'; 'Central Railway Station Sofia - София'
    railway_cities_BG = ['София', 'Варна', 'Бургас', 'Пловдив', 'Русе', 'Горна оряховица', 'Стара загова', 'Плевен',
                         'Айтос', 'Асеновград', 'Батановци', 'Белово', 'Белозем', 'Белослав', 'Благоеврад',
                         'Бойчиновци',
                         'Брусарци', 'Бяла', 'Велико Търново', 'Велинград', 'Видин', 'Враца', 'Габрово', 'Даскалово',
                         'Две могили', 'Димитровград', 'Добрич', 'Дряново', 'Дупница', 'Дългопол', 'Елин Пелин',
                         'Земен',
                         'Златица', 'Зверино', 'Ихтиман', 'Казанлък', 'Карлово', 'Карнобат', 'Каспичан', 'Криводол',
                         'Крумово', 'Кюстендил', 'Кърджали', 'Лакатник', 'Левски', 'Лом', 'Ловеч', 'Мездра', 'Метал',
                         'Монтана', 'Нова Загора', 'Пазарджик', 'Павликени', 'Перник', 'Перник Разпред.', 'Пертич',
                         'Пирдоп', 'Попово', 'Попски тръмбеш', 'Провадия', 'Първомай', 'Радомир', 'Роман', 'Разград',
                         'Самуил', 'Сандански', 'Свиленград', 'Свищов', 'Своге', 'Септември', 'Силистра', 'Сливен',
                         'Сливница', 'Стамболийски', 'Стралджа', 'Стражица', 'Твърдица', 'Трявна', 'Тулово',
                         'Търговище',
                         'Филипово', 'Хисар', 'Церово', 'Червен бряг', 'Чирпан', 'Шумен', 'Ямбол']

    railway_cities_EN = ['Sofia', 'Varna', 'Burgas', 'Plovdiv', 'Ruse', 'Gorna Oryakhovitsa', 'Stara Zagora', 'Pleven',
                         'Aytos', 'Asenovgrad', 'Batanovtsi', 'Belovo', 'Belozem', 'Beloslav', 'Blagoevgrad',
                         'Boychinovtsi',
                         'Brusartsi', 'Bqla', 'Veliko Tarnovo', 'Velingrad', 'Vidin', 'Vratsa', 'Gabrovo', 'Daskalovo',
                         'Dve mogili', 'Dimitrovgrad', 'Dobrich', 'Drqnovo', 'Dupnitsa', 'Dulgopol', 'Elin Pelin',
                         'Zemen',
                         'Zlatitsa', 'Zverino', 'Ihtiman', 'Kazanlak', 'Karlovo', 'Karnobat', 'Kaspichan', 'Krivodol',
                         'Krumovo', 'Kyustendil', 'Kardzhali', 'Lakatnik', 'Levski', 'Lom', 'Lovech', 'Mezdra', 'Metal',
                         'Montana', 'Nova Zagora', 'Pazardzhik', 'Pavlikeni', 'Pernik', 'Pernik razpred.', 'Petrich',
                         'Pirdop', 'Popovo', 'Polski Trambesh', 'Provadia', 'Parvomay', 'Radomir', 'Roman', 'Razgrad',
                         'Samuil', 'Sandandski', 'Svilengrad', 'Svishtov', 'Svoge', 'Septemvri', 'Silistra', 'Sliven',
                         'Slivnitsa', 'Stamboliyski', 'Straldzha', 'Strazhitsa', 'Tvarditsa', 'Tryavna', 'Tulovo',
                         'Targovishte',
                         'Filipovo', 'Hisar', 'Tserovo', 'Cherven bryag', 'Chirpan', 'Shumen', 'Yambol']

    driver = chromedriver_setup(bulgarian_railways_website)

    # python find the index of a list which contains a value
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_index = [index + 1 for index, el in enumerate(months) if el in weekday]
    month_index = ''.join(str(i) for i in month_index)
    l_day = [el for el in weekday if el.isdigit()]
    day = ''.join(str(d) for d in l_day)

    full_date = f'{day}.{month_index}.{2022}'

    BG_start_station = [el for el in railway_cities_BG if el in starting_station]
    BG_departure_station = [el for el in railway_cities_BG if el in departure_station]
    if len(BG_start_station) < 1:
        start_index = [index for index, el in enumerate(railway_cities_EN) if el in starting_station]
        starting_station = railway_cities_BG[start_index[0]]
    else:
        starting_station = BG_start_station
    if len(BG_departure_station) < 1:
        end_index = [index for index, el in enumerate(railway_cities_EN) if el in departure_station]
        departure_station = railway_cities_BG[end_index[0]]
    else:
        departure_station = BG_departure_station
    # .cw-close
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".cw-close"))).click()
    start = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#from")))
    end = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#to")))
    ActionChains(driver).move_to_element(start)
    start.clear()
    start.send_keys(starting_station)
    ActionChains(driver).move_to_element(end)
    end.send_keys(departure_station)

    send_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".search-submit")))

    # TODO: Implement logic to set correct date & time corresponding to the game that makes sense

    # #destination-date; #type; #hour;
    travel_date = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#destination-date")))
    # travel_type = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#type")))
    arriving_after = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#hour")))
    x = ActionChains(driver).move_to_element(travel_date).click()
    travel_date.send_keys(Keys.CONTROL, 'a')
    travel_date.send_keys(full_date)

    ActionChains(driver).move_to_element(arriving_after)
    game_time = game_time.replace(':', '.')
    #game_time = float(game_time) - 4
    game_time = 0
    arriving_after.send_keys(game_time)
    # ActionChains(driver).move_to_element(send_button)
    send_button.click()
    # WebDriverWait(driver, 30).until('.btn-sm').click()
    # # go = WebDriverWait(driver, 30).until(
    # #     EC.element_to_be_clickable((By.CSS_SELECTOR, 'btn btn-success btn-sm'))).click()
    # st_station = WebDriverWait(driver, 30).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, '#id-search-trips-station-from .css-1hwfws3'))).click()
    # ed_station = WebDriverWait(driver, 30).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, '#id-search-trips-station-to .css-1hwfws3'))).click()
    # dep_date = WebDriverWait(driver, 30).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, '#id-search-trips-going-date'))).click()
    # ActionChains(driver).move_to_element(st_station)
    # st_station.send_keys(*starting_station)
    # ActionChains(driver).move_to_element(ed_station)
    # ed_station.send_keys(*departure_station)
    # ActionChains(driver).move_to_element(dep_date)
    # dep_date.send_keys(weekday)
    # WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn--trip-select-submit'))).click()

    link = driver.current_url
    return link


def get_stadium_coordinates(driver):
    start_time = time.time()
    stadium_coordinates = None

    if driver.title == 'Stadion Vasil Levski, Sredets, Bulgaria - Bing Карти':
        stadium_coordinates = '42.687562, 23.335261'

    while stadium_coordinates is None:
        try:
            stadium_coordinates = driver.find_element_by_class_name('geochainModuleLatLong').text
        except selenium.common.exceptions.NoSuchElementException:
            pass
    end = time.time()

    # print("get_stadium_coordinates is :",
    #       (end - start_time) * 10 ** 3, "ms")
    driver.quit()
    return stadium_coordinates


def chromedriver_setup(url):
    # TODO: This is very time consuming

    PATH = "C:\Program Files (x86)\chromedriver.exe"  # PATH TO THE chromedriver.exe downloaded (check requirements.txt)
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(PATH, options=op)
    driver.get(url)
    return driver


def distance_to_stadium(bing_address):
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        driver = executor.submit(chromedriver_setup, bing_address).result()
        current_loc = executor.submit(get_my_location)

    # Using Selenium
    # ACCEPTING COOKIES
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#bnp_btn_accept"))).click()
    # 3 seconds --> 3000 miliseconds

    button = driver.find_element_by_css_selector(".directionsIcon")
    driver.execute_script("arguments[0].click();", button)

    start = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".start+ input")))

    x, y = current_loc.result()
    from_loc = f"{str(x)}, {str(y)}"

    ActionChains(driver).move_to_element(start)
    start.send_keys(from_loc)

    go_btn = driver.find_element_by_class_name("dirBtnGo.commonButton")
    go_btn.click()
    time_minutes = None
    time_hours = None
    while time_hours is None:
        try:
            time_hours = driver.find_element_by_class_name('drHours')
            time_minutes = driver.find_element_by_class_name('drMins')
        except selenium.common.exceptions.NoSuchElementException:
            pass

    if time_hours.text == "":
        travel_time = f"{time_minutes.text} min"
    else:
        travel_time = f"{time_hours.text} h: {time_minutes.text} min"

    end = time.time()

    # print("Distance_to_stadium is :",
    #       (end - start_time) * 10 ** 3, "ms")
    # driver.quit()
    return travel_time
