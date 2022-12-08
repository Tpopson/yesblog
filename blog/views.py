from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Post,Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages 
from django.utils.text import slugify


from .forms import SignupForm,PostForm,CommentForm


def all_post(request):
    post = Post.objects.filter(status='publish').order_by('-date_created')
    paginator = Paginator(post,2)
    page= request.GET.get('page')
    paged = paginator.get_page(page)
    
    context ={
        'post': paged,
    }

    return render(request, 'index.html', context)


# authentication 
def signout(request):
    logout(request)
    messages.success(request, 'Signout successful!')
    return redirect('signin')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username= username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Signin successful!')
            return redirect('index')
        else:
            messages.warning(request, 'Username/Password incorrect. Kindly supply valid details')
            return redirect('signin')
    return render(request, 'signin.html')



def adminsignin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username= username, password=password)
        if user.is_authenticated:
            login(request, user)
            messages.success(request, 'Welcome Admin!')
            return redirect('allpost')
        else:
            messages.warning(request, 'Admin signin only! Confirm Username/Password')
            return redirect('adminsignin')
    return render(request, 'adminsignin.html')



def signup(request):
    form =  SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            newuser = form.save()
            login(request, newuser)
            messages.success(request, 'Signup successful!')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    return render(request, 'signup.html')

# authentication done


@login_required(login_url='adminsignin')
def createpost(request):
    user = User.objects.get(username = request.user.username)
    form = PostForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                newpost = form.save(commit=False)
                newpost.author = user
                newpost.slug = slugify(newpost.title)
                newpost.save()
                messages.success(request, 'Post created successfully.')
                return redirect('allpost')
    context = {
        'form': form,
    }
    return render(request, 'allpost.html', context)


@login_required(login_url='adminsignin')
def allpost(request):
    form = PostForm()
    post = Post.objects.filter(status='publish').order_by('-date_created')
    paginator = Paginator(post, 2)
    page= request.GET.get('page')
    paged = paginator.get_page(page)
    
    context ={
        'post': paged,
        'form': form,
    }
    return render(request, 'allpost.html', context)



@login_required(login_url='adminsignin')
def editpost(request, id):
    postedit = Post.objects.get(pk=id)
    form = PostForm(instance = postedit)
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = PostForm(request.POST, request.FILES, instance = postedit)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post Edited successfully.')
                return redirect('allpost')
            else:
                messages.error(request, 'You are not admin user.')
                return redirect('allpost')
    context = {
        'form': form,
        'postedit': postedit,
    }
    return render(request, 'editpost.html', context)


@login_required(login_url='adminsignin')
def deleteapost(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        if request.user.is_authenticated:
            postid = request.POST['deletepost']
            postdel = Post.objects.get(pk=postid)
            postdel.delete()
            messages.success(request, 'Post delete success!')
    return redirect(url)



def post_details(request,slug):
    url = request.META.get('HTTP_REFERER')
    detail = Post.objects.get(slug=slug, status='publish')
    comments = Comment.objects.filter(active=True).filter(parent=None)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = detail
            new_comment.save()
            messages.success(request, 'Comment added.')
            return redirect(url)
    else:
        comment_form = CommentForm()

    context ={
        'detail': detail,
        'comments': comments,
        'comment_form':comment_form,
    }

    return render(request, 'details.html', context)




def reply(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')  
            parent_id = request.POST.get('parent') 
            reply = form.save(commit=False)
            reply.post = Post(id=post_id)
            reply.parent = Comment(id=parent_id)
            reply.save()
            messages.success(request, 'Reply added.')
            return redirect(url)
    return redirect(url)



def deletecomment(request,id):
    url = request.META.get('HTTP_REFERER')
    Comment.objects.filter(pk=id).delete()
    return redirect(url)

