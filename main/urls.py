from django.urls import path
from . import views
from .views import * 
from .api import *
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.flatpages import views as flatpages_views

urlpatterns = [
    path('', views.Index.as_view(), name='main'),
    path('projects/', views.Projects.as_view(), name='projects'),
    path('articles/', views.Articles.as_view(), name='articles'),
    path('discussions/', views.Discussions.as_view(), name='discussions'),
    path('questions/', views.Questions.as_view(), name='questions'),
    path('project/<int:id>/', views.ProjectsDetailView.as_view(), name='project-detailed'),
    path('load_more_projects/', LoadMoreProjects.as_view(), name='load_more_projects'),
    path('article/<int:id>/', views.ArticlesDetailView.as_view(), name='article-detailed'),
    path('discussion/<int:id>/', views.DiscussionsDetailView.as_view(), name='discussion-detailed'),
    path('question/<int:id>/', views.QuestionsDetailView.as_view(), name='question-detailed'),
    path('project/<int:id>/delete', views.ProjectDelete.as_view(), name='project-delete'),
    path('article/<int:id>/delete', views.ArticleDelete.as_view(), name='article-delete'),
    path('discussion/<int:id>/delete', views.DiscussionDelete.as_view(), name='discussion-delete'),
    path('question/<int:id>/delete', views.QuestionDelete.as_view(), name='question-delete'),
    path('project/<int:id>/edit', views.ProjectEdit.as_view(), name='project-edit'),
    path('article/<int:id>/edit', views.ArticleEdit.as_view(), name='article-edit'),
    path('discussion/<int:id>/edit', views.DiscussionEdit.as_view(), name='discussion-edit'),
    path('question/<int:id>/edit', views.QuestionEdit.as_view(), name='question-edit'),
    path('api/like/', views.LikeAPIView.as_view(), name='api-like'),
    path('api/save/', views.SaveAPIView.as_view(), name='api-save'),
    path('api/auth/register/', RegisterAPIView.as_view(), name='api-register'),
    path('api/auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/auth/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('api/auth/new-password/', NewPasswordAPIView.as_view(), name='new-password'),
    path('profile/<int:id>/', ProfileAPIView.as_view(), name='profile'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path('publications/', views.UserPublications.as_view(), name='publications'),
    path('saved-publications/', views.SavedPublications.as_view(), name='saved-publications'),
    path('meetings/', views.MeetEngine.as_view(), name='meetings'),
    path('new-meeting/', views.NewMeetingView.as_view(), name='new-meeting'),
    path('meeting/<int:id>/delete', views.MeetingDelete.as_view(), name='meeting-delete'),
    path('profile/<int:id>/settings', views.Settings.as_view(), name='settings'),
    path('user/<int:id>/delete', views.DeleteAccount.as_view(), name='account-delete'),
    path('new-project/', views.NewProjectView.as_view(), name='new-project'),
    path('new-article/', views.NewArticleView.as_view(), name='new-article'),
    path('new-discussion/', views.NewDiscussionView.as_view(), name='new-discussion'),
    path('new-question/', views.NewQuestionView.as_view(), name='new-question'),
    path('terms/', flatpages_views.flatpage, {'url': '/terms/'}, name='terms'),
    path('privacy/', flatpages_views.flatpage, {'url': '/privacy/'}, name='privacy'),


]