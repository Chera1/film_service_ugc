# Исследование хранилищ

В рамках исследования хранилищ, с целью определения наиболее подходящего для
осуществления хранения данных пользователей были взяты следующие варианты:

- MongoDB;
- Cassandra;

## Запись данных
Сначала осуществлялась вставка 150 тыс записей батчами по 10 тыс в хранилище
 и замер времени на осуществление операции
 
###### Среднее время вставки 100 тыс. записей, мс на одну запись:
 
- MongoDB - 1.5644 мс ;
- Cassandra - 1.809 мс

###### Среднее время вставки дополнительных 50 тыс. строк, мс на одну запись:

- MongoDB - 1.8928 мс;
- Cassandra - 3 мс;

## Чтение данных

###### Среднее время на получение списка понравившихся пользователю фильмов (список лайков пользователя):

- MongoDB - 139 мс;
- Cassandra - 124 мс

###### Среднее время на получение количества лайков или дизлайков у определённого фильма;

- MongoDB - 129 мс;
- Cassandra - 100 мс;

###### Среднее время на получение списка закладок;

- MongoDB - 98 мс;
- Cassandra - 103 мс;

###### Среднее время на получение средней пользовательской оценки фильма

- MongoDB - 129 мс;
- Cassandra - 132 мс;

Таким образом на основании полученных данных в качестве хранилища было выбрано MongoDB
