from django.core.validators import RegexValidator
from django.db import models

KEY_VALIDATOR = RegexValidator(
    r"^[a-z0-9._-]+$", "Lowercase letters, digits, dots, dashes and underscores only."
)


class SiteText(models.Model):
    """Client-editable text. The ONLY model for editable content."""

    key = models.CharField("Key", unique=True, max_length=100, validators=[KEY_VALIDATOR])
    label = models.CharField(
        "Label", blank=True, max_length=120, help_text="Admin-only helper text."
    )
    text = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["key"]
        verbose_name = "Site text"
        verbose_name_plural = "Site texts"

    def __str__(self):
        return self.label or self.key


class Review(models.Model):
    """Public testimonial. The public form creates unpublished reviews."""

    name = models.CharField(max_length=120)
    role = models.CharField(max_length=80, default="Customer")
    text = models.TextField()
    is_published = models.BooleanField(default=False)  # pyright: ignore[reportArgumentType]
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    """Submitted via the contact form on the home page."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact message"
        verbose_name_plural = "Contact messages"

    def __str__(self):
        return f"{self.name} - {self.created_at:%Y-%m-%d}"
