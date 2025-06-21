from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse # Import reverse for get_absolute_url
from taggit.managers import TaggableManager # Ensure TaggableManager is imported


# --- Custom Managers ---
class PostManager(models.Manager):
    """
    Custom manager for the Post model to provide additional query methods.
    """
    def featured_posts(self):
        """
        Returns a queryset of published and featured posts.
        """
        return self.filter(is_published=True, is_featured=True).order_by('-published_date')

    def published(self):
        """
        Returns a queryset of only published posts.
        """
        return self.filter(is_published=True).order_by('-published_date')


# --- Models ---
class Post(models.Model):
    """
    Represents a blog post.
    """
    title = models.CharField(max_length=200)
    # Slug for clean URLs, should be unique
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text="A short summary of the post (optional).")
    image = models.ImageField(upload_to='post_pics/', blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager(blank=True) # Allow tags to be optional
    is_published = models.BooleanField(default=True) # Controls visibility of the post
    is_featured = models.BooleanField(default=False) # Marks post as featured

    # Attach the custom manager to the Post model
    objects = PostManager() # Default manager is now PostManager

    class Meta:
        # Order posts by publication date in descending order (most recent first)
        ordering = ['-published_date']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate a unique slug
        from the post's title if it's not already set.
        """
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Loop until a unique slug is found by appending a counter
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs) # Call the original save method to save the instance

    def __str__(self):
        """
        String representation of the Post model.
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the URL to the detail view of the post.
        Used by CreateView and UpdateView's get_success_url by default.
        """
        return reverse('post_detail', kwargs={'pk': self.pk})


class Profile(models.Model):
    """
    Extends the built-in User model with additional profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='default.jpg', # Set a default picture for new profiles
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        """
        String representation of the Profile model.
        """
        return f'{self.user.username} Profile'


class Comment(models.Model):
    """
    Represents a comment on a blog post.
    """
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Order comments by creation date (oldest first by default, or newest by '-created_at')
        ordering = ['created_at']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        """
        String representation of the Comment model.
        """
        return f'Comment by {self.author.username} on {self.post.title[:30]}...' # Truncate title for display

    def get_absolute_url(self):
        """
        Returns the URL to the detail view of the post the comment belongs to.
        Useful for redirects after comment creation/update/deletion.
        """
        return reverse('post_detail', kwargs={'pk': self.post.pk})
    