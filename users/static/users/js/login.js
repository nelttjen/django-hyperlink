const CSRF = getCookie('csrftoken');

$(document).ready(function () {
    buttons();
});

function on_sublit_login(sender) { 
    let nick = $('#username').val();
        let pass = $('#password').val();
        $.ajax({
            type: "POST",
            url: `${ENDPOINT}/users/login/`,
            data: {
                "username": nick,
                "password": pass,
            },
            dataType: "application/json",
            success: function (response) {
                console.log(response);
                console.log(CSRF);
            },
            error: function (response) {
                console.log(response);
            }
        });
}



function buttons() { 
    $("#button-login").click((e) => {
        e.preventDefault();
        on_sublit_login();
    })
 }