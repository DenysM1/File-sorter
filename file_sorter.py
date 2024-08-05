from tkinter import filedialog
import tkinter as tk
from pathlib import Path

# Словник з розширеннями( Можна доповнити за бажанням)
extensions = {
    'документи': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'відео файли': ('AVI', 'MP4', 'MOV', 'MKV'),
    'зображення': ('JPEG', 'PNG', 'JPG', 'SVG'),
    'музика': ('MP3', 'OGG', 'WAV', 'AMR'),
    'архіви': ('ZIP', 'GZ', 'TAR')
}


# Отриманий шлях


def select_folder():
    """
    Ця функція відповідає за відкриття графічного інтерфейсу TKinter для визначення шляху папки, яку треба відсортувати

    """

    root = tk.Tk()
    root.withdraw()  # Сховати головне вікно, оскільки воно не потрібне

    # Відкрити вікно для вибору папки та відформатувати шлях
    folder_path = filedialog.askdirectory(title="Оберіть папку для сортування")

    if not folder_path:
        return None
    folder_path = rf'{folder_path}'
    folder_path = Path(folder_path.replace('\\', '/'))
    return folder_path


p = select_folder()
print(p)


class CreatePaths:

    """
    Цей клас відповідає за створення необхідних каталогів, куди будуть сортуватися файли. 

    Атрибути:

    - main_path: шлях до папки, що буде сортуватись.
    - extension_dict: словник, де ключ - назва категорії, значення - множина файлових розширень, які будуть до неї відноситись.
    - dict_of_path: словник, де ключ - назва категорії, значення - шлях до неї.

    Методи:

    - __init__(path, dict): ініціалізує об'єкт, записує передані значення до атрибутів, 
                            створює порожній словник з шляхами та ініціалізує метод create_folders.

    - create_folders(): створює необхідні каталоги (якщо нема) та записує їх шляхи в словник.

    """

    def __init__(self, path, dict):
        """
        Параметри:

        path(str): шлях до папки, яка буде сортуватись.
        dict(dict): словник, де ключ - назва категорії, значення - множина файлових розширень, які будуть до неї відноситись.

        Кроки виконання:

        1) ініціалізує об'єкт класу
        2) записує значення path в атрибут класу main_path.
        3) записує значення dict в атрибут класу extension_dict.
        4) Створює порожній атрибут класу dict_of_paths(dict).
        5) ініціалізує метод create_folders()

        """

        self.main_path = path
        self.extension_dict = dict
        self.dict_of_paths = {}
        self.create_folders()

    def create_folders(self):
        """
        Для кожного ключа в атрибуті класу extension_dict створює папку з назвою цього ключа
        Записує в словник dict_of_paths назву цієї папки в ключ та шлях до неї в значення

        """
        for key in self.extension_dict.keys():
            dir_path = self.main_path / key
            dir_path.mkdir(exist_ok=True)
            self.dict_of_paths.update({f'{dir_path.name}': dir_path})


# Клас, що відповідає за сортування файлів. Наслідує клас "CreatePaths"
class SortFiles(CreatePaths):

    """
    *** Наслідується з класу CreatePaths ***

    Клас відповідає за сортування всіх файлів, що є в обраній категорії по каталогам, що були створеня в класі CreatePaths

    Атрибути:

    - main_path: шлях до папки, що буде сортуватись.
    - extension_dict: словник, де ключ - назва категорії, значення - множина файлових розширень, які будуть до неї відноситись.
    - dict_of_path: словник, де ключ - назва категорії, значення - шлях до неї.
    - problem_files: множина з назв файлів, що не були відсортовані 

    Методи:

    - __init__(path, dict): Викликає метод __init__(self, path, dict) батьківського класу CreatePaths, 
                            створює пусту множину, куди будуть записуватись імена проблемних файлів

    - sort_files(): через словник extension_dict для кожної категорії(ключа), фільтрує всі файи, що туди підходять за значенням,
                    кожний шлях відфільтрованого файлу та шлях до відповідної категорії передається в метод move_file( file, category),
                    викликається метод move_rest_files, що відправляє решту файлів в папку "Невідомі розширення".

    - move_file(file, category): Має параметри file(вказує шлях до обраного файлу) та category(вказує назву категорії, в яку потріно пересунути обраний файл).
                                 Метод створює шлях, з якого відбувається пересування та шлях призначення,
                                 пересуває файл за шляхом призначення з перевіркою на FileExistsError,
                                 в разі спрацювання FileExistsError, додає в problem_files ім'я файлу та переходить до наступної ітерації.

    - move_rest_files(): Створює каталог "Невідомі розширення",
                         кожний файл, що є файлом та його ім'я відсутнє в problem_files, пересуває в "Невідомі розширення".



    """

    def __init__(self, path, dict):
        """
        Параметри:

        - path(str): шлях до папки, яка буде сортуватись.
        - dict(dict): словник, де ключ - назва категорії, значення - множина файлових розширень, які будуть до неї відноситись.

        Кроки виконання:
        1) Викликає метод __init__(self, path, dict) батьківського класу CreatePaths.
        2) Створює пусту множину, куди будуть записуватись імена проблемних файлів.

        """
        super().__init__(path, dict)
        self.problem_files = set()

    # Метод сортування

    def sort_files(self):
        """
        Кроки виконаня:

        1) Для кожної категорії, що є в ключах словника з розширеннями.
        2) Знаходиться шлях, що належить цій категорії (буде помилка, якщо не знайде).
        3) Кожний файл/директорія проходить фільтр, який перевіряє, що:
                                                                        1. це файл 
                                                                        2. суфікс файлу (переведений в капс) є в розширеннях цієї категорії

        4) Викликає метод move_file(file,category), куди передається назва категорії та шлях до файлу.
        5) Викликає метод move_rest_files().
        6) Перевірка на наявність проблемних файлів.

        """

        for category in self.extension_dict.keys():
            destination = self.dict_of_paths[category]

            for file in filter(
                    lambda x: x.is_file() and x.suffix[1:].upper(
                    ) in self.extension_dict.get(f'{destination.name}'),
                    self.main_path.iterdir()):

                self.move_file(file, category)

        self.move_rest_files()

        if len(self.problem_files) > 0:
            print(
                f"Деякі файли не були відсортовані, оскільки вже існують в каталогах: {self.problem_files}")

    def move_file(self, file, category):
        """
        Параметри: 

        - file(str): шлях до файлу, що буде пересуватись в категорію
        - category(str): назва категорії до якої буде пересуватись файл

        Кроки виконання: 

        1) Створює шлях source, що дорівнює file. Це шлях з якого буде відбуватись пересування.
        2) Створює destination_path, що дорівнює <обрана папка>/<назва категорії>/<назва файлу>. Це шлях куди буде пересуватись обраний файл.
        3) Пересуває файл за шляхом призначення з перевіркою на FileExistsError. 
           Ця перевірка необхідна, щоб в певнетись, що в категорії відсутній файл з такою самою назвою.
        4) В разі спрацювання FileExistsError, додає в problem_files ім'я файлу та переходить до наступної ітерації.

        """
        source = file
        destination_path = self.main_path / category / file.name

        try:
            source.rename(destination_path)
        except FileExistsError:
            self.problem_files.add(file.name)
            pass

    # Метод для пересування решти файлів
    def move_rest_files(self):
        """

        Кроки виконання:

        1) Створює каталог "Невідомі розширення", який має шлях rest_dir_path.
        2) Кожний файл/директорія проходить фільтр, який перевіряє, що:
                                                                        1. Це файл
                                                                        2. Назва файлу відсутня в problem_files
        3) Створює шлях призначення file_destination.
        4) Пересуває файл за шляхом призначення з перевіркою на FileExistsError. 
           Ця перевірка необхідна, щоб в певнетись, що в категорії відсутній файл з такою самою назвою.
        5) В разі спрацювання FileExistsError, додає в problem_files ім'я файлу та переходить до наступної ітерації.

        """
        rest_dir_path = self.main_path / "невідомі розширення"
        rest_dir_path.mkdir(exist_ok=True)
        for file in filter(lambda x: x.is_file() and x.name not in self.problem_files, self.main_path.iterdir()):
            file_destination = rest_dir_path / file.name
            try:
                file.rename(file_destination)
            except FileExistsError:
                self.problem_files.add(file.name)
                pass


if p and extensions != None:

    # Створюється об'єкт класу SortFiles
    sort_files = SortFiles(p, extensions)
    # Виклик методу sort_files()
    sort_files.sort_files()
