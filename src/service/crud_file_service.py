import os
from pathlib import Path


def create_dir_if_not_exists(directory_path):
    path = Path(directory_path)
    if not path.exists():
        path.mkdir(parents=True)
        print(f"Папка '{directory_path}' была создана.")
        return directory_path
    else:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                os.remove(os.path.join(root, file))
                for dir in dirs:
                    os.rmdir(os.path.join(root, dir))
        path.rmdir()
        path.mkdir(parents=True)
        return directory_path


def get_data_files(directory, filename):
    print(directory)
    dir_path = directory
    file_path = dir_path / filename
    if not dir_path.is_dir():
        return False

        # Проверяем, существует ли файл
    if not file_path.is_file():
        return False

        # Чтение и возврат содержимого файла
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return False