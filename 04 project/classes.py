import requests

class Cats:
    # Инициализация класса
    def __init__(self, url: str):
        self.url = url

    # Метод: на основании введённого пользователем числа формируем url для картинки
    def get_cat_url(self, number):
        url_cat = f"{self.url}/{str(number)}.jpg"
        return url_cat

class Numbers:
    # Инициализация класса
    def __init__(self, url: str):
        self.url = url

    # Метод: на основании введённого числа формируем url для вывода факта о числе
    def get_fact(self, number: int = 42):
        response = requests.get(f"{self.url}/{str(number)}")
        return response.text

'''
    # Выводим для примера и проверки работы на экран полученный url на код 400:
if __name__ == '__main__':
    cats = Cats(f'https://http.cat')  # Создание экземпляра класса
    print(cats.get_cat_url(400))
'''