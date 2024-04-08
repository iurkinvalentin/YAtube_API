# api_final
api final
-информация об авторе:
 Юркин Валентин- студент Яндекс Практикума, факультета Бэкенд. Когорта 78
(https://github.com/iurkinvalentin)

# Название Проекта: API Yatube

Описание:

Проект "API Социальной Yatube" представляет собой backend часть сети, позволяющей пользователям публиковать личные дневники с текстовыми записями. Это API предоставляет возможность регистрации и аутентификации пользователей, публикации постов, комментирования, подписки на других пользователей и отслеживания их публикаций.

Польза проекта заключается в универсальности и масштабируемости: API поддерживает стандартные протоколы и может быть легко интегрирован в различные платформы. Кроме того, он поддерживает стандарты безопасности и аутентификации, гарантируя защиту личных данных пользователей.


Инструкция по разворачиванию:

1.Клонируйте репозиторий:

git clone https://github.com/yourusername/api_yatube.git
cd api_yatube

2.Установите виртуальное окружение и активируйте его:

python -m venv venv
source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`

3.Установите зависимости и выполните миграции:

pip install -r requirements.txt
python manage.py migrate

4.Запустите сервер:

python manage.py runserver

Примеры:

-Получение публикаций

GET /api/v1/posts/

Ответ:

http
Copy code
Status: 200 OK
Content-Type: application/json

{
    "id": 7,
    "author": "root",
    "text": "Создаем пост от лица другого пользователя",
    "pub_date": "2024-04-08T07:03:21.895212Z",        
    "image": null,
    "group": null
}


-Создание публикации

POST /api/v1/posts/

{
    "text": "Новый пост в блоге",
    "image": "string",
    "group": null
}

Ответ:

http
Copy code
Status: 201 Created

{
    "id": 1,
    "author": "string",
    "text": "Новый пост в блоге",
    "pub_date": "2019-08-24T14:15:22Z",
    "image": "string",
    "group": null
}
