from django.contrib import admin
from .models import *

admin.site.site_header = 'Tabernacle of Grace · Church Manager'
admin.site.site_title = 'Church Manager'
admin.site.index_title = 'What would you like to update?'


class Inbox(admin.ModelAdmin):
    """Visitor submissions: staff can read and tick them off, not add."""
    def has_add_permission(self, request):
        return False


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'date', 'published')
    list_filter = ('published',)
    search_fields = ('title', 'speaker')
    date_hierarchy = 'date'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time_text', 'category', 'published')
    list_filter = ('published', 'category')
    search_fields = ('title',)
    date_hierarchy = 'date'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('caption', 'image', 'uploaded')


@admin.register(PrayerRequest)
class PrayerRequestAdmin(Inbox):
    list_display = ('name', 'category', 'short', 'created', 'prayed_for')
    list_filter = ('prayed_for', 'category')
    readonly_fields = ('name', 'contact', 'category', 'request', 'created')
    actions = ['mark_prayed']

    @admin.display(description='Request')
    def short(self, o):
        return o.request[:70]

    @admin.action(description='Mark selected as prayed for')
    def mark_prayed(self, request, qs):
        qs.update(prayed_for=True)


@admin.register(ContactMessage)
class ContactMessageAdmin(Inbox):
    list_display = ('name', 'subject', 'created', 'handled')
    list_filter = ('handled',)
    readonly_fields = ('name', 'contact', 'subject', 'message', 'created')
    actions = ['mark_handled']

    @admin.action(description='Mark selected as replied / done')
    def mark_handled(self, request, qs):
        qs.update(handled=True)


@admin.register(Subscriber)
class SubscriberAdmin(Inbox):
    list_display = ('email', 'created')
    search_fields = ('email',)


@admin.register(SiteDetails)
class SiteDetailsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteDetails.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
