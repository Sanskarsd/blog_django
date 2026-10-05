from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from blog.models import Category, Comment, Post

class Command(BaseCommand):
    help = 'Create useful local demo content.'
    def handle(self, *args, **kwargs):
        user, created = get_user_model().objects.get_or_create(username='editor', defaults={'email':'editor@example.com'})
        if created: user.set_password('ChangeMe123!'); user.save()
        for name, description in [('Django','Building dependable web applications.'),('Technology','Tools and ideas that shape our work.'),('Design','Crafting useful, humane interfaces.')]:
            cat, _ = Category.objects.get_or_create(name=name, defaults={'slug': name.lower(), 'description': description})
            Post.objects.get_or_create(title=f'Notes on {name}', author=user, defaults={'category':cat,'excerpt':f'A considered introduction to {name.lower()}.','content':f'This is a starter story about {name}. Replace it with your own perspective and publish when ready.','status':Post.Status.PUBLISHED,'featured':True})
        self.stdout.write(self.style.SUCCESS('Seeded categories and sample stories. Editor password: ChangeMe123!'))
