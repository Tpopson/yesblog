from django.contrib import admin
from .models import Post,Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'slug','author','date_created','image')
    prepopulated_fields = {'slug': ('title',)}
  


class CommentAdmin(admin.ModelAdmin):
    list_display=('name', 'email', 'post', 'date_created', 'active')
    

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)