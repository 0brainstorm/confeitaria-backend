from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from recipes.models import Unit, SOLID_UNITS, LIQUID_UNITS


class Command(BaseCommand):
    def handle(self, *args, **options):
        for u in (SOLID_UNITS+LIQUID_UNITS):
            try:
                unit = Unit.objects.create(short_name=u[0], long_name=u[1])
                unit.save()
            except IntegrityError:
                raise CommandError("Mock data possibly already loaded.")
            print(repr(u) + ' --saved')
