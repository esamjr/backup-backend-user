from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def print_r(data):
    return {
        "testing": str(dir(data))
    }


def global_settings(request):
    facebook = getattr(settings, 'SOCIAL_FACEBOOK', '')
    instagram = getattr(settings, 'SOCIAL_INSTAGRAM', '')
    twitter = getattr(settings, 'SOCIAL_TWITTER', '')
    youtube = getattr(settings, 'SOCIAL_YOUTUBE', '')

    return {
        'debug': getattr(settings, 'DEBUG', False),
        'MEDIA_URL': getattr(settings, 'MEDIA_URL', ''),
        'SOCIAL_FACEBOOK': facebook,
        'SOCIAL_INSTAGRAM': instagram,
        'SOCIAL_TWITTER': twitter,
        'SOCIAL_YOUTUBE': youtube,
        'SOCIAL_MEDIA': [
            {
                'link': instagram,
                'icon': 'fa fa-instagram',
                'name': ''
            },
            {
                'link': facebook,
                'icon': 'fa fa-facebook',
                'name': 'Facebook'
            },
            {
                'link': twitter,
                'icon': 'fa fa-twitter',
                'name': 'Twitter'
            },
            {
                'link': youtube,
                'icon': 'fa fa-youtube-play',
                'name': 'Youtube'
            },
        ],
        'SHOP_NAME': getattr(settings, 'OSCAR_SHOP_NAME', ''),
        'SHOP_TAGLINE': getattr(settings, 'OSCAR_SHOP_TAGLINE', ''),
        'SCHEME': request.is_secure() and "https://" or "http://",
        'SITE_DESC': getattr(settings, 'SITE_DESCRIPTION', ''),
        'IMG_LOGO': getattr(settings, 'DEFAULT_IMAGE_LOGO', ''),
        'CONTACT_NUMBER': getattr(settings, 'PARTNER_PHONE_NUMBER', ''),
        'CONTACT_WHATSAPP': getattr(settings, 'PARTNER_WHATSAPP_NUMBER', ''),
        'CONTACT_EMAIL': getattr(settings, 'PARTNER_EMAIL', ''),
        'CONTACT_ADDRESS': getattr(settings, 'PARTNER_ADDRESS', ''),
    }

