$(document).ready(function () {
    function getCookie(cname) {
        let name = cname + "=";
        let decodedCookie = decodeURIComponent(document.cookie);
        let ca = decodedCookie.split(';');
        for(let i = 0; i <ca.length; i++) {
          let c = ca[i];
          while (c.charAt(0) == ' ') {
            c = c.substring(1);
          }
          if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
          }
        }
        return "";
      }


    let CSRF = getCookie('csrftoken');
    $("#button-login").click((e) => {
        e.preventDefault();
        let nick = $('#username').val()
        let pass = $('#password').val()
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/api/login/",
            data: {
                "username": nick,
                "password": pass,
            },
            dataType: "application/json",
            success: function (response) {
                console.log(response);
            }
        });
    })
});