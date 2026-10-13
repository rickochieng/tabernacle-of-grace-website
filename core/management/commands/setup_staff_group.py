from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create the "Church Staff" group (sermons, events, photos, inbox, church details only).'

    def handle(self, *a, **k):
        g, _ = Group.objects.get_or_create(name='Church Staff')
        perms = Permission.objects.filter(content_type__app_label='core')
        full = perms.filter(content_type__model__in=['sermon', 'event', 'photo'])
        inbox = perms.filter(content_type__model__in=['prayerrequest', 'contactmessage', 'sitedetails', 'subscriber'],
                             codename__regex=r'^(view|change)_')
        g.permissions.set(list(full) + list(inbox))
        self.stdout.write('Group "Church Staff" is ready.')
