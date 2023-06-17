import bs4
import datetime
import re
import requests

from requests.adapters import HTTPAdapter

def get_page_block_ids(args):
    n, block_size, url_format_string = args
    session = requests.Session()
    session.mount(
        prefix='https://albumoftheyear.org', 
        adapter=HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=10))
    session.headers.update({'User-Agent': 'Warehouse'})
    out = {}
    for i in range(n, n + block_size):
        try:
            url = url_format_string.format(i)
            request = session.get(url)
            if request.ok and str(i) in request.url:
                out[i] = {'url': request.url, 'text': request.text}
            else:
                pass
                # print('failed to get data', i, request.status_code)
        except Exception as e:
            pass
            # print('failed to get album', i, '\n', e)
    return out

def get_page_block_links(args):
    links, expression = args
    session = requests.Session()
    session.mount(
        prefix='https://albumoftheyear.org', 
        adapter=HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=10))
    session.headers.update({'User-Agent': 'Warehouse'})
    out = {}
    for link in links:
        try:
            request = session.get(link)
            if request.ok and request.url.strip('/') not in ('https://albumoftheyear.org', 'https://www.albumoftheyear.org'):
                id = re.match(expression, request.url).groups()[0]
                out[id] = {'url': request.url, 'text': request.text}
            else:
                print('failed to get link', link, request.status_code, request.url)
        except Exception as e:
            print('failed to get link', e)
    return out


def get_artist_pages(args):
    session = requests.Session()
    session.mount(
        prefix='https://albumoftheyear.org', 
        adapter=HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=10))
    session.headers.update({'User-Agent': 'Warehouse'})
    out = {}
    for id, link in args:
        try:
            request = session.get(link)
            if request.ok and '/artist/' in request.url:
                out[id] = {'url': request.url, 'text': request.text}
        except Exception as e:
            print('failed to get artist', id, '\n', e)
    return out

def get_reviews(ids):
    session = requests.Session()
    session.mount(
        prefix='https://albumoftheyear.org', 
        adapter=HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=10))
    session.headers.update({'User-Agent': 'Warehouse'})
    out = {}
    for id in ids:
        try:
            p = 1
            while True:
                request = session.get(f'https://www.albumoftheyear.org/album/{id}/user-reviews/?p={p}')
                if not request.ok:
                    break
                parsed = bs4.BeautifulSoup(request.text, 'lxml')
                reviews = parsed.find_all('div', attrs={'itemprop': 'review'})
                if not reviews:
                    break
                if id not in out:
                    out[id] = {}
                for review in reviews:
                    review_id = review['id']
                    review_datetime = datetime.datetime.strptime(review.find('meta', attrs={'itemprop': 'dateCreated'})['content'], '%Y-%m-%d %H:%M:%S')
                    review_rating = review.find('span', attrs={'itemprop': 'ratingValue'}).text
                    out[id][review_id] = {
                        'datetime': review_datetime,
                        'rating': review_rating
                    }
                p += 1
        except Exception as e:
            print(e)
    return out

