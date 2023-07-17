from django.contrib import admin
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from modeltranslation.admin import TranslationAdmin

class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget= CKEditorUploadingWidget())
    class Meta:
        model = Article
        fields = '__all__'


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm

class CommentAdminForm(forms.ModelForm):
    content = forms.CharField(widget= CKEditorUploadingWidget())
    class Meta:
        model = Comment
        fields = ('content', "photos")
        widgets= {
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'comment-content'}),  
            }
class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm

class AnswerAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Answer
        fields = ('content', "photos", "code")
        widgets= {
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'answer-content'}),
            'code': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'code'}),  
            }

class AnswerAdmin(admin.ModelAdmin):
    form = AnswerAdminForm


class ProjectAdminForm(forms.ModelForm):
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

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm

class QuestionAdminForm(forms.ModelForm):
    info = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Question
        fields = ('title', 'code', 'info', 'photos')
        widgets= {
            'title': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'question-title'}),
            'code': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'code'}),  
            'info': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'question-info'}),
            }
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm


class FlatPageAdmin(TranslationAdmin, FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorUploadingWidget}
    }



admin.site.register(Profile)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Discussion)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)
admin.site.register(Save)
admin.site.register(Meeting)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

