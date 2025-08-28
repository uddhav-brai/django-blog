from django.conf import settings
from django.db import models
from django.utils import timezone

# Custom manager for published posts
class PublishedManager(models.Manager):
    def get_queryset(self):
        # Use self.model instead of Post
        return super().get_queryset().filter(status=self.model.Status.PUBLISHED)

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Custom manager

    class Meta:
        ordering = ('-publish',)
        indexes = (
            models.Index(fields=['-publish']),
        )

    def __str__(self):
        return self.title
