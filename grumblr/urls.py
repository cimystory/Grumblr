from django.conf.urls import include, url
from django.contrib.auth import views

import grumblr.views

urlpatterns = [
    url(r'^$', grumblr.views.home,name='home'),
    url(r'^login$', views.login,{'template_name':'grumblr/login.html'},name='login'),
    url(r'^register', grumblr.views.register,name='register'),
    url(r'^confirm-registration/(?P<user_id>\d+)/(?P<token>[A-Za-z0-9\-]+)$',
        grumblr.views.confirm_registration, name='confirm'),
    url(r'^forgot_password', grumblr.views.forgot_password,name='forgot_password'),
    url(r'^reset_password_page/(?P<username>[a-zA-Z0-9]+)/(?P<token>[A-Za-z0-9\-]+)$',
        grumblr.views.reset_password_page, name='reset_password_page'),
    url(r'^message_post', grumblr.views.message_post,name='message_post'),
    url(r'^profile/(?P<user_id>\d+)$', grumblr.views.profile,name='profile'),
    url(r'^edit', grumblr.views.edit_profile,name='edit'),
    url(r'^avatar/(?P<user_id>\d+)$', grumblr.views.get_avatar, name='avatar'),
    url(r'^follow/(?P<user_id>\d+)$', grumblr.views.add_following, name='add_following'),
    url(r'^unfollow/(?P<user_id>\d+)$', grumblr.views.remove_following, name='remove_following'),
    url(r'^following', grumblr.views.following_stream, name='following_stream'),
    url(r'^update_new_blog$', grumblr.views.get_new_blogs_json,name='get_new_blogs_json'),
    url(r'^add-comment/(?P<blog_id>\d+)$', grumblr.views.add_comment,name='add_comment'),
    url(r'^logout$', views.logout_then_login,name='logout'),
]
 

    
