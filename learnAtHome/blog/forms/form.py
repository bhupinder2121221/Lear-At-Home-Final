from django import forms


class GetName(forms.Form):
    email = forms.CharField(label="User Email",max_length=30)
    # password = forms.Password('Password',max_length=16)