const token = getCookie('Token');
let timer = undefined;
let link = undefined;
let code = undefined;

function createTimer() { 
    $("h1#main-info").removeAttr('style');
    $('#timer').text(timer);
    setInterval(redirectTimer, 1000);
}

function redirectTimer() {
    timer -= 1;
    $('#timer').text(timer);
    if (timer === 0) {
        makeRedirect();
    }
}

function makeRedirect() {
    $("h1#main-info").text('Перенаправление...');
    $.ajax({
        type: "POST",
        url: `${ENDPOINT}/links/${code}/`,
        headers: token ? get_auth() : {}
    });

    clearInterval(redirectTimer);
    window.location.replace(link);
}

$(document).ready(function () {
    code = $('#code').val();

    $.ajax({
        type: "GET",
        url: `${ENDPOINT}/links/${code}/`,
    })
    .done((response) => {
        response = get_response(response);
        
        link = response.content.redirect_to;
        timer = response.content.redirect_timer;
        
        timer === 0 ? makeRedirect() : createTimer()
    })
    .fail((response) => {
        response = get_response(response);
        let elem = $("h1#main-info")
        elem.removeAttr('style');
        elem.text(response.errors.msg)
    });
});