from django.template import Context, Template
from django.test import TestCase, override_settings

from .models import ContactMessage, Review, SiteText


class HomeTests(TestCase):
    def test_home_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)  # pyright: ignore[reportAttributeAccessIssue]
        self.assertContains(response, "We Offer Services")


class ReviewTests(TestCase):
    def test_review_submit_is_unpublished(self):
        response = self.client.post(
            "/review/",
            {"name": "Tester", "role": "Customer", "text": "Great work."},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)  # pyright: ignore[reportAttributeAccessIssue]
        review = Review.objects.get(name="Tester")
        self.assertFalse(review.is_published)

    def test_review_honeypot_rejected(self):
        self.client.post(
            "/review/",
            {"name": "Spam", "role": "x", "text": "y", "website": "http://spam"},
        )
        self.assertFalse(Review.objects.filter(name="Spam").exists())


class SiteTextTagTests(TestCase):
    def setUp(self):
        SiteText.objects.create(key="about.body", label="About body", text="About copy text")
        self.tagged = Template('{% load v2r_tags %}{% site_text "about.body" %}')

    def test_badge_shown_when_refs_on(self):
        with override_settings(SHOW_TEXT_REFS=True):
            html = self.tagged.render(Context({}))
        self.assertIn("text-ref-badge", html)
        self.assertIn("[about.body]", html)

    def test_badge_links_absolute_admin_url_in_new_tab(self):
        site = SiteText.objects.get(key="about.body")
        with override_settings(SHOW_TEXT_REFS=True, HOSTED_URL="http://example.test"):
            html = self.tagged.render(Context({}))
        self.assertIn(
            f'href="http://example.test/admin/core/sitetext/{site.pk}/change/"',
            html,
        )
        self.assertIn('target="_blank"', html)

    def test_unlabeled_text_has_no_badge(self):
        SiteText.objects.create(key="footer.note", text="Some text")
        t = Template('{% load v2r_tags %}{% site_text "footer.note" %}')
        with override_settings(SHOW_TEXT_REFS=True):
            html = t.render(Context({}))
        self.assertNotIn("text-ref-badge", html)
        self.assertIn("Some text", html)

    def test_plain_when_refs_off(self):
        with override_settings(SHOW_TEXT_REFS=False):
            html = self.tagged.render(Context({}))
        self.assertNotIn("text-ref-badge", html)
        self.assertIn("About copy text", html)

    def test_plain_flag_never_badges(self):
        t = Template('{% load v2r_tags %}{% site_text "about.body" plain %}')
        with override_settings(SHOW_TEXT_REFS=True):
            html = t.render(Context({}))
        self.assertNotIn("text-ref-badge", html)
        self.assertIn("About copy text", html)

    def test_missing_key_placeholder(self):
        t = Template('{% load v2r_tags %}{% site_text "nope.missing" plain %}')
        self.assertEqual(t.render(Context({})), "[text missing: nope.missing]")


class GenericPageTests(TestCase):
    def test_unknown_slug_404(self):
        response = self.client.get("/p/does-not-exist/")
        self.assertEqual(response.status_code, 404)  # pyright: ignore[reportAttributeAccessIssue]

    def test_known_slug_renders_text(self):
        SiteText.objects.create(key="page.terms.body", text="Terms body copy")
        response = self.client.get("/p/terms/")
        self.assertEqual(response.status_code, 200)  # pyright: ignore[reportAttributeAccessIssue]
        self.assertContains(response, "Terms body copy")


class ContactFormTests(TestCase):
    def test_contact_submit_creates_message(self):
        response = self.client.post(
            "/contact/", {"name": "Ann", "email": "a@b.co", "message": "Hi there"}
        )
        self.assertEqual(response.status_code, 302)  # pyright: ignore[reportAttributeAccessIssue]
        self.assertTrue(ContactMessage.objects.filter(name="Ann").exists())
