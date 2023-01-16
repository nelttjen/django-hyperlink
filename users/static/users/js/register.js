function register_submit(sender) { 
    let username = $('#username-input').val();
    let email = $('#email-input').val();
    let password = $('#pass1-input').val();
    let password2 = $('#pass2-input').val();
    if (email.indexOf("@") == -1) {
        $(".error").text("Неверный формат Email адреса");
        return
    } else if (email.indexOf(".") == -1) {
        $(".error").text("Неверный формат Email адреса");
        return
    }
    $.ajax({
        type: "POST",
        url: `${ENDPOINT}/users/register/`,
        data: {
            "username": username,
            "email": email,
            "password": password,
            "password_again": password2
        },
        
    })
    .done((response) => {
        response = get_response(response);
        let msg = response.msg;
        let link = response.extra.link;
        window.location.replace(link + "?info=" + msg);
    })
    .fail((response) => {
        response = get_response(response);
        $(".error").text(response.msg);
    });
}   


function buttons() {
    $("#submit-btn").click(function (e) { 
        e.preventDefault();
        register_submit(e);
    });
}

$(document).ready(function () {
    buttons();
});