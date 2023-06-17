import bs4
import multiprocessing
import re
import tqdm

from django_extensions.management.jobs import HourlyJob
from warehouse.models import  AOTYAlbumRating, AOTYAlbum
from warehouse.utils import get_reviews

class Job(HourlyJob):
    help = "Scrape AOTY album reviews"

    def execute(self):
        return
        print('scraping reviews')
        albums = AOTYPage.objects.filter(type=AOTYPage.Type.ALBUM)
        ids = [album.id for album in albums]
        block_size = 10
        processes = 10
        blocks = [ids[i:i+block_size] for i in range(0, len(ids), block_size)]
        process_blocks = [blocks[i:i+processes] for i in range(0, len(blocks), processes)]
        for process_block in tqdm.tqdm(process_blocks):
            with multiprocessing.Pool(processes) as p:
                review_block = p.map(get_reviews, process_block)
            for block in review_block:
                for album_id, reviews in block.items():
                    for review_id, review in reviews.items():
                        rating = AOTYAlbumRating()
                        rating.album_id = AOTYAlbum.objects.get(album_id=int(album_id))
                        rating.rating = review['rating'] if review['rating'] != 'NR' else None
                        rating.date = review['datetime']
                        rating.review_id = review_id
                        rating.save()
