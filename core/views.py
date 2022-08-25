from django.shortcuts import render
from core.teams.BulgarianLeague import export_team_names
from core.teams.BulgarianLeague import export_next_fixture


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

    result = export_next_fixture(team_name, team_number)
    context['home'] = result['home']
    context['away'] = result['away']
    return render(request, 'team.html', context)
