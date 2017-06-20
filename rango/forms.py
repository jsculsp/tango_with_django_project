from django import forms
from rango.models import Page, Category
from django.contrib.auth.models import User
from rango.models import UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text='Please enter the category name.',
                           widget=forms.TextInput(attrs={'placeholder': '请在此处输入'}))

    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name', 'views')


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text='Please enter the title of the page.',
                            widget=forms.TextInput(attrs={'placeholder': '请在此处输入 title'}),
                            )
    url = forms.CharField(max_length=200,
                          help_text='Please enter the URL of the page.',
                          widget=forms.TextInput(attrs={'placeholder': '请在此处输入 url'}),
                          )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not (url.startswith('http://') or url.startswith('https://')):
            url += 'http://'
            cleaned_data['url'] = url
            return cleaned_data

    class Meta:
        model = Page
        exclude = ('category', 'views')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
