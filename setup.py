#!/usr/bin/env python
"""
Quick setup script for Telegram Downloader Bot
Run this after cloning/installing the project
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def run_command(cmd, description):
    print(f"> {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   [OK] Success")
            return True
        else:
            print(f"   [ERROR] Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False

def main():
    print_header("Telegram Downloader Bot - Setup Wizard")

    # Check Python
    print(f"Python version: {sys.version.split()[0]}")

    # Step 1: Install dependencies
    print("\n1. Installing dependencies...")
    if not run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages"
    ):
        print("\n❌ Failed to install dependencies. Run manually:")
        print("   pip install -r requirements.txt")
        return 1

    # Step 2: Check FFmpeg
    print("\n2. Checking FFmpeg...")
    if not run_command("ffmpeg -version", "Verifying FFmpeg installation"):
    print("\n! FFmpeg not found!")
    print("  Please install from https://ffmpeg.org/download.html")
    print("  Windows: Download, extract to C:\\ffmpeg, add to PATH")
    print("  Mac: brew install ffmpeg")
    print("  Linux: sudo apt install ffmpeg")
        return 1

    # Step 3: Create directories
    print("\n3. Creating directories...")
    Path("media/downloads").mkdir(parents=True, exist_ok=True)
    print("   ✓ media/downloads/ created")

    # Step 4: Run migrations
    print("\n4. Setting up database...")
    if not run_command(f"{sys.executable} manage.py migrate", "Running migrations"):
        print("\n❌ Migration failed")
        return 1

    # Step 5: Ask for superuser creation
    print("\n5. Create admin user?")
    response = input("   (Y/n): ").strip().lower()
    if response in ['', 'y', 'yes']:
        print("   Creating superuser...")
        os.system(f"{sys.executable} manage.py createsuperuser")

    # Step 6: Create sample data
    print("\n6. Create sample data?")
    response = input("   (Y/n): ").strip().lower()
    if response in ['', 'y', 'yes']:
        if not run_command(f"{sys.executable} manage.py sample_data", "Creating sample data"):
            print("   (You can run later: python manage.py sample_data)")

    print_header("Setup Complete!")

    print("\n✅ Installation complete!\n")
    print("Next steps:")
    print("1. Add your Telegram bot token in Django admin")
    print("   URL: http://127.0.0.1:8000/admin")
    print("   Navigate to Bots → Add Bot")
    print("   Get token from @BotFather on Telegram\n")

    print("2. Start the Django server (Terminal 1):")
    print(f"   {sys.executable} manage.py runserver\n")

    print("3. Start the Telegram bot (Terminal 2):")
    print(f"   {sys.executable} run_bot.py\n")

    print("4. Test your bot:")
    print("   Open Telegram, find your bot, send /start\n")

    open_browser = input("Open browser to admin panel? (Y/n): ").strip().lower()
    if open_browser in ['', 'y', 'yes']:
        webbrowser.open("http://127.0.0.1:8000/admin")

    print("\n📚 Documentation files:")
    print("   README.md - Full documentation")
    print("   QUICKSTART.md - Quick reference")
    print("   ARCHITECTURE.md - Technical details")
    print("\nHappy downloading! 🚀\n")

    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(1)
