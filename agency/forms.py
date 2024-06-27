from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from agency.models import Redactor, Newspaper


class RedactorCreationForm(UserCreationForm):
    class Meta:
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience"
        )


class RedactorLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ("first_name", "last_name", "username", "years_of_experience",)

    def clean_years_of_experience(self):
        years_of_experience = self.cleaned_data.get("years_of_experience")
        if years_of_experience is None:
            raise forms.ValidationError("This field is required.")

        if not isinstance(years_of_experience, int):
            raise forms.ValidationError(
                "Years of experience must be a number."
            )

        if years_of_experience < 0 or years_of_experience > 15:
            raise forms.ValidationError(
                "Years of experience must be between 0 and 15."
            )

        return years_of_experience


class NewspaperForm(forms.ModelForm):
    publisher = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Newspaper
        fields = ["title", "content", "published_date", "topic", "publisher"]


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=250,
        required=False,
        label="",
        widget=forms.TextInput()
    )

    def __init__(self, *args, **kwargs):
        placeholder = kwargs.pop("placeholder", "")
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields["query"].widget.attrs["placeholder"] = placeholder


class NewspaperSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        kwargs["placeholder"] = "Search by title"
        super().__init__(*args, **kwargs)


class RedactorSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        kwargs["placeholder"] = "Search by username"
        super().__init__(*args, **kwargs)


class TopicSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        kwargs["placeholder"] = "Search by name"
        super().__init__(*args, **kwargs)
