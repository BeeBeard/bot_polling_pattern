function add_listener() {
    document.getElementById('eventForm').addEventListener('submit', function(event) {

        event.preventDefault(); // Отменяем стандартное поведение отправки формы

         // Собираем emails
         let emails = new Array();
            try {

                inputs = document.querySelectorAll("input[name='userEmail']")
                inputs.forEach((element) => {  // Добавляем остальные emails
                    if (element.value) { emails.push({email: element.value}) }
                })
            } catch {}

        // Добавляем emails
        const jsonData = {}
        jsonData["attendees"] = emails

        console.log("Данные передаваемые в API:\n", jsonData)

        let submit_button = document.getElementById("manage_event")
        let path = 'edit_event?flag=add&event_id=' + submit_button.value


        fetch(
            '/calendar/google/' + path, {
                method: 'POST',
                body: JSON.stringify(jsonData),
                headers: {"Content-type": "application/json; charset=UTF-8"}
            }
        ).then(
            response => response.json()
        ).then(
            data => {
                alert('Событие успешно создано/изменено');
                console.log('Ответ бот-сервера:', data);
                tg.close()
            }
        ).catch(error => {
            console.error('Ошибка:', error);
        });
    });
}

window.onload = () => {
    add_listener()

}




