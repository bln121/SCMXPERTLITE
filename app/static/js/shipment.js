//Script code for extending the menu bar


// Script to return delivery date -->

function del(inputfield) {
    document.getElementById("delivery-date")
    // Get the current date
    var currentDate = new Date();
    // Add 7 days to the current date
    var deliveryDate = new Date();
    deliveryDate.setDate(currentDate.getDate() + 7);
    var formattedDeliveryDate = ("0" + deliveryDate.getDate()).slice(-2) + "-" + ("0" + (deliveryDate.getMonth() + 1)).slice(-2) + "-" + deliveryDate.getFullYear();
    inputfield.value = formattedDeliveryDate;
}

function clearForm() {
    // Get the form element
    var form = document.getElementById("myForm");

    // Reset the form fields
    form.reset();
}

