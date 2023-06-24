import bs4
import datetime
import tqdm

from django_extensions.management.jobs import DailyJob
from warehouse.models import AOTYAlbumPage, AOTYAlbum, AOTYArtist, AOTYGenre


class Job(DailyJob):
    help = "Pulls albums from AOTY"

    def execute(self):
        
        last_album_page_id = AOTYAlbumPage.objects.last().id
        for album_page_id in tqdm.tqdm(range(0, last_album_page_id + 1)):
            try:
                album_page = AOTYAlbumPage.objects.get(id=album_page_id)
            except:
                continue
            album = AOTYAlbum.objects.filter(page=album_page)
            if album:
                continue

            album = AOTYAlbum()
            album.id = album_page.id
            album.page = album_page

            parsed = bs4.BeautifulSoup(album_page.page, 'lxml')


            album_title = parsed.find('div', class_='albumTitle').find('span').text
            
            critic_score = parsed.find('div', class_='albumCriticScore').find('a')
            user_score = parsed.find('div', class_='albumUserScore').find('a')
            
            release_info = parsed.find('div', class_='detailRow')
            raw_release_info = release_info.text.split('/\xa0')
            for format in ["%B %d, %Y", "%Y", "%B  %d"]:
                try:
                    release_date = datetime.datetime.strptime(raw_release_info[0].strip(), format)
                    break
                except:
                    release_date = None

            spotify_link = parsed.find('a', title="Spotify")
            
            album.title = album_title
            album.critic_score = critic_score.text if critic_score and critic_score.text != 'NR' else None
            album.user_score = user_score.text if user_score and user_score.text != 'NR'else None
            album.release_date = release_date
            album.spotify_link = spotify_link['href'] if spotify_link else None

            album.save()

            artist_a_tags = parsed.find('div', class_='albumHeadline').find('div', class_='artist').find_all('a')
            artists = {
                tag['href'].lstrip('/artist/').split('-')[0]: tag.text
                for tag in artist_a_tags
            }
            for artist_id, artist_name in artists.items():
                artist, created = AOTYArtist.objects.get_or_create(id=artist_id)
                artist.name = artist_name
                artist.save()
                album.artists.add(artist)
            
            detail_row_divs = parsed.find('div', class_='albumTopBox info').find_all('div', class_='detailRow')
            if not detail_row_divs:
                print('no detail_row_divs')
                continue

            genre_a_tags = detail_row_divs[0].find_all('meta', attrs={'itemprop': 'genre'})

            for div in detail_row_divs:
                genre_a_tags = genre_a_tags or div.find_all('meta', attrs={'itemprop': 'genre'})

            if genre_a_tags:
                genres = {
                    tag.find_next('a')['href'].split('=')[1]:tag.find_next('a').text
                    for tag in genre_a_tags
                }
                for genre_id, genre_name in genres.items():
                    genre, created = AOTYGenre.objects.get_or_create(id=genre_id, name=genre_name)
                    album.genres.add(genre)
