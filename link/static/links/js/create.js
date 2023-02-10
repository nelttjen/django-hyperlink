let created = false;
let link = undefined;

function on_submit(sender) {
    if (created) return;
    let auth = get_auth();

    let redirect_to = $('#id_redirect_to').val();
    let valid_until = $('#id_valid_until').val();
    let json_data = {'redirect_to': redirect_to, 'valid_until' : valid_until};

    if (auth != {}){
        let redirect_timer = $('#id_redirect_timer').val();
        let allowed_redirects = $('#id_allowed_redirects').val();
        let only_unique_redirects = $('#id_only_unique_redirects').is(':checked'); 
        let is_active = true;
        let is_active_elem = $('#id_is_active')
        if (is_active_elem.length){
            is_active = is_active_elem.is(':checked')
        }
        console.log(is_active);
        json_data = {'redirect_to': redirect_to, 
        'valid_until': valid_until, 'redirect_timer': redirect_timer, 
        'allowed_redirects': allowed_redirects, 'only_unique_redirects': only_unique_redirects, 'is_active': is_active};
    }

    $.ajax({
        type: "POST",
        url: `${ENDPOINT}/links/create/`,
        data: json_data,
        headers: auth,
    })
    .done((response) => {
        response = get_response(response);

        let elem = $("#info");
        elem.removeClass('info-error');
        elem.addClass('info-succ');
        

        link = window.location.href.replace("/new/", "");
        link = `${link}/${response.content.share_code}`;

        elem.html(`Ваша ссылка готова: <a href="${link}">${link}</a> <button class="btn btn-primary" id="btn-copy">Скопировать</button>`);
        
        created = true;
        buttons();

    })
    .fail((response) => {
        response = get_response(response);

        let elem = $("#info");
            elem.removeClass('info-succ');
            elem.addClass('info-error');

        let msg = response.errors.msg;
        if (msg != 'extended') {
            elem.text(msg);
        } else {
            elem.text('12');
        }
    })
    ;
}

function copy(e) {
    navigator.clipboard.writeText(link).then(function () {
        let elem = $("#btn-copy");
        elem.text('Скопировано!');
        elem.attr('disabled', true);
        elem.removeClass('btn-primary');
        elem.addClass('btn-success');
    }, function () {
        let elem = $("#btn-copy");
        elem.text('Ошибка при копировании');
        elem.removeClass('btn-primary');
        elem.addClass('btn-danger');
    });
}

function buttons() {
    $("#btn-save").click(function (e) { 
        e.preventDefault();
        on_submit(e);
    });
    
    $("#btn-copy").click(function (e) { 
        e.preventDefault();
        copy(e);
    });
}

$(document).ready(function () {
    buttons();
});