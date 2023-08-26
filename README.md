# **Клуб любителей рецептов**


![img.png](/data/img.png)

### Оглавление
<ol>
 <li><a href="#description">Описание проекта</a></li>
 <li><a href="#stack">Используемые технологии</a></li>
 <li><a href="#architecture">Архитектура проекта</a></li>
 <li><a href="#docker">Как запустить проект в Docker?</a></li>
 <li><a href="#start_project">Как развернуть API локально?</a></li>
 <li><a href="#load_data">Заполнение базы начальными данными</a></li>
 <li><a href="#workflow">Workflow</a></li>
 <li><a href="#author">Авторы проекта</a></li>
</ol>


---
### Описание проекта:<a name="description"></a>
Сайт предназначен для публикации свои любимых рецептов, подписок на интересных
авторов. Есть возможность добавлять рецепты в избранные и свой список продуктов,
который можно скачать сводных списком

---
### **Используемые технологии**<a name="stack"></a>
![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

---

### Архитектура проекта<a name="architecture"></a>

| Директория    | Описание                                                 |
|---------------|----------------------------------------------------------|
| `docs`        | Содержит схему архитектуры проекта в разных расширениях  |
| `infra`       | Файлы для запуска с помощью Docker, настройки Nginx      |
| `backend`     | Код Django приложения                                    |
| `frontend`    | Код приложения на React                                  |

---
### Как запустить проект в Docker?<a name="docker"></a>
* Запустите терминал и клонируйте репозиторий 
    ```
    git clone https://github.com/FakaFakaYeah/recipes_club.git
    ```

* Установите Docker по ссылке https://www.docker.com/products/docker-desktop

* Перейдите в директорию с Docker-compose.yaml
    ```
    cd infra
    ```

* Создайте .env файл и заполните его

  Шаблон наполнения env файла
    ```
  USE_POSTGRESQL=True  # Установите True, чтобы в докере использовалась PostgreSQL
  SECRET_KEY=   #укажите свой SECRET_KEY
  DB_ENGINE=django.db.backends.postgresql  #указываем, что работаем с postgresql
  DB_NAME=    #имя базы данных
  POSTGRES_USER=  #логин для подключения к базе данных
  POSTGRES_PASSWORD=   #пароль для подключения к БД (установите свой)
  DB_HOST=    #название сервиса (контейнера)
  DB_PORT=    #порт для подключения к БД
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
  
* Выполните сбор статики проекта по следующей команде:
    ```
    docker-compose exec web python manage.py collectstatic --no-input
    ```

* Cоздайте суперпользователя
  ```
  docker-compose exec web python manage.py createsuperuser
  ```
  укажите имя пользователя, почту и пароль

* Проект будет доступен по следующим адресам:
  ```
  http://localhost/recipes/ - главная страница сайта
  http://localhost/admin/ - админ зона
  ```
  
___
### Как развернуть API локально?<a name="start_project"></a>

* Запустите терминал и клонируйте репозиторий 
    ```
    git clone https://github.com/FakaFakaYeah/recipes_club.git
    ```
* Создайте и активируйте виртуальное окружение

  Если у вас Linux/macOS

  ```
  python3 -m venv venv
  source venv/bin/activate
  ```
  
  Если у вас windows

  ```
  python -m venv venv
  source venv/scripts/activate
  ```
  
* Установите зависимости из файла requirements.txt:

  ```
  pip install -r requirements.txt
  ```

* Перейдите в директорию с файлами проекта
  ```
  cd backend
  ```

* Выполните миграции по следующей команде:
  ```
  python manage.py migrate
  ```

* Создайте суперпользователя
  ```
  python manage.py createsuperuser
  ```
  укажите имя пользователя, почту и пароль
  
* Запустите проект
  ```
  python manage.py runserver
  ```
  
* API будет доступно по следующим адресам:
  ```
  http://127.0.0.1:8000/redoc/ - документация со всеми эндпоинтами
  http://127.0.0.1:8000/admin/ - админ зона
  ```

* API запросы можно протестировать через приложение Postman, которое можно скачать по ссылке: https://www.postman.com/downloads/

---
### Заполнение базы начальными данными<a name="load_data"></a>


Для заполнения базы этими данными выполните следующие команды в терминале:

* Если проект развернут в Docker
    ```
    docker-compose exec web python manage.py load_ingredients
    ```
* Если проект развернут локально
    ```
    cd backend
    python manage.py load_ingredients
    ```

---
### Workflow<a name="workflow"></a>

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
---

### Авторы проекта:<a name="author"></a>
Смирнов Степан
<div>
  <a href="https://github.com/FakaFakaYeah">
    <img src="https://github.com/FakaFakaYeah/FakaFakaYeah/blob/main/files/images/GitHub.png" title="GitHub" alt="Github" width="39" height="39"/>&nbsp
  </a>
  <a href="https://t.me/s_smirnov_work" target="_blank">
      <img src="https://github.com/FakaFakaYeah/FakaFakaYeah/blob/main/files/images/telegram.png" title="Telegram" alt="Telegram" width="40" height="40"/>&nbsp
  </a>
</div>
