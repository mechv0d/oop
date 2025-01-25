from pydantic import BaseModel, Field, ValidationError
from hashlib import md5
from datetime import datetime, date, timedelta
import typing as ty
import json


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

    def dump_json(self):
        return self.model_dump_json(indent=2)

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
        self.id = md5(self.__hash_str).hexdigest()

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

            self.id = md5(
                (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + self.client_id + self.book_id).encode('utf-8')) \
                .hexdigest()

    # endregion

    # region Variables

    id: str | None
    name: str
    address: str

    clients: list[Client] = []
    books: list[BookInArchive] = []

    books_requests: list[BookRequest] = []

    # endregion

    # region Properties

    @property
    def __hash_str(self):
        return (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + self.name + self.address).encode('utf-8')

    @property
    def expired_requests(self) -> list[BookRequest]:
        rqs = list()
        for req in self.books_requests:
            if req.is_expired():
                rqs.append(req)
        return rqs

    # endregion

    # region Methods

    def __init__(self, **data: ty.Any):
        super().__init__(**data)
        self.id = md5(self.__hash_str).hexdigest()

    def find_client(self, hash_id: str) -> Client | None:
        for client in self.clients:
            if client.id.startswith(hash_id) or client.id == hash_id:
                return client
        return None

    def find_book(self, hash_id: str) -> Book | None:
        for book, count in self.books:
            if book.id.startswith(hash_id) or book.id == hash_id:
                return book
        return None

    def find_request(self, hash_id: str) -> BookRequest | None:
        for req in self.books_requests:
            if req.id.startswith(hash_id) or req.id == hash_id:
                return req
        return None

    def has_client(self, hash_id: str) -> bool:
        return self.find_client(hash_id) is not None

    def has_book(self, hash_id: str) -> bool:
        return self.find_book(hash_id) is not None

    def has_request(self, hash_id: str) -> bool:
        return self.find_request(hash_id) is not None

    def add_client(self, other: Client):
        if other is None:
            return
        self.clients.append(other)

    def add_book(self, other: Book, count=1):
        if other is None:
            return
        self.books.append(self.BookInArchive(book=other, count=count))

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

        for book_list in self.books:
            if book_list.book.id == other.id and book_list.count - value >= 0:
                book_list.count += value
                return

    def add_book_request(self, client_id: str, book_id: str, days_to_claim: int,
                         start_date=date.today()) -> BookRequest | None:
        # region Checks

        if not self.has_client(client_id):
            print('Ошибка! Неверный идентификатор клиента!')
            return

        if not self.has_book(book_id):
            print('Ошибка! Неверный идентификатор книги!')
            return

        if self.book_count(book_id) - 1 < 0:
            print('Ошибка! Данной книги нет в библиотеке или все экземпляры уже выданы на руки!')

        if days_to_claim < 0:
            print(f'Ошибка! Неверное количество дней {days_to_claim}!')
            return

        if start_date > date.today():
            print(f'Ошибка! Неверная дата выдачи!')
            return

        # endregion

        self.add_book_count(book_id, -1)

        end_date = start_date + timedelta(days_to_claim)
        if end_date < start_date:
            end_date = date.today()
            print('Дата сдачи книги меньше чем дата взятия. Срок сдачи книги установлен на сегодня!')

        request = self.BookRequest(id=None, client_id=client_id, book_id=book_id,
                                   start_date=start_date, end_date=end_date)
        self.books_requests.append(request)

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

    # endregion


class Genre:
    tag: str
    title: str
    for_adults_only: bool

    def __init__(self, tag: str, title: str, for_adults_only=False, add_itself=True):
        self.tag = tag
        self.title = title
        self.for_adults_only = for_adults_only
        if add_itself and GenreExtensions.find_by_tag(tag) is None:
            GenreExtensions.genres.append(self)

    @property
    def dump_data(self) -> dict:
        return {'tag': self.tag, 'title': self.title, 'for_adults_only': self.for_adults_only}

    def dump_json(self) -> str:
        try:
            return json.dumps(self.dump_data, indent=4, ensure_ascii=False)
        except TypeError:
            return "{}"


class GenreExtensions:
    genres: list[Genre] = []

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
