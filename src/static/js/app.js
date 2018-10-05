function check_user(){
  console.log('check_user');
    $.ajax({url: "/user", success: function(result){
        var html = "";
        var side_html = "";
        if (result.login){
            // side_html = '<li><a href="/logout?next=' + window.location.pathname + '">Logout</a></li>';
            if (result.avatar_url){
              $('#navPhoto').attr("src", result.avatar_url);
              html += "<li class='nav-item'><a class='nav-link' id='navPhotoLink' href='/dashboard'><img id='navPhoto' class='circle responsive-img' src='"+result.avatar_url+"' alt='user photo'></a></li>";
          }
          html += "<li><a class='btn btn-danger' href='/logout?next=" + window.location.pathname + "'>Logout</a></li>";
          side_html += "<li><a class='text-primary nav-item' href='/dashboard'>My Dashboard</a></li><li><a class='text-danger' href='/logout?next=" + window.location.pathname + "'>Logout</a></li>";
        }else{
            html += "<li class='nav-item'><a class='nav-link' href='/oauth'>Login</a></li>";
            side_html += html;
        }
        // Append new items to navigation
        $("#user_link").append(html)
        // .promise().done(function(){
        //     $('.tooltipped').tooltip();
        //     $(".dropdown-button").dropdown();
        // });
        // $("#side_user_link").append(side_html);
    }});
};

$(function(){
  // Check user status
  check_user();
});
