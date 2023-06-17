import bs4
import datetime
import re
import tqdm

from django_extensions.management.jobs import HourlyJob
from warehouse.models import  AOTYAlbum, AOTYArtist


class Job(HourlyJob):
    help = "Extract data from the AOTY pages."

    def execute(self):
        return
        pages = AOTYPage.objects.filter(type=AOTYPage.Type.ALBUM)
        for page in tqdm.tqdm(pages):
            parsed = bs4.BeautifulSoup(page.page, 'lxml')
            
            album_id_match = re.match('https:\/\/(?:www\.)?albumoftheyear.org\/album\/([0-9]+)-.*', page.url)
            if album_id_match:
                album_id = album_id_match.groups()[0]
            else:
                continue

            artist_a = parsed.find('div', class_='artist').find('a')
            artist_id = artist_a['href'].lstrip('/artist/').split('-')[0]
            album_title = parsed.find('div', class_='albumTitle').find('span').text
            
            try:
                artist = AOTYArtist.objects.get(artist_id=artist_id)
            except:
                artist = AOTYArtist()
                artist.artist_id = artist_id
                artist.page_id = page
                artist.save()
                
            try:
                album = AOTYAlbum.objects.get(album_id=album_id)
            except:
                album = AOTYAlbum()
                album.album_id = album_id
                album.page_id = page
                album.artist_id = artist
                album.title = album_title
                album.save()
            
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