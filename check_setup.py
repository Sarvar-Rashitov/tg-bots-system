#!/usr/bin/env python
"""
Quick setup verification script
Checks dependencies, configurations, and database
"""

import os
import sys
import importlib
import subprocess

def check_python():
    print("✓ Python version:", sys.version.split()[0])
    return True

def check_deps():
    required = ['django', 'aiogram', 'yt_dlp', 'PIL']
    missing = []

    for dep in required:
        try:
            if dep == 'PIL':
                importlib.import_module('PIL')
            else:
                importlib.import_module(dep)
            print(f"✓ {dep} installed")
        except ImportError:
            missing.append(dep)
            print(f"✗ {dep} NOT installed")

    if missing:
        print(f"\n❌ Missing: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    return True

def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✓ FFmpeg: {version}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("✗ FFmpeg not found in PATH")
        print("  Install from https://ffmpeg.org/download.html")
        print("  Add to PATH and restart terminal")
        return False

def check_django_settings():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_downloader.settings')

    try:
        import django
        django.setup()
        from django.conf import settings

        checks = [
            ('DEBUG', settings.DEBUG),
            ('SECRET_KEY set', settings.SECRET_KEY != 'django-insecure-your-secret-key-here-change-in-production'),
            ('DATABASES configured', 'default' in settings.DATABASES),
            ('STATIC_URL set', bool(settings.STATIC_URL)),
            ('MEDIA_ROOT set', bool(settings.MEDIA_ROOT)),
        ]

        all_good = True
        for name, passed in checks:
            status = "✓" if passed else "✗"
            print(f"{status} {name}: {'OK' if passed else 'ISSUE'}")
            if not passed:
                all_good = False

        return all_good
    except Exception as e:
        print(f"✗ Django settings error: {e}")
        return False

def check_migrations():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_downloader.settings')

    try:
        import django
        django.setup()
        from django.core.management import call_command
        from io import StringIO

        # Check migrations
        out = StringIO()
        call_command('showmigrations', stdout=out)
        output = out.getvalue()

        unapplied = [line for line in output.split('\n') if line.startswith(' [ ]')]
        if unapplied:
            print(f"✗ {len(unapplied)} migrations not applied")
            print("  Run: python manage.py migrate")
            return False
        else:
            print("✓ All migrations applied")
            return True
    except Exception as e:
        print(f"✗ Migration check failed: {e}")
        return False

def check_media_dirs():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    media_dir = os.path.join(base_dir, 'media')
    downloads_dir = os.path.join(media_dir, 'downloads')

    os.makedirs(downloads_dir, exist_ok=True)

    print(f"✓ media directory: {os.path.exists(media_dir)}")
    print(f"✓ downloads directory: {os.path.exists(downloads_dir)}")
    return True

def main():
    print("=" * 50)
    print("Telegram Downloader Bot - Setup Check")
    print("=" * 50)
    print()

    results = []

    print("1. Python Environment")
    results.append(check_python())
    print()

    print("2. Dependencies")
    results.append(check_deps())
    print()

    print("3. FFmpeg")
    results.append(check_ffmpeg())
    print()

    print("4. Django Configuration")
    results.append(check_django_settings())
    print()

    print("5. Database Migrations")
    results.append(check_migrations() if results[0] else False)
    print()

    print("6. Media Directories")
    results.append(check_media_dirs())
    print()

    print("=" * 50)
    if all(results):
        print("✅ All checks passed! Ready to run!")
        print()
        print("Next steps:")
        print("1. python manage.py runserver  (Django admin)")
        print("2. python run_bot.py           (Telegram bot)")
        print("3. Visit http://127.0.0.1:8000/admin")
    else:
        print("❌ Some checks failed. Please fix issues above.")
        return 1
    print("=" * 50)
    return 0

if __name__ == '__main__':
    sys.exit(main())
