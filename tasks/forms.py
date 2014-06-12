# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from models import *
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u'用户名',
        error_messages={'required':'请输入用户名'},
        widget=forms.TextInput(
            attrs={'placeholder':u'Username',}
            ),
        )
    
    password = forms.CharField(
        required=True,
        label=u'密码',
        error_messages={'required':'请输入密码'},
        widget=forms.PasswordInput(
            attrs={'placeholder':r'Password'}
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'不输入用户名跟密码是进不去的...')
        else:
            cleaned_data = super(LoginForm, self).clean()


class TaskForm(forms.Form):
    creator = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        label=u"创建者",
        error_messages={'required': u'Required'},
        )
    tasktype = forms.CharField(
        label=u'任务类型',
        max_length=1,
        widget=forms.Select(choices=TASKTYPE),
    )
    product = forms.CharField(label=u'Product',required=True, widget=forms.Textarea(attrs={'rows':1,'style':'width:30%'}))
    seller = forms.CharField(label=u'Seller',required=True)
    buyer = forms.CharField(label=r'Buyer',required=True)
    address = forms.CharField(
        required=True,
        label=u'地址',
        widget=forms.Textarea(
            attrs={
                'placeholder':'Buyer\'s Address goes in here!',
                'rows': 5,
                'style':'width:60%',
            }
        )
    )
    tracking = forms.CharField(label=r'Tracking number',required=False)
    status = forms.CharField(
        label=u'状态',
        max_length=1,
        widget=forms.Select(choices=STATUS),
    )
    comment = forms.CharField(
        required=False,
        label=u'留言',
        widget=forms.Textarea(
            attrs={
                'placeholder':'',
                'rows': 5,
                'style':'width:60%',
            }
        )
    )
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'红色的看到没有？那些要填！')
        else:
            cleaned_data = super(TaskForm,self).clean()
        return cleaned_data

