from django.contrib import admin

# Register your models here.
from .models import Announcement
from django_summernote.admin import SummernoteModelAdmin


class AnnouncementAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'title', 'create_time', 'last_update_time', 'created_by', 'visible', )
    list_display_links = ('pk', 'title', )

admin.site.register(Announcement, AnnouncementAdmin)
