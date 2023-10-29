from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'type', 'category', 'title', 'textPost']
        
class RegisterForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Password')
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                label='Confirm Password')

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # ��� ������� ������ �� ��������.
            # ����� ������ ��������, ��������, �������� ������, ������� ������������ ���� ������, ��� �������� ����.
            # 'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            # 'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this name already exists")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists")
        return super().clean()


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='common')[0]
        basic_group.user_set.add(user)
        return user
