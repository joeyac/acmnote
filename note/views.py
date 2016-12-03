from django.shortcuts import render
from .models import ClassicNote
from django.http import Http404, HttpResponseNotAllowed,HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test, login_required
from authentication.models import MyUser, ADMIN, SUPER_ADMIN
from util.verification import user_check
# Create your views here.
from .forms import ClassicNoteForm
from problem.models import Problem, ProblemTag
from .tables import ClassicNoteTable

from dal import autocomplete
from .models import NoteTag
from django.db.models import Q, Count
from functools import reduce
from table.views import FeedDataView


class MyDataView(FeedDataView):
    token = ClassicNoteTable.token

    def sort_queryset(self, queryset):
        def get_sort_arguments():
            """
            Get list of arguments passed to `order_by()` function.
            """
            arguments = []
            for key, value in self.query_data.items():
                if not key.startswith("iSortCol_"):
                    continue
                print(self.columns[value].field)
                print(len(self.columns[value].field))
                if isinstance(self.columns[value].field, set):
                    for field in self.columns[value].field:
                        field = field.replace('.', '__')
                        dir = self.query_data["sSortDir_" + key.split("_")[1]]
                        if dir == "asc":
                            arguments.insert(0, field)
                            # arguments.append(field)
                        else:
                            arguments.insert(0, "-" + field)
                            # arguments.append("-" + field)
                else:
                    field = self.columns[value].field.replace('.', '__')
                    dir = self.query_data["sSortDir_" + key.split("_")[1]]
                    if dir == "asc":
                        arguments.append(field)
                    else:
                        arguments.append("-" + field)
            return arguments
        order_args = get_sort_arguments()
        if order_args:
            queryset = queryset.order_by(*order_args)
        return queryset

    def get_queryset(self, **kwargs):
        return super(MyDataView, self).get_queryset().filter()

    def filter_queryset(self, queryset):
        def get_filter_arguments(filter_target):
            """
            Get `Q` object passed to `filter` function.
            """
            queries = []
            fields = [col.field for col in self.columns if col.searchable]
            value = filter_target
            # 暂时的解决办法
            if value:
                if value[0] == '*':
                    value = value[1:]
                    queries.append(Q(**{"tags__name__contains": value}))
                    queries.append(Q(**{"tags__abbreviation__contains": value}))
                    reduce(lambda x, y: x | y, queries)

            for field in fields:
                if field:
                    if isinstance(field, set):
                        for sub_field in field:
                            key = "__".join(sub_field.split(".") + ["contains"])
                            queries.append(Q(**{key: value}))
                    else:
                        key = "__".join(field.split(".") + ["contains"])
                        queries.append(Q(**{key: value}))
                else:
                    raise NameError

            return reduce(lambda x, y: x | y, queries)

        filter_text = self.query_data["sSearch"]
        if filter_text:
            for target in filter_text.split():
                queryset = queryset.filter(get_filter_arguments(target))
        return queryset


class NoteTagAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.has_add_permission:
            return NoteTag.objects.none()
        qs = NoteTag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

    def has_add_permission(self, request):
        return user_check(request.user)

    def create_object(self, text):
        """Create an object given a text."""
        print("SSS")

        user = self.request.user if self.request.user.is_authenticated() else None
        my_user = MyUser.objects.get(user=user) if user else None
        return self.get_queryset().create(**{self.create_field: text,
                                             'create_user': my_user})


def note_list_page(request):
    """
    前台的笔记列表
    """
    # 正常情况
    notes = ClassicNoteTable()
    content = {
        'notes': notes,
    }
    return render(request, 'note/note_list.html', content)


def note_page(request, note_id):
    user = request.user if request.user.is_authenticated() else None
    my_user = MyUser.objects.get(user=user) if user else None
    try:
        note = ClassicNote.objects.get(pk=note_id)
    except ClassicNote.DoesNotExist:
        raise Http404(u"笔记不存在")
    editable = False
    if my_user:
        if my_user.pk == note.author.pk:
            editable = True
    content = {
        'user': my_user,
        'note': note,
        'editable': editable,
    }
    return render(request, 'note/note_page.html', content)


@user_passes_test(user_check)
def edit_note(request, note_id):
    user = request.user if request.user.is_authenticated() else None
    my_user = MyUser.objects.get(user=user) if user else None
    try:
        note = ClassicNote.objects.get(pk=note_id)
    except ClassicNote.DoesNotExist:
        raise Http404(u"笔记不存在")
    if not my_user or note.author != my_user:
        raise PermissionDenied
    if request.method == 'POST':
        form = ClassicNoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            if my_user.admin_type == ADMIN or my_user.admin_type == SUPER_ADMIN:
                problem = note.problem
                tags = note.tags.all()
                for tag in tags:
                    t_tag = ProblemTag.objects.get_or_create(name=tag.name, abbreviation=tag.name)
                    # t_tag.save()
                    # print(t_tag)
                    problem.tags.add(t_tag[0])
                problem.save()
            content = {
                'note': note,
                'editable': True,
            }
            return render(request, 'note/note_page.html', content)
        else:
            content = {
                'form': form,
                'note': note,
            }
            return render(request, 'note/edit_note.html', content)
    else:
        form = ClassicNoteForm(instance=note)
        content = {
            'form': form,
            'note': note,
        }
        return render(request, 'note/edit_note.html', content)


@user_passes_test(user_check)
def add_note(request, problem_id):
    user = request.user if request.user.is_authenticated() else None
    my_user = MyUser.objects.get(user=user) if user else None
    try:
        problem = Problem.objects.get(id=problem_id)
    except Problem.DoesNotExist:
        raise Http404(u"题目不存在")
    if request.method == 'POST':
        form = ClassicNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = my_user
            note.problem = problem
            content = {
                'note': note,
                'editable': True,
            }
            form.save(commit=True)
            if my_user.admin_type == ADMIN or my_user.admin_type == SUPER_ADMIN:
                problem = note.problem
                tags = note.tags.all()
                for tag in tags:
                    t_tag = ProblemTag.objects.get_or_create(name=tag.name, abbreviation=tag.name)
                    # t_tag.save()
                    # print(t_tag)
                    problem.tags.add(t_tag[0])
                problem.save()
            return render(request, 'note/note_page.html', content)
        else:
            content = {
                'form': form,
                'problem': problem
            }
            return render(request, 'note/edit_note.html', content)
    else:
        form = ClassicNoteForm()
        content = {
            'form': form,
            'problem': problem
        }
        return render(request, 'note/add_note.html', content)



