"""URL configuration for the core app."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("review/", views.review_form, name="review_form"),
    path("review/thanks/", views.review_thanks, name="review_thanks"),
    path("contact/", views.contact_submit, name="contact_submit"),
    path("p/<slug:slug>/", views.generic_page, name="generic_page"),
]
