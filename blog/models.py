from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
    '''created a custom manage that retrives published post'''
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    

class Post(models.Model):

    class Status(models.TextChoices):
        '''A class for the choice status of a post'''
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to='images/blog/', blank=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    # adding a many to one relationship between author and post 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    # managers
    objects = models.Manager() #the defualt manager
    published = PublishedManager() #custom manager
    tags = TaggableManager() #for tagging posts



    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish']),]

    def __str__(self):
        return self.title
    
    # auto filling slug with title 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # for canonical url that aids SEO 
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id, self.slug])
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['-created']),]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'