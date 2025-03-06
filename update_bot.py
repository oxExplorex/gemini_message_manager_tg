import io
import os
import traceback
import zipfile

import requests
import asyncio

def download_and_extract_github_repo():
    try:
        # Формируем URL для скачивания архива
        zip_url = f'https://github.com/oxExplorex/gemini_message_manager_tg/archive/refs/heads/main.zip'

        # Скачиваем архив
        response = requests.get(zip_url)
        response.raise_for_status()  # Проверяем, что запрос успешен

        # Распаковываем архив
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            # Получаем имя корневой папки архива
            root_folder = z.namelist()[0]

            # Распаковываем все файлы, удаляя корневую папку из пути
            for file in z.namelist():
                if file.startswith(root_folder):
                    target_path = os.path.join("/", file[len(root_folder):])
                    if not target_path.endswith('/'):  # Пропускаем папки
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        with open(target_path.replace("/", "", 1), 'wb') as f:
                            f.write(z.read(file))




        print("Репозиторий успешно скачан и распакован.")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка скачивания: {e}")
    except zipfile.BadZipFile:
        print("Ошибка: Некорректный ZIP-архив.")
    except:
        print(f"Произошла непредвиденная ошибка: {traceback.format_exc()}")


if __name__ == "__main__":
    download_and_extract_github_repo()

