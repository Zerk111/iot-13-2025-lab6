import os
import json
import logging
from functools import wraps


class FileCorrupted(Exception):
    pass


def logged(exc_type, mode="console"):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except exc_type as e:
                logger = logging.getLogger(func.__name__)
                logger.setLevel(logging.ERROR)

                handler = (
                    logging.FileHandler("log.txt", encoding="utf-8")
                    if mode == "file"
                    else logging.StreamHandler()
                )

                logger.addHandler(handler)
                logger.error(str(e))
                logger.removeHandler(handler)

                raise
        return wrapper
    return decorator


def convert_numbers_to_strings(obj):
    if isinstance(obj, dict):
        return {k: convert_numbers_to_strings(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numbers_to_strings(x) for x in obj]
    elif isinstance(obj, (int, float)):
        return str(obj)
    else:
        return obj


class JSON_File:
    def __init__(self, path: str, filename: str) -> None:
        full_file_path = os.path.join(path, filename)
        self.__full_file_path = full_file_path


        if not os.path.exists(full_file_path):
            os.makedirs(path, exist_ok=True)
            initial_data = [{"message": "hello"}]
            with open(full_file_path, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=4)
            print(f"Файл створено з початковими даними: {full_file_path}")
        else:
            print(f"Файл існує: {full_file_path}")

    @logged(FileCorrupted, mode="console")
    def read(self):
        try:
            with open(self.__full_file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            raise FileCorrupted("Помилка читання JSON файлу")

    @logged(FileCorrupted, mode="file")
    def write(self, data):
        try:
            data = convert_numbers_to_strings(data)
            with open(self.__full_file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception:
            raise FileCorrupted("Помилка запису у JSON файл")

    @logged(FileCorrupted, mode="file")
    def append(self, item):
        try:
            item = convert_numbers_to_strings(item)
            content = self.read()
            if not isinstance(content, list):
                raise FileCorrupted("Append можливий тільки якщо JSON містить список")
            content.append(item)
            self.write(content)
        except Exception:
            raise FileCorrupted("Помилка дописування у JSON файл")


if __name__ == "__main__":
    file = JSON_File("C:\\Users\\zariv\\Desktop", "data.json")

    print("Поточний вміст:", file.read())


    file.append({"new": 123, "flag": True, "neww": 1234455566})
    print("Після append:", file.read())
