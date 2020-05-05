# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 00:32:11 2019

@author: James Beaudoin
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, TeamCreation, Join
from django.forms import TextInput

GENDER_CHOICES= [
    ('0', 'Male'),
    ('1', 'Female'),
    ('2', 'Prefer not to say'),
]

EXP_CHOICES= [
    ('0', 'Intern'),
    ('1', 'Entry-level'),
    ('2', 'Mid-level'),
    ('3', 'Experienced'),
    ('4', 'Managerial'),
    ('5', 'Decision-maker'),

]

ASP_CHOICES= [
    ('0', 'Promotion'),
    ('1', 'Retirement'),
    ('2', 'Job security'),
    ('3', 'Self-development'),
    ('4', 'Flexbility'),

]

WORK_CHOICES= [
    ('0', 'Placeholder 1'),
    ('1', 'Placeholder 2'),
    ('2', 'Placeholder 3'),
]

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model=TeamCreation
        fields=['team_name','team_k']
        widgets={
                'team_name':TextInput(attrs={'placeholder': 'MY TEAM','id':'inputText'}),
                'team_k':TextInput(attrs={'placeholder': 'ENTER KEY','id':'inputText'})
            }
        
class JoinForm(forms.ModelForm):
    class Meta:
        model = Join
        fields=['team_name','team_k']

class PreferencesForm(forms.Form):
    gender = forms.ChoiceField(label='', choices=GENDER_CHOICES)
    gender.widget.attrs.update({'class':'inputwidget','id' : 'gender'})
    
    experience = forms.ChoiceField(label='', choices=EXP_CHOICES)
    gender.widget.attrs.update({'class':'inputwidget','id' : 'experience'})
    
    areawork = forms.ChoiceField(label='', choices=WORK_CHOICES)
    gender.widget.attrs.update({'class':'inputwidget','id' : 'areawork'})

    aspirations = forms.MultipleChoiceField(label='', choices=ASP_CHOICES)
    gender.widget.attrs.update({'class':'inputwidget','id' : 'aspirations'})




    

