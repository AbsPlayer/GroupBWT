1. Створити БД MySql
2. Створити правильне підключення до БД у файлі alembic.ini:
   рядок sqlalchemy.url = mysql+pymysql://root:root@localhost/tesco_com_db заповнити своїми даними,
   де root:root - це логін та пароль адміна до БД,
   localhost - ім'я або ip хоста з БД,
   tesco_com_db - ім'я БД, що створена у п.1   
3. Виконати міграцію, що розташована в теці /alembic/versions
   консольною командою 'alembic upgrade head'
4. Згідно завдання поля БД 'Review' та 'Usually Bought Next Products' мусять мати тип Array of objects,
   але БД MySql не підтримує такий тип (цей тип даних притаманний БД PostgreSQL).
   Тому був використаний тип JSON
5. Заповнити дані для підключення до БД у файлі .env   
6. Запустити спайдера консольною командою 'scrapy crawl tesco_com_spider'
7. Спайдер збереже дані в БД, у теці проекта сформується log-файл
   
   ---
   
1. Create MySQL DB
2. Create right connection to DB in alembic.ini:
   line sqlalchemy.url = mysql+pymysql://root:root@localhost/tesco_com fill own data,
   root:root - login and password of administrator to DB,
   localhost - name or ip of the host with DB,
   tesco_com_db - DB name created in par. 1
3. Perform migration located in /alembic/versions
   via console command 'alembic upgrade head'
4. According to the task DB fields 'Review' and 'Usually Bought Next Products' must have the type Array of objects,
   but MySql database does not support this type (this data type is inherent in the PostgreSQL).
   Therefore, the JSON type was used
5. Fill data for connection to DB in file ".env"   
5. Run spider via console command 'scrapy crawl tesco_com_spider'
6. Spider will save data to DB, log-file will be formed in project folder
