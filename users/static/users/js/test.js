function on_submit(sender) {
    headers = {
        "Authorization": get_auth()['Authorization'],
        "Cookie": ''
    }
    console.log(get_auth());
    console.log(headers);
    $.ajax({
        type: "POST",
        url: `${ENDPOINT}/users/test/`,
        headers: get_auth(),
        data: {"test": "123"},
    });
}


function buttons() {
    $("#submit-btn").click(function (e) { 
        e.preventDefault();
        on_submit(e);
    });
}

$(document).ready(function () {
    buttons();
});