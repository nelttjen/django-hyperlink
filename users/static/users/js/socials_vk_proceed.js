
function process_login() { 
    const url = new URL(window.location.href);
    let code = url.searchParams.get("code");
    let state = url.searchParams.get("state");
    let provider = 'vk';
    let redirect_to  = DOMAIN + '/users/login/socials/vk/process/';
    let redirect_after = DOMAIN + '/new/'

console.log(code);
console.log(state);

    if (!code || !state){
        $("#error").text("Что-то пошло не так. Попробуйте ещё раз.");
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
    });
}

$(document).ready(function () {
    process_login();
});