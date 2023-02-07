function on_submit(sender) {
    let value = $("#code_input").val();
    $.ajax({
        type: "POST",
        url: `${ENDPOINT}/users/activate/`,
        data: {"code": value},
    })
    .done((response) => {
        response = get_response(response);
        
        let link = response.content.redirect;
        let text = response.content.redirect_msg;
        window.location.replace(link + `?message=${text}`);
    })
    .fail((response) => {
        response = get_response(response);
        $('.status').text(response.errors.msg);
    });
}

function buttons() {
    $("#submit_btn").click(function (e) { 
        e.preventDefault();
        on_submit(e);
    });
}

$(document).ready(function () {
    buttons();
});