from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import filters
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .forms import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import *
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import logout
from django.contrib.contenttypes.models import ContentType
from djoser.serializers import TokenSerializer
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.utils.translation import gettext as _

def user(self):
    return User.objects.get(pk=self.user_id)


class Index(View):
    def get(self, request):
        if request.user.is_authenticated:
            profile = get_object_or_404(Profile, user_id=request.user.id)
            return redirect('profile', profile.id)
        return render(request, 'main/index.html')
        
class Projects(View):
   def get(self, request):
        query = request.GET.get('q')
        projects = Project.objects.order_by('-posted')
        if query:
            projects = projects.filter(
                Q(title__icontains=query) | Q(info__icontains=query)
            )

        paginator = Paginator(projects, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'projects': page_obj,
            'query': query
        }
        return render(request, 'main/projects.html', context)

class LoadMoreProjects(View):
    def get(self, request):
        page_number = request.GET.get('page')
        projects = Project.objects.order_by('-posted')
        paginator = Paginator(projects, 10) 
        page_obj = paginator.get_page(page_number)

        project_data = []
        for project in page_obj:
            project_data.append({
                'title': project.title,
                'info': project.info,
                'posted': project.posted,
                'colab': project.colab
            })

        return JsonResponse({
            'projects': project_data,
            'has_next': page_obj.has_next()
        })

class Articles(View):
    def get(self, request):
        query = request.GET.get('q')
        articles = Article.objects.order_by('-posted')
        if query:
            articles = articles.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

        paginator = Paginator(articles, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'articles': page_obj,
            'query': query
        }
        return render(request, "main/articles.html", context)

class LoadMoreArticles(View):
    def get(self, request):
        page_number = request.GET.get('page')
        articles = Article.objects.order_by('-posted')
        paginator = Paginator(articles, 10) 
        page_obj = paginator.get_page(page_number)

        article_data = []
        for article in page_obj:
            article_data.append({
                'title': article.title,
                'info': article.info,
                'posted': article.posted,
                'colab': article.colab
            })

        return JsonResponse({
            'articles': article_data,
            'has_next': page_obj.has_next()
        })

class Discussions(View):
    def get(self, request):
        query = request.GET.get('q')
        discussions = Discussion.objects.order_by('-launched') 
        if query: 
            discussions = discussions.filter(
                Q(title__icontains=query)
            ) 
        
        paginator = Paginator(discussions, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'discussions': page_obj,
            'query': query
        }
        return render(request, "main/discussions.html", context)

class LoadMoreDiscussions(View):
    def get(self, request):
        page_number = request.GET.get('page')
        discussions = Discussion.objects.order_by('-posted')
        paginator = Paginator(discussions, 10) 
        page_obj = paginator.get_page(page_number)

        discussion_data = []
        for discussion in page_obj:
            discussion_data.append({
                'title': discussion.title,
                'info': discussion.info,
                'posted': discussion.posted,
                'colab': discussion.colab
            })

        return JsonResponse({
            'discussions': discussion_data,
            'has_next': page_obj.has_next()
        })

class Questions(View):
   def get(self, request):
        query = request.GET.get('q')
        questions = Question.objects.order_by('-posted')
        if query:
            questions = questions.filter(
                Q(title__icontains=query) | Q(info__icontains=query)
            )

        paginator = Paginator(questions, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'questions': page_obj,
            'query': query
        }
        return render(request, 'main/questions.html', context)

class LoadMoreQuestions(View):
    def get(self, request):
        page_number = request.GET.get('page')
        questions = Question.objects.order_by('-posted')
        paginator = Paginator(questions, 10) 
        page_obj = paginator.get_page(page_number)

        question_data = []
        for question in page_obj:
            question_data.append({
                'title': question.title,
                'info': question.info,
                'posted': question.posted,
                'colab': question.colab
            })

        return JsonResponse({
            'questions': question_data,
            'has_next': page_obj.has_next()
        })

class QuestionsDetailView(DetailView):
    model = Question
    pk_url_kwarg = 'id'
    def get(self, request, id):
        question = get_object_or_404(Question, id=id)
        form = CommentForm(request.POST, request.FILES)
        form_answer = AnswerForm(request.POST, request.FILES)
        return render(request, "main/question_detail.html", {'form': form, 'form_answer': form_answer, 'question': question})
    def post(self, request, id):
        question = get_object_or_404(Question, id=id)
        profile = Profile.objects.get(user=request.user)
        comment = Comment.objects.filter(question=id, moderation=True)
        answer = Answer.objects.filter(question=id, moderation=True)
        if request.method == "POST":
            form = CommentForm(request.POST, request.FILES)
            form_answer = AnswerForm(request.POST, request.FILES)
            if form_answer.is_valid():
               
                form_answer = form_answer.save(commit=False)
               
                form_answer.user = profile
               
                form_answer.question = question
                
                form_answer.save()
                return redirect('question-detailed', id=question.id)
            elif form.is_valid():
                form = form.save(commit=False)  
                form.user = profile 
                form.question = question
                form.save()
                return redirect('question-detailed', id=question.id)
        else:
            form = CommentForm()
            form_answer = AnswerForm()
        context = {
            'question': question,
            "answer": answer,
            "comment": comment,
            "form": form,
            "form_answer": form_answer
        }
        return render(request, "main/question_detail.html", context)



class ProjectsDetailView(DetailView):
    model = Project
    pk_url_kwarg = 'id'
    def get(self, request, id):
        project = get_object_or_404(Project, id=id)
        form = CommentForm(request.POST, request.FILES)
        return render(request, "main/project_detail.html", {'form': form, 'project': project})
    def post(self, request, id):
        project = get_object_or_404(Project, id=id)
        profile = Profile.objects.get(user=request.user)
        comment = Comment.objects.filter(project=id, moderation=True)
        if request.method == "POST":
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = profile
                form.project = project
                form.save()
                return redirect('project-detailed', id=project.id)
        else:
            form = CommentForm()
        context = {
            'project': project,
            "comment": comment,
            "form": form
        }
        return render(request, "main/project_detail.html", context)


class ArticlesDetailView(DetailView):
    model = Article
    pk_url_kwarg = 'id'
    def get(self, request, id):
        article = get_object_or_404(Article, id=id)
        form = CommentForm(request.POST, request.FILES)
        return render(request, "main/article_detail.html", {'form': form, 'article': article})

    def post(self, request, id):
        article = get_object_or_404(Article, id=id)
        profile = Profile.objects.get(user=request.user)
        comment = Comment.objects.filter(article=id, moderation=True)
        if request.method == "POST":
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = profile
                form.article = article
                form.save()
                return redirect('article-detailed', id=article.id)
        else:
            form = CommentForm()
        context = {
            'article': article,
            "comment": comment,
            "form": form
        }
        return render(request, "main/article_detail.html", context)

class DiscussionsDetailView(DetailView):
    model = Discussion
    pk_url_kwarg = 'id'
    def get(self, request, id):
        discussion = get_object_or_404(Discussion, id=id)
        form = CommentForm(request.POST, request.FILES)
        return render(request, "main/discussion_detail.html", {'form': form, 'discussion': discussion})

    def post(self, request, id):
        discussion = get_object_or_404(Discussion, id=id)
        profile = Profile.objects.get(user=request.user)
        comment = Comment.objects.filter(discussion=id, moderation=True)
        if request.method == "POST":
            form = CommentForm(request.POST, request.FILES)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = profile
                form.discussion = discussion
                form.save()
                return redirect('discussion-detailed', id=discussion.id)
        else:
            form = CommentForm()
        context = {
            'discussion': discussion,
            "comment": comment,
            "form": form
        }
        return render(request, "main/discussion_detail.html", context)

class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        objects = {}
        project_id = request.POST.get('project_id')
        article_id = request.POST.get('article_id')

        if project_id:
            objects['project'] = (Project.objects.get(id=project_id), project_id)
        elif article_id:
            objects['article'] = (Article.objects.get(id=article_id), article_id)

        profile = Profile.objects.get(user=user)
        for model_obj, model_id in objects.values():
            model_liked_field = f"{model_obj._meta.model_name}_liked"
            liked_field = getattr(model_obj, model_liked_field)
            if profile in liked_field.all():
                liked_field.remove(profile)
            else:
                liked_field.add(profile)

            content_type = ContentType.objects.get_for_model(model_obj)
            like, liked = Like.objects.get_or_create(user=profile, object_id=model_id, content_type=content_type)

        if not liked:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        else:
            like.value = 'Like'

        model_obj.save()
        like.save()

        if model_id == project_id:
            return redirect('projects')
        else: 
            return redirect('articles')  


class SaveAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        objects = {}
        project_id = request.POST.get('project_id')
        article_id = request.POST.get('article_id')
        discussion_id = request.POST.get('discussion_id')
        question_id = request.POST.get('question_id')

        if project_id:
            objects['project'] = (Project.objects.get(id=project_id), project_id)
        elif article_id:
            objects['article'] = (Article.objects.get(id=article_id), article_id)
        elif discussion_id:
            objects['discussion'] = (Discussion.objects.get(id=discussion_id), discussion_id)
        elif question_id:
            objects['question'] = (Question.objects.get(id=question_id), question_id)

        profile = Profile.objects.get(user=user)
        for model_obj, model_id in objects.values():
            model_saved_field = f"{model_obj._meta.model_name}_saved"
            saved_field = getattr(model_obj, model_saved_field)
            if profile in saved_field.all():
                saved_field.remove(profile)
            else:
                saved_field.add(profile)

            content_type = ContentType.objects.get_for_model(model_obj)
            saving, saved = Save.objects.get_or_create(user=profile, object_id=model_id, content_type=content_type)

        if not saved:
            if saving.value == 'Save':
                saving.value = 'Unsave'
            else:
                saving.value = 'Save'
        else:
            saving.value = 'Save'

        model_obj.save()
        saving.save()

        redirect_destinations = {
            project_id: 'project',
            article_id: 'article',
            discussion_id: 'discussion',
            question_id: 'question'
        }
        return redirect(redirect_destinations.get(model_id) + 's')


class UserPublications(View):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query = request.GET.get('q')
        message_tags = messages.get_messages(request)
        profile = Profile.objects.get(user=request.user)
        projects = Project.objects.filter(user=profile)
        articles = Article.objects.filter(user=profile)
        discussions = Discussion.objects.filter(user=profile)
        questions = Question.objects.filter(user=profile)
        if query:
            projects = projects.filter(
                Q(title__icontains=query) | Q(info__icontains=query)
            )
            articles = articles.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            questions = questions.filter(
                Q(title__icontains=query) | Q(info__icontains=query)
            )

        context = {
            'projects': projects,
            'articles': articles,
            'discussions': discussions,
            'questions': questions,
            'message_tags': message_tags
        }
        return render(request, 'main/publications.html', context)

class ProjectDelete(SingleObjectMixin, View):
    permission_classes = [IsAuthenticated]
    model = Project
    success_url = reverse_lazy('publications')

    def get_object(self):
        return get_object_or_404(Project, id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        project.delete()
        messages.success(request, _('Project deleted successfully.'))
        return redirect(self.success_url)

class ArticleDelete(SingleObjectMixin, View):
    permission_classes = [IsAuthenticated]
    model = Article
    success_url = reverse_lazy('publications')

    def get_object(self):
        return get_object_or_404(Article, id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        article.delete()
        messages.success(request, _('Article deleted successfully.'))
        return redirect(self.success_url)

class DiscussionDelete(SingleObjectMixin, View):
    permission_classes = [IsAuthenticated]
    model = Discussion
    success_url = reverse_lazy('publications')

    def get_object(self):
        return get_object_or_404(Discussion, id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        discussion = self.get_object()
        discussion.delete()
        messages.success(request, _('Discussion deleted successfully.'))
        return redirect(self.success_url)

class QuestionDelete(SingleObjectMixin, View):
    permission_classes = [IsAuthenticated]
    model = Question
    success_url = reverse_lazy('publications')

    def get_object(self):
        return get_object_or_404(Question, id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        question = self.get_object()
        question.delete()
        messages.success(request, _('Question deleted successfully.'))
        return redirect(self.success_url)


class ProjectEdit(SingleObjectMixin, View):
    permission_classes = [IsAuthenticated]
    model = Project
    template_name = "main/project_edit.html"
    success_url = reverse_lazy("publications")
    
    def get_object(self):
        return get_object_or_404(Project, id=self.kwargs['id'])
    
    def get(self, request, *args, **kwargs):
        project = self.get_object()
        form = ProjectForm(request.POST, request.FILES)
        return render(request, self.template_name, {'project': project, 'form': form})

    def post(self, request, *args, **kwargs):
        project = self.get_object()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, _('Project edited successfully.'))
            return redirect(self.success_url)
        else:
            form = ProjectForm(request.POST, request.FILES)
        return render(request, self.template_name, {'form':form})
        

class ArticleEdit(SingleObjectMixin, View):
    permission_classes = [IsAuthenticated]
    model = Article
    template_name = "main/article_edit.html"
    success_url = reverse_lazy("publications")
    
    def get_object(self):
        return get_object_or_404(Article, id=self.kwargs['id'])
    
    def get(self, request, *args, **kwargs):
        article = self.get_object()
        form = ArticleForm(request.POST, request.FILES)
        return render(request, self.template_name, {'article': article, 'form': form})

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, _('Article edited successfully.'))
            return redirect(self.success_url)
        else:
            form = ArticleForm(request.POST, request.FILES)
        return render(request, self.template_name, {'form':form})

class DiscussionEdit(SingleObjectMixin, View):
    permission_classes = [IsAuthenticated]
    model = Discussion
    template_name = "main/discussion_edit.html"
    success_url = reverse_lazy("publications")
    
    def get_object(self):
        return get_object_or_404(discussion, id=self.kwargs['id'])
    
    def get(self, request, *args, **kwargs):
        discussion = self.get_object()
        form = DiscussionForm(request.POST, request.FILES)
        return render(request, self.template_name, {'discussion': discussion, 'form': form})

    def post(self, request, *args, **kwargs):
        discussion = self.get_object()
        form = DiscussionForm(request.POST, request.FILES, instance=discussion)
        if form.is_valid():
            form.save()
            messages.success(request, _('Discussion edited successfully.'))
            return redirect(self.success_url)
        else:
            form = DiscussionForm(request.POST, request.FILES)
        return render(request, self.template_name, {'form':form})

class QuestionEdit(SingleObjectMixin, View):
    permission_classes = [IsAuthenticated]
    model = Question
    template_name = "main/question_edit.html"
    success_url = reverse_lazy("publications")
    
    def get_object(self):
        return get_object_or_404(Question, id=self.kwargs['id'])
    
    def get(self, request, *args, **kwargs):
        question = self.get_object()
        form = QuestionForm(request.POST, request.FILES)
        return render(request, self.template_name, {'question': question, 'form': form})

    def post(self, request, *args, **kwargs):
        question = self.get_object()
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, _('Question edited successfully.'))
            return redirect(self.success_url)
        else:
            form = QuestionForm(request.POST, request.FILES)
        return render(request, self.template_name, {'form':form})  


class SavedPublications(View):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        query = request.GET.get('q')
        profile = Profile.objects.get(user=request.user)
        projects = Project.objects.filter(project_saved=True)
        articles = Article.objects.filter(article_saved=True)
        discussions = Discussion.objects.filter(discussion_saved=True)
        questions = Question.objects.filter(question_saved=True)

        if query:
            projects = projects.filter(
                Q(title__icontains=query) | Q(info__icontains=query)
            )
            articles = articles.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
            questions = questions.filter(
                Q(title__icontains=query) | Q(info__icontains=query)
            )
        
        context = {
            'projects': projects,
            'articles': articles,
            'discussions': discussions,
            'questions': questions 
        }
        return render(request, 'main/saved_publications.html', context)

class MeetEngine(View):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        meetings = Meeting.objects.filter(assigned__isnull=False)
        context = {
            'meetings': meetings,
        }
        return render(request, 'main/meetings.html', context)

    def post(self, request):
        organiser = Profile.objects.get(user=request.user)
        participant = Profile.objects.get(id=request.POST.get('participant_id'))
        assigned = datetime.now()
        meeting = Meeting.objects.create(organiser=organiser, participant=participant, assigned=assigned)  
        return redirect('meetings')


class NewMeetingView(CreateView):
    permission_classes = [IsAuthenticated]
    model = Meeting
    form_class = MeetingForm
    template_name = "main/new-meeting.html"
    success_url = reverse_lazy('meetings')

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        return super().form_valid(form)

class MeetingDelete(SingleObjectMixin, View):
    permission_classes = [IsAuthenticated]
    model = Meeting
    success_url = reverse_lazy('meetings')

    def get_object(self):
        return get_object_or_404(Meeting, id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        meeting = self.get_object()
        meeting.delete()
        messages.success(request, _('Meeting deleted successfully.'))
        return redirect(self.success_url)

class Settings(View):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        profile = get_object_or_404(Profile, id=id)
        serializer = ProfileSerializer(profile)
        return render(request, 'main/settings.html', {'profile': profile})

    def post(self, request, id):
        profile = get_object_or_404(Profile, id=id)
        if int(request.user.id) == id:
            data = dict(request.POST)
            data.update(request.FILES)
            serializer = ProfileSerializer(profile, data=data, partial=True)
            if serializer.is_valid():
                if serializer.validated_data:
                    serializer.validated_data['user'] = request.user 
                    serializer.save()
                    return redirect("profile", id=profile.id)
                else: 
                    return redirect("profile", id=profile.id)
            else: 
                print(serializer.errors)
            return render(request, 'main/settings.html', {'profile': profile, 'serializer': serializer})
        else: 
            return HttpResponse('Unauthorized', status=401)


class DeleteAccount(LoginRequiredMixin, View):
    permission_classes = [IsAuthenticated]
    model = User
    success_url = reverse_lazy('main')

    def get_object(self):
        return get_object_or_404(User, id=self.kwargs['id'])

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return render(request, 'main/account_delete.html', {'user': user})
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        password = request.POST.get('password')

        if user.check_password(password):
            user.delete()
            return redirect(self.success_url)
        else:
            messages.error(request, _('Invalid password.'))
            return render(request, 'main/account_delete.html', {'user': user})


class NewProjectView(CreateView):
    permission_classes = [IsAuthenticated]
    model = Project
    form_class = ProjectForm
    template_name = "main/new-project.html"
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        return super().form_valid(form)


class NewArticleView(CreateView):
    permission_classes = [IsAuthenticated]
    model = Article
    form_class = ArticleForm
    template_name = "main/new-article.html"
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        return super().form_valid(form)

class NewDiscussionView(CreateView):
    permission_classes = [IsAuthenticated]
    model = Discussion
    form_class = DiscussionForm
    template_name = "main/new-discussion.html"
    success_url = reverse_lazy('discussions')

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        return super().form_valid(form)

class NewQuestionView(CreateView):
    permission_classes = [IsAuthenticated]
    model = Question
    form_class = QuestionForm
    template_name = "main/new-question.html"
    success_url = reverse_lazy('questions')

    def form_valid(self, form):
        form.instance.user = self.request.user.profile
        return super().form_valid(form)
