from django.shortcuts import render
from .tables import GroupTable
# Create your views here.


def group_list_page(request):
    """
    前台的小组
    """
    # 正常情况
    groups = GroupTable()
    content = {
        'groups': groups,
    }
    return render(request, 'group/group_list.html', content)

