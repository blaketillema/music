from django.contrib import admin

from warehouse.models import AOTYAlbum, AOTYArtist, AOTYAlbumRating

# Register your models here.
admin.site.register(AOTYArtist)
admin.site.register(AOTYAlbum)
admin.site.register(AOTYAlbumRating)