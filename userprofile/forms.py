from django import forms

from userprofile.models import UserProfile


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'qualification', 'year_of_ex']

    def __init__(self, *args, **kwargs):
        super(CreateProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['qualification'].required = False
        self.fields['year_of_ex'].required = False


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'qualification', 'year_of_ex']

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone'].required = False
        self.fields['qualification'].required = False
        self.fields['year_of_ex'].required = False

    def save(self, commit=True):
        query = self.instance

        if self.cleaned_data['phone']:
            query.phone = self.cleaned_data['phone']

        if self.cleaned_data['qualification']:
            query.qualification = self.cleaned_data['qualification']

        if self.cleaned_data['year_of_ex']:
            query.year_of_ex = self.cleaned_data['year_of_ex']

        if commit:
            query.save()
        return query
