from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, Textarea
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Comment
        fields = ('content', "photos")
        widgets= {
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'comment-content'}),  
            }

class AnswerForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Answer
        fields = ('content', "photos", "code")
        widgets= {
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'answer-content'}),
            'code': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'code'}),  
            }


class ProjectForm(forms.ModelForm):
    info = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta: 
        model = Project
        fields = ('title', 'colab', 'code', 'info', 'photos')
        widgets= {
            'title': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'project-title'}),
            'colab': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'project-colab'}),
            'code': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'code'}),  
            'info': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'project-info'}),
            }

class MeetingForm(forms.ModelForm):
    class Meta: 
        model = Meeting
        fields = ('title', 'participant')
        widgets= {
            'title': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'meeting-title'}),
            'participant': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'meeting-participant'}),
            }


class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Article
        fields = ('title', 'content', 'photos')
        widgets= {
            'title': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'article-title'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'article-content'}),
            }

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ('title', 'photos')
        widgets= {
            'title': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'discussion-title'}),
            }

class QuestionForm(forms.ModelForm):
    info = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Question
        fields = ('title', 'code', 'info', 'photos')
        widgets= {
            'title': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'question-title'}),
            'code': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'code'}),  
            'info': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'question-info'}),
            }
