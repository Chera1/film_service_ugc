from random import randrange, randint, choice
from datetime import datetime, timedelta
import uuid
import functools
import time

from pymongo import MongoClient

film_ids = ["ef57acb3-c17c-4d08-91fd-c63a2ee4d8d7", "f0526214-30ba-44f2-873e-480c7bfa8af7",
            "d5213b38-850d-4cb8-8f34-273e3e87b388", "eb4cca1a-e3a4-4981-8def-83e98388659e",
            "ba9e84f4-5e0c-48a2-9b3a-2f5444c87d7b", "64ed4649-09e1-407a-9bdc-d9fc8cc36722",
            "01aba386-cee8-441e-90f9-a735007a2794", "08742144-9a52-4937-a764-149b5ad5b07e",
            "707966d2-73a0-486f-a434-20a683947afb", "4b6ad245-2ab8-49d1-b948-3653239da65d",
            "1c50eafa-b30e-4f1d-9df9-fa729596d768", "d22bc89b-d76e-4c32-89f7-93db8c0edf3e",
            "9db26029-8b72-4953-9a3b-7f7cc926790a", "78193721-94e2-4032-905a-73368ec488c0",
            "6f76377a-1ed1-4b27-b650-f8b1a9c77e72", "b66e4d3e-c9dc-4893-91d2-e4813aaad1b7",
            "da68309b-89cc-4a91-ac4f-f8133bb0d1c4", "d0e43d63-4d84-4a3d-948f-236324031ff8",
            "c724d996-a099-41e0-9865-09ae11cda9ef", "468e171e-0c17-4656-b94e-7222dd92334d"
            ]

user_ids = ["e2b348a6-0846-443a-96c1-f04e30218c8f",  "9770d012-08ba-4d38-88ff-ddb3c886cc7b",
            "77783124-0b21-41a5-bdde-b7a504e59784", "bafcd6c3-f023-44ae-af97-e9f448ca3c56",
            "ca496433-33de-47c8-9450-5f924867f7c3", "e9f983eb-633e-4ac6-9f91-a758490d0fd3",
            "e6c259d5-a943-47ab-b073-8bf0e41e3d76", "ee9b00ce-14b8-4953-afa3-cd094ef24c3a",
            "17f2b5a8-fae3-4f72-83bc-b67e5d4eba03", "cc6befc6-cade-4e29-86d3-225717ea436d",
            "7e46c812-dba9-40a0-8adb-12d23901ee97", "0e7d3f8b-ed7a-4fd2-94ea-96293e945838",
            "fbb9494b-36a8-4349-881b-432319eb3101", "db11fbb5-c2be-40d8-be61-660bd059e7e5",
            "25dcbf03-5b5f-41cb-8291-858bfd65cb09", "229d49e6-1010-4acb-9282-59474612d896",
            "a9cfbaf0-93c7-4ff5-a059-f6ffb804c631", "5125d5df-1e5b-4119-a991-3762ccec8544",
            "530a5000-ba24-4a9d-88de-53e98892a555", "0ba75aea-c6b4-4525-92c6-e5498cd69c09"
            ]

NUMBER_OF_DOCS = 10 ** 5
BATCH_SIZE = 10 ** 4
TEST_TEXT = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the " \
            "industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and " \
            "scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap " \
            "into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the " \
            "release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing " \
            "software like Aldus PageMaker including versions of Lorem Ipsum."


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time of func {func.__name__}: {elapsed_time:0.4f} seconds")
        print(f"Average time for one doc is : {elapsed_time * 1000 / NUMBER_OF_DOCS:0.4f} ms")
        return value

    return wrapper_timer


def get_mongo_client(connection_string: str) -> MongoClient:
    return MongoClient(connection_string)


def random_date():
    start = datetime.strptime('1/1/2008 1:00 AM', '%m/%d/%Y %I:%M %p')
    end = datetime.strptime('12/31/2022 11:59 pM', '%m/%d/%Y %I:%M %p')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


@timer
def generate_bookmarks(bookmarks):
    gen_list = []
    for i in range(NUMBER_OF_DOCS):
        gen_data = {
            "film_id": str(uuid.uuid4()),  # choice(film_ids),
            "user_id": str(uuid.uuid4()),  # choice(user_ids),
            "added_at": random_date()
        }
        gen_list.append(gen_data)
        if i % BATCH_SIZE == 0 or i == NUMBER_OF_DOCS:
            bookmarks.insert_many(gen_list)
            gen_list = []


@timer
def generate_film_likes(film_likes):
    gen_list = []
    for i in range(1, NUMBER_OF_DOCS + 1):
        gen_data = {
            "film_id": str(uuid.uuid4()),  # choice(film_ids),
            "user_id": str(uuid.uuid4()),  # choice(user_ids),
            "added_at": random_date(),
            "value": randint(0, 10)
        }
        gen_list.append(gen_data)
        if i % BATCH_SIZE == 0 or i == NUMBER_OF_DOCS:
            film_likes.insert_many(gen_list)
            gen_list = []


@timer
def generate_review_likes(review_likes):
    gen_list = []
    for i in range(1, NUMBER_OF_DOCS + 1):
        gen_data = {
            "review_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),  # choice(user_ids),
            "added_at": random_date(),
            "value": randint(0, 10)
        }
        gen_list.append(gen_data)
        if i % BATCH_SIZE == 0 or i == NUMBER_OF_DOCS:
            review_likes.insert_many(gen_list)
            gen_list = []


@timer
def generate_review(review):
    gen_list = []
    for i in range(1, NUMBER_OF_DOCS + 1):
        gen_data = {
            "film_id": str(uuid.uuid4()),  # choice(film_ids),
            "user_id": str(uuid.uuid4()),  # choice(user_ids),
            "published_at": random_date(),
            "text": TEST_TEXT
        }
        gen_list.append(gen_data)
        if i % BATCH_SIZE == 0 or i == NUMBER_OF_DOCS:
            review.insert_many(gen_list)
            gen_list = []


def main():
    CONNECTION_STRING = "mongodb://localhost:27019,localhost:27020"
    mongo = get_mongo_client(CONNECTION_STRING)
    db = mongo.ugcService

    bookmarks = db.bookmarks
    film_likes = db.filmLikes
    review_likes = db.reviewLikes
    reviews = db.reviews

    generate_bookmarks(bookmarks)
    generate_film_likes(film_likes)
    generate_review_likes(review_likes)
    generate_review(reviews)


if __name__ == '__main__':
    main()
