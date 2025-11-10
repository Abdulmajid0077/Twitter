from django.contrib import admin
from api.models import Comment, Post, User, Media

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Media)

# Register your models here.
