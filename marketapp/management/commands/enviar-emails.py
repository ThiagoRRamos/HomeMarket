'''
Created on Jun 11, 2013

@author: thiagorramos
'''

from django.core.management.base import BaseCommand, CommandError
from marketapp.services import marketing

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        marketing.enviar_emails_promocoes()