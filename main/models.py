from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import uuid
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django_countries.fields import CountryField
from ckeditor_uploader.fields import RichTextUploadingField

class ProfileManager(models.Manager):
    def get_all_profiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

class Profile(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.TextField(default="", null=True, blank=True, max_length=300)
    country = CountryField(blank_label="(select country)", null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='profile')
    created = models.DateTimeField(auto_now_add=True)
    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    def get_articles_no(self):
        return self.articles.all().count()

    def get_all_authors_articles(self):
        return self.articles.all()

    def get_projects_no(self):
        return self.projects.all().count()

    def get_all_authors_projects(self):
        return self.projects.all()

    def get_discussions_no(self):
        return self.discussions.all().count()

    def get_all_authors_discussions(self):
        return self.discussions.all()

    def get_questions_no(self):
        return self.discussions.all().count()

    def get_all_authors_questions(self):
        return self.discussions.all()

    def get_likes_given_no(self):
        likes = self.like_set.all()
        total_liked = 0
        for item in likes:
            if item.value == 'Like':
                total_liked += 1
        return total_liked

class Project(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=300)
    colab = models.URLField(null=True, blank=True)
    code = models.TextField()
    info = RichTextUploadingField(null=True, blank=True)
    photos = models.ImageField(upload_to="img/%Y/%m/%d", null=True, blank=True)
    project_liked = models.ManyToManyField(Profile, blank=True, related_name='liked_projects')
    project_saved = models.ManyToManyField(Profile, blank=True, related_name='saved_projects')
    posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Projects'
        ordering = ['-posted']

    def get_absolute_url(self):
        return reverse('project:project_detail', args=[self.id])

    @property
    def colab_link(self):
        if self.colab and 'colab.research.google.com' in self.colab:
            return self.colab
        return None

    def get_highlighted_code_project(self):
        lexer = get_lexer_by_name('python')
        formatter = HtmlFormatter(style='vs')
        return highlight(self.code, lexer, formatter)

class Article(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=300)
    content = RichTextUploadingField(null=True, blank=True)
    photos = models.ImageField(upload_to="media/img/%Y/%m/%d/", null=True, blank=True)
    article_liked = models.ManyToManyField(Profile, blank=True, related_name='liked_articles')
    article_saved = models.ManyToManyField(Profile, blank=True, related_name='saved_articles')
    posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Articles'
        ordering = ['-posted']

    def __str__(self):
        return self.title

    def num_likes(self):
        return self.article_liked.all().count()

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

class Discussion(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=300)
    photos = models.ImageField(upload_to="media/img/%Y/%m/%d/", null=True, blank=True)
    launched = models.DateTimeField(auto_now_add=True)
    discussion_saved = models.ManyToManyField(Profile, blank=True, related_name='saved_discussions')

    class Meta:
        verbose_name_plural = 'Discussions'
        ordering = ['-launched']

    def get_absolute_url(self):
        return reverse('discussion:discussion_detail', args=[self.id])


class Question(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=300)
    code = models.TextField()
    info = RichTextUploadingField(null=True, blank=True)
    photos = models.ImageField(upload_to="img/%Y/%m/%d", null=True, blank=True)
    question_saved = models.ManyToManyField(Profile, blank=True, related_name='saved_questions')
    posted = models.DateTimeField(auto_now_add=True)
    meetengine = models.CharField(max_length=400, blank=True)


    class Meta:
        verbose_name_plural = 'Questions'
        ordering = ['-posted']

    def get_absolute_url(self):
        return reverse('question:question_detail', args=[self.id])

    def meetengine_link(self, *args, **kwargs):
        if not self.link:
            base_url = "https://meetengine.onrender.com/new-room/"
            uuid_link = str(uuid.uuid4())
            full_url = base_url + uuid_link
        if not self.link.startswith(base_url):
            raise  ValidationError("Invalid link format")
        super().save(*args, **kwargs)


    def get_highlighted_code_question(self):
        lexer = get_lexer_by_name('python')
        formatter = HtmlFormatter(style='vs')
        return highlight(self.code, lexer, formatter)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, null=True)
    photos = models.ImageField(upload_to="media/img/%Y/%m/%d/", null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    code = models.TextField()
    posted = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    moderation = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Answers'
        ordering = ["-posted"]

    def __str__(self):
        return str(self.user)

    def get_highlighted_code_answer(self):
        lexer = get_lexer_by_name('python')
        formatter = HtmlFormatter(style='vs')
        return highlight(self.code, lexer, formatter)


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE, null=True)
    discussion = models.ForeignKey(Discussion, related_name='comments', on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE, null=True)
    photos = models.ImageField(upload_to="media/img/%Y/%m/%d/", null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    posted = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    moderation = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Comments'
        ordering = ["-posted"]

    def __str__(self):
        return str(self.user)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    liked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.content_object:
            return f"{self.user}-{self.content_object}-{self.value}"
        else:
            return ""

SAVE_CHOICES = (
    ('Save', 'Save'),
    ('Unsave', 'Unsave'),
)

class Save(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    value = models.CharField(choices=SAVE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    saved = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Savings'
        ordering = ["-saved"]


    def __str__(self):
        if self.content_object:
            return f"{self.user}-{self.content_object}-{self.value}"
        else:
            return ""


class Meeting(models.Model):
    title = models.CharField(max_length=300)
    organiser = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="organiser_meetings")
    participant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="participant_meetings")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    assigned = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Meetings'
        ordering = ["-assigned"]