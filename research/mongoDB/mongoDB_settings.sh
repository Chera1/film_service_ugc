# Для начала настроим серверы конфигурации.
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
# Можно проверить статус, выполнив команду на первом сервере конфигурации
docker exec -it mongocfg1 bash -c 'echo "rs.status()" | mongosh'
# Далее, соберём набор реплик первого шарда.
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
# Вы можете проверить статус реплик с помощью такой команды:
docker exec -it mongors1n1 bash -c 'echo "rs.status()" | mongosh'
# Наконец, познакомим шард с маршрутизаторами.
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
# Второй шард добавим по аналогии. Сначала инициализируем реплики.
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
# Затем добавим их в кластер.
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
# Можно проверить статус с помощью команды, запущенной на первом маршрутизаторе.
docker exec -it mongos1 bash -c 'echo "sh.status()" | mongosh'


# Создадим БД для хранения данных пользователей.
docker exec -it mongors1n1 bash -c 'echo "use ugcService" | mongosh'
# Включим шардирование.
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"ugcService\")" | mongosh'


# Пришло время создать коллекцию для лайков фильмов.
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugcService.filmLikes\")" | mongosh'
# Настроим шардирование по полям film_id
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugcService.filmLikes\", {\"film_id\": \"hashed\"})" | mongosh'

# Пришло время создать коллекцию для лайков отзывов.
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugcService.reviewLikes\")" | mongosh'
# Настроим шардирование по полям review_id
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugcService.reviewLikes\", {\"review_id\": \"hashed\"})" | mongosh'

# Пришло время создать коллекцию для отзывов.
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugcService.reviews\")" | mongosh'
# Настроим шардирование по полям film_id
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugcService.reviews\", {\"film_id\": \"hashed\"})" | mongosh'

# Пришло время создать коллекцию для закладок.
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugcService.bookmarks\")" | mongosh'
# Настроим шардирование по полям user_id
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugcService.bookmarks\", {\"user_id\": \"hashed\"})" | mongosh'



