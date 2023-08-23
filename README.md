# **Клуб любителей рецептов**

![](https://github.com/FakaFakaYeah/recipes_club/actions/workflows/foodgram_main.yml/badge.svg)

![img.png](/data/img.png)



### Описание проекта:
Сайт предназначен для публикации свои любимых рецептов, подписок на интересных
авторов. Есть возможность добавлять рецепты в избранные и свой список продуктов,
который можно скачать сводных списком

Проект доступен по адресам:

http://recipesgram.ddns.net/recipes/

http://81.163.31.244/recipes/  


### Данные для авторизации в админ-зоне и на сайте:

```
email: test@test.ru
пароль: 1029384756
```

### **Используемые технологии**
![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

### Архитектура проекта<a name="architecture"></a>

| Директория    | Описание                                                 |
|---------------|----------------------------------------------------------|
| `docs`        | Содержит схему архитектуры проекта в разных расширениях  |
| `infra`       | Файлы для запуска с помощью Docker, настройки Nginx      |
| `backend`     | Код Django приложения                                    |
| `frontend`    | Код приложения на React                                  |

### **Как развернуть проект локально?**
* Запустите терминал и клонируйте репозиторий 
    ```
    git clone https://github.com/FakaFakaYeah/foodgram-project-react/
    ```

* Установите Docker по ссылке https://www.docker.com/products/docker-desktop

* Перейдите в директорию с Docker-compose.yaml
    ```
    cd infra
    ```

* Создайте .env файл и заполните его

  Шаблон наполнения env файла
    ```
    DB_ENGINE=django.db.backends.postgresql   указываем, что работаем с postgresql
    DB_NAME=   имя базы данных
    POSTGRES_USER=   логин для подключения к базе данных
    POSTGRES_PASSWORD=   пароль для подключения к БД (установите свой)
    DB_HOST=db   название сервиса (контейнера)
    DB_PORT=  порт для подключения к БД
    ```

* Выполните команду по разворачиванию docker-compose
    ```
    docker-compose up -d
    ```

  Будет проведена сборка образа по Dockerfile и запуск проекта в четырех контейнерах

* Выполните миграции по следующей команде:
    ```
    docker-compose exec backend python manage.py migrate
    ```

### Создание суперпользователя
По следующей команде вы можете создать суперпользователя, если вам нужен доступ в админ зону
```
docker-compose exec backend python manage.py createsuperuser
```
Потребуется ввести имя пользователя, почту и пароль

После успешного создания суперпользователя и ввода логин/пароль на страницу http://127.0.0.1/admin/ 

### Заполнение базы начальными ингредиентами

Ингредиенты хранятся в файле ingredients.json.
Для заполнения базы этими данными выполните следующую команду менеджера из директории с manage.py:
```
docker-compose exec backend python manage.py load_ingredients
```
После этого загрузятся начальные данные

API запросы можно протестировать через приложение Postman, которое можно скачать по ссылке: https://www.postman.com/downloads/

### Workflow

В проекте есть готовый шаблон workflow, в котором есть тесты по PEP8, пуш образов
бэкенда и фронтеда на DockerHub, деплой на боевой сервер и информирование в telegram и discord.

В workflow используются следующие константы:

```
DB_ENGINE = "django.db.backends.postgresql"

DB_NAME = "имя базы данных postgres"

DB_USER = "пользователь бд"

DB_PASSWORD = "пароль"

DB_HOST = "db"

DB_PORT = "5432"

DOCKER_PASSWORD=<пароль от DockerHub>

DOCKER_USERNAME=<имя пользователя>

USER=<username для подключения к серверу>

HOST=<IP сервера>

PASSPHRASE=<пароль для сервера, если он установлен>

SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>(Копировать полностью)

TELEGRAM_TO=<id чата, куда должны приходить уведомления>

TELEGRAM_TOKEN<= токен вашего бота-информатора в телеграмме>

DISCORD_WEBHOOK<= Вебхук из чата в Discord, для резервного информировани>
```


Проект выполнил: Смирнов Степан
<div>
  <a href="https://github.com/FakaFakaYeah">
    <img src="https://github.com/FakaFakaYeah/FakaFakaYeah/blob/main/files/images/GitHub.png" title="GitHub" alt="Github" width="39" height="39"/>&nbsp
  </a>
  <a href="https://t.me/s_smirnov_work" target="_blank">
      <img src="https://github.com/FakaFakaYeah/FakaFakaYeah/blob/main/files/images/telegram.png" title="Telegram" alt="Telegram" width="40" height="40"/>&nbsp
  </a>
</div>
