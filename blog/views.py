from sre_constants import SUCCESS
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User
from .models import Post
from users.models import Profile
from django.views.generic import  (ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

def home(request):
    all_posts=Post.objects.all()
    return render(request,'blog/home.html', {'posts': all_posts})


def about(request):
    return render(request,'blog/about.html')

class PostListView(ListView):
    model=Post
    template_name='blog/home.html'
    context_object_name='posts'

class PostCreateView(LoginRequiredMixin, CreateView):
    model=Post
    fields=['title', 'content']
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    model=Post

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=Post
    fields=['title', 'content']
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=Post
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False         

"""class Profile_post(DetailView):
    template_name='blog/user_post.html'
    
    def get_object(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        def get_context_data(self, **kwargs):
           context = super(Profile_post, self).get_context_data(**kwargs)
           context['posts'] = Post.objects.all().filter(author= user)
           context['profiles'] = Profile.objects.all().filter(user= user)
           return context

def Profile_post(request,username):
    user = User.objects.get(username='username')  # grabs <username> from url and stores it in obj to  be passed into the context
    
    posts= Post.objects.filter(author=user),
    profiles=Profile.objects.filter(user=user),  # obj is now accesible in the html via the variable {{ username }}
    
    response = render(request, 'blog/user_post.html', {'posts': 'posts','profiles':'profiles'})
    return response"""
class Profile_post(DetailView):
    model=Post
    template_name='blog/user_post.html'
    context_object_name='posts'
    def get_object(self, **kwargs):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user)
        





        
    