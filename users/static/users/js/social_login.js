const providers = ["vk", ]

// https://oauth.vk.com/authorize?client_id=51547215&redirect_uri=http://127.0.0.1:8000/users/login/socials/vk/process/&scope=email&response_type=code&state=test

function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

function reidrect_to_auth() { 
    const url = new URL(window.location.href);
    let provider = url.searchParams.get("provider");
    let redirect_next = url.searchParams.get("next");
    if (providers.indexOf(provider) == -1) {
        $("#error").text('Неизвестный тип авторизации');
        return;
    }

    if (provider == "vk"){
        let app_id = VK_APP_ID;
        let state = makeid(20);
        let link = `https://oauth.vk.com/authorize?client_id=${app_id}&redirect_uri=http://127.0.0.1:8000/users/login/socials/vk/process/&scope=email&response_type=code&state=${state}`;
        if (redirect_next) {
            link = `https://oauth.vk.com/authorize?client_id=${app_id}&redirect_uri=http://127.0.0.1:8000/users/login/socials/vk/process/?next=${redirect_next}&scope=email&response_type=code&state=${state}`
        }

        $.ajax({
            type: "PUT",
            url: `${ENDPOINT}/users/login/socials/`,
            data: {state},
        });
        window.location.replace(link);
    }
}

$(document).ready(function () {
    reidrect_to_auth();
});
