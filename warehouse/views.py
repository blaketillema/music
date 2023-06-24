from django.db.models import Count, Case, When, IntegerField
from django.shortcuts import render
from warehouse.models import AOTYAlbum, AOTYArtist

# Create your views here.
def home(request):
    albums = AOTYAlbum.objects.annotate(
        num_ratings=Count(
            Case(
                When(
                    ratings__rating__isnull=False,
                    then=1
                ),
                output_field=IntegerField()
            )
        )
    ).order_by('-num_ratings')[:20]
    return render(request, 'home.html', context={'albums': albums, 'show_artist': True})

def artist(request, id):
    artist_ = AOTYArtist.objects.get(id=id)
    albums = AOTYAlbum.objects.annotate(
        num_ratings=Count(
            Case(
                When(
                    ratings__rating__isnull=False,
                    then=1
                ),
                output_field=IntegerField()
            )
        )
    ).filter(
        artists__id=id
    ).order_by('-num_ratings', 'title')
    return render(request, 'artist.html', context={'albums': albums, 'artist': artist_})