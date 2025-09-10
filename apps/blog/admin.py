from django.contrib import admin
from .models import Post, Category, Heading, PostAnalytics
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'title', 'description', 'slug')
    list_filter = ('parent',)
    ordering = ('name',)
    readonly_fields = ('id',)
    list_editable = ('title',)

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default'))

    class Meta:
        model = Post
        fields = '__all__'

class HeadingInline(admin.TabularInline):
    model = Heading
    extra = 1
    fields = ('title', 'level', 'order', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'status', 'category', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'content', 'keywords', 'slug')
    list_filter = ('status', 'category', 'updated_at')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
       ('General information', {
           'fields': ('title', 'slug','thumbnail', 'category', 'status', 'content', 'description', 'keywords')
       }),
       ('Status & dates', {
           'fields': ('created_at', 'updated_at')
       }),
    )
    inlines = [HeadingInline]


'''@admin.register(Heading)
class HeadingAdmin(admin.ModelAdmin):
    list_display = ('title', 'post', 'order')
    search_fields = ('title',)'''

#admin.site.register(PostAnalytics)

@admin.register(PostAnalytics)
class PostAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('post_title','views', 'impressions', 'clicks_through_rate', 'avg_time_on_page')
    search_fields = ('post__title',)
    readonly_fields = ('post','views', 'impressions', 'clicks_through_rate', 'avg_time_on_page')
    ordering = ('-post__created_at',)

    def post_title(self, obj):
        return obj.post.title
    post_title.short_descriptions = 'post title'
