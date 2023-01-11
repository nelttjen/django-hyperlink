const RECOVERY_HTML = `
<label for="code-input">Код восстановления</label>
<input type="text" placeholder="Код" id="code-input" class="form-control" value="">
<label for="pass1-input">Новый пароль</label>
<input type="password" placeholder="Новый пароль" id="pass1-input" class="form-control">
<label for="pass2-input">Повторите пароль</label>
<input type="password" placeholder="Повторите пароль" id="pass2-input" class="form-control">
<button id="password-submit" class="btn btn-primary">Подтвердить</button>
`;

function set_error(response) {
    let validation_p = $("#validation_msg")
    response = get_response(response);
    validation_p.removeClass("validation_succ");
    validation_p.addClass("validation_error");
    validation_p.text(response.msg);
    return response;
}

function set_success(response) {
    let validation_p = $("#validation_msg")
    response = get_response(response);
    validation_p.removeClass("validation_error");
    validation_p.addClass("validation_succ");
    validation_p.text(response.msg);
    return response;
}

function on_usr_submit(sender) {
    let username = $("#username-input").val();
    let data = {};
    if (username.indexOf("@") > -1){
        data = {"email": username};
    } else data = {"username": username};
    $.ajax({
        type: "POST",
        url: `${ENDPOINT}/users/recovery/`,
        data: data,
    })
    .done((response) => {
        set_success(response);
        $('.input_block').html(RECOVERY_HTML);
        $("#password-submit").click(function (e) { 
            e.preventDefault();
            on_code_submit(e);
        });
    })
    .fail((response) => {
        set_error(response);
    });
}

function on_code_submit(sender) {
    let code = $("#code-input").val();
    let pass1 = $("#pass1-input").val();
    let pass2 = $("#pass2-input").val();
    $.ajax({
        type: "PUT",
        url: `${ENDPOINT}/users/recovery/`,
        data: {
            "code": code,
            "password": pass1,
            "password_again": pass2
        },
    })
    .done((response) => {
        response = get_response(response);
        let link = response.content.link;
        let message = response.msg;
        window.location.replace(link + "?message=" + message)
    })
    .fail((response) => {
        set_error(response);
    });
}


function buttons() {
    $("#username-submit").click(function (e) { 
        e.preventDefault();
        on_usr_submit(e);
    });
    $("#password-submit").click(function (e) { 
        e.preventDefault();
        on_code_submit(e);
    });
}


$(document).ready(function () {
    buttons();
});