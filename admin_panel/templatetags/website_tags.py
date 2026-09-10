from django import template
from admin_panel.models import WebsiteSetting

register = template.Library()


@register.simple_tag
def get_website_setting():
    return WebsiteSetting.objects.first()