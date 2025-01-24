#!/usr/bin/env sh

cd /app/; gunicorn -b 0.0.0.0:8000 contact_restful_api.wsgi
