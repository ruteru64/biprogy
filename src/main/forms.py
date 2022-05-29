from types import ClassMethodDescriptorType
from django import forms
from .models import Meeting, Partner
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# ユーザー登録フォーム


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # htmlの表示を変更可能にします
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

# ログインフォーム


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # htmlの表示を変更可能にします
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'

# 営業先を入力するform


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ('name', 'belongs',)  # 営業先名と企業名を入力してもらう

# ミーティングで出た話題を入力するform


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ('topic1', 'topic2', 'topic3',)  # 話題を3つ入力してもらう
