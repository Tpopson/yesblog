from django.db import models
from django.contrib.auth.models import User

STATUS = [
    ('draft', 'draft'),
    ('publish', 'publish'),
]

class Post(models.Model):
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    title = models.CharField(max_length=200, unique=True, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='post_image/%Y/%m/%d/', default='img.jpg', blank=True, null=True) 
    content = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now= True)
    status = models.CharField(max_length=200, choices=STATUS, default='draft', blank=True, null=True)
    
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)



# Create Comment Model
class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name=models.CharField(max_length=50)
    email=models.EmailField()
    parent=models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date_created',)
    
    def __str__(self):
        return f'Comment {self.body} by {self.name}.'

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)

