from django.urls import path
from warehouse.views import albums, artist

urlpatterns = [
    path('albums/', albums, name='albums'),
    path('artist/<int:id>', artist, name='artist'),
]