from datetime import datetime

from django.db import models

class SiteText(models.Model):
    key: str
    label: str
    text: str
    updated_at: datetime
    objects: models.Manager

class Review(models.Model):
    name: str
    role: str
    text: str
    is_published: bool
    created_at: datetime
    objects: models.Manager

class ContactMessage(models.Model):
    name: str
    email: str
    message: str
    created_at: datetime
    objects: models.Manager
