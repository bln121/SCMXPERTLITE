// Script code to hide and display eye icons
function myFunction() {
    var x = document.getElementById("new_password");
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
    var password = document.getElementById("new_password").value;

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

