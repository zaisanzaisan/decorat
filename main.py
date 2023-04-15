import os
import datetime


def logger(old_function):
    def new_function(*args, **kwargs):
        data = f"date: {datetime.datetime.now().strftime('дата %d-%m-%Y время %H:%M:%S')} , " \
               f"function_name: {old_function.__name__}," \
               f" arguments: {args},{kwargs}, result: {old_function(*args, **kwargs)}\n"

        with open('main.log', 'a', encoding='utf-8') as log:
            log.write(data)
        return old_function(*args, **kwargs)

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()

    @logger
    def lst_to_dict(some_list):
        dct = {}
        temporary_dct = {}
        count = len(some_list) - 1
        for i in some_list[:-1]:
            if i == some_list[0]:
                dct[some_list[count - 1]] = some_list[count]
            else:
                dct[some_list[count - 1]] = temporary_dct
            temporary_dct = dct.copy()
            dct.clear()
            count -= 1
        return temporary_dct


    lst_to_dict(['2018-01-01', 'yandex', 'cpc', 100])


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            data = f"date: {datetime.datetime.now().strftime('дата %d-%m-%Y время %H:%M:%S')} , " \
                   f"function_name: {old_function.__name__}," \
                   f" arguments: {args},{kwargs}, result: {old_function(*args, **kwargs)}\n"

            with open(f'{path}', 'a', encoding='utf-8') as log:
                log.write(data)
            return old_function(*args, **kwargs)

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
