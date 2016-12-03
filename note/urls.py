# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from .views import NoteTagAutoComplete
urlpatterns = [
    url(r'^note/(?P<note_id>\d+)/$', views.note_page, name='note_page'),

    url(r'^notes/$', views.note_list_page, name='note_list_page'),

    url(r'^edit/note/(?P<note_id>\d+)/$', views.edit_note, name='edit_note'),

    url(r'^add/note/(?P<problem_id>\d+)/$', views.add_note, name='add_note'),

    url(
        r'^note-tag-autocomplete/$',
        NoteTagAutoComplete.as_view(create_field='name'),
        name='note-tag-autocomplete',
    ),
    url(r'^table/data/notes/$', views.MyDataView.as_view(), name='table_data_note'),
]
