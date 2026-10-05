from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from .forms import CommentForm, PostForm
from .models import Category, Comment, Post

def paginate(request, queryset, per_page=9):
    return Paginator(queryset, per_page).get_page(request.GET.get('page'))

def home(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED).select_related('author','category').annotate(comment_total=Count('comments', filter=Q(comments__approved=True)))
    return render(request, 'blog/home.html', {'featured_posts': posts.filter(featured=True)[:3], 'popular_posts': posts.order_by('-views')[:3], 'page_obj': paginate(request, posts), 'categories': Category.objects.annotate(post_total=Count('posts', filter=Q(posts__status=Post.Status.PUBLISHED)))[:8]})

def explore(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED).select_related('author','category')
    return render(request, 'blog/list.html', {'page_obj': paginate(request, posts), 'heading': 'Explore stories'})

def category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    posts = cat.posts.filter(status=Post.Status.PUBLISHED).select_related('author','category')
    return render(request, 'blog/list.html', {'page_obj': paginate(request, posts), 'heading': cat.name, 'category': cat})

def categories(request):
    return render(request, 'blog/categories.html', {'categories': Category.objects.annotate(post_total=Count('posts', filter=Q(posts__status=Post.Status.PUBLISHED)))})

def about(request):
    return render(request, 'blog/about.html')

def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related('author','category'), slug=slug)
    if post.status != Post.Status.PUBLISHED and not (request.user.is_authenticated and (request.user == post.author or request.user.is_staff)):
        return render(request, '404.html', status=404)
    if post.status == Post.Status.PUBLISHED:
        Post.objects.filter(pk=post.pk).update(views=F('views') + 1); post.refresh_from_db(fields=['views'])
    comments = post.comments.filter(approved=True).select_related('author')
    related = Post.objects.filter(status=Post.Status.PUBLISHED, category=post.category).exclude(pk=post.pk)[:3]
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': CommentForm(), 'related': related})

@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False); post.author = request.user; post.save(); messages.success(request, 'Your post has been saved.'); return redirect(post)
    return render(request, 'blog/post_form.html', {'form': form, 'heading': 'Write a story'})

def can_manage(user, post): return user.is_staff or user == post.author
@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not can_manage(request.user, post): return render(request, '403.html', status=403)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid(): form.save(); messages.success(request, 'Post updated.'); return redirect(post)
    return render(request, 'blog/post_form.html', {'form': form, 'heading': 'Edit story', 'post': post})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if not can_manage(request.user, post): return render(request, '403.html', status=403)
    if request.method == 'POST': post.delete(); messages.success(request, 'Post deleted.'); return redirect('blog:dashboard')
    return render(request, 'blog/confirm_delete.html', {'object': post, 'kind': 'post'})

@login_required
@require_POST
def comment_create(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False); comment.author = request.user; comment.post = post; comment.save(); messages.success(request, 'Comment posted.')
    else: messages.error(request, 'Please enter a valid comment.')
    return redirect(post)

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if not (request.user.is_staff or request.user == comment.author): return render(request, '403.html', status=403)
    if request.method == 'POST':
        slug = comment.post.slug; comment.delete(); messages.success(request, 'Comment deleted.'); return redirect('blog:post_detail', slug=slug)
    return render(request, 'blog/confirm_delete.html', {'object': comment, 'kind': 'comment'})

def search(request):
    query = request.GET.get('q','').strip()
    posts = Post.objects.none()
    if query:
        posts = Post.objects.filter(status=Post.Status.PUBLISHED).filter(Q(title__icontains=query)|Q(content__icontains=query)|Q(excerpt__icontains=query)|Q(category__name__icontains=query)|Q(author__username__icontains=query)).select_related('author','category').distinct()
    return render(request, 'blog/search.html', {'page_obj': paginate(request, posts), 'query': query, 'result_count': posts.count()})

@login_required
def dashboard(request):
    posts = request.user.posts.select_related('category')
    stats = {'total': posts.count(), 'published': posts.filter(status=Post.Status.PUBLISHED).count(), 'drafts': posts.filter(status=Post.Status.DRAFT).count(), 'views': posts.aggregate(v=Sum('views'))['v'] or 0, 'comments': Comment.objects.filter(post__author=request.user).count()}
    return render(request, 'blog/dashboard.html', {'stats': stats, 'page_obj': paginate(request, posts, 6)})

def robots(request): return HttpResponse('User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n', content_type='text/plain')
def error_400(request, exception=None): return render(request, '400.html', status=400)
def error_403(request, exception=None): return render(request, '403.html', status=403)
def error_404(request, exception=None): return render(request, '404.html', status=404)
def error_500(request): return render(request, '500.html', status=500)
