import csv
import yaml
import re

from django.core.management.base import BaseCommand

from backend.models import Shop, Category


class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        with open('shop1.yaml', encoding='utf-8') as file:
            zapis = yaml.safe_load(file.read())
            shop = Shop(
                name=zapis['shop']
            )
            shop.save()
