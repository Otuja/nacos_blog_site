from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post, Subscriber
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import EmailPostForm, CommentForm, LoginForm, SignupForm, SubscribeForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.db.models import Count, Q

from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin


from django.views.generic.edit import DeleteView


from django.urls import reverse_lazy


# view for list page
def post_list(request, tag_slug=None):
    """
    Displays a list of published blog posts.
    
    Supports pagination, filtering by tags, and search.
    
    Args:
        request: The HTTP request object.
        tag_slug (str, optional): The slug of the tag to filter by.
    """
    post_list = Post.published.all()
    tag = None
    query = request.GET.get('q')

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )

    # paginatin with 4 posts per page
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1) #the int 1 loads the first page if requested page is not available
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    subscribe_form = SubscribeForm()

    return render(request, 'blog/post/list.html', {
        'posts': posts, 
        'tag': tag, 
        'query': query,
        'subscribe_form': subscribe_form
    })


def subscribe_view(request):
    """
    Handles newsletter subscription.
    """
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not Subscriber.objects.filter(email=email).exists():
                Subscriber.objects.create(email=email)
                messages.success(request, "Thank you for subscribing!")
            else:
                messages.info(request, "You are already subscribed.")
        else:
            messages.error(request, "Invalid email address.")
    return redirect('blog:post_list')


# view for detail and rendering comment 
def post_detail(request, id, post):
    """
    Displays a single blog post and its comments.
    
    Handles comment submission and displays similar posts.
    
    Args:
        request: The HTTP request object.
        id (int): The ID of the post.
        post (str): The slug of the post.
    """
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED, slug=post)
    comments = post.comments.filter(active=True)
    comment = None

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            messages.success(request, "Your comment has been submitted successfully!")
            return redirect('blog:post_detail', id=post.id, post=post.slug)
    else:
        form = CommentForm()

    post_tag_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'comment': comment,
        'similar_post': similar_posts
    }) 


def post_share(request, post_id):
    """
    Allows users to share a post via email.
    
    Args:
        request: The HTTP request object.
        post_id (int): The ID of the post to share.
    """
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    post_url = request.build_absolute_uri(post.get_absolute_url()) #building the absolute url for domain
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']],
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form':form, 'sent': sent, 'post_url': post_url,}) 


# login view 
def login_view(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('blog:post_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, 'blog/login.html', {'form': form})

# signup view 
def signup_view(request):
    """
    Handles user registration.
    """
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Automatically log in the user
                login(request, user)
                messages.success(request, "Signup successful! You are now logged in.")
                return redirect('blog:post_list')  # change to your preferred URL
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()

    return render(request, 'blog/signup.html', {'form': form})

# view for authors blog
@login_required
def profile_view(request):
    """
    Displays the logged-in user's profile and their posts.
    """
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/post/profile.html', {'user_posts': user_posts})


# create with django built in view 
class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new blog post.
    Requires login.
    """
    model = Post
    fields = ['title', 'body', 'image', 'status', 'tags']
    template_name = 'blog/post/post_form.html'
    success_url = reverse_lazy('blog:post_list')  # Change to your desired URL

    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign the logged-in user as author
        return super().form_valid(form)
    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing blog post.
    Requires login and author permission.
    """
    model = Post
    fields = ['title', 'body', 'image', 'status']
    template_name = 'blog/post/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a blog post.
    Requires login and author permission.
    """
    model = Post
    template_name = 'blog/post/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
