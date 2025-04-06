function add_listener() {
    document.getElementById('testButton').addEventListener('onclick', function(event) {
        alert("Вы нажали на кнопку, скрипты отрабатывают")
        tg.close()
    }
}

window.onload = () => {
    add_listener()
}