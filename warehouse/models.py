from django.db import models


class AOTYAlbumPage(models.Model):
    class Meta:
        verbose_name = "AOTY Album Page"
    id = models.BigIntegerField(primary_key=True)
    url = models.URLField(max_length=2000)
    page = models.TextField()

    def __str__(self):
        return self.url


class AOTYArtist(models.Model):
    class Meta:
        verbose_name = "AOTY Artist"
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=2000)

    def __str__(self):
        return self.name


class AOTYGenre(models.Model):
    class Meta:
        verbose_name = "AOTY Genre"
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AOTYAlbum(models.Model):
    class Meta:
        verbose_name = "AOTY Album"
    id = models.BigIntegerField(primary_key=True)
    page = models.ForeignKey(AOTYAlbumPage, on_delete=models.SET_NULL, null=True, blank=True)

    artists = models.ManyToManyField(AOTYArtist, related_name='albums')
    genres = models.ManyToManyField(AOTYGenre, related_name='albums', blank=True)

    title = models.CharField(max_length=2000)
    
    critic_score = models.IntegerField(blank=True, null=True)
    user_score = models.IntegerField(blank=True, null=True)
    
    release_date = models.DateField(blank=True, null=True)
    
    spotify_link = models.URLField(blank=True, null=True)

    @property
    def num_ratings(self):
        return AOTYAlbumRating.objects.filter(album=self.id).count()

    def __str__(self):
        return self.title


class AOTYAlbumRating(models.Model):
    class Meta:
        verbose_name = "AOTY Album Rating"
    id = models.CharField(max_length=32, primary_key=True)
    album = models.ForeignKey(AOTYAlbum, on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)