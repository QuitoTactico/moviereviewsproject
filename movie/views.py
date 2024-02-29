from django.shortcuts import render
from django.http import HttpResponse

#gráficos
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

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


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})


# SUPER ÚTIL PARA ANÁLISIS NUMÉRICO
def statistics_view(request):
    matplotlib.use('Agg')
    # Obtiene todos los años de las películas
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    #diccionario para almacenar el conteo de películas por año
    movie_counts_by_year = {}

    # Cuenta las películas por año
    for year in years:
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = 'None'

        count = movies_in_year.count()
        movie_counts_by_year[year] = count

    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_year)) # Posiciones

    plt.bar(bar_positions, movie_counts_by_year.values(), bar_width, align='center')
    
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)

    # espaciado entre barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la imagen en un buffer (BytesIO)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Codificar la imagen en base64, parece que es necesario
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Y ya te deja renderizarlo
    return render(request, 'statistics.html', {'graphic': graphic})