from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin

from .models import ContactMessage, Review, SiteText

admin.site.site_header = "V2R Admin"
admin.site.site_title = "V2R Admin"
admin.site.index_title = "V2R Admin"


@admin.register(SiteText)
class SiteTextAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ["key", "label", "updated_at"]
    search_fields = ["key", "label", "text"]
    readonly_fields = ["updated_at"]


def _publish(modeladmin, request, queryset):
    queryset.update(is_published=True)


_publish.short_description = "Publish selected reviews"


def _unpublish(modeladmin, request, queryset):
    queryset.update(is_published=False)


_unpublish.short_description = "Unpublish selected reviews"


@admin.register(Review)
class ReviewAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ["name", "role", "is_published", "created_at"]
    list_editable = ["is_published"]
    list_filter = ["is_published"]
    search_fields = ["name", "text"]
    actions = [_publish, _unpublish]


@admin.register(ContactMessage)
class ContactMessageAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ["name", "email", "created_at"]
    search_fields = ["name", "email", "message"]
    readonly_fields = ["created_at"]
