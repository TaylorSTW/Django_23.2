from django.core.management import BaseCommand

from catalog.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Clear data in Category
        Category.objects.all().delete()

        # Create list of categories
        category_list = [
            {'name': 'Toys', 'description': 'Products for kids'},
            {'name': 'Clothes', 'description': 'Products to wear'},
            {'name': 'Food & Beverages', 'description': 'Products to consume'},
            {'name': 'Electronics', 'description': 'Electronic equipment for '},
        ]

        categories_to_create = []
        for category in category_list:
            categories_to_create.append(
                Category(**category)
            )

        Category.objects.bulk_create(categories_to_create)