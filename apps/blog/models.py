from django.db import models
from django.utils import timezone
import uuid


# Create your models here.
def blog_thumbnail_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/blog_thumbnails/<filename>
    return 'blog/{0}/{1}'.format(instance.title, filename)

def category_thumbnail_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/category_thumbnails/<filename>
    return 'category/{0}/{1}'.format(instance.name, filename)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True)

    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField()
    thumbnail = models.ImageField(upload_to=category_thumbnail_path)
    slug= models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Post(models.Model):

    class PostObject(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    status_options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to=blog_thumbnail_path)
    keywords = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    status = models.CharField(max_length=10, choices=status_options, default='draft')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    objects = models.Manager() # default manager
    postObject = PostObject() # custom manager

    class Meta:
        ordering = ('-published',)


    def __str__(self):
        return self.title