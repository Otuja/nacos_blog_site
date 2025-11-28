from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
    """
    Custom manager to retrieve only published posts.
    """
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    

class Post(models.Model):
    """
    Represents a blog post.
    
    Attributes:
        title (str): The title of the post.
        slug (str): The URL-friendly slug for the post.
        author (User): The author of the post.
        body (str): The main content of the post.
        image (ImageField): An optional featured image for the post.
        publish (datetime): The date and time the post was published.
        created (datetime): The date and time the post was created.
        updated (datetime): The date and time the post was last updated.
        status (str): The status of the post (Draft or Published).
        tags (TaggableManager): The tags associated with the post.
    """

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
        """
        Returns the canonical URL for the post.
        """
        return reverse('blog:post_detail', args=[self.id, self.slug])
    
    @property
    def reading_time(self):
        """
        Calculates the estimated reading time of the post in minutes.
        Assumes an average reading speed of 200 words per minute.
        """
        words = self.body.split()
        # Average reading speed is 200 words per minute
        minutes = len(words) // 200
        return max(1, minutes)


class Subscriber(models.Model):
    """
    Represents a newsletter subscriber.
    """
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class Comment(models.Model):
    """
    Represents a comment on a blog post.
    
    Attributes:
        post (Post): The post the comment belongs to.
        name (str): The name of the commenter.
        email (str): The email of the commenter.
        body (str): The content of the comment.
        created (datetime): The date and time the comment was created.
        updated (datetime): The date and time the comment was last updated.
        active (bool): Whether the comment is active/visible.
    """
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