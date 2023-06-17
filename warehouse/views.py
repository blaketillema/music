from django.shortcuts import render
from warehouse.models import AOTYAlbum

# Create your views here.
def albums(request):
    albums = AOTYAlbum.objects.all()
    return render(request, 'albums.html', context={'albums': albums})

def artist(request, id):
    albums = AOTYAlbum.objects.filter(artist_id=id)
    return render(request, 'albums.html', context={'albums': albums})