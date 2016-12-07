#!/bin/bash
nohup gunicorn acmnote2.wsgi:application -b 127.0.0.1:8020 --reload &
