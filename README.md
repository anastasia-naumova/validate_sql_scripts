# Validate sql scripts

В скрипте реализована проверка синтаксиса sql файлов(postgres). 

Путь к директории с sql файлами передается в переменную - path_directory.

Для проверки валидности файлов необходимо подключение к базе данных postgres.
Для подключения необходимо указать:

  name_database = "db_name",
  name_user = "db_user",
  db_password = "db_password",
  db_host = "db_host",
  db_port = "db_port".

Если sql файл невалиден, то все найденые ошибки записываются в файл error.txt:

[error.txt](https://github.com/anastasia-naumova/validate_sql_scripts/files/6863889/error.txt)


