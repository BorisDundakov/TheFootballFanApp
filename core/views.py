from django.shortcuts import render


# Create your views here.

def frontpage(request):
    return render(request, 'frontpage.html')


def team(request):
    context = {}
    team_name = request.POST.get('team_name')

    context['team_name'] = team_name
    return render(request, 'team.html', context)
