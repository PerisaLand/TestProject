from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# from django_extensions.db.fields import AutoSlugField
from django.utils.text import slugify
from taggit.managers import TaggableManager


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
    title = models.CharField(max_length=80, verbose_name='عنوان')
    slug = models.SlugField(max_length=80, unique_for_date='publish', allow_unicode=True, verbose_name='اسلاگ')
    # slug = AutoSlugField(max_length=90, unique_for_date='publish', populate_from=['name'], unique=True, \
    # allow_unicode=True, slugify_function=my_slugify_function)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='نویسنده')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    # thumbnail = models.ImageField(upload_to='images', verbose_name='تصاویر')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='وضعیت')
    tags = TaggableManager()

    # 1st approach
    # model manager
    # objects = PublishedManager()

    # 2nd approach
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('publish',)
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=90)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'نظرات'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return f"نظر توسط {self.name} در {self.post}"
