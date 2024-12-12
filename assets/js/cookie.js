function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

// async function fetchUserData() {
//     const msv = getCookie('msv');
//     if (msv) {
//         console.log("MSV from cookie:", msv);
//     } else {
//         console.log("MSV not found in cookies");
//     }
// }
