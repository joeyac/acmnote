# -*- coding: utf-8 -*-
import os
import hashlib
from django.shortcuts import render


def error_page(request, error_reason):
    return render(request, "utils/error.html", {"error": error_reason})


def rand_str(length=32):
    if length > 128:
        raise ValueError("length must <= 128")
    return hashlib.sha512(os.urandom(128)).hexdigest()[0:length]

