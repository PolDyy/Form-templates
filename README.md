# Form-templates
Парсинг данных из xlsx в БД

## Запуск с помощью docker-compose

1) Создаем директорию для проекта и переходим в него  

2) Клонируем репозиторий с github:  

    `git init`  

    `git clone https://github.com/PolDyy/Space-agency.gi)`

3) Создаем файл .env на основе env_example

4)  Проверяем установлен ли докер, если нет, то устанавливаем его  
(обратитесь к документации Docker)

5) Использовать команду.

  `docker compose up -d --build`

6) запускаем файл main.js

## Обратите внимание   

Данные БД должны храниться в файле .env  

Данные для входа в pgadmin  

логин:admin@admin.com  
пароль:1234  

Для их изменения переопределите переменные в docker-compose.yaml
