
function process_login() { 
    const url = new URL(window.location.href);
    let code = url.searchParams.get("code");
    let state = url.searchParams.get("state");
    let redirect_next = url.searchParams.get("next");
    let type = url.searchParams.get("link");
    let provider = 'vk';
    let redirect_to = undefined;
    let is_typed = false;
    if (redirect_next) {
        redirect_to = DOMAIN + `/users/login/socials/vk/process/?next=${redirect_next}`;
    } else if (type) {
        redirect_to = DOMAIN + `/users/login/socials/vk/process/?link=${type}`;
        is_typed = true;
    } else redirect_to = DOMAIN + '/users/login/socials/vk/process/';
    let redirect_after = redirect_next ? DOMAIN + redirect_next : DOMAIN + '/new/'

    if (!code || !state){
        $("#error").text("Что-то пошло не так. Попробуйте ещё раз.");
        $('#error').removeClass('succ');
        $('#error').addClass('err');
        return;
    }

    let endp, headers = undefined;

    if (!is_typed) {
        endp = `${ENDPOINT}/users/login/socials/`;
        headers = {};
    } else {
        endp = `${ENDPOINT}/users/link_socials/`;
        headers = get_auth();
    }

    $.ajax({
        type: "POST",
        url: endp,
        headers: headers,
        data: {code, state, provider, redirect_to},
    })
    .done((response) => {
        response = get_response(response);

        setCookie('token', response.content.token, 365);
        setCookie("user_id", response.content.profile.user.id, 365);
        
        if (!is_typed){
            window.location.replace(redirect_after);
        } else {
            window.location.replace(DOMAIN + '/users/profile/')
        }
        
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