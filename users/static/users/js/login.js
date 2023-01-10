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
        })
        .done((response) => {
            response = get_response(response);
            setCookie("Token", response.token, 365);
            $(".done-msg").text("Авторизация успешна");
        })
        .fail((response) => {
            response = get_response(response);
            $(".errors").text(response.msg);
        });

}



function buttons() { 
    $("#button-login").click((e) => {
        e.preventDefault();
        on_sublit_login();
    })
 }