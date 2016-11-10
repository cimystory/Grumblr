from django.shortcuts import render,redirect,get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.db import transaction

from django.http import HttpResponse, Http404

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate

from django.contrib.auth.tokens import default_token_generator

from django.core.mail import send_mail

from django.utils import timezone

from datetime import datetime,timedelta
from mimetypes import guess_type

from grumblr.models import *
from grumblr.forms import *

import base64


@login_required
def home(request):
    context = {'blogs':Blog.get_blogs(),'comments':Comment.get_comments()}
    return render(request,'grumblr/Globalstream.html',context)

@login_required
@transaction.atomic
def message_post(request):
    errors=[]
    form = Blog_form(request.POST)
    if not form.is_valid():
        raise Http404
    else:
        new_blog=Blog(text=request.POST['text'],user=request.user,time=timezone.now(),username=request.user.username)
        new_blog.save()
    context = {'blogs': Blog.get_blogs(), 'errors': errors,'comments':Comment.get_comments()}
    return render(request,'grumblr/Globalstream.html',context)

@transaction.atomic
def register(request):
    context={}
    if request.method=='GET':
        context['form']=RegistrationForm()
        return render(request,'grumblr/Registration.html',context)
    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/Registration.html', context)
    new_user=User.objects.create_user(username=form.cleaned_data['username'],
                                      password=form.cleaned_data['password1'],
                                      first_name=form.cleaned_data['first_name'],
                                      last_name=form.cleaned_data['last_name'],
                                      email=form.cleaned_data['email'])
    new_user.is_active=False
    new_user.save()

    token = default_token_generator.make_token(new_user)

    email_body="""
    Welcome to grumblr! Please click the link below to verify your email address and 
    complete the registration of your account: 

    http://%s%s
    """%(request.get_host(),reverse('confirm',args=(new_user.id,token)))
    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="jingdonl@andrew.cmu.edu",
              recipient_list=[new_user.email])
    context['email']=form.cleaned_data['email']
    new_profile = Profile(first_name = new_user.first_name, 
                          last_name = new_user.last_name,
                          owner = new_user)
    
    new_profile.save()
    new_user=authenticate(username=form.cleaned_data['username'],
                          password=form.cleaned_data['password1'])

    #login(request,new_user)???
    return render(request,'grumblr/confirmation-needed.html',context)

@transaction.atomic
def confirm_registration(request, user_id, token):
    user = get_object_or_404(User, id=user_id)
    if not default_token_generator.check_token(user, token):
        raise Http404
    user.is_active = True
    user.save()
    return render(request, 'grumblr/confirm.html', {})

@transaction.atomic
def forgot_password(request):
    context={}
    if request.method=='GET':
        context['form']=Reset_password()
        return render(request,'grumblr/reset_password.html',context)
    form = Reset_password(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/reset_password.html', context)
    user_reset=get_object_or_404(User, username=form.cleaned_data['username'])
    token = default_token_generator.make_token(user_reset)
    email_body="""
    Please click the link below to reset your password: 

    http://%s%s
    """%(request.get_host(),reverse('reset_password_page',args=(user_reset.username,token)))
    send_mail(subject="Reset your password",
              message=email_body,
              from_email="jingdonl@andrew.cmu.edu",
              recipient_list=[user_reset.email])
    return redirect('login')

@transaction.atomic
def reset_password_page(request,username,token):
    context={}
    if request.method=='GET':
        try:
            context['username']=username
            context['token']=token
            context['form']=Reset_password_form2()
            return render(request,'grumblr/reset_password_todo.html',context)
        except:
            raise Http404
    form = Reset_password_form2(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request,'grumblr/reset_password_todo.html',context)
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, token):
        raise Http404
    user.set_password(form.cleaned_data['password'])
    user.save()
    return redirect('login')

@login_required
@transaction.atomic
def profile(request,user_id):
    context = {}
    me=False
    following=None
    user = get_object_or_404(User, id=user_id)
    current_profile = get_object_or_404(Profile, owner=user)
    my_profile = get_object_or_404(Profile, owner=request.user)
    if user==request.user:
        me = True
    try:
        following_user = my_profile.follow.all()
    except:
        following_user=[]
    if user in following_user:
        following = True
    else:
        following = False
    blogs = Blog.objects.filter(user=user).order_by('-time')
    context['me'] = me
    context['following'] = following
    context['blogs'] = blogs
    context['profile'] = current_profile
    return render(request, 'grumblr/profile.html', context)

@login_required
@transaction.atomic
def edit_profile(request):
    if request.method == 'GET':
        my_profile = get_object_or_404(Profile, owner=request.user)
        form = ProfileForm(instance=my_profile) 
        context = {'form':form,'profile':my_profile}  
        return render(request, 'grumblr/edit.html', context)
    my_profile = Profile.objects.select_for_update().get(owner=request.user)
    form = ProfileForm(request.POST, request.FILES, instance=my_profile)
    if not form.is_valid():
        context = {'form':form,'profile':my_profile} 
        return render(request, 'grumblr/edit.html', context)
    form.save()
    my_profile.save()
    if my_profile.password:
        user = get_object_or_404(User, id=request.user.id)
        user.set_password(my_profile.password)
        user.save()
        return redirect(reverse('home'))
        #after set new password, need to re-login.
    context = {'form':form,'profile':my_profile} 
    return render(request, 'grumblr/edit.html', context)

@login_required
@transaction.atomic
def add_following(request, user_id):
    my_profile = get_object_or_404(Profile, owner=request.user)
    add_following_user = get_object_or_404(User, id=user_id)
    if my_profile.follow.filter(id=user_id).count()==0:
        my_profile.follow.add(add_following_user)
        my_profile.save()
    return redirect(reverse('profile', kwargs={'user_id': user_id}))

@login_required
@transaction.atomic
def remove_following(request, user_id):
    my_profile = get_object_or_404(Profile, owner=request.user)
    remove_following_user = get_object_or_404(User, id=user_id)
    if my_profile.follow.filter(id=user_id).count()==1:
        my_profile.follow.remove(remove_following_user)
        my_profile.save()
    return redirect(reverse('profile', kwargs={'user_id': user_id}))

@login_required
@transaction.atomic
def following_stream(request):
    my_profile = get_object_or_404(Profile, owner=request.user)
    following = my_profile.follow.all()
    context = {'blogs': Blog.objects.filter(user__in=following).order_by('-time'),
               'comments':Comment.get_comments()}
    return render(request, 'grumblr/Followingstream.html', context)

@login_required
@transaction.atomic
def get_avatar(request, user_id):
    user = get_object_or_404(User, id=user_id)
    current_profile = get_object_or_404(Profile, owner=user)
    if not current_profile.photo:
        current_profile.photo='avatar1.png'
        return HttpResponse(current_profile.photo)
    content_type = guess_type(current_profile.photo.name)
    return HttpResponse(current_profile.photo, content_type=content_type)

#update new blog without refresh.
@login_required
@transaction.atomic
def get_new_blogs_json(request):
    time_now = timezone.now()
    five_seconds_before = time_now-timedelta(seconds=5)
    update_blogs = Blog.get_new_blogs(five_seconds_before,time_now)
    response_text = serializers.serialize('json',update_blogs)
    return HttpResponse(response_text,content_type='application/json')

@login_required
@transaction.atomic
def add_comment(request,blog_id):
    current_blog = get_object_or_404(Blog, id=blog_id)
    form = Comment_form(request.POST)
    if not form.is_valid():
        raise Http404
    else:
        new_comment=Comment(comment_text=request.POST['comment_text'],comment_user=request.user,comment_time=timezone.now(),
                            comment_blog=current_blog,comment_username=request.user.username)
        new_comment.save()
        response_text = serializers.serialize('json',[new_comment,])
    return HttpResponse(response_text,content_type='application/json')

