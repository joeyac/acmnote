from django.contrib import admin

# Register your models here.
from .models import ClassicNote, NoteTag
from django_summernote.admin import SummernoteModelAdmin


class ClassicNoteAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'ordinal', 'pub_time', 'update_time', )
    list_display_links = ('pk', 'ordinal', )


class NoteTagAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'name', 'create_time', 'create_user')
    list_display_links = ('pk', 'name',)

admin.site.register(ClassicNote, ClassicNoteAdmin)
admin.site.register(NoteTag, NoteTagAdmin)
