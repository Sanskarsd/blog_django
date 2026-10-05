from django import forms
from .models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'excerpt', 'content', 'category', 'cover_image', 'status', 'featured')
        widgets = {'content': forms.Textarea(attrs={'rows': 16}), 'excerpt': forms.Textarea(attrs={'rows': 3})}
    def clean_cover_image(self):
        image = self.cleaned_data.get('cover_image')
        if image and image.size > 5 * 1024 * 1024: raise forms.ValidationError('Image must be 5 MB or smaller.')
        return image

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment; fields = ('content',)
        widgets = {'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Join the discussion…'})}
