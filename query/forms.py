from django import forms

from query.models import Query


class CreateQueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['heading', 'body', 'image', 'image2', 'image3', 'image4',
                  'image5', 'image6', 'image7', 'image8', 'image9', 'image10']

    def __init__(self, *args, **kwargs):
        super(CreateQueryForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image2'].required = False
        self.fields['image3'].required = False
        self.fields['image4'].required = False
        self.fields['image5'].required = False
        self.fields['image6'].required = False
        self.fields['image7'].required = False
        self.fields['image8'].required = False
        self.fields['image9'].required = False
        self.fields['image10'].required = False


class UpdateQueryForm(forms.ModelForm):
    class Meta:
        model = Query
        fields = ['heading', 'body', 'image', 'image2', 'image3', 'image4',
                  'image5', 'image6', 'image7', 'image8', 'image9', 'image10']

    def __init__(self, *args, **kwargs):
        super(UpdateQueryForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image2'].required = False
        self.fields['image3'].required = False
        self.fields['image4'].required = False
        self.fields['image5'].required = False
        self.fields['image6'].required = False
        self.fields['image7'].required = False
        self.fields['image8'].required = False
        self.fields['image9'].required = False
        self.fields['image10'].required = False

    def save(self, commit=True):
        query = self.instance
        query.heading = self.cleaned_data['heading']
        query.body = self.cleaned_data['body']

        if self.cleaned_data['image']:
            query.image = self.cleaned_data['image']
        if self.cleaned_data['image2']:
            query.image2 = self.cleaned_data['image2']
        if self.cleaned_data['image3']:
            query.image3 = self.cleaned_data['image3']
        if self.cleaned_data['image4']:
            query.image4 = self.cleaned_data['image4']
        if self.cleaned_data['image5']:
            query.image5 = self.cleaned_data['image5']
        if self.cleaned_data['image6']:
            query.image6 = self.cleaned_data['image6']
        if self.cleaned_data['image7']:
            query.image7 = self.cleaned_data['image7']
        if self.cleaned_data['image8']:
            query.image8 = self.cleaned_data['image8']
        if self.cleaned_data['image9']:
            query.image9 = self.cleaned_data['image9']
        if self.cleaned_data['image10']:
            query.image10 = self.cleaned_data['image10']

        if commit:
            query.save()
        return query
