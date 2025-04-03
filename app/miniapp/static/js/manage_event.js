function add_listener() {
    document.getElementById('eventForm').addEventListener('submit', function(event) {


        event.preventDefault(); // Отменяем стандартное поведение отправки формы
        let manage_type = document.getElementById('manage_event').value

        // Ищем user_id в запросе

        let location_href = new URL(window.location.href);
        let href_user_id = location_href.searchParams.get("user_id");
        let tg_user_id = null
        try { tg_user_id = tg.initDataUnsafe.user.id; // Переменная, которую нужно передать
        } catch {  }


        let user_id = href_user_id || tg_user_id

        console.log("Данные юзера в запросе", user_id)
        // Ищем user_id в запросе

        const jsonData = {
            "summary": document.getElementById("summary").value,
            "location": document.getElementById("location").value,
            "description": document.getElementById("description").value,
            "start": {
                "dateTime": document.getElementById("startDateTime").value + ":00+03:00",
                "timeZone": "Europe/Moscow"
            },
            "end": {
                "dateTime": document.getElementById("endDateTime").value + ":00+03:00",
                "timeZone": "Europe/Moscow"
                }
        }

         let recurrence = document.getElementById('recurrence');
         let recurrenceValue = recurrence.value;

         // Устанавливаем повторение событий если требуется
         console.log("Значение для повторения события:\n", recurrenceValue)
         if (recurrenceValue != "null") { jsonData["recurrence"] = new Array(recurrenceValue)}

         // Собираем emails
         let emails = new Array();
         let initiator = document.getElementById("initiatorEmail").value
         emails.push({email: initiator})
            try {

                inputs = document.querySelectorAll("input[name='userEmail']")
                inputs.forEach((element) => {  // Добавляем остальные emails
                    if (element.value) { emails.push({email: element.value}) }
                })
            } catch {}

        // Добавляем emails
        jsonData["initiator"] = initiator // Добавляем email инициатора
        jsonData["attendees"] = emails

        console.log("Данные передаваемые в API:\n", jsonData)

        let submit_button = document.getElementById("manage_event")
        let path = 'create_event?user_id=' + user_id
        if (submit_button.value != "None") {
            path = 'edit_event?user_id=' + user_id + '&event_id=' + submit_button.value
        }

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
//                tg.close()
            }
        ).catch(error => {
            console.error('Ошибка:', error);
        });
    });
}

window.onload = () => {
    add_listener()
    let submit_button = document.getElementById("manage_event")
    console.log("ТИП СОБЫТИЯ", submit_button.value)
    if (submit_button.value != "None") {
        submit_button.textContent = "Изменить событие"
    }
}

//window.addEventListener("load", () => {
//
//    const starTime = new Date();
//	// Добавление 30 минут (в миллисекундах)
//	const thirtyMinutesInMs = 30 * 60 * 1000; // 30 минут × 60 секунд × 1000 мс/секунду
//
//	// Новая дата — текущее время + 30 минут
//	const endTime = new Date(starTime.getTime() + thirtyMinutesInMs);
//
//    // Преобразуем дату в ISO формат (например, '2023-10-05T12:34')
//    const isoStartTime = starTime.toISOString().slice(0, 16);
//    const isoEndTime = endTime.toISOString().slice(0, 16);
//
//    // Устанавливаем значение input
//    document.getElementById('startDateTime').value = isoStartTime;
//    document.getElementById('endDateTime').value = isoEndTime;
//});


