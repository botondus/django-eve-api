from django.core.management.base import BaseCommand, CommandError
from eve_api.models import ApiAccount
from eve_api.api_puller.account.character_list import query_character_list

class Command(BaseCommand):
    help = "Queries all accounts, pulling character data."

    def handle(self, *args, **options):
        accounts = ApiAccount.objects.all()
        for account in accounts:
            query_character_list(account.api_key, account.api_user_id)