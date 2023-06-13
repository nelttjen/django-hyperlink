function onTelegramAuth(user) {
    console.log('succ')
    let headers = get_auth()
    $.ajax({
        type: "POST",
        url: `${ENDPOINT}/users/link_socials/`,
        headers: headers,
        data: {tgdata: JSON.stringify(user), provider: 'tg'},
    }
    ).done((r) => {
        window.close()
    }).fail((r) => {
        r = get_response(r)
        alert(r.errors.msg)
        window.close()
    })
}