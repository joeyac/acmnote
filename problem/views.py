# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Problem, ProblemTag
from django.http import Http404
from note.models import ClassicNote
from authentication.models import MyUser
from django.db.models import Q, Count
# Create your views here.
from table.views import FeedDataView
from problem.tables import ProblemTable
from functools import reduce


class MyDataView(FeedDataView):
    token = ProblemTable.token

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
        return super(MyDataView, self).get_queryset().filter(visible=True)

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


def problem_list_page(request):
    """
    前台的问题列表
    """
    # 正常情况
    problems = ProblemTable()
    tags = ProblemTag.objects.annotate(problem_number=Count("problem")).filter(problem_number__gt=0).order_by(
        "-problem_number")
    return render(request, 'problem/problem_list.html',
                  {'problem': problems, 'tags': tags})


def problem_page(request, problem_id):
    """
    前台题目详情页
    """
    user = request.user if request.user.is_authenticated() else None
    my_user = MyUser.objects.filter(user=user)
    try:
        problem = Problem.objects.get(id=problem_id, visible=True)
    except Problem.DoesNotExist:
        raise Http404(u"题目不存在")
    # status==0 表示尚未登陆只能查看
    # status==1 表示已经登陆且与该题没有relation，可以添加classic note
    # status==2 表示已经登陆且与该题有relation，可以修改classic note
    status = 0
    try:
        note = ClassicNote.objects.get(author=my_user, problem=problem)
    except ClassicNote.DoesNotExist:
        note = None
    if user:
        status = 2 if note else 1
    # print(problem.input)
    # ins = problem.input[2:-2].split("', '")
    # _input = []
    # for obj in ins:
    #     _input.append(obj.replace("\\r\\n", "<br>"))
    # ous = problem.output[2:-2].split("', '")
    # _output = []
    # for obj in ous:
    #     _output.append(obj.replace("\\r\\n", "<br>"))
    return render(request, 'problem/problem_page.html',
                  {'problem': problem, 'status': status, 'note': note})

