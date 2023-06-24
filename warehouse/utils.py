import bs4
import datetime
import requests

from requests.adapters import HTTPAdapter

def get_many_pages(links) -> dict[str, requests.Response]:
    session = requests.Session()
    session.mount(
        prefix='https://albumoftheyear.org', 
        adapter=HTTPAdapter(pool_connections=100, pool_maxsize=100, max_retries=10))
    session.headers.update({'User-Agent': 'Warehouse'})
    out = {}
    for link in links:
        try:
            request = session.get(link)
            if request.ok and not request.url.strip('/').endswith('.org'):
                out[request.url] = request
        except Exception as e:
            pass
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

            request = session.get(f'https://www.albumoftheyear.org/album/{id}/user-reviews/?type=ratings&p={p}')
            if not request.ok:
                continue

            parsed = bs4.BeautifulSoup(request.text, 'lxml')
            reviews = parsed.find_all('div', class_="userRatingBlock")

            while reviews:
                if id not in out:
                    out[id] = {}
                for i, review in enumerate(reviews):
                    review_id = f'{id}:{i + (p - 1) * 80}'
                    review_date = review.find('div', class_="date")['title']
                    review_datetime = datetime.datetime.strptime(review_date, '%d %b %Y %H:%M:%S %Z').replace(tzinfo=datetime.timezone.utc)
                    review_rating = review.find('div', class_='rating').text
                    out[id][review_id] = {
                        'datetime': review_datetime,
                        'rating': review_rating
                    }
                p += 1

                request = session.get(f'https://www.albumoftheyear.org/album/{id}/user-reviews/?type=ratings&p={p}')
                if not request.ok:
                    break

                parsed = bs4.BeautifulSoup(request.text, 'lxml')
                reviews = parsed.find_all('div', class_="userRatingBlock")

        except Exception as e:
            print(e)
    return out

