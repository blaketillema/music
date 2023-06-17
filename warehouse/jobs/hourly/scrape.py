import bs4
import datetime
import multiprocessing
import tqdm

from django_extensions.management.jobs import HourlyJob
from itertools import repeat
from warehouse.models import AOTYArtist, AOTYAlbum
from warehouse.utils import get_page_block_ids, get_page_block_links


class Job(HourlyJob):
    help = "Scrape AOTY artists"

    def execute(self):
        # return
        print('scraping artists')
        last_artist = AOTYArtist.objects.last()
        last_id = last_artist.id if last_artist else 1
        
        processes = 10
        block_size = 50
        num_to_scrape = processes * block_size * 10
        
        for i in tqdm.tqdm(range(last_id, last_id + num_to_scrape, block_size)):
            blocks = zip(
                range(i, i + block_size, block_size // processes), 
                repeat(block_size // processes),
                repeat("https://albumoftheyear.org/artist/{}/?type=all")
            )
            with multiprocessing.Pool(processes) as p:
                page_blocks = p.map(get_page_block_ids, blocks)
            if not any(block for block in page_blocks):
                break
            for block in page_blocks:
                for id, data in block.items():
                    url, text = data['url'], data['text']
                    artist = AOTYArtist()
                    artist.id = id
                    artist.url = url
                    artist.save()

                    parsed = bs4.BeautifulSoup(text, 'lxml')
                    albums = parsed.find_all('div', class_='albumBlock small', attrs={'data-type': 'lp'})
                    links = ["https://albumoftheyear.org{}".format(a['href']) for album in albums if (a := album.find('a'))]
                    link_blocks = [links[i:i+block_size] for i in range(0, len(links), block_size)]

                    process_blocks = [
                        zip(link_blocks[i:i+processes], repeat('https:\/\/(?:www\.)?albumoftheyear.org/album/([0-9])+.*'))
                        for i in range(0, len(link_blocks), processes)
                    ]
                    for process_block in process_blocks:
                        with multiprocessing.Pool(processes) as p:
                            album_blocks = p.map(get_page_block_links, process_block)
                        if not any(album_block for album_block in album_blocks):
                            continue
                        for album_block in album_blocks:
                            for album_id, album_data in album_block.items():

                                album_url, album_text = album_data['url'], album_data['text']

                                parsed = bs4.BeautifulSoup(album_text, 'lxml')
                                album_title = parsed.find('div', class_='albumTitle').find('span').text
                                    
                                try:
                                    album = AOTYAlbum.objects.get(album_id=album_id)
                                except:
                                    album = AOTYAlbum()
                                    album.id = album_id
                                    album.artist = artist
                                    album.url = album_url
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



