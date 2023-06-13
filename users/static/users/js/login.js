const CSRF = getCookie('csrftoken');

$(document).ready(function () {
    buttons();
});

function processLogin(response) {
    response = get_response(response);
    setCookie("token", response.content.token, 365);
    setCookie("user_id", response.content.profile.user.id, 365);
    $(".done-msg").text("Авторизация успешна");
    $(".errors").text("");
}

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
            processLogin(response)

            if (window.location.href.indexOf('?next=') != -1) {
                window.location.replace(DOMAIN + "/" + window.location.href.split('?next=')[1].split('&')[0])
            } else {
                new Promise(resolve => setTimeout(resolve, 1500))
                window.location.replace(DOMAIN + '/users/profile/')
            }
        })
        .fail((response) => {
            response = get_response(response);
            if (response.errors.msg) {
                $(".errors").text(response.errors.msg);
            } else $(".errors").text("Неправильный логин или пароль");
            
        });

}
function onTelegramAuth(user) {
    $.ajax({
        type: "POST",
        url: `${ENDPOINT}/users/login/socials/`,
        data: {tgdata: JSON.stringify(user), provider: 'tg'},
    }
    ).done((r) => {
        processLogin(r);
        window.close();
    }).fail((r) => {
        r = get_response(r);
        alert(r.errors.msg);
        window.close();
    });

  }


function buttons() { 
    $("#button-login").click((e) => {
        e.preventDefault();
        on_sublit_login();
    })
 }