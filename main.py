from library import *

genres = GenreExtensions.load_genres_from_json('genres.json', True)

'''
test_cl = Client(id=None, surname='Рем', name='Сергей', last_name='Борисович', phone_num='+79339334964')

test_b = Book(id=None, title='Жизнь', author='Я', pages=51,
              publication_date='12.05.2006', isbn='AC951-8524-BVM', description='Эгоист.', genre_tag='autobiography')
              
with open('test_lib.json', 'r', encoding='utf-8') as f:
    cont = f.read()
    test_lib = Library.model_validate_json(cont)

test_lib.print_sorted_by_genre()
'''



