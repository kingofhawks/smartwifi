$(function() {
    //Refresh Login/Signup page's captcha image when clicked
    $('.captcha').click(function(){
            var tmp = Math.random().toString();
            var url = "/accounts/captcha/";
            $.get(url+"?newsn=1&tmp="+tmp, function(result){
                $('.captcha').attr("src", result);
                $('#id_captcha_0').attr("value", result.split('/')[3]);
            });
        return false;
    });
});

