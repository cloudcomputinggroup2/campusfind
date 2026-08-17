from .models import Item, SystemSetting, SecurityAlert
from django.conf import settings

def campusfind_globals(request):
    """
    Context processor to inject global stats, categories, system settings,
    and AWS deployment metadata across all Django templates.
    """
    active_items = Item.objects.filter(is_deleted=False)
    total_count = active_items.count()
    lost_count = active_items.filter(status=Item.STATUS_LOST).count()
    found_count = active_items.filter(status=Item.STATUS_FOUND).count()
    claimed_count = active_items.filter(status=Item.STATUS_CLAIMED).count()

    # System broadcast banner
    banner_active = SystemSetting.get_val('CAMPUS_ALERT_BANNER_ACTIVE', False)
    banner_text = SystemSetting.get_val('CAMPUS_ALERT_BANNER_TEXT', '')

    # Admin active alerts count
    open_alerts_count = 0
    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        open_alerts_count = SecurityAlert.objects.filter(is_resolved=False).count()

    return {
        'GLOBAL_STATS': {
            'total': total_count,
            'lost': lost_count,
            'found': found_count,
            'claimed': claimed_count,
        },
        'ALL_CATEGORIES': Item.CATEGORY_CHOICES,
        'LOCATION_PRESETS': Item.LOCATION_PRESETS,
        'IS_AWS_S3_ENABLED': getattr(settings, 'USE_S3', False),
        'CAMPUS_BANNER': {
            'active': banner_active,
            'text': banner_text,
        },
        'ADMIN_OPEN_ALERTS_COUNT': open_alerts_count,
    }
