from django.core.management.base import BaseCommand
from django.db import connection
from main.models import Invite, Guest, RSVP, Music


class Command(BaseCommand):
    help = 'Creates any missing main app tables'

    def handle(self, *args, **kwargs):
        existing = connection.introspection.table_names()
        models = [Invite, Guest, RSVP, Music]
        for model in models:
            table = model._meta.db_table
            if table not in existing:
                with connection.schema_editor() as schema:
                    schema.create_model(model)
                self.stdout.write(f'Created {table}')
            else:
                self.stdout.write(f'Skipped {table} (already exists)')
