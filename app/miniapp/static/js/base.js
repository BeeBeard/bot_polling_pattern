function addInputField() {
    // Функция добавления полей при нажатии на button id="manage_event"

    inputs = document.querySelectorAll("input[name='userEmail']")
    let is_empty = true
    inputs.forEach((element) => {
        if (element.value && is_empty){} else { is_empty = false }

    });

    if (is_empty){
        const newInput = document.createElement("input");
        newInput.type = "email";
        newInput.placeholder = "Укажите email";
        newInput.name = "userEmail";
        document.getElementById("inputs-container").appendChild(newInput);
    }
}