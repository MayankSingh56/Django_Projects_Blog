from django.contrib import admin
from .models import Blog, Category

# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'is_featured', 'category')
    search_fields = ('title', 'short_description', 'blog_body')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)
