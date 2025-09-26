from django import template
from django.utils.html import strip_tags


register = template.Library()


@register.filter
def reading_time(html: str) -> str:
    text = strip_tags(html or "")
    words = max(1, len(text.split()))
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


@register.filter
def excerpt(html: str, chars: int = 140) -> str:
    text = strip_tags(html or "").strip()
    if len(text) <= chars:
        return text
    return text[: chars - 1].rsplit(" ", 1)[0] + "…"



