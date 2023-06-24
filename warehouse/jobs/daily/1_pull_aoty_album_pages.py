import multiprocessing
import re
import tqdm

from django_extensions.management.jobs import DailyJob
from warehouse.models import AOTYAlbumPage
from warehouse.utils import get_many_pages


class Job(DailyJob):
    help = "Pulls albums from AOTY"

    def execute(self):
        N = 700_000 # roughly last album id as of now
        M = AOTYAlbumPage.objects.last().id

        block_size = 32
        processes = 32
        process_block_size = 32

        links = [
            "https://albumoftheyear.org/album/{}/".format(i)
            for i in range(M, N)
        ]
        link_blocks = [
            links[i:i+block_size]
            for i in range(0, len(links), block_size)
        ]
        process_blocks = [
            link_blocks[i:i+process_block_size]
            for i in range(0, len(link_blocks), process_block_size)
        ]

        with multiprocessing.Pool(processes) as pool:
            for process_block in tqdm.tqdm(process_blocks):
                page_blocks = pool.map(get_many_pages, process_block)
                if not any(page_block for page_block in page_blocks):
                    break
                for page_block in page_blocks:
                    for url, request in page_block.items():
                        id_match = re.match(
                            r'https://(?:www\.)?albumoftheyear\.org/album/(?P<id>[0-9]+).*',
                            url)
                        if not id_match:
                            continue
                        id = id_match.group('id')
                        aoty_album_page = AOTYAlbumPage()
                        aoty_album_page.id = id
                        aoty_album_page.url = url
                        aoty_album_page.page = request.text
                        aoty_album_page.save()
