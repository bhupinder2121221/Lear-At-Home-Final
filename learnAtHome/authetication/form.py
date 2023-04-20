from django.forms import forms
from django.core.exceptions import ValidationError


class nameFieled(forms.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        fullname = value.split(" ")
        return fullname[0]

    def validate(self, value):
        super().validate(value)
        for v in value:
            if v == "":
                raise ValidationError("The Name filed is empty")


class RegisterForm(forms.Form):
    first_name = nameFieled(label='First Name', required=True, min_length=3, max_length=15, error_messages={
                       'required': 'Please provide First Name', 'max_length': 'Cannot exeads 15 characters', 'min_length': 'Must be alteast 3 characters'})
    last_name = nameFieled(label='Last Name', required=True, min_length=3, max_length=15, error_messages={
                       'required': 'Please provide First Name', 'max_length': 'Cannot exeads 15 characters', 'min_length': 'Must be alteast 3 characters'})
    email = forms.EmailField(label='Email', required=True, min_length=10, max_length=30, error_messages={
                             'required': 'Email is required', 'min_length': 'Atleast 10 charcters', 'max_length': 'Maximum 30 charcters allowed'})
    dob = forms.DateField(label='D.O.B', widget=forms.SelectDateWidget, required=True, error_messages={
                          'required': 'DOB is required', 'invalid': 'Your DOB is not valid'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True, max_length=16, min_length=8, error_messages={
                               'requied': 'Password is required', 'min_length': 'Atleast8 characters', 'max_length': 'Atmost 16 charcters'})
    confirm_password = forms.CharField(label='Rewrite Password', widget=forms.PasswordInput, required=True, max_length=16, min_length=8, error_messages={
                                  'requied': 'Password is required', 'min_length': 'Atleast8 characters', 'max_length': 'Atmost 16 charcters'})
    profile = forms.ImageField(label='Profile Pic', widget=forms.FileInput)
    terms = forms.BooleanField(label='T&Cs', widget=forms.CheckboxInput,
                               required=True, error_messages={'required': 'Accept our T&Cs'})
    def clean_fname(self):
        first_name:str = self.changed_data['first_name']
        if first_name.isalpha()

    def clean_terms(self):
        value = self.cleaned_data.get('term')
        if value == False:
            raise ValidationError("Tearms Conditions are not checked")

    def clean(self):
        super().clean()
        pass1 = self.cleaned_data.get['password']
        pass2 = self.cleaned_data['confirm_password']
        if pass1 != pass2:
            raise ValidationError("The Passwords did not match!")
