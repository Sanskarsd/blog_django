from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Category, Comment, Post

class BlogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('writer', 'writer@example.com', 'Pass12345!')
        self.other = User.objects.create_user('other', 'other@example.com', 'Pass12345!')
        self.category = Category.objects.create(name='Django', slug='django')
        self.post = Post.objects.create(title='Published story', excerpt='An excerpt', content='A useful story about Django.', author=self.user, category=self.category, status=Post.Status.PUBLISHED)
        self.draft = Post.objects.create(title='Private draft', excerpt='Draft', content='Secret', author=self.user, category=self.category)
    def test_published_visible_draft_hidden(self):
        self.assertEqual(self.client.get(self.post.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(self.draft.get_absolute_url()).status_code, 404)
    def test_owner_can_create_and_other_cannot_edit(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('blog:post_create'), {'title':'New','excerpt':'Short','content':'Long enough content','category':self.category.pk,'status':'DRAFT'})
        self.assertEqual(response.status_code, 302)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(reverse('blog:post_edit', args=[self.post.slug])).status_code, 403)
    def test_search_and_comment_authentication(self):
        self.assertContains(self.client.get(reverse('blog:search'), {'q':'Django'}), 'Published story')
        self.assertEqual(self.client.post(reverse('blog:comment_create', args=[self.post.slug]), {'content':'Great'}).status_code, 302)
        self.client.force_login(self.user)
        self.client.post(reverse('blog:comment_create', args=[self.post.slug]), {'content':'Great'})
        self.assertEqual(Comment.objects.count(), 1)
