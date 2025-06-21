from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import Http404 

from taggit.models import Tag

from .forms import ExtendedUserCreationForm, UserForm, ProfileForm, PostForm, CommentForm
from .models import Profile, Post, Comment


def home_view(request):
    """
    Displays the home page with featured posts.
    """
    # Use the custom manager method to get featured posts
    featured_posts = Post.objects.featured_posts()

    context = {
        'featured_posts': featured_posts,
        'title': 'Home - Django Blog'
    }
    return render(request, 'blog/home.html', context)


def register(request):
    """
    Handles user registration. Displays the form and handles submission,
    showing success messages or detailed error messages.
    """
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            # Display all form errors as individual messages
            for field, errors in form.errors.items():
                for error in errors:
                    # Capitalize field names for better readability (e.g., 'first_name' becomes 'First name')
                    field_name = field.replace('_', ' ').capitalize()
                    messages.error(request, f"{field_name}: {error}")
    else:
        form = ExtendedUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


def logout_view(request):
    """
    Logs out the current user and redirects to the home page with a message.
    """
    auth_logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def profile(request):
    """
    Displays and handles updates for the user's profile.
    Automatically creates a Profile object if one doesn't exist for the user.
    """
    # Get or create the user's profile instance
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile') # Redirect to the profile page to show changes
        else:
            messages.error(request, 'There was an error updating your profile. Please check the form.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile_obj)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'blog/profile.html', context)


def post_list_by_tag(request, tag_slug=None):
    """
    Displays a list of published posts, optionally filtered by a specific tag.
    """
    # Start with all published posts, ordered by most recent
    posts = Post.objects.filter(is_published=True).order_by('-published_date')
    tag = None

    if tag_slug:
        # Get the tag object, or return a 404 if not found
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Further filter posts by the selected tag
        posts = posts.filter(tags__in=[tag])

    context = {
        'posts': posts,
        'tag': tag
    }
    return render(request, 'blog/post_list.html', context)


def post_search(request):
    """
    Handles searching for published posts by title, content, or tags.
    """
    query = request.GET.get('q')
    results = [] # Initialize an empty list for search results

    if query:
        # Filter published posts that match the query across multiple fields
        results = Post.objects.filter(is_published=True).filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-published_date') # Remove duplicates and order by date

    context = {
        'query': query,
        'results': results
    }
    return render(request, 'blog/search_results.html', context)


def privacy_policy_view(request):
    """
    Displays the privacy policy page.
    """
    return render(request, 'blog/privacy_policy.html', {'title': 'Privacy Policy'})


class PostListView(ListView):
    """
    Displays a list of all published posts, ordered by most recent.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date'] # Default ordering

    def get_queryset(self):
        """
        Custom queryset to ensure only published posts are retrieved for the list view.
        """
        return super().get_queryset().filter(is_published=True)


class PostDetailView(DetailView):
    """
    Displays the details of a single post.
    Ensures only published posts are viewable by non-authors,
    and allows authors to view their own unpublished posts.
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        """
        Adjusts the queryset to allow authors to view their own unpublished posts,
        while only showing published posts to other users.
        """
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # Allow author to view their own posts, regardless of published status
            return queryset.filter(Q(is_published=True) | Q(author=self.request.user))
        return queryset.filter(is_published=True) # Only published for anonymous users

    def get_context_data(self, **kwargs):
        """
        Adds a comment form to the context for the post detail page.
        """
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Handles creating a new post. Requires the user to be logged in.
    Automatically sets the post author to the current user.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list') # Redirect to the post list after creation

    def form_valid(self, form):
        """
        Sets the author of the post to the currently logged-in user before saving the form.
        Adds a success message.
        """
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Handles updating an existing post.
    Requires the user to be logged in and to be the author of the post.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    context_object_name = 'post'

    def get_success_url(self):
        """
        Redirects to the updated post's detail page after a successful update.
        """
        messages.success(self.request, "Post updated successfully!")
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        """
        Checks if the current user is the author of the post being updated.
        """
        post = self.get_object()
        return post.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Handles deleting a post.
    Requires the user to be logged in and to be the author of the post.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('post_list') # Redirect to the post list after deletion

    def test_func(self):
        """
        Checks if the current user is the author of the post being deleted.
        """
        post = self.get_object()
        return post.author == self.request.user

    def delete(self, request, *args, **kwargs):
        """
        Adds a success message before proceeding with post deletion.
        """
        messages.success(self.request, "Post deleted successfully!")
        return super().delete(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Handles creating a new comment for a specific post.
    Requires the user to be logged in.
    """
    model = Comment
    form_class = CommentForm
    # template_name is often not explicitly needed here if the form is rendered
    # directly within another template (e.g., post_detail.html)

    def form_valid(self, form):
        """
        Associates the comment with its parent post (retrieved from URL kwargs)
        and the current logged-in user before saving.
        """
        post_pk = self.kwargs.get('pk')  # Get the post's primary key from the URL
        post = get_object_or_404(Post, pk=post_pk)
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, "Comment added successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirects back to the parent post's detail page after a comment is added.
        """
        # self.object.post.pk refers to the primary key of the post associated with the new comment
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Handles updating an existing comment.
    Requires the user to be logged in and to be the author of the comment.
    """
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    context_object_name = 'comment'

    def get_success_url(self):
        """
        Redirects to the parent post's detail page after a comment is updated.
        """
        messages.success(self.request, "Comment updated successfully!")
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        """
        Checks if the current user is the author of the comment being updated.
        """
        comment = self.get_object()
        return comment.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Handles deleting a comment.
    Requires the user to be logged in and to be the author of the comment.
    """
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'comment'

    def get_success_url(self):
        """
        Redirects to the parent post's detail page after a comment is deleted.
        """
        messages.success(self.request, "Comment deleted successfully!")
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        """
        Checks if the current user is the author of the comment being deleted.
        """
        comment = self.get_object()
        return comment.author == self.request.user