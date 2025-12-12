import os

class Exeptions():
    UNEXPECTED_ERROR = 0
    FILE_NOT_EXIST = 1
    FILE_CORRUPTED = 2
    FILE_WRITNG_IMPOSSIBLE = 3
    

class CSV_File:
    def __init__(self, path: str, file_name: str) -> None:

        full_file_path = os.path.join(path, file_name) 
        if os.path.exists(full_file_path) == False:
            print("bad")

        self.__full_file_path: str = full_file_path

    def read(self) -> str:
        with open(self.__full_file_path , "r") as file:
            content = file.read()
        return content
    
    def append(self, text: str) -> None:

        with open(self.__full_file_path, "a", encoding="utf-8") as file:
            file.write(text)

file = CSV_File("/home/Taras/","test.txt")
print(file.read())
