from django.shortcuts import render
from core.teams.BulgarianLeague import export_team_names
from core.teams.BulgarianLeague import export_next_fixture
from core.teams.BulgarianLeague import export_last_3_results
from core.teams.BulgarianLeague import export_team_location

# Create your views here.

def frontpage(request):
    return render(request, 'frontpage.html')


def team(request):
    context = {}
    team_name = request.POST.get('team_name')
    # team_name = team_name.capitalize()
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
    context['team_location'] = team_location
    return render(request, 'team.html', context)
