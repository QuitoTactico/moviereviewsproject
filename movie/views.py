from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html', {'name':'Esteban Vergara Giraldo'})

    #Trae el valor del input con name="searchMovie"
    searchTerm = request.GET.get('searchMovie')

    # SELECT * FROM Movie
    # movies = Movie.objects.all()

    # SELECT * FROM Movie WHERE title LIKE '%searchTerm%'
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {'name': 'Esteban Vergara Giraldo','searchTerm' : searchTerm,'movies':movies})


def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')
