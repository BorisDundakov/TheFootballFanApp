from django.shortcuts import render
from core.leagues.BulgarianLeague import *


# Create your views here.

def frontpage(request):
    context = {}
    matchday_results = export_matchday_results()
    context['gameweek'] = matchday_results[0]
    context['results'] = matchday_results[1]
    return render(request, 'frontpage.html', context)


def team(request):
    context = {}
    team_name = request.POST.get('team_name')
    context['team_name'] = team_name

    teams = export_team_names()

    correct_name = False

    # TODO: Would it would be quicker with lambda function?

    team_number = 0
    for number, name in teams.items():
        if team_name in name:
            team_name = name
            context['team_name'] = team_name
            team_number = number
            correct_name = True
            break

    if not correct_name:
        context['error'] = True
        return render(request, 'frontpage.html', context)

    next_match = export_next_fixture(team_name, team_number)
    last_3_matches = export_last_3_results(team_name, team_number)
    team_location = export_team_location(team_name)
    context['home'] = next_match['home']
    context['away'] = next_match['away']
    context['home_badge'] = next_match['home_badge']
    context['away_badge'] = next_match['away_badge']
    context['weekday'] = next_match['weekday']
    context['game_time'] = next_match['game_time']

    context['last_3_matches'] = last_3_matches
    context['team_location'] = team_location

    badges = export_last_game_badges(team_name, team_number)

    if next_match['home'] == team_name:
        context['team_logo'] = next_match['home_badge']
    else:
        context['team_logo'] = next_match['away_badge']

    context['previous_home_badge'] = badges['home']
    context['previous_away_badge'] = badges['away']

    return render(request, 'team.html', context)


def travel_next_game(request):
    context = {}
    teams = request.POST.get('teams')

    selected_team = request.POST.get('team_name')

    context['team_name'] = selected_team

    context['home'] = teams.split(',')[0]
    context['away'] = teams.split(',')[1]

    selected_stadium = request.POST.get('team_location')
    context['team_logo'] = request.POST.get('team_logo')

    context['home_badge'] = request.POST.get('home_badge')
    context['away_badge'] = request.POST.get('away_badge')
    context['weekday'] = request.POST.get('weekday')
    context['game_time'] = request.POST.get('game_time')
    # TODO: quicker sorting algorithm (quick sort?)

    if context['home'] == selected_team:
        context['location'] = selected_stadium
    else:
        team_location = export_team_location(context['home'])
        context['location'] = team_location

    bing_maps_link = load_bing_maps(context['location'])
    context['maps'] = bing_maps_link

    distance = distance_to_stadium(bing_maps_link)
    context['distance'] = distance

    current_loc = get_my_location()

    starting_trainstation = locate_nearest_trainstation(current_loc)
    departure_trainstaion = locate_trainstation(bing_maps_link)
    weekday = context['weekday']
    game_time = context['game_time']

    context['buy_train_tickets'] = generate_railways_website_link(starting_trainstation, departure_trainstaion, weekday)

    # TODO FUTURE:
    # TODO - integrate google maps instead of bing maps, bus alternatives,
    #  fuel expenditure (go by car alternative price comparison)
    # TODO 3): display a list of the possible trips as buttons --> starting date & time, end date & time, price
    # TODO 4): clicking the button would redirect you to the БДЖ website for buying the tickets

    return render(request, 'travelNextGame.html', context)
