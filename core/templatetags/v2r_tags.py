from django import template
from django.conf import settings
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from core.models import SiteText

register = template.Library()

_MISSING = "[text missing: {key}]"


def _render(key, plain):
    text = SiteText.objects.filter(key=key).first()
    show_refs = getattr(settings, "SHOW_TEXT_REFS", settings.DEBUG)

    if text is None:
        body = escape(_MISSING.format(key=key))
        if plain or not show_refs:
            return body
        url = f"{settings.HOSTED_URL}{reverse('admin:core_sitetext_add')}"
        badge = (
            f'<a class="text-ref-badge" href="{url}" target="_blank" rel="noopener" '
            f'title="Create this text in the admin">[{key}]</a>'
        )
        return mark_safe(f'<span class="text-ref text-ref--missing">{badge} {body}</span>')
    # Badge only when SHOW_TEXT_REFS is on AND the text has a non-empty label.
    if plain or not show_refs or not text.label:
        return escape(text.text)
    url = f"{settings.HOSTED_URL}{reverse('admin:core_sitetext_change', args=[text.pk])}"
    badge = (
        f'<a class="text-ref-badge" href="{url}" target="_blank" rel="noopener" '
        f'title="Edit this text in the admin">[{text.key}]</a>'
    )
    return mark_safe(f'<span class="text-ref">{escape(text.text)} {badge}</span>')


class SiteTextNode(template.Node):
    def __init__(self, key_node, plain):
        self.key_node = key_node
        self.plain = plain

    def render(self, context):
        return _render(self.key_node.resolve(context), self.plain)


@register.tag
def site_text(parser, token):
    """Usage: {% site_text "about.body" %} or {% site_text "header.tagline" plain %}."""
    bits = token.split_contents()
    if len(bits) not in (2, 3):
        raise template.TemplateSyntaxError(f"{bits[0]} takes a key and optionally the flag 'plain'")
    plain = False
    if len(bits) == 3:
        if bits[2] != "plain":
            raise template.TemplateSyntaxError(
                f"{bits[0]} second argument must be the flag 'plain'"
            )
        plain = True
    key_node = parser.compile_filter(bits[1])
    return SiteTextNode(key_node, plain)
