# -*- coding: utf-8 -*-
from .models import *
from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, Link
from util.mytables import MyLink, MyLinkColumn
from django.core.urlresolvers import reverse_lazy


class ProblemTable(Table):
    tag = None

    ids = Column(field='id', header=u'#', header_attrs={'width': '5%'})
    oj_all = LinkColumn(header=u'OJ&ID', field={'oj', 'oj_id'},
                        links=[MyLink(field='oj_all',
                                      attrs={"href": A('origin_url')}, ), ],

                        header_attrs={'width': '10%'}, searchable=True
                        )
    title = LinkColumn(header=u'标题', field='title',
                       links=[MyLink(field='title', viewname='problem_page', args=(A('id'),)), ],
                       header_attrs={'width': '40%'}, searchable=True
                       )
    difficulty_rank = Column(field='difficulty_rank', header=u'难度等级',
                             header_attrs={'width': '13%'}, searchable=False, sortable=False)
    difficulty_num = Column(field='difficulty_num', header=u'平均指数',
                            header_attrs={'width': '13%'}, searchable=False, sortable=False)

    class Meta:
        model = Problem
        search = True
        search_placeholder = 'search'
        pagination = True
        ajax_source = reverse_lazy('table_data_problem')
        ajax = True
