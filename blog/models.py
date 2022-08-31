from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.utils.text import slugify

# Create your models here.

# 1st method
# class PublishedManager(models.Manager):
#     def published(self):
#         return super(PublishedManager, self).get_queryset().filter(status='published')


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

# you can use this for PersianSlug
def my_slugify_function(content):
    return slugify(content, allow_unicode=True)


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'چرک نویس'), ('published', 'منتشر شده'))
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, unique_for_date='publish', allow_unicode=True)
    # slug = AutoSlugField(max_length=90, unique_for_date='publish', populate_from=['name'], unique=True, allow_unicode=True, slugify_function=my_slugify_function)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    #1st approach
    # model manager
    # objects = PublishedManager()

    #2nd approach
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug ])

    def __str__(self):
        return self.title


