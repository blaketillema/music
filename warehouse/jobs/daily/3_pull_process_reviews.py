import multiprocessing
import tqdm

from django_extensions.management.jobs import DailyJob
from warehouse.models import  AOTYAlbumRating, AOTYAlbumPage, AOTYAlbum
from warehouse.utils import get_reviews

class Job(DailyJob):
    help = "Scrape AOTY album reviews"

    def execute(self):

        albums = AOTYAlbum.objects.all()
        ids = [album.id for album in albums if album.id > 27341]
        block_size = 32
        processes = 32
        blocks = [ids[i:i+block_size] for i in range(0, len(ids), block_size)]
        process_blocks = [blocks[i:i+processes] for i in range(0, len(blocks), processes)]
        with multiprocessing.Pool(processes) as p:
            for process_block in tqdm.tqdm(process_blocks):
                review_block = p.map(get_reviews, process_block)
                for block in review_block:
                    for album_id, reviews in block.items():
                        for review_id, review in reviews.items():
                            rating = AOTYAlbumRating()
                            rating.id = review_id
                            rating.album = AOTYAlbum.objects.get(id=int(album_id))
                            rating.date = review['datetime']
                            rating.rating = review['rating'] if review['rating'] != 'NR' else None
                            rating.save()
