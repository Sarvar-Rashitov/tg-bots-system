"""
WSGI config for telegram_downloader project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_downloader.settings')

application = get_wsgi_application()
