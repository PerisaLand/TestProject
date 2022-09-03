from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

# Create your views here.


# 1st approach
# def post_list(request):
#     posts = Post.published.all()
#     return render(request, 'blog/post/list.html', {'posts': posts})

# class-based-view
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'  # default: object_list
    paginate_by = 2
    template_name = 'blog/post/list.html'


# 2nd approach: pagination
# function-based-view
# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 1)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})

# forms.view
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"پیشنهاد خواندن {post.title} از طرف {cd['name']}"
            message = f"{post.title} را در {post_url} بخوانید \n\n" \
                f"{cd['name']} در اینباره میگه: {cd['comment']}"
            send_mail(subject, message, 'admin@admin.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    #     hate = {
    #         'post': post
    #     }
    # return render(request, 'blog/post/share.html', hate, {'form': form})
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, status='published', publish__year=year, publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form =CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})
