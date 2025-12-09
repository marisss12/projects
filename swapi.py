import requests
from pathlib import Path
"""Импортируемые биботеки."""


class APIRequester:
    """Родитеский класс."""

    def __init__(self, base_url: str):
        """Метод инициазации объектов
        для всего класса.
        """
        self.base_url = base_url
        base_url = 'https://swapi.dev/api/'

    def get(self, url: str):
        """Метод, формирующий get-запрос."""                    
        try:
            response = requests.get(f'{self.base_url}{url}')
            code = response.raise_for_status()
            return response
        except requests.RequestException:
            print('Возникла ошибка при выполнении запроса')
        except requests.ConnectionError:
            print(f'Сетевая ошибка, статус-код:{code}')
        except Exception:
            print('Возникла ошибка')


class SWRequester(APIRequester):
    """Дочерний класс."""

    def __init__(self, base_url):
        super().__init__(base_url)

    def get_sw_categories(self):
        """Метод получения dict_keys."""
        response = requests.get(self.base_url + '/')
        requesst = response.json()
        return requesst.keys()

    def get_sw_info(self, sw_type):
        """Метод формирования get-запроса
        к категории.
        """
        self.sw_type = sw_type
        full_url = f'{self.base_url}/{self.sw_type}/'
        response = requests.get(full_url)
        return response.text


def save_sw_data():
    """Метод сохранения информации
    по категории в файл.
    """
    requester = SWRequester('https://swapi.dev/api')
    Path('data').mkdir(exist_ok=True)
    categories = requester.get_sw_categories()
    for category in categories:
        sw_info = requester.get_sw_info(category)
        with open(f'data/{category}.txt', 'w') as file:
            file.write(sw_info) 


if __name__ == '__main__':
    save_sw_data()
