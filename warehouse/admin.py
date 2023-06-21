from django.contrib import admin

from warehouse.models import AOTYArtist, AOTYAlbum, AOTYAlbumPage, AOTYAlbumRating, AOTYGenre

# Register your models here.

@admin.register(AOTYArtist)
class AOTYArtistAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(AOTYGenre)
class AOTYGenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(AOTYAlbum)
class AOTYAlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_artists', 'critic_score', 'user_score']
    search_fields = ['title', 'artists__name']

    def get_artists(self, obj):
        return ', '.join(artist.name for artist in obj.artists.all())

@admin.register(AOTYAlbumPage)
class AOTYAlbumPageAdmin(admin.ModelAdmin):
    list_display = ['url']
    search_fields = ['url']

@admin.register(AOTYAlbumRating)
class AOTYAlbumRatingAdmin(admin.ModelAdmin):
    list_display = ['album', 'rating', 'date']
    search_fields = ['album']