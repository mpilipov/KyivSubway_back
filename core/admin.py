from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['h1', 'title', 'descr', 'image', 'created', 'author','url_slug']
    prepopulated_fields = {'url_slug': ('h1',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'username', 'text', 'created']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)