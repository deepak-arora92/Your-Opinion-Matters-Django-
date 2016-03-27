!function (){
   if ((window.location.pathname == "/home" || window.location.pathname == "/createPoll") && !getCookies("username")) {
    window.location.href="/";
    }
}();

function setCookies(name, exp)
    {
    var exdays = exp || 1;
    var c_name= name || "username";
    var value = $("[name='user_login']").val();
    var exdate=new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
    document.cookie=c_name + "=" + c_value;
    }

function getCookies(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
  }
  
function clearCookies()
{
    //alert('clearing cookies');
    setCookies('username',-2);
}

function validateUserData() {
    if ($("#user_login").val()=="")
    {
     alert("user name is mandatory.");
     return false;
    }
    var email = $("#user_email").val()
    if (email=="") {
        alert("Please Give an Email Address.");
        return false; }
    var pattern = /^[a-z0-9_\+-]+(\.[a-z0-9_\+-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*\.([a-z]{2,4})$/;
    if(!pattern.test(email)) {
        alert("Email Address doen't seem to be valid.");
        return false;}
    
    var pwd = $("#user_password").val()
    if (pwd=="") {
        alert("Please choose a password.");
        return false; }
    setCookies();
    return true;
}
function dont_use_space() {
    var key=window.event.keyCode;
    if(key ==32)
    {
        window.event.keyCode=0;
    }
}

function checkAvailability(name,value) {
    $("#status_"+name).css("display","block")
    $("#status_"+name).html('<img src="/static/images/loader.gif" height="32" width="32" align="absmiddle">&nbsp;Checking availability...');
    data="";
    if (name=="user_login") {
        data = "username="+ value;
    }
    else{
        data = "emailId="+ value;
    }
    $.ajax({
    dataType: "json",
    type: "POST", 
    url: "/signup_check", 
    data: data,
    success: function(response){
        msg = response.msg;
        if(msg == 'OK')
            {
                $("#status_"+name).removeClass('object_error');
                $("#status_"+name).addClass("object_ok");
                $("#status_"+name).html('<img src="/static/images/tick.gif">');
            } 
        else 
            {
                $("#status_"+name).removeClass('object_ok'); // if necessary
                $("#status_"+name).addClass("object_error");
                $("#status_"+name).text(msg);
            } 
    }
  });
}
 