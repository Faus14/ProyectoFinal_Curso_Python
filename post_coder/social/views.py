from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Relationship,Comment, Like
from .forms import UserRegisterForm, PostForm, CommentForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def feed(request):
	posts = Post.objects.all()
	comment_form = CommentForm()

	context = { 'posts': posts, 'comment_form': comment_form }
	return render(request, 'social/feed.html', context)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado')
			return redirect('feed')
	else:
		form = UserRegisterForm()

	context = { 'form' : form }
	return render(request, 'social/register.html', context)

@login_required
def post(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = current_user
			post.save()
			messages.success(request, 'Post enviado')
			return redirect('feed')
	else:
		form = PostForm()
	return render(request, 'social/post.html', {'form' : form })



def profile(request, username=None):
	current_user = request.user
	if username and username != current_user.username:
		user = User.objects.get(username=username)
		posts = user.posts.all()
	else:
		posts = current_user.posts.all()
		user = current_user
	return render(request, 'social/profile.html', {'user':user, 'posts':posts})


def follow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user, to_user=to_user_id)
	rel.save()
	messages.success(request, f'sigues a {username}')
	return redirect('feed')

def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
	rel.delete()
	messages.success(request, f'Ya no sigues a {username}')
	return redirect('feed')


def about(request):
	return render(request, 'social/about.html')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comentario añadido correctamente')
            
            # Redirigir a la página de origen
            return redirect(request.META.get('HTTP_REFERER', 'feed'))
    
    # Si algo falla, redirigir al feed
    return redirect('feed')



@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Tu perfil ha sido actualizado')
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    
    return render(request, 'social/edit_profile.html', context)


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Verificar si ya le dio like
    like = Like.objects.filter(post=post, user=request.user).first()
    
    if like:
        # Si ya existe un like, lo eliminamos (unlike)
        like.delete()
        messages.success(request, 'Has quitado tu me gusta')
    else:
        # Si no existe, creamos uno nuevo
        Like.objects.create(post=post, user=request.user)
        messages.success(request, 'Te gusta esta publicación')
    
    # Redirigir a la página desde donde se hizo la solicitud
    return redirect(request.META.get('HTTP_REFERER', 'feed'))