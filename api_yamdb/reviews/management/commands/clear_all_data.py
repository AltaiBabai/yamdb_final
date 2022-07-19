from django.core.management import BaseCommand
from reviews.models import Comment, Category, Genre
from reviews.models import Title, Genre_Title, Review


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Delete user data...")
        Comment.objects.all().delete()
        Review.objects.all().delete()
        Genre_Title.objects.all().delete()
        Genre.objects.all().delete()
        Title.objects.all().delete()
        Category.objects.all().delete()
        print("...done")
