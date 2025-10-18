import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"

def print_separator(title):
    print("\n" + "-"*60)
    print(f" {title}")

def get_all_posts():
    print_separator("1. Получение списка всех постов")
    try:
        response = requests.get(f"{BASE_URL}/posts") #GET-запрос для получения всех постов
        print(f"Код статуса: {response.status_code}")
        
        if response.status_code == 200:
            posts = response.json() #JSON-ответ -> Python-объект
            
            print(f"Получено постов: {len(posts)}")
            print("\nЗаголовки первых 5 постов:")
            print("-" * 40)

            for i, post in enumerate(posts[:5], 1):
                print(f"{i}. {post['title']}")
                
        else:
            print(f"Ошибка при получении постов: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")

def get_single_post():
    print_separator("2. Получение одного поста id-1")
    
    try:
        response = requests.get(f"{BASE_URL}/posts/1")
        print(f"Код статуса: {response.status_code}")
        
        if response.status_code == 200:
            post = response.json()
            print("Полная информация о посте:")
            print("-" * 40)

            for key, value in post.items():
                print(f"{key}: {value}")
                
        else:
            print(f"Ошибка при получении поста: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")

def create_new_post():
    print_separator("3. Создание поста")
    
    try:
        new_post = {
            "title": "Долой Марио! Почему Валуиджи — непревзойденный гений POST-запросов!",
            "body": "ВАА-ХА-ХА! Пока Марио борется с черепахами, Валуиджи покоряет цифровое пространство! Один POST-запрос — и весь мир узнает правду! Серверы трепещут перед моим мощным JSON! WAA!",
            "userId": 1
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Waluigi-Supremacy/1.0"
        }
        
        print("Отправляемые данные:")
        print(json.dumps(new_post, indent=2, ensure_ascii=False))
        
        response = requests.post( #POST-запрос для создания нового поста
            f"{BASE_URL}/posts",
            json=new_post,
            headers=headers
        )
        
        print(f"\nКод статуса: {response.status_code}")
        
        if response.status_code == 201:
            print("ВААА-ХА-ХА! Мой манифест опубликован! Мир содрогнётся!")
            print(f"ID моего величайшего творения: {response.json()['id']}")
            print("Запомните этот день, день, когда Валуиджи покорил API!")
            created_post = response.json()
            
            print("Созданный пост (ответ от сервера):")
            print("-" * 40)
            
            for key, value in created_post.items():
                print(f"{key}: {value}")
                
        else:
            print(f"WAAAAH! Сервер осмелился ответить {response.status_code}!")
            print("Это проделки Марио! Он должен за это заплатить!")
            print("Запомните: ВАЛУИДЖИ всегда побеждает... в следующий раз! ВААА-ХА-ХА!")

            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        print(f"ВААА-ХА-ХА! Даже вселенная не выдерживает моего кода: {e}")
        print("Но Валуиджи непобедим! Я вернусь сильнее!")
        print("Запомните: Валуиджи всегда побеждает... в следующий раз! ВААА-ХА-ХА!")
    

def main():
    print("Rest API клиент для JSONPLACEHOLDER")

    get_all_posts()
    get_single_post()
    create_new_post()

if __name__ == "__main__":
    main()