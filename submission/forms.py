# -*- coding: utf-8 -*-
from django import forms
from .result import re_language as language_choice


class SubmissionForm(forms.Form):
    # language = forms.ChoiceField(choices=language_choice, label='语言') # 无序下拉选择框
    language = forms.TypedChoiceField(choices=language_choice, label='语言')
    code = forms.CharField(label='代码', widget=forms.Textarea)
