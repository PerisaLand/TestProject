# from django.urls import path, register_converter
# from django.urls.converters import SlugConverter
from django.urls import path, re_path
from . import views

app_name = 'blog'


# class PersianSlugConvertor(SlugConverter):
#     regex = '+[-0123456789_ضصثقفغعهخحجچشسیبلاتنمکگظطزرذدئوپ]'
#
#
# register_converter(PersianSlugConvertor, 'persian_slug')

urlpatterns = [

    # path('', views.post_list, name='post_list'),
    # class base-view url
    path('', views.PostListView.as_view(), name='post_list' ),
    path("<int:year>/<int:month>/<int:day>/<slug>/", views.post_detail, name='post_detail'),
    # this can replace to PersianSlug
    re_path('person_list/(?P<slug>[-\w]+)/', views.post_detail, name='post_detail'),

]
