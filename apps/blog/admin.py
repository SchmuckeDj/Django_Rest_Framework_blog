from django.contrib import admin
from .models import Post, Category, Heading

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'title', 'description', 'slug')
    list_filter = ('parent',)
    ordering = ('name',)
    readonly_fields = ('id',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'content', 'keywords', 'slug')
    list_filter = ('status', 'category', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('id','created_at', 'updated_at')
    fieldsets = (
       ('general information', {
           'fields': ('title', 'slug','thumbnail', 'category', 'status', 'content', 'description', 'keywords')
       }),
       ('status & dates', {
           'fields': ('created_at', 'updated_at')
       }),
    )

'''@admin.register(Heading)
class HeadingAdmin(admin.ModelAdmin):
    list_display = ('title', 'post', 'order')
    search_fields = ('title',)'''