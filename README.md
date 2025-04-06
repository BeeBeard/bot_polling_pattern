# 🚀 Bot-Pattern

Этот проект — бот шаблон на python, с поддержкой miniapp

## 📂 Структура проекта

```
📦 bot-pattern
 ┣ 📂 app/                   # Основной код бота
 ┃ ┣ 📂 api/                 # API и эндпоинты
 ┃ ┃ ┣ 📜 bot_webhook.py     # Webhook длябота
 ┃ ┃ ┣ 📜 healthcheck.py     # Проверка API
 ┃ ┃ ┗ 📜 miniapp.py         # Эндпоинты miniapp
 ┃ ┣ 📂 bot/                 # Логика бота
 ┃ ┃ ┣ 📂 content/           # Текст, кнопки и команды для работы бота
 ┃ ┃ ┣ 📂 middleware/        # Middleware для обработки данных бота
 ┃ ┃ ┗ 📂 routers/           # Роутеры команд бота
 ┃ ┃   ┣ 📂 channel/         # Роутеры работающие в каналах
 ┃ ┃   ┣ 📂 group/           # Роутеры работающие в группах и супергруппах
 ┃ ┃   ┗ 📂 private/         # Роутеры в личных сообщениях с ботом
 ┃ ┣ 📂 assistant/           # Вспомогательные классы и утилиты
 ┃ ┣ 📂 frontend/            # Директория для хранения файлов miniapp
 ┃ ┃ ┣ 📂 static/            # Статические файлы
 ┃ ┃ ┃ ┣ 📂 js/              # Скрипты
 ┃ ┃ ┃ ┗ 📂 style/           # Стили 
 ┃ ┃ ┗ 📂 templates/         # HTML-шаблоны
 ┃ ┃   ┗ 📂 pages/           # Страницы
 ┃ ┣ 📂 conn/                # Подключение к БД
 ┃ ┃ ┣ 📜 engines.py         # Движки баз данных
 ┃ ┃ ┣ 📜 sql.py             # SQL-запросы
 ┃ ┃ ┗ 📜 tables.py          # Определение таблиц
 ┃ ┣ 📂 models/              # Модели данных
 ┃ ┗ 📜 config.py            # Конфигурационные параметры
 ┣ 📜 .env                   # Файл с переменными окружения
 ┣ 📜 .env-example           # Примен .env файла
 ┣ 📜 main.py                # Точка входа в приложение
 ┣ 📜 requirements.txt       # Зависимости проекта
 ┗ 📜 README.md              # Этот файл
```

## 🚀 Запуск проекта

### 0️⃣ Настройте BotFather

* Запустите @BotFather и пропишите /mybots
* Из списка выберите необходимый бот
* Выберите: Bot Settings -> Configure Mini App -> Edit Mini App URL
* Укажите URL из CONFIG.miniapp.path


### 1️⃣ Установите зависимости (локально)

```sh
pip install -r  requirements.txt
```

### 2️⃣ Создайте `.env` файл

Создайте `.env` в корневой папке и укажите все данные (пример ниже):

```
HOST_IP=0.0.0.0
HOST_PORT=8000

DB_HOST=db
DB_PORT=3306
DB_NAME=bot_db
DB_USER=bot_user
DB_PASSWORD=bot_password
```

### 3️⃣ Запуск в Docker

```sh
docker-compose up -d --build
```

⏳ Подождите, пока соберется образ.

После успешного запуска бот будет доступен на `http://localhost:8009` .

## 🛠 Использование команд Docker

📌 **Остановить контейнеры:**

```sh
docker-compose down
```

📌 **Пересобрать образы и запустить:**

```sh
docker-compose up -d --build
```

📌 **Логи сервиса бота:**

```sh
docker logs -f bot-server
```

📌 **Зайти в контейнер MySQL:**

```sh
docker exec -it mysql-db mysql -u bot_user -p
```

## 🔗 Подключение к MySQL

Если хотите подключиться к базе данных извне, используйте:

```
HOST: 127.0.0.1
PORT: 3306
USER: bot_user
PASSWORD: bot_password
DATABASE: bot_db
```

## 📝 TODO

- [ ] Добавить тесты
- [ ] Настроить CI/CD
- [ ] Улучшить логирование
