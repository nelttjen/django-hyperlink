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
            setCookie("Token", response.content.token, 365);
            $(".done-msg").text("Авторизация успешна");
            $(".errors").text("");

            if (window.location.href.indexOf('?next=') != -1) {
                window.location.replace(DOMAIN + "/" + window.location.href.split('?next=')[1].split('&')[0])
            }
        })
        .fail((response) => {
            response = get_response(response);
            if (response.errors.msg) {
                $(".errors").text(response.errors.msg);
            } else $(".errors").text("Неправильный логин или пароль");
            
        });

}



function buttons() { 
    $("#button-login").click((e) => {
        e.preventDefault();
        on_sublit_login();
    })
 }