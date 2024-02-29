from django.shortcuts import render
from .models import News

# Create your views here.
def news(request):
    # why newss?, la idea es que no se confundan o
    # interfieran los nombres entre sí?
    newss = News.objects.all().order_by('-date')
    return render(request, 'news.html', {'newss':newss})