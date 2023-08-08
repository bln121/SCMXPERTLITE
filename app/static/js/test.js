
//javascript code to verify either password and confirm password both are same or not

function checkPasswordMatch() {
    var password = document.getElementById("password"),
        confirm_password = document.getElementById("confirm_password");
    password.onchange = validatePassword;
    confirm_password.onkeyup = validatePassword;


}
function validatePassword() {
    if (password.value != confirm_password.value) {
        password_match_message.innerText = "Password and confirm password don't match";
    } else {
        password_match_message.innerText = "";
    }
}





//script code to see password

function myFunction() {
    var x = document.getElementById("password");
    var y = document.getElementById("password_hide1");
    var z = document.getElementById("password_hide2");

    if (x.type === 'password') {
        x.type = "text";
        y.style.display = "block";
        z.style.display = "none";
    }
    else {
        x.type = "password";
        y.style.display = "none";
        z.style.display = "block";

    }

}
//script code to see confirm password

function myFunction1() {
    var x = document.getElementById("confirm_password");
    var y = document.getElementById("confirm_password_hide1");
    var z = document.getElementById("confirm_password_hide2");

    if (x.type === 'password') {
        x.type = "text";
        y.style.display = "block";
        z.style.display = "none";
    }
    else {
        x.type = "password";
        y.style.display = "none";
        z.style.display = "block";

    }
}
//Script code to verify the password conditions-- >

function checkPasswordStrength() {
    var password = document.getElementById("password").value;

    var conditionsList = document.querySelector(".password-conditions"); // Select the conditions list element

    // Toggle the visibility of conditions based on the presence of input
    conditionsList.style.display = password.length > 0 ? "block" : "none";

    var lengthCondition = document.querySelector(".length-condition");
    var uppercaseCondition = document.querySelector(".uppercase-condition");
    var lowercaseCondition = document.querySelector(".lowercase-condition");
    var numberCondition = document.querySelector(".number-condition");

    lengthCondition.classList.toggle("valid", password.length >= 8);
    uppercaseCondition.classList.toggle("valid", /[A-Z]/.test(password));
    lowercaseCondition.classList.toggle("valid", /[a-z]/.test(password));
    numberCondition.classList.toggle("valid", /\d/.test(password));
}

