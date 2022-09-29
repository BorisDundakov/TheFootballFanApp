from django.shortcuts import render
from core.teams.BulgarianLeague import *


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
    selected_stadium = request.POST.get('team_location')

    context['home_badge'] = request.POST.get('home_badge')
    context['away_badge'] = request.POST.get('away_badge')
    context['weekday'] = request.POST.get('weekday')
    context['game_time'] = request.POST.get('game_time')

    context['home'] = teams.split(',')[0]
    context['away'] = teams.split(',')[1]

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

    """"""

    # TODO 0): think of program logistics
    # TODO 1): extract the stadium location of the home team --> web scraping
    # TODO 2): get the current location of the user
    # TODO 3): calculate the distance between the 2 points
    # TODO 4): locate the nearest train stops on БДЖ to the starting and end locations
    # TODO 5): find a trip between the БДЖ stops
    # TODO 6): display a list of the possible trips as buttons --> starting date & time, end date & time, price
    # TODO 7): clicking the button would redirect you to the БДЖ website for buying the tickets
    # TODO FUTURE:
    # TODO - integrate google maps, bus alternatives, fuel expenditure (go by car alternative price comparison)

    return render(request, 'travelNextGame.html', context)
