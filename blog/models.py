from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['name']
    def __str__(self): return self.name
    def get_absolute_url(self): return reverse('blog:category', args=[self.slug])

class Post(models.Model):
    class Status(models.TextChoices): DRAFT = 'DRAFT', 'Draft'; PUBLISHED = 'PUBLISHED', 'Published'
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, max_length=260, editable=False)
    content = models.TextField()
    excerpt = models.CharField(max_length=300)
    cover_image = models.ImageField(upload_to='posts/%Y/%m/', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False, db_index=True)
    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', 'published_at'], name='blog_post_status_540a96_idx'),
            models.Index(fields=['category', 'status'], name='blog_post_categor_34a04f_idx'),
        ]
    def __str__(self): return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            base, suffix = slugify(self.title)[:240] or 'post', 1
            candidate = base
            while Post.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                suffix += 1; candidate = f'{base[:250-len(str(suffix))]}-{suffix}'
            self.slug = candidate
        if self.status == self.Status.PUBLISHED and not self.published_at: self.published_at = timezone.now()
        super().save(*args, **kwargs)
    def get_absolute_url(self): return reverse('blog:post_detail', args=[self.slug])
    @property
    def reading_time(self): return max(1, round(len(self.content.split()) / 200))

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=True, db_index=True)
    class Meta: ordering = ['-created_at']
    def __str__(self): return f'Comment by {self.author} on {self.post}'
