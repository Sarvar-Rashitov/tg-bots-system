"""
Custom template filters for Telegram Downloader
"""

from django import template

register = template.Library()

@register.filter
def percentage(value, total):
    """Calculate percentage: value/total * 100"""
    try:
        total = float(total)
        if total == 0:
            return 0
        return float(value) / total * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def filesizeformat(value):
    """Format file size in human readable format"""
    try:
        bytes_val = float(value)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} TB"
    except (ValueError, TypeError):
        return value

@register.filter
def platform_icon(platform):
    """Return Font Awesome icon for platform"""
    icons = {
        'YOUTUBE': 'fab fa-youtube',
        'INSTAGRAM': 'fab fa-instagram',
        'TIKTOK': 'fab fa-tiktok',
    }
    return icons.get(platform.upper(), 'fas fa-link')

@register.filter
def platform_color(platform):
    """Return Bootstrap color class for platform"""
    colors = {
        'YOUTUBE': 'danger',
        'INSTAGRAM': 'danger',
        'TIKTOK': 'dark',
    }
    return colors.get(platform.upper(), 'primary')

@register.filter
def replace(value, arg):
    """Replace first argument with second argument in the value"""
    try:
        parts = arg.split(',')
        if len(parts) != 2:
            return value
        old = parts[0]
        new = parts[1]
        return str(value).replace(old, new)
    except (ValueError, AttributeError):
        return value

@register.filter
def mul(value, arg):
    """Multiply value by argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def divide(value, arg):
    """Divide value by argument"""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
