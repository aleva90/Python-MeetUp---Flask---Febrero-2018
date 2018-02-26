$(function() {
    $('#btnSignUp').click(function() {
        $.ajax({
            url: '/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
              console.log(response);
              window.location.reload();
              //setTimeout(function(){window.location.reload();}, 1000);
              //setTimeout(function(){window.location.href='/';}, 1000);
            },
            error: function(error) {
              console.log(error);
              window.location.reload();
            }
        });
    });
});
