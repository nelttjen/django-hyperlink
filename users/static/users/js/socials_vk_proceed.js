
function process_login() { 
    const url = new URL(window.location.href);
    let code = url.searchParams.get("code");
    let state = url.searchParams.get("state");
    let provider = 'vk';
    let redirect_to  = DOMAIN + '/users/login/socials/vk/process/';
    let redirect_after = DOMAIN + '/new/'

    if (!code || !state){
        $("#error").text("Что-то пошло не так. Попробуйте ещё раз.");
        $('#error').removeClass('succ');
        $('#error').addClass('err');
        return;
    }

    $.ajax({
        type: "POST",
        url: `${ENDPOINT}/users/login/socials/`,
        data: {code, state, provider, redirect_to},
    })
    .done((response) => {
        response = get_response(response);

        setCookie('token', response.content.token, 365);
        window.location.replace(redirect_after);
    })
    .fail((response) => {
        response = get_response(response);

        $("#error").text(response.errors.msg);
        $('#error').removeClass('succ');
        $('#error').addClass('err');
    });
}

$(document).ready(function () {
    process_login();
});