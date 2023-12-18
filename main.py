import os
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

def parse_website(url, save_location):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Если произойдет ошибка, выбросит исключение
    except requests.RequestException as e:
        print(f"Произошла ошибка при запросе к {url}: {e}")
        return

    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    wrote = 0

    with open(save_location, 'wb') as file:
        for data in tqdm(response.iter_content(block_size), total=total_size//block_size, unit='KB', unit_scale=True):
            wrote = wrote  + len(data)
            file.write(data)

    if total_size != 0 and wrote != total_size:
        print("ERROR, something went wrong")

url = input("Введите URL сайта: ")
filename = input("Введите имя файла: ")

# Получаем директорию текущего файла
current_dir = os.path.dirname(__file__)

# Создаем путь к файлу
save_location = os.path.join(current_dir, filename)

# Проверяем, существует ли файл
if os.path.exists(save_location):
    print(f"Файл {filename} уже существует. Введите новое имя файла.")
    filename = input("Введите новое имя файла: ")
    save_location = os.path.join(current_dir, filename)

parse_website(url, save_location)
