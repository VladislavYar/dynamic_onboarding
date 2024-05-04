<div align="center">
  <h1>dynamic_onboarding_nomia</h1>
  <h3>Описание</h3>
  <p>Сервис динамического формирования онбординга, сбора статистики и вывода её через RestAPI.</p>
  <hr>
</div>
<details>
<summary align="center"><h3>Примечание</h3></summary>
  <p align="center">Мной было решено уйти от концепции дерева, т.к. такая реализация не позволяет
    достаточно гибко формировать вопросы для клиента и вызывает неудобство работы с множественными полями.<br>
    В итоге было решено реализовать онбординг в виде <b>однонаправленной сети</b>.<br>
    "Цельным" онбордингом является только <b>начальный</b>, при этом его <b>потомки</b> больше похожи на конструктор,
    из которых собирается следующая страница онбординга, так же в основе такого решения лежит концепция в виде <b>от общего к частному</b>.<br><br>
    Есть определённые условия, которых необходимо придерживаться для корректного вывода<b>(в проекте реализована валидация сохранения/редактирование через админ-панель и ORM)</b>:<br>
    <ol>
      <li> Запрещены циклические вызовы опросников, чтобы клиент не попал в бесконечные ответы и не "ломал" статистику;</li>
      <li> Опросник ссылается на следующий опросник только из одного поля, иначе сама логика онбординга построена не правильно;</li>
      <li> Скрытие опросников, клиент на которые уже отвечал - поддержка чистоты статистики и защита от случайных связей;</li>
      <li> Начало онбординга всегда состоит из одного опросника, при этом любой потомок может стать "началом", отдельно от родителя.</li>
    </ol>
  </p>
</details>
<hr>
<details>
<summary align="center"><h3>Уточнения по работе проекта</h3></summary>
<ol>
  <p align="center">Работа с пользователем упрощена до минимума, одна форма для регистрации и авторизации.</p>
  <p align="center">В объекте модели <b>"Тип поля"</b> регулярное выражение "главнее" типа, т.е. его наличие поменяет поле на <b>"text"</b>.</p>
  <p align="center">В форме создания <b>"Поле опроса"</b> пункт <b>"Значения поля"</b> закастомлен через <code>JS</code>, от выбора в <b>"Тип поля"</b> он может быть множественным или единичным,
    следите за состоянием, возможно, могло что-то поломаться.
  </p>
  <p align="center">В <b>"Начальные опросы"</b> можно указать другое начало онбординга, изменив единсвенный элемент.</p>
  <p align="center">На детальной странице элемента <b>"Поля опроса"</b>, если у него несколько значений для выбора, выводится диаграмма с информацией из <b>"Данные по опросу"</b>.</p>
  <p align="center">Имеется <b>"ручка"</b> с выводом ответов клиентов на опросники, подключен filter и пагинация, с реализацией можно познакомиться на странице <code>Swagger-a</code><b>(кнопка-ссылка на главной странице)</b>.</p>
  <p align="center">Тестовые данные<b>(типы полей, опросы, поля опросов)</b> формируются через <a     
     href="https://github.com/VladislavYar/dynamic_onboarding_nomia/blob/main/src/core/management/commands/test_data.py">
    <code>management command</code></a>, там вы можете убрать, например, обязательные поля или "мешающие" типы.
  </p>
  </details>
<hr>

<h3 align="center">Как запустить</h3>
<details>
  <p align="center"><summary align="center"><ins>Через Docker</ins></summary></p>
  <ul>
    <li align="center">1. Создать и заполнить файл <code>.env</code> в папке 
      <a href="https://github.com/VladislavYar/dynamic_onboarding_nomia/tree/main/infra"><code>infra</code></a> по шаблону 
        <a href="https://github.com/VladislavYar/dynamic_onboarding_nomia/blob/main/infra/.env.example"><code>.env.example</code></a>.
    </li>
    <li align="center">
      <p>2. Если имеется утилита <code>Make</code>, в корне проекта выполнить команду <code>make project-init</code>,</p>
      <p>иначе</p>
      <p>выполнить команду <code>docker compose -f ./infra/docker-compose.yml --env-file ./infra/.env up -d</code>.</p>
      <p><code>Docker</code> соберёт контейнеры с <code>postgreSQL</code>, <b>приложением</b>, выполнит миграцию,</p>
      <p>заполнит БД тестовыми данными, создаст superuser-a.</p>
      <p>После сервер будет доступен по адрессу: <code>http://127.0.0.1:8000/</code>.</p>
    </li>
    <li align="center">
      <p><b>Примечание</b></p>
      <p>В контейнер с приложением проброшен <code>volume</code> с кодом, изменение кода в проекте обновляет его в контейнере и перезапускает сервер.</p>
    </li>
    <li align="center">
      <p>Последующие запуски проекта осуществляются через команду <code>make project-start</code></p>
      <p>или</p>
      <p><code>docker compose -f ./infra/docker-compose-start.yml --env-file ./infra/.env up -d</code></p>
    </li>
  </ul>
</details>

<details>
  <p align="center"><summary align="center"><ins>Через консоль</ins></summary></p>
  <ul>
    <li align="center">1. Создать и заполнить файл <code>.env</code> в папке 
      <a href="https://github.com/VladislavYar/dynamic_onboarding_nomia/tree/main/infra"><code>infra</code></a> по шаблону 
        <a href="https://github.com/VladislavYar/dynamic_onboarding_nomia/blob/main/infra/.env.example"><code>.env.example</code></a>.
    </li>
    <li align="center">
      <p>2. Создать БД в <code>postgreSQL</code>.</p>
    </li>
    <li align="center">
      <p>3. Установить poetry <code>pip install poetry</code>.</p>
    </li>
    <li align="center">
      <p>4. Создать и активировать виртуальную оболочку <code>poetry shell</code>.</p>
    </li>
    <li align="center">
      <p>5. Установить зависимости <code>poetry install</code>.</p>
    </li>
    <li align="center">
      <p>6. Выполнить миграцию БД <code>python src/manage.py migrate</code>.</p>
    </li>
        <li align="center">
      <p>7. Создать superuser-a <code>python src/manage.py createsuperuser --noinput</code>.</p>
    </li>
    </li>
        <li align="center">
      <p>8. Заполнить БД тестовыми данными <code>python src/manage.py test_data</code>.</p>
    </li>
    </li>
        <li align="center">
      <p>9. Запустить сервер <code>python src/manage.py runserver</code>.</p>
    </li>
    <li align="center">
      <p>10. Сервер будет доступен по адрессу: <code>http://127.0.0.1:8000/</code>.</p>
    </li>
  </ul>
</details>
<hr>

<h3 align="center">Стек</h3>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12.3-red?style=flat&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Django-5.0.4-red?style=flat&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/DjangoRestFramework-3.15.1-red?style=flat">
  <img src="https://img.shields.io/badge/PostgreSQL-Latest-red?style=flat&logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-Latest-red?style=flat&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/Swagger-Latest-red?style=flat&logo=swagger&logoColor=white">
  <img src="https://img.shields.io/badge/Poetry-Latest-red?style=flat&logo=poetry&logoColor=white">
</p>
<hr>
