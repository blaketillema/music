# What is it?
A django project that stores albums and their ratings from AlbumOfTheYear.org

# How does it work?
Under the `warehouse/jobs/daily` directory are a few DailyJob classes, with their own execute methods. These pull the album pages, process said album pages, and pull the album ratings respectively. Should this project be deployed somewhere, a crontab entry should be made as per the django-extension [docs](https://django-extensions.readthedocs.io/en/latest/jobs_scheduling.html#run-a-job).

# How do I set it up?
These steps come down to user preference. You could change the database to sqlite in `music/settings.py` for example, but for the OOB setup, you'll need a configured PostgreSQL environment running locally. There are a few environment variables you need to set first, namely:  

- DJANGO_SECRET
- DB_USER
- DB_PASS  

Or you could hardcode them - you're the boss.
```
pip install -r requirements.txt
python manage.py migrate
```
Voila. The project is set up. Running `python manage.py runserver` will get the django app running, but you'll have no data.

# Why?
It is wholly a personal project that fetches a lot of data for me to practice data analysis/science on.

# What's next?
Maybe make some views for albums/artists with relevant statistics. The multiprocessing implementation for scraping the pages isn't ideal, that could also be improved.