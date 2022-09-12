from django.shortcuts import render
from core.teams.BulgarianLeague import export_team_names
from core.teams.BulgarianLeague import export_next_fixture
from core.teams.BulgarianLeague import export_last_3_results
from core.teams.BulgarianLeague import export_team_location
from core.teams.BulgarianLeague import load_bing_maps
from core.teams.BulgarianLeague import distance_to_stadium
from core.teams.BulgarianLeague import export_matchday_results


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

    for t in teams.values():
        if team_name in t:
            team_name = t
            context['team_name'] = t
            correct_name = True
            break

    if not correct_name:
        return render(request, 'frontpage.html')

    team_number = 0
    for key, value in teams.items():
        if value == team_name:
            team_number = key
            break

    next_match = export_next_fixture(team_name, team_number)
    last_3_matches = export_last_3_results(team_name, team_number)
    team_location = export_team_location(team_name)
    context['home'] = next_match['home']
    context['away'] = next_match['away']
    context['last_3_matches'] = last_3_matches
    # TODO: Fix Team location so that it shows the actual address of the stadium
    context['team_location'] = team_location
    return render(request, 'team.html', context)


def travel_next_game(request):
    context = {}
    teams = request.POST.get('team_name')

    context['home'] = teams.split(',')[0]
    context['away'] = teams.split(',')[1]

    next_location = export_team_location(context['home'])
    context['location'] = next_location

    bing_maps_link = load_bing_maps(next_location)
    context['maps'] = bing_maps_link

    distance = distance_to_stadium(bing_maps_link)
    context['distance'] = distance

    distance = 0
    current_location = ''

    # gmaps = googlemaps.Client()
    # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

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
