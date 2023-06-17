from django.db import models

# Create your models here.

class AOTYArtist(models.Model):
    class Meta:
        verbose_name = "Album of the Year artist"
    id = models.BigIntegerField(primary_key=True)
    url = models.URLField()

class AOTYAlbum(models.Model):
    class Meta:
        verbose_name = "Album of the Year album"
    id = models.BigIntegerField(primary_key=True)
    artist = models.ForeignKey(AOTYArtist, on_delete=models.CASCADE)
    url = models.URLField()

    title = models.CharField(max_length=255)
    
    critic_score = models.IntegerField(blank=True, null=True)
    user_score = models.IntegerField(blank=True, null=True)
    
    release_date = models.DateField(blank=True, null=True)
    
    spotify_link = models.URLField(blank=True, null=True)
    
    label = models.CharField(max_length=64, blank=True, null=True)
    genres = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)

class AOTYAlbumRating(models.Model):
    class Meta:
        verbose_name = "Album of the Year album rating"
    id = models.CharField(max_length=32, primary_key=True)
    album = models.ForeignKey(AOTYAlbum, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)