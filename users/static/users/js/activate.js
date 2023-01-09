function on_submit(sender) {
    let value = $("#code_input").val();
    $.ajax({
        type: "POST",
        url: `${ENDPOINT}/users/activate/`,
        data: {"code": value},
    })
    .done((response) => {
        let raw = response;
        try {
            response = $.parseJSON(response.responseText);
        } catch {
            response = raw;
        }
        
        let link = response.content.redirect;
        let text = response.content.redirect_msg;
        window.location.replace(link + `?message=${text}`);
    })
    .fail((response) => {
        response = $.parseJSON(response.responseText);
        $('.status').text(response.msg);
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