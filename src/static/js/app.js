function check_user(){
    $.ajax({url: "/user", success: function(result){
        // console.log('/USER')
        var html = "";
        var side_html = "";
        if (result.login){
            if (result.avatar_url){
              $('#navPhoto').attr("src", result.avatar_url);
              html += "<li class='nav-item'><a class='nav-link pulse' id='navPhotoLink' href='/dashboard/'>"+result.login+" <img id='navPhoto' class='userImage' src='"+result.avatar_url+"' alt='user photo'></a></li>";
          }
          html += "<li class='nav-item'><a class='nav-link' href='./logout?next=" + window.location.pathname + "'>Logout</a></li>";
        }else{
            html += "<li class='nav-item'><a class='nav-link' href='./oauth'>Login</a></li>";
            side_html += html;
        }
        // Append new items to navigation
        $("#user_link").append(html)
    },
  cache: false});
};

$(function(){
  // Check user status
  check_user();
});
