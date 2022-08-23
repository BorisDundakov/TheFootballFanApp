from django.shortcuts import render


# Create your views here.

def frontpage(request):
    return render(request, 'frontpage.html')


def team(request):
    return render(request, 'team.html')
