from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Category', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=80, unique=True)), ('slug', models.SlugField(max_length=100, unique=True)),
            ('description', models.TextField(blank=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
        ], options={'ordering':['name']}),
        migrations.CreateModel(name='Post', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('title', models.CharField(max_length=220)), ('slug', models.SlugField(editable=False, max_length=260, unique=True)),
            ('content', models.TextField()), ('excerpt', models.CharField(max_length=300)), ('cover_image', models.ImageField(blank=True, upload_to='posts/%Y/%m/')),
            ('status', models.CharField(choices=[('DRAFT','Draft'),('PUBLISHED','Published')], db_index=True, default='DRAFT', max_length=10)),
            ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)), ('updated_at', models.DateTimeField(auto_now=True)),
            ('published_at', models.DateTimeField(blank=True, db_index=True, null=True)), ('views', models.PositiveIntegerField(default=0)), ('featured', models.BooleanField(db_index=True, default=False)),
            ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='blog.category')),
        ], options={'ordering':['-published_at','-created_at']}),
        migrations.AddIndex(model_name='post', index=models.Index(fields=['status','published_at'], name='blog_post_status_540a96_idx')),
        migrations.AddIndex(model_name='post', index=models.Index(fields=['category','status'], name='blog_post_categor_34a04f_idx')),
        migrations.CreateModel(name='Comment', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('content', models.TextField(max_length=2000)), ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True)), ('approved', models.BooleanField(db_index=True, default=True)),
            ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
        ], options={'ordering':['-created_at']}),
    ]
