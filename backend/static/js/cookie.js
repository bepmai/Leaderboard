function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}
const domain = "http://localhost:5000"
// const domain = "https://secure-koi-wholly.ngrok-free.app"
// async function fetchUserData() {
//     const msv = getCookie('msv');
//     if (msv) {
//         console.log("MSV from cookie:", msv);
//     } else {
//         console.log("MSV not found in cookies");
//     }
// }
