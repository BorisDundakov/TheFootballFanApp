from django.shortcuts import render
from core.teams.BulgarianLeague import export_team_names


# Create your views here.

def frontpage(request):
    return render(request, 'frontpage.html')


def team(request):
    context = {}
    team_name = request.POST.get('team_name')
    #team_name = team_name.capitalize()
    context['team_name'] = team_name
    # TODO: Teams web scraping!

    teams = export_team_names()
    if team_name not in teams:
        return render(request, 'frontpage.html')
    return render(request, 'team.html', context)
