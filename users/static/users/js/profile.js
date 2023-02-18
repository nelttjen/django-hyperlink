let vk_action_link = `<a href="/users/login/socials/?provider=vk&link=1" class="btn btn-primary">Привязать</a>`

function onload() {
    let user_id = getCookie('user_id');
    if (!user_id) {
        window.location.replace(`${DOMAIN}/users/logout/`);
    }

    $.ajax({
        method: "GET",
        url: `${ENDPOINT}/users/${user_id}/`,
        headers: get_auth()
    }).done((response) => {
        response = get_response(response);
        let social_btn, rewards;

        if (response.content.vk_id) {
            social_btn = `<span id="social-vk-action"><button id="social-remove-vk" class="btn btn-primary">Удалить привязку</button></span>`
        } else {

            social_btn = '<span id="social-vk-action">`<a href="/users/login/socials/?provider=vk&link=1" class="btn btn-primary">Привязать</a>`</span>'
        }
        if (response.content.rewards.length > 0){
            rewards = `<div class="reward">rewards here</div>`
        } else {
            rewards = `<p>Награды пока не получены :(</p>`
        }

        let card = `
        <div class="line" style="display: inline" ">
            <img src="${response.content.avatar}" alt="avatar" width="128" height="128" id="avatar-display">
            <input type="file" id="avatar-upload">
            <button id="avatar-save" class="btn btn-primary">Обновить аватар</button>
        </div>
        <br>
        <label for="dipslay-name">Отображаемое имя</label>
        <input class="form-control" id="dipslay-name" type="text" value="${response.content.display_name}">
        <br>
        <label for="title">Заголовок профиля</label>
        <input class="form-control" type="text" id="title" value="${response.content.title}">
        <br>
        <label for="bio">Обо мне</label>
        <textarea class="form-control" type="text" id="bio">${response.content.bio}</textarea>
        <br>
        <label for="email">Email</label>
        <input class="form-control" type="email" id="email" value="${response.content.user.email}">
        <br>
        <button id="save-profile" class="btn btn-primary">Сохранить</button>
        <br><br>
        <div class="socials">
            <div class="social" style="border: 1px solid blue; padding: 5px">
                <p>Vk id: <span id="vk-id">${response.content.vk_id}</span></p>
                ${social_btn}
            </div>
        </div>
        
        <br><br><br>
        
        <div class="stats">
            <h3>Стата</h3>
            <p>Всего переадресаций: <span>${response.content.total_redirects}</span></p>
            <p>Переадресаций по вашим ссылкам: <span>${response.content.total_redirected}</span></p>
            <p>Всего переадресаций за день: <span>${response.content.daily_redirects}</span></p>
            <p>Переадресаций по вашим ссылкам за день: <span>${response.content.daily_redirected}</span></p>
        </div>
        <br>
        <div class="rewards">
            <h3>Награды</h3>
            ${rewards}
        </div>
        
        <br>
        
        <div class="change_pass mt5" style="padding: 5px; border: 1px solid orange">
        <h3>Смена пароля</h3>
        <input class="form-control mb-2" type="password" id="old_pass" placeholder="Старый пароль">
        <input class="form-control mb-2" type="password" id="new_pass" placeholder="Новый пароль">
        <input class="form-control mb-2" type="password" id="new_pass2" placeholder="Ещё раз">
        <button class="btn btn-primary" id="pass-save">Обновить пароль</button>
        <style>p.err{color: red;} p.succ{color: green;}</style>
        <p class="err" id="pass-info"></p>
        </div>
        `

        $('.profile-card').html(card)
        buttons();
    }).fail((response) => {
        response = get_response(response);

        alert(response.errors.msg);
    })
}

function save_file() {
    let file_inp = $("#avatar-upload").prop("files")[0];
    if (file_inp && (file_inp.name.endsWith("png") || file_inp.name.endsWith("jpg") || file_inp.name.endsWith("jpeg"))) {
        var reader = new FileReader();
        reader.readAsDataURL(file_inp);
        reader.onload = function () {
        let b64 = reader.result;
        let user_id = getCookie('user_id');
        $.ajax({
            method: 'PUT',
            url: `${ENDPOINT}/users/${user_id}/`,
            data: {avatar: b64}
        }).done((response) => {
            response = get_response(response);
            $('#avatar-display').attr('src', response.content.avatar);
        }).fail((response) => {
            response = get_response(response);

            alert(response.errors);
        })
        };
    } else {
        alert('File must be png, jpg or jpeg');
    }
}

function change_pass() {
    let old_password = $("#old_pass").val();
    let new_password = $("#new_pass").val();
    let new_password2 = $("#new_pass2").val();
    let user_id = getCookie('user_id');
    if (old_password && new_password && new_password2) {
        $.ajax({
            method: 'PUT',
            data: {old_password, new_password, new_password2},
            headers: get_auth(),
            url: `${ENDPOINT}/users/${user_id}/`
        }).done((response) => {
            response = get_response(response);
            $("#old_pass").val('');
            $("#new_pass").val('');
            $("#new_pass2").val('');

            alert('Пароль изменен');
        }).fail((response) => {
            response = get_response(response);
            alert(response.errors.msg);
        })
    }
}

function save_profile() {
    let display_name = $('#dipslay-name').val();
    let title = $('#title').val();
    let bio = $('#bio').val();
    let email = $('#email').val();
    let user_id = getCookie('user_id');

    $.ajax({
        method: 'PUT',
        data: {display_name, title, bio, email},
        headers: get_auth(),
        url: `${ENDPOINT}/users/${user_id}/`
    }).done((response) => {
       response = get_response(response)

       alert('Профиль изменен');
    }).fail((response) => {
        response = get_response(response);

        alert(response.errors.msg);
    });
}

function buttons() {
    $('#social-remove-vk').click((e) => {
        e.preventDefault();
        remove_vk();
    });
    $('#avatar-save').click((e) => {
        e.preventDefault();
        save_file();
    });
    $('#pass-save').click((e) => {
        e.preventDefault();
        change_pass();
    });
    $('#save-profile').click((e) => {
        e.preventDefault();
        save_profile();
    });
}

function remove_vk() {

    $.ajax({
        method: 'DELETE',
        url: `${ENDPOINT}/users/link_socials/`,
        headers: get_auth(),
        data: {"provider": "vk"}
    }).done((response) => {
        $("#vk-id").text('null');

        $('#social-vk-action').html(vk_action_link);
    })
}

$(document).ready(function () {
    onload();
});