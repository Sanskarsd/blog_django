from django.contrib import admin
from .models import Category, Comment, Post
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug','created_at'); search_fields = ('name','description'); prepopulated_fields = {'slug': ('name',)}
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','category','status','featured','published_at','views')
    list_filter = ('status','category','author','featured','published_at'); search_fields = ('title','excerpt','content','author__username'); readonly_fields = ('slug','views','created_at','updated_at')
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author','post','approved','created_at'); list_filter = ('approved','post','author'); search_fields = ('content','author__username','post__title'); actions = ('approve_comments',)
    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset): queryset.update(approved=True)
