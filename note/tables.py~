# -*- coding: utf-8 -*-
from .models import *
from table import Table
from table.utils import A
from table.columns import Column, LinkColumn, DatetimeColumn
from util.mytables import MyLink
from util.mytables import MyDateTimeColumn
from django.core.urlresolvers import reverse_lazy


class ClassicNoteTable(Table):

    id = LinkColumn(header=u'#', field='id',
                    links=[MyLink(field='id',
                                  viewname='note_page',
                                  args=(A('id'),)), ],
                    )
    # id = Column(field='id', header=u'#',
    #             header_attrs={'width': '5%'})
    user = Column(field='author', header=u'用户',
                  header_attrs={'width': '20%'})

    problem_info = LinkColumn(header=u'题目信息', field='problem',
                              links=[MyLink(field='get_problem_info',
                                            viewname='problem_page',
                                            args=(A('problem.id'),)), ],
                              header_attrs={'width': '30%'},
                              )
    # problem_info = Column(field='get_problem_info', header=u'题目信息',
    #                       header_attrs={'width': '20%'})

    pub_time = MyDateTimeColumn(field='pub_time', header=u'发表时间',
                                format="%Y年%m月%d日 %H:%I"
                                )
    update_time = MyDateTimeColumn(field='update_time', header=u'最后更新时间',
                                   format="%Y年%m月%d日 %H:%I"
                                   )

    class Meta:
        model = ClassicNote
        search = True
        search_placeholder = 'search'
        pagination = True
        ajax_source = reverse_lazy('table_data_note')
        ajax = True
