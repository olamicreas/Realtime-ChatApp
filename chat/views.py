from django.shortcuts import render , redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Messages, Post
from django.views.generic.edit import UpdateView
from .forms import MessageForm, PostForm, SearchForm
from django.urls import reverse_lazy
from online_users.models import OnlineUserActivity
from django.contrib import messages as flash

# Create your views here.



class EditPost(UpdateView):
    model = Post
    fields = ['about']

    template_name = 'chat/profile.html'

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()  # Pass all posts to the template
        return context

@login_required
def index(request):
    
    users = User.objects.exclude(username=request.user.username)
    users_with_unread_counts = []
    
    for user in users:
        unread_count = Messages.objects.filter(sender=user, recipient=request.user, is_read=False).count()
        users_with_unread_counts.append({
            'user': user,
            'unread_count': unread_count
        })

    context = {
        'users_with_unread_counts': users_with_unread_counts,
    }
    return render(request, 'chat/index.html', context)

def message_view(request, username):
    recipient = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        message = form.save(commit=False)
        message.sender = request.user
        message.recipient = recipient
        message.save()
        return redirect('message', username=username)

    else:
        form = MessageForm()
    
    messages_sent = Messages.objects.filter(sender = request.user, recipient = recipient)
    messages_recieved = Messages.objects.filter(sender=recipient, recipient = request.user)

    messages = messages_sent | messages_recieved
    
    for message in messages_recieved:
        if not message.is_read:
            message.is_read = True
            message.save()
    
    messages.order_by('timestamp')

    context = {
        'recipient': recipient,
        'messages' : messages,
        'form' : form
    }
    return render(request, 'chat/room.html', context)



def post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            
            post = form.save(commit=False)
           
            post.profile = request.user
            
            post.save()
            return redirect('profile')  
    else:
        form = PostForm()

   
    posts = Post.objects.filter(profile=request.user)
 

    context = {
        'username': request.user.username,
        'email': request.user.email,
        'form': form,
        'posts': posts,  
    }

    return render(request, 'chat/profile.html', context)


def search(request):
    if request.GET.get('q', ''):

        name = request.GET.get('q', '')
        users = User.objects.filter(username__icontains=name)

    
    return render(request, 'chat/search.html', {'users':users} )
        
        
        



def online_user(request):
    user_activity_objects = OnlineUserActivity.get_user_activities()
    print(user_activity_objects)

    return render(request, 'chat/online.html', {'user_activity_objects': user_activity_objects})

def unread_message(request):
    users = User.objects.exclude(id=request.user.id)
    unread_counts = []

    for user in users:
        unread_count = Messages.objects.filter(sender=user, recipient=request.user, is_read=False).count()
        unread_counts.append(unread_count)

    return JsonResponse(unread_counts, safe=False)
def loggout(request):
    logout(request)
    return redirect('/users/login')