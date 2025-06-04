from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import EmailPostForm, CommentForm, LoginForm, SignupForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from django.db.models import Count

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
    '''list views with paginator to navigate the site'''
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # paginatin with 2 posts per page
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1) #the int 1 loads the first page if requested page is not available
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})


# view for detail and rendering comment 
def post_detail(request, id, post):
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
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/post/profile.html', {'user_posts': user_posts})


# create with django built in view 
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'body', 'image', 'status', 'tags']
    template_name = 'blog/post/post_form.html'
    success_url = reverse_lazy('blog:post_list')  # Change to your desired URL

    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign the logged-in user as author
        return super().form_valid(form)
    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'body', 'image', 'status']
    template_name = 'blog/post/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
