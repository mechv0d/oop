from pydantic import BaseModel, Field, ValidationError
from hashlib import md5
from datetime import datetime, date, timedelta
import typing as ty
import json
from abc import ABC


# region Classes
class Client(BaseModel):
    # region Variables
    id: str | None
    surname: str
    name: str
    last_name: str
    phone_num: str

    # endregion

    # region Properties
    @property
    def __hash_str(self):
        return (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + self.name + self.surname + self.last_name) \
            .encode('utf-8')

    # endregion

    # region Methods
    def __init__(self, **data: ty.Any):
        super().__init__(**data)
        if self.id is None:
            self.id = md5(self.__hash_str).hexdigest()

    @staticmethod
    def create_from_console():
        fields = ['Фамилия', 'Имя', 'Отчество', 'Номер телефона']
        ask_dict: dict[int, str] = {0: None, 1: None, 2: None,
                                    3: None}  # Change it with the __init__ method!

        for key in ask_dict.keys():
            inp = input(f'Введите значение для строки "{fields[key]}": ')
            ask_dict[key] = inp

        return Client(id=None, surname=ask_dict[0], name=ask_dict[1], last_name=ask_dict[2], phone_num=ask_dict[3], )

    def dump_json(self) -> str:
        json_str = '{}'
        try:
            json_str = self.model_dump_json(indent=2)
        except ValidationError as e:
            print(f'Client dump has some errors! Returning empty dictionary.\n{e}')
        except LibraryIOError as e:
            print(e)
        finally:
            return json_str
    # endregion


class Book(BaseModel):
    # region Variables
    id: str | None
    title: str
    author: str
    pages: int
    publication_date: str
    isbn: str
    description: str
    genre_tag: str

    # endregion

    # region Properties
    @property
    def __hash_str(self):
        return (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + self.title + self.author + self.isbn) \
            .encode('utf-8')

    # endregion

    # region Methods
    def __init__(self, **data: ty.Any):
        super().__init__(**data)
        if self.id is None:
            self.id = md5(self.__hash_str).hexdigest()

    def __eq__(self, other):
        return self.id == other.id

    @staticmethod
    def create_from_console():
        fields = ['Название', 'Автор', 'Страницы', 'Дата публикации', 'ISBN', 'Описание',
                  'Тег жанра (впишите default если сомневаетесь)']
        ask_dict: dict[int, str] = {}  # Change it with the __init__ method!

        for key in range(len(fields)):
            inp = input(f'Введите значение для строки "{fields[key]}": ')
            ask_dict[key] = inp

        return Book(id=None, title=ask_dict[0], author=ask_dict[1], pages=int(ask_dict[2]),
                    publication_date=ask_dict[3], isbn=ask_dict[4])

    def dump_json(self):
        return self.model_dump_json(indent=2)

    # endregion


class Library(BaseModel):
    # region Subclasses

    class BookInArchive(BaseModel):
        book: Book
        count: int

        def __iter__(self):
            return iter([self.book, self.count])

        def __contains__(self, item):
            if isinstance(item, Book):
                return self.book == item
            return False

    class BookRequest(BaseModel):
        id: str | None
        client_id: str
        book_id: str

        start_date: date
        end_date: date

        def is_expired(self, to_date=date.today()) -> bool:
            return to_date > self.end_date

        def __init__(self, /, **data: ty.Any):
            super().__init__(**data)

            if self.id is None:
                self.id = md5(
                    (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + self.client_id + self.book_id).encode('utf-8')) \
                    .hexdigest()

    # endregion

    # region Variables

    id: str | None
    name: str
    address: str

    clients: list[Client]
    books: list[BookInArchive]
    books_requests: list[BookRequest]

    # endregion

    # region Properties

    @property
    def __hash_str(self):
        return (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + self.name + self.address).encode('utf-8')

    # endregion

    # region Methods

    def __init__(self, **data: ty.Any):
        # self.clients = []
        # self.books = []
        # self.books_requests = []
        super().__init__(**data)
        if self.id is None:
            self.id = md5(self.__hash_str).hexdigest()

    def __contains__(self, item):
        if isinstance(item, Book):
            for archive in self.books:
                if item in archive:
                    return True
            return False

        elif isinstance(item, Client):
            return item in self.clients

        else:
            return False

    def find_client(self, hash_id: str) -> Client | None:
        for client in self.clients:
            if Library.hash_similar(client.id, hash_id):
                return client
        return None

    def find_book(self, hash_id: str) -> Book | None:
        for archive in self.books:
            if Library.hash_similar(archive.book.id, hash_id):
                return archive.book
        return None

    def find_request(self, hash_id: str) -> BookRequest | None:
        for req in self.books_requests:
            if Library.hash_similar(req.id, hash_id):
                return req
        return None

    def has_client(self, hash_id: str) -> bool:
        return self.find_client(hash_id) is not None

    def has_book(self, hash_id: str) -> bool:
        return self.find_book(hash_id) is not None

    def has_request(self, hash_id: str) -> bool:
        return self.find_request(hash_id) is not None

    def add_client(self, other: Client):
        if other is None or not isinstance(other, Client):
            return
        self.clients.append(other)
        print(f'Клиент {other.surname} {other.name} {other.last_name} успешно добавлен!\n')

    def add_book(self, other: Book, count=1):
        if other is None or not isinstance(other, Book):
            return
        self.books.append(self.BookInArchive(book=other, count=count))
        print(f'Книга "{other.title}" успешно добавлена в количестве: {count}шт.\n')

    def remove_client(self, hash_id: str):
        target = None

        for client in self.clients:
            if Library.hash_similar(client.id, hash_id):
                target = client
                break

        if target:
            self.clients.remove(target)

    def remove_book(self, hash_id: str):
        target = None

        for archive in self.books:
            if Library.hash_similar(archive.book.id, hash_id):
                target = archive
                break

        if target:
            self.books.remove(target)

    def remove_request(self, hash_id: str):
        target = None

        for req in self.books_requests:
            if Library.hash_similar(req.id, hash_id):
                target = req
                break

        if target:
            client = self.find_client(target.client_id)
            book = self.find_book(target.book_id)

            self.add_book_count(target.book_id, 1)
            self.books_requests.remove(target)

            print(f'{client.name} {client.surname} успешно вернул книгу {book.title}\n'
                  f'Книг теперь в наличии: {self.book_count(book.id)}\n')
        else:
            print('Случилась непредвиденная ошибка при удалении запроса!\n')

    def book_count(self, book_id: str) -> int:
        if not self.has_book(book_id):
            return 0
        other = self.find_book(book_id)

        for book, count in self.books:
            if other.id == book.id:
                return count
        return 0

    def add_book_count(self, book_id: str, value: int):
        if not self.has_book(book_id):
            return

        other = self.find_book(book_id)

        for archive in self.books:
            if archive.book.id == other.id and archive.count - value >= 0:
                archive.count += value
                return

    def add_book_request(self, client_id: str, book_id: str, days_to_claim: int,
                         start_date=date.today()) -> BookRequest | None:
        # region Checks

        if not self.has_client(client_id):
            print('Ошибка! Неверный идентификатор клиента!\n')
            return

        if not self.has_book(book_id):
            print('Ошибка! Неверный идентификатор книги!\n')
            return

        if self.book_count(book_id) - 1 < 0:
            print('Ошибка! Данной книги нет в библиотеке или все экземпляры уже выданы на руки!\n')

        if days_to_claim < 0:
            print(f'Ошибка! Неверное количество дней {days_to_claim}!\n')
            return

        if start_date > date.today():
            print(f'Ошибка! Неверная дата выдачи!\n')
            return

        # endregion

        client = self.find_client(client_id)
        book = self.find_book(book_id)

        self.add_book_count(book.id, -1)

        end_date = start_date + timedelta(days_to_claim)
        if end_date < start_date:
            end_date = date.today()
            print('Дата сдачи книги меньше чем дата взятия. Срок сдачи книги установлен на сегодня!\n')

        request = self.BookRequest(id=None, client_id=client_id, book_id=book_id,
                                   start_date=start_date, end_date=end_date)
        if request:
            self.books_requests.append(request)

            print(
                f'Книга "{book.title}" успешно взята клиентом '
                f'{client.name} {client.surname} до {end_date.strftime("%d.%m.%Y")}'
                '\nДоп. информация:\n'
                f'Клиент: {client.id}\n'
                f'Книга: {book.id}\n'
                f'Идентификатор запроса: {request.id}\n'
                f'Книг осталось в наличии: {self.book_count(book.id)}\n')

            return request
        else:
            raise SimpleError('Возникла непредвиденная ошибка при создании запроса!\n')

    def dump_json(self):
        return self.model_dump_json(indent=2)

    def load_from_file(self, filepath: str):
        with open(filepath, 'r') as f:
            self.model_validate_json(f.read())

    # endregion

    # region Additional Methods (Sort)

    def print_sorted_by_genre(self):
        scores: dict[str: int] = {}

        for archived_book in self.books:
            if archived_book.book.genre_tag not in list(scores.keys()):
                scores[archived_book.book.genre_tag] = 0
            scores[archived_book.book.genre_tag] += archived_book.count

        for tag, count in scores.items():
            genre = GenreExtensions.find_by_tag(tag)
            title = genre.title if genre else tag
            print(f'Книг в жанре "{title}" хранится: {count}')

    def expired_requests(self) -> list[BookRequest]:
        rqs = list()
        for req in self.books_requests:
            if req.is_expired():
                rqs.append(req)
        return rqs

    @staticmethod
    def hash_similar(hash_id: str, substr: str) -> bool:
        return hash_id.startswith(substr) or hash_id == substr

    @staticmethod
    def __print_book(book_obj: Book, count: int, i=1):
        print(f'''Книга №{i} ({count}шт.) {book_obj.id}
"{book_obj.title}"
— {book_obj.author}, {book_obj.publication_date}
{GenreExtensions.find_by_tag(book_obj.genre_tag).title}
ISBN {book_obj.isbn}
                    ''')

    @staticmethod
    def __print_client(client_obj: Client, i=1):
        print(f'''Клиент №{i} {client_obj.id}
{client_obj.surname} {client_obj.name} {client_obj.last_name}
{client_obj.phone_num}
                            ''')

    def __print_request(self, request_obj: BookRequest, i=1):
        if request_obj is None:
            return
        client = self.find_client(request_obj.client_id)
        book = self.find_book(request_obj.book_id)
        print(f'''Запрос №{i} {request_obj.id}
Клиент: {client.surname} {client.name} {client.last_name} ({client.id})
Книга: "{book.title}", {book.author} ({book.id})
Дата выдачи: {request_obj.start_date} до {request_obj.end_date}
Просрочен: {"ДА" if request_obj.is_expired() else "-"}
        ''')

    def print_books(self, limit=50, title='', author='', publication_date='', isbn='', description='',
                    genre_tag=''):
        printed_count = 0
        for archive in self.books:
            i = self.books.index(archive) + 1
            book = archive.book

            if (title != '' and book.title.lower().count(title.lower()) < 1) \
                    or (author != '' and book.author.lower().count(author.lower()) < 1) \
                    or (publication_date != '' and book.publication_date.lower().count(publication_date.lower()) < 1) \
                    or (isbn != '' and book.isbn.lower().count(isbn.lower()) < 1) \
                    or (description != '' and book.description.lower().count(description.lower()) < 1) \
                    or (genre_tag != '' and book.genre_tag.lower().count(genre_tag.lower()) < 1):
                continue

            printed_count += 1
            Library.__print_book(book, archive.count, i)
            if printed_count == limit:
                break
        if printed_count == 0:
            print('По данному запросу не нашлось записей. Проверьте правильность написания')
        print(f'>>> Найдено записей: {printed_count}.\n')

    def print_clients(self, limit=50, surname='', name='', last_name='', phone_num=''):
        printed_count = 0
        for client in self.clients:
            i = self.clients.index(client) + 1

            if (surname != '' and client.surname.lower().count(surname.lower()) < 1) \
                    or (name != '' and client.name.lower().count(name.lower()) < 1) \
                    or (last_name != '' and client.last_name.lower().count(last_name.lower()) < 1) \
                    or (phone_num != '' and client.phone_num.count(phone_num.lower()) < 1):
                continue

            printed_count += 1
            Library.__print_client(client, i)
            if printed_count == limit:
                break
        if printed_count == 0:
            print('По данному запросу не нашлось записей. Проверьте правильность написания')
        print(f'>>> Найдено записей: {printed_count}.\n')

    def print_requests(self, limit=50, request_id='', client_id='', book_id='', only_expired=False):
        printed_count = 0
        for req in self.books_requests:
            i = self.books_requests.index(req) + 1

            if (request_id != '' and not Library.hash_similar(req.id, request_id)) \
                    or (client_id != '' and not Library.hash_similar(req.client_id, client_id)) \
                    or (book_id != '' and not Library.hash_similar(req.book_id, book_id)) \
                    or (only_expired is not False and not req.is_expired()):
                continue

            printed_count += 1
            self.__print_request(req, i)
            if printed_count == limit:
                break
        if printed_count == 0:
            print('По данному запросу не нашлось записей. Проверьте правильность написания')
        print(f'>>> Найдено записей: {printed_count}.\n')

        # endregion

    # endregion


class Genre:
    # region Variables
    tag: str
    title: str
    for_adults_only: bool

    # endregion

    # region Properties
    @property
    def dump_data(self) -> dict:
        return {'tag': self.tag, 'title': self.title, 'for_adults_only': self.for_adults_only}

    # endregion

    # region Methods
    def __init__(self, tag: str, title: str, for_adults_only=False, add_itself=True):
        self.tag = tag
        self.title = title
        self.for_adults_only = for_adults_only
        if add_itself and GenreExtensions.find_by_tag(tag) is None:
            GenreExtensions.genres.append(self)

    def dump_json(self) -> str:
        try:
            return json.dumps(self.dump_data, indent=4, ensure_ascii=False)
        except TypeError:
            return "{}"

    # endregion


class GenreExtensions:
    # region Variables
    genres: list[Genre] = []

    # endregion

    # region Methods
    @staticmethod
    def clear_repeats():
        GenreExtensions.genres = set(GenreExtensions.genres)

    @staticmethod
    def find_by_tag(tag: str) -> Genre | None:
        for g in GenreExtensions.genres:
            if g.tag == tag:
                return g
        return None

    @staticmethod
    def load_genres_from_json(filepath: str, auto_add=False) -> list[Genre]:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                loaded_genres = []
                for item in data:
                    tag = item.get('tag')
                    title = item.get('title')
                    for_adults_only = item.get('for_adults_only', auto_add)
                    loaded_genres.append(Genre(tag, title, for_adults_only))
                return loaded_genres
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    # endregion


class ConstructorExtensions:
    @staticmethod
    def create_book(title: str, author: str, pages: int, publication_date: str, isbn: str, description: str,
                    genre_tag: str) -> Book:
        return Book(id=None, title=title, author=author, pages=pages, publication_date=publication_date, isbn=isbn,
                    description=description, genre_tag=genre_tag)

    @staticmethod
    def create_client(surname: str, name: str, last_name: str, phone_num: str) -> Client:
        return Client(id=None, surname=surname, name=name, last_name=last_name, phone_num=phone_num)

    @staticmethod
    def create_library(name: str, address: str) -> Library:
        return Library(id=None, name=name, address=address, books=[], clients=[], books_requests=[])


# Объект, с которым заключено юридическое соглашение на сотрудничество
class LegalCoopObject(ABC):
    __name: str
    __kpp: str  # Код причины постановки на учет
    __ogrn: str  # Основной государственный регистрационный номер
    __legal_address: str  # Адрес, указанный в ЕГРЮЛ
    __actual_address: str
    __phone: str
    __email: str
    __registration_date: datetime
    __status: str  # "Действующее", "Ликвидировано", "В процессе банкротства"
    __notes: str

    def __init__(self,
                 name: str,
                 kpp: str,
                 ogrn: str,
                 legal_address: str,
                 actual_address: str,
                 phone: str,
                 email: str,
                 registration_date: datetime,
                 status: str,
                 notes: str
                 ):
        self.__name = name
        self.__kpp = kpp
        self.__ogrn = ogrn
        self.__legal_address = legal_address
        self.__actual_address = actual_address
        self.__phone = phone
        self.__email = email
        self.__registration_date = registration_date
        self.__status = status
        self.__notes = notes


class School(LegalCoopObject):
    __director_name: str
    __contact_person: str

    def __init__(self, name: str, kpp: str, ogrn: str, legal_address: str, phone: str,
                 email: str, registration_date: datetime, status: str, notes: str, director_name: str,
                 contact_person: str):
        super().__init__(name, kpp, ogrn, legal_address, legal_address, phone, email, registration_date, status, notes)
        self.__director_name = director_name
        self.__contact_person = contact_person


# endregion

# region Exceptions
class SimpleError(BaseException):
    """Базовая ошибка"""

    __message: str

    def __init__(self, message="Произошла некоторая ошибка"):
        self.__message = message
        super().__init__(self.__message)

    def __str__(self):
        return f"SimpleError: {self.__message}"


class LibraryIOError(SimpleError):
    """Класс для конкретных ошибок, например, ошибка ввода."""

    def __init__(self, message="Некорректный ввод/вывод данных"):
        self.__message = message
        super().__init__(self.__message)

    def __str__(self):
        return f"SpecificError: {self.__message}"
# endregion
