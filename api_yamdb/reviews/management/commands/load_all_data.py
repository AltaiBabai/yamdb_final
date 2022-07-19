from csv import DictReader
from django.core.management import BaseCommand
from reviews.models import Comment, Category, Genre
from reviews.models import Title, Genre_Title, Review

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Show this if the data already exist in the database
        if (Title.objects.count() > 0
                or Category.objects.count() > 0
                or Comment.objects.count() > 0
                or Genre.objects.count() > 0
                or Genre_Title.objects.count() > 0
                or Review.objects.count() > 0):
            print('data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
        # Show this before loading the data into the database
        print("Loading all data...")
        # Code to load the data into database
        for row in DictReader(open(
                './static/data/category.csv', encoding='utf-8')):
            category = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug'])
            category.save()
        for row in DictReader(open(
                './static/data/genre.csv', encoding='utf-8')):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'])
            genre.save()
        for row in DictReader(open(
                './static/data/titles.csv', encoding='utf-8')):
            title = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'])
            title.save()
        for row in DictReader(open(
                './static/data/genre_title.csv', encoding='utf-8')):
            genre_title = Genre_Title(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id'])
            genre_title.save()
        for row in DictReader(open(
                './static/data/review.csv', encoding='utf-8')):
            review = Review(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'])
            review.save()
        for row in DictReader(open(
                './static/data/comments.csv', encoding='utf-8')):
            comment = Comment(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'])
            comment.save()
        print('...done')
