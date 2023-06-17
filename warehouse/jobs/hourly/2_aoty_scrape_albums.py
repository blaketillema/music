import multiprocessing
import tqdm

from django_extensions.management.jobs import HourlyJob
from itertools import repeat
from warehouse.models import AOTYAlbum
# from warehouse.utils import get_page_block


class Job(HourlyJob):
    help = "Scrape AOTY albums"

    def execute(self):
        return
        print('scraping albums')
        last_album = AOTYAlbum.objects.last()
        last_id = last_album.id if last_album else 0
        
        processes = 10
        block_size = 50
        num_to_scrape = processes * block_size * 20
        
        for i in tqdm.tqdm(range(last_id, last_id + num_to_scrape, block_size)):
            blocks = zip(
                range(i, i + block_size, block_size // processes), 
                repeat(block_size // processes),
                repeat("https://albumoftheyear.org/album/{}")
            )
            with multiprocessing.Pool(processes) as p:
                page_blocks = p.map(get_page_block, blocks)
            if not any(block for block in page_blocks):
                break
            for block in page_blocks:
                for id, data in block.items():
                    url, text = data['url'], data['text']
                    aoty_page = AOTYPage()
                    aoty_page.url = url
                    aoty_page.id = id
                    aoty_page.type = AOTYPage.Type.ALBUM
                    aoty_page.page = text
                    aoty_page.save()
