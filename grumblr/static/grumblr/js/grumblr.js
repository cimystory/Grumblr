function get_new_blogs(){
    $.ajax({
        type: "GET",
        url: "/grumblr/update_new_blog",
        datatype: 'json',
        success: function(blogs) {
            $.each(blogs, function(id,blog) {
                $("#new_blog").prepend(
                    "<div class='panel panel-default'>"+"<div class='panel-heading'>"
                    +"<a href=\"/grumblr/profile/"+blog.fields.user+"\">"
                    +"<img src=\"/grumblr/avatar/"+blog.fields.user+"\" height=\"20\" width=\"20\" align=\"left\" /></a>"
                    +"<a href=\"/grumblr/profile/"+blog.fields.user+" \"><h2 class=\"panel-title\" style=\"text-indent: 0.5em;\" align=\"left\">"
                    +blog.fields.username+"</h2></a>"
                    +"</div><div class=\"panel-body\"><h4>"+blog.fields.text+"</h4><h5 align=\"right\">"
                    +blog.fields.time+"</h5></div><div class=\"panel-footer\">"
                    +"<form class=\"new_comment\" id=\""+blog.pk+"\" method=\"post\">"
                    +"<input type=\"text\" name=\"comment\" id=\"new_input_comment"+blog.pk+"\" placeholder=\"Comment here\" required><br><br>"+"<button class=\"btn btn-sm btn-primary\" type=\"submit\">Comment</button>"
                    +"</form>"+"<div id=\"old_comment"+blog.pk+"\"></div>"
                    );
            });
        },
        error: function() {
            console.log('error');
        }
    });
}

function post_new_comment(){
    $(document).on('submit',"form.new_comment",function(event) {
        event.preventDefault();// Prevent form from being submitted
        var blog_id = $(this).attr('id');
        var new_comment= $('#new_input_comment'+blog_id).val();
        $.ajax({
            type: "POST",
            url: "/grumblr/add-comment/"+blog_id,
            datatype: 'json',
            data: {'comment_text':new_comment},
            success: function(data) {
                $('#new_input_comment'+blog_id).val('');
                var fields_value=data[0].fields;
                $('#old_comment'+blog_id).append(
                    "<hr><img src=\"/grumblr/avatar/"+fields_value.comment_user+"\" height=\"20\" width=\"20\" align=\"left\" />"
                    +"<h4 style=\"text-indent: 0.5em;\" align=\"left\">"+fields_value.comment_username+"</h4>"
                    +"<h4>"+fields_value.comment_text+"</h4>"
                    +"<h5 align=\"right\">"+fields_value.comment_time+"</h5>"
                );
            },
            error: function() {
                console.log('error');
            }
        });
    });
}

$( document ).ready(function() {  // Runs when the document is ready
  
  post_new_comment();
  window.setInterval(get_new_blogs, 5000);

  // using jQuery
  // https://docs.djangoproject.com/en/1.10/ref/csrf/
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

}); // End of $(document).ready 

