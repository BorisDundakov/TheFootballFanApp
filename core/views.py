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
    if team_name not in teams.values():
        return render(request, 'frontpage.html')

    team_number = 0
    for key, value in teams.items():
        if value == team_name:
            team_number = key
            break

    result = export_next_fixture(team_name, team_number)
    context['next_fixture'] = result

    return render(request, 'team.html', context)
