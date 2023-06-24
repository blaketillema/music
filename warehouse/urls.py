from django.urls import path
from warehouse.views import home, artist

urlpatterns = [
    path('', home, name='home'),
    path('artist/<int:id>', artist, name='artist'),
]