if(getCookie('token')==null){
    window.location.href="/"
}
const userattend = document.getElementById("attendance-user")
const adminattend = document.getElementById("attendance-admin")
const stated = document.getElementById("stated-user")
const tongquan = document.getElementById("tongquan")

if(getCookie('role')=="admin"){ 
}
else{
    adminattend.classList.add("hidden")
    stated.classList.add("hidden")
    tongquan.classList.add("hidden")
}

const msv = document.getElementById("student-id");
const name_ = document.getElementById("fullname");
const lastname = document.getElementById("lastname");
const email = document.getElementById("email");
const class_= document.getElementById("class");
const class_year = document.getElementById("class-year");
const class_department = document.getElementById("class-department");
const major = document.getElementById("major")
const gpa = document.getElementById("gpa");
const gender = document.getElementById("gender");
const phone = document.getElementById("phone");
const birthday = document.getElementById("birthday");
const address = document.getElementById("address");

const getDataInfor =async ()=>{
    try{
        const response = await fetch(`${domain}/api/infor/getInfor`,{
            headers:{
                "Authorization":getCookie("token")
            },
            method:"GET"
        })
        const data = await response.json();
        msv.value = data.data.MSV;
        class_.value = data.data.class;
        class_year.value = data.data.courseyear;
        class_department.value = data.data.department;
        major.value = data.data.speciality;
        gpa.value = data.data.gpa;
        phone.value = data.data.phoneNumber;
        gender.value = data.data.gender;
        address.value = data.data.address;
        let dateParts = data.data.dateOfBirth.split('/');
        let formattedDate = `${dateParts[2]}-${dateParts[1]}-${dateParts[0]}`;
        birthday.value = formattedDate;
        name_.innerHTML = data.data.fullname;
        email.innerHTML = data.data.email;
        let listname = data.data.fullname.split(" ");
        lastname.innerHTML = listname[listname.length-1];
    }
    catch(error){
        console.log(error)
    }
}
getDataInfor()