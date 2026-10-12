from django import forms


class HoneypotForm(forms.Form):
    """Shared anti-spam base: a hidden field bots tend to fill in."""

    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def clean_website(self):
        website = self.cleaned_data.get("website")
        if website:
            raise forms.ValidationError("Spam detected.")
        return website


class ReviewForm(HoneypotForm):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Your name"}),
    )
    role = forms.CharField(
        max_length=80,
        required=False,
        initial="Customer",
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Your role (e.g. Customer)"}
        ),
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-input", "rows": 5, "placeholder": "Tell us about your experience"}
        ),
    )


class ContactForm(HoneypotForm):
    name = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Your name"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-input", "placeholder": "Your email"}),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-input", "rows": 5, "placeholder": "Your message"}
        ),
    )
