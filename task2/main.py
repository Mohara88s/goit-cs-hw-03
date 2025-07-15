from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

barsik = {
            "name": "barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"],
        }

several_cats = [{
            "name": "Lama",
            "age": 2,
            "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
        },
        {
            "name": "Liza",
            "age": 4,
            "features": ["ходить в лоток", "дає себе гладити", "білий"],
        },]

def add_cat(cat, db):
    result = db.cats.insert_one(cat)
    return(result.inserted_id)

def add_cats(arr_of_cats, db):
    result = db.cats.insert_many(arr_of_cats)
    return(result.inserted_ids)

def find_cat_by_name(cat_name, db):
    result = db.cats.find_one({"name": cat_name})
    return(result)

def print_all_cats(db):
    if db.cats.count_documents({}):
        cats_set = db.cats.find({})
        for cat in cats_set:
            print(cat)            
    else:
        print('Коти відсутні в базі даних. Будьласка, додайте котів!')

def update_age_of_cat_by_name(cat_name, new_age, db):
    db.cats.update_one({"name": cat_name}, {"$set": {"age": new_age}})
    result = db.cats.find_one({"name": cat_name})
    return(result)

def add_new_feature_for_cat_by_name(cat_name, new_feature, db):
    db.cats.update_one({"name": cat_name}, {"$push": {"features": new_feature}})
    result = db.cats.find_one({"name": cat_name})
    return(result)

def delete_cat_by_name(cat_name, db):
    result = db.cats.delete_one({"name": cat_name})
    return(bool(result.deleted_count))

def delete_all_cats(db):
    db.cats.delete_many({})
    return('База даних котів видалена!')

def main():
    try:

        # Завантаження змінних з файлу .env
        load_dotenv()

        # Витягання URL для підключення до БД
        db_url = os.getenv("DATABASE_URL")
       
        # Підключення до БД
        client = MongoClient(db_url, server_api=ServerApi('1'))
        db = client.catsColection


        # Додавання одного кота barsik
        
        print(f'Ідентифікатор доданого кота - {add_cat(barsik, db)}\n')

        # Додавання колекції котів
        print(f'Набір ідентифікаторів доданих котів - {add_cats(several_cats, db)}\n')

        # Видалення кота за іменем 
        print(f'Результат видалення кота - {delete_cat_by_name("Lama", db)}\n')

        # Пошук кота за іменем
        print(f'Результат пошуку кота - {find_cat_by_name("barsik", db)}\n')

        # Виведення всіх котів
        print("База даних котів:")
        print_all_cats(db)
        print()

        # Оновлення віку кота
        print(f'Результат оновлення віку кота - {update_age_of_cat_by_name("barsik", 5, db)}\n')
        
        # Додавання нової фічі коту
        print(f'Результат додавання фічі коту - {add_new_feature_for_cat_by_name("barsik", "python programmer", db)}\n')

        # Видалення всіх котів з бази даних
        print(delete_all_cats(db))

    # Відслідковуємо помилки
    except Exception as e:
        print(e)
    

if __name__ == "__main__":
    main()