
from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', min_length=10, max_length=30, widget=forms.EmailInput(attrs={'class': 'form-control'}), error_messages={
                             'required': 'Email is required', 'max_length': 'Almost 30 charcaters allowed in email', 'min_length': 'Minimum 10 characters allowed'})
    password = forms.CharField(max_length=16, min_length=8, label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}), error_messages={
                               'requied': 'Password is required', 'max_length': 'Maximum 18 characters allowed', 'min_length': 'Minimum 8 characters allowed'})


class addSubject(forms.Form):
    subjectName = forms.CharField(label="Subject Name", min_length=2, max_length=20, error_messages={
        'required': 'Subject name is required.', 'min_length': 'Minimum 2 characters are required.', 'max_length': "Characters cannot exceed 30."})


class addItemForm(forms.Form):
    sellersChoices = (
        ('1', 'Bhupinder'),
        ('2', 'Yash'),
    )
    category_choice = (
        ('books', 'Books'),
        ('extra', 'Extra')
    )
    title = forms.CharField(label="Item Name", max_length=100, widget=forms.TextInput(attrs={
                            'class': 'form-control'}))
    price = forms.IntegerField(
        label="Price", widget=forms.TextInput(attrs={'class': 'form-control'}))
    seller = forms.ChoiceField(
        choices=sellersChoices, widget=forms.Select(attrs={'class': 'form-select'}))
    classtype = forms.CharField(
        label="Class Type", widget=forms.TextInput(attrs={'class': 'form-control'}))
    noOfItems = forms.IntegerField(
        label="No Of Items", widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(
        label="Category", choices=category_choice, widget=forms.Select(attrs={'class': 'form-select'}))
    image = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'subject_hidden_img'})
                            )


class addLecture(forms.Form):
    lecturesName = forms.CharField(label="Lecture Title", max_length=100)
    lectureUrl = forms.CharField(label="Lecture Link")


class addClass(forms.Form):
    className = forms.CharField(label="Class", max_length=15, error_messages={
                                'required': "Class field is required.", "max_length": "Max 15 characters allowed."})
    classType = forms.CharField(
        label='class Type', max_length=15, min_length=2)


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


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

        def clean_title(self):
            if len(title) > 255:
                raise ValidationError("Title Cannot exceds 255 characters.")

        def clean_content(self):
            if len(content) > 10000:
                raise ValidationError("Content cannot exceds 10000 characters")

    def fill_rest_fileds(self, user_given, pl, dt):
        self.author = user_given
        self.postlike = pl
        self.dateTime = dt


class RegisterForm(forms.Form):
    fname = nameFieled(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, min_length=1, max_length=15, error_messages={
                       'required': 'Please provide First Name', 'max_length': 'Cannot exeads 15 characters', 'min_length': 'Must be alteast 1 characters'})
    lname = nameFieled(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, min_length=1, max_length=15, error_messages={
                       'required': 'Please provide First Name', 'max_length': 'Cannot exeads 15 characters', 'min_length': 'Must be alteast 1 characters'})
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True, min_length=10, max_length=30, error_messages={
                             'required': 'Email is required', 'min_length': 'Atleast 10 charcters', 'max_length': 'Maximum 30 charcters allowed'})
    address = nameFieled(label='Address', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, min_length=4, max_length=115, error_messages={
        'required': 'Please provide First Name', 'max_length': 'Cannot exeads 15 characters', 'min_length': 'Must be alteast 1 characters'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, max_length=16, min_length=8, error_messages={
                               'requied': 'Password is required', 'min_length': 'Atleast8 characters', 'max_length': 'Atmost 16 charcters'})
    re_password = forms.CharField(label='Rewrite Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True, max_length=16, min_length=8, error_messages={
                                  'requied': 'Password is required', 'min_length': 'Atleast8 characters', 'max_length': 'Atmost 16 charcters'})

    terms = forms.BooleanField(label='T&Cs', widget=forms.CheckboxInput,
                               required=True, error_messages={'required': 'Accept our T&Cs'})

    def clean_terms(self):
        value = self.cleaned_data.get('term')
        if value == False:
            raise ValidationError("Tearms Conditions are not checked")

    def clean(self):
        super().clean()
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('re_password')
        if pass1 != pass2:
            raise ValidationError("The Passwords did not match!")
