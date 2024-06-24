from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

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
        fields = ("years_of_experience",)

    def clean_years_of_experience(self):
        years_of_experience = self.cleaned_data.get("years_of_experience")

        if years_of_experience is None:
            raise forms.ValidationError("This field is required.")

        if not isinstance(years_of_experience, int):
            raise forms.ValidationError("Years of experience must be a number.")

        if years_of_experience < 0 or years_of_experience > 15:
            raise forms.ValidationError("Years of experience must be between 0 and 15.")

        return years_of_experience


class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Newspaper
        fields = "__all__"
