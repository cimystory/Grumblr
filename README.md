#Grumblr version 1.5

Run python manage.py runserver and open 127.0.0.1:8000 or localhost:8000 in your web browser

You need to register for an account to see all the post and people's profile.

You must confirm your email to login Grumblr.

If you reset your password, you will be redirect to the login page and need to login again.

If you forgot your password, after you successfully enter your username, you will be redirect to the login page. At this time, you need to see your email to finish the reset password process.

Login users can edit their profile and change their avatars.

Login users can follow and unfollow people and there is another page to show all the following stream.

Add email feature. After registration, people must confirm their email before login. People can also reset their password using the email when they registered.

Newly add features:

1. New post will update automatically every 5 minutes.
2. Every post can add comment and new comment won't need to refresh the whole page to see.

Fixed:

1. Hard code url
2. Validation use Django form

Problems:

1. After Serialize time data, it changes the format and I can't find a good way to make it back to normal time format.


If you have any problems, feel free to contact jingdonl@gmail.com.

Enjoy!

Citation:

bootstrap.min.css: http://getbootstrap.com/

avatar images: https://www.tumblr.com/

main-background image: http://www.bestwallpapers.club/pages/s/simple-background-patterns-for-websites/

icon images: http://glyphicons.com/

Django documentation: https://docs.djangoproject.com/en/1.10/

Jquery documentation: http://api.jquery.com/
