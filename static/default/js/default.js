const DOMAIN = 'http://127.0.0.1:8000'
const ENDPOINT = 'http://127.0.0.1:8000/api/v1'
const AUTH_TYPE = 'Token'

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

function setCookie(name,value,days) {
  var expires = "";
  if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days*24*60*60*1000));
      expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function get_response(response) {
  let raw = response;
  try {
      response = $.parseJSON(response.responseText);
  } catch {
      response = raw;
  }
  return response;
}

function get_auth() {
    let token = getCookie("Token");
    
    let headers = token ? {"Authorization": `${AUTH_TYPE} ${token}`} : {}
    return headers;
}

