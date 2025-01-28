from library import *
from library import ConstructorExtensions as con
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


GenreExtensions.load_genres_from_json('genres.json', True)
genres = GenreExtensions.genres


def write_to_file(filename, write_data):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(write_data)
    except (IOError, OSError) as open_error:
        print(f"Ошибка при работе с файлом: {open_error}")


with open('test_lib.json', 'r', encoding='utf-8') as f:
    cont = f.read()
    try:
        test_lib = Library.model_validate_json(cont)
    except ValidationError as val_error:
        print(f"Failed to load general library JSON file\n{val_error}")
    else:
        # Для более легкого создания экземпляров класса я написал специальный класс ConstructorExtensions,
        # методы которого облегчают создание основных классов программы.

        # Такой костыль вызван наследованием от класса BaseModel из библиотеки pydantic. Он позволяет легко сохранять
        # и загружать данные в JSON, но имеет некоторые проблемы с __init__ методом дочернего класса.
        # Даже так, классы всё равно можно создавать напрямую

        # Создание второй библиотеки
        other_lib = con.create_library('Вторая библиотека', 'ул. Пушкина, д. Колотушкина')

        # Добавление книг
        books = [con.create_book('Герой нашего времени', 'Лермонтов', 111, 'long time ago', 'None', 'test', ''),
                 con.create_book(
                     'Конституция Российской Федерации. Новая редакция (с комментариями Конституционного Суда РФ)',
                     'Проспект', 120, '2022',
                     '978-5-392-32914-4, 978-5-392-33207-6, 9785392343942, 978-5-392-35252-4, 978-5-392-36498-5, 978-5-392-37237-9 ',
                     '', 'social')
                 ]
        other_lib.add_book(books[0], 25)
        other_lib.add_book(books[1], 10)

        # Добавление клиента
        clients = [con.create_client('Трамп', 'Дональд', '', '+71234567879')]
        other_lib.add_client(clients[0])

        # print(f'\n\n{clients[0] in other_lib}\n{books[0] in other_lib}\n{books[0] == books[1]}\n\n')

        # Посмотрим, добавились ли они
        other_lib.print_clients(name='нальд')
        other_lib.print_books(title='конст')

        # Кажется, Дональд собирается почитать интересную литературу
        trump_request = other_lib.add_book_request(clients[0].id, books[1].id, 30)

        # Он ошибся
        other_lib.remove_request(trump_request.id)

        # Он забыл, что уже вернул книгу, и решил снова попытаться сдать её
        other_lib.remove_request(trump_request.id)

        # Он позвал своего старого друга посидеть в библиотеке
        clients.append(con.create_client('Байден', 'Джозеф', '', '+79139135566'))
        other_lib.add_client(clients[1])

        # Джо решил почитать классику
        joe_request = other_lib.add_book_request(clients[1].id, books[0].id, 15)

        save_input = input(
            'Тестирование созданной библиотеки завершено. Если хотите, можете сохранить данные, вписав имя файла '
            '(например, "other_lib.json"). Если не хотите, оставьте поле пустым."\n'
            'После этого начнётся тестирование загруженной библиотеки из файла test_lib.json\n')

        if not save_input == '':
            write_data = other_lib.dump_json()
            write_to_file(save_input, write_data)

        clear()

        # Вывести книги жанра "Антиутопия"
        test_lib.print_books(genre_tag='dyst')

        # Вывести клиентов
        test_lib.print_clients()

        # Вывести запросы у клиента, чей хеш начинается с '4a69' (это я)
        test_lib.print_requests(client_id='4a69')

        # Вывести только просроченные запросы
        test_lib.print_requests(only_expired=True)

        # Я извинился и вернул книгу
        test_lib.remove_request('466d3')

        # И запрос исчез
        test_lib.print_requests(only_expired=True)
