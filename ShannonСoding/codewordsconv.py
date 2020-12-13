"""
Created on 03.12.2020

:author: Ilya Krasnokutskiy
converting codewords to Newick format

:functions:
    add_brackets
    add_commas
    codewords_conversion
"""


def add_brackets(code_words: list, code_chars: list) -> str:
    '''
    Перевод кодовых слов в скобочную последовательность (The Newick format).
    Должно выполнятся равенство: len(code_words) = len(code_chars)

    :param code_words: Отсортированный (во возрастанию) список кодовых слов (str).
    :type code_words:  list

    :param code_chars: Список соответствующих кодовым словам символов (str).
    :type code_chars:  list

    :return: Строка скобочной последовательности.
    :rtype:  str
    '''

    #((.  c - 00,(.  a - 011)),((.  f - 101),((.  d - 1100),(.  e - 1110,(((.  b - 1111110)))))));

    # Проверка на совпадение длин списков
    if(len(code_words) != len(code_chars)):
        print('Длины списков не совпадают!')
        return 'er'

    code_words = list(reversed(code_words))
    code_chars = list(reversed(code_chars))

    max_word = code_words[0]
    dif_w1 = 0
    dif_w2 = 0

    # Инициализация строки
    back_brackets = len(max_word) - 1
    result = '.  ' + code_chars[0] + ' - ' + max_word + ')'*back_brackets

    # Наполнение строки
    for k in range(len(code_words) - 1):
        w1 = code_words[k]
        w2 = code_words[k + 1]

        for ind in range(len(w2)):
            if(w2[ind] != w1[ind]):
                dif_w1 = len(w1) - ind - 1
                dif_w2 = len(w2) - ind - 1

                result = '.  ' + code_chars[k + 1] + ' - ' + w2 + ')'*dif_w2 + '('*dif_w1 + result
                break

    brackets = 0
    for i in result:
        if i == ')':
            brackets += 1
        elif i == '(':
            brackets -= 1

    result ='('*abs(brackets) + result

    return result


def add_commas(brackets_line: str) -> str:
    '''
    Добавление запятых в скобочную последовательность.

    :param brackets_line: Строка скобочной последовательности.
    :type brackets_line:  str

    :return: Строка скобочной последовательности в формате Ньюика.
    :rtype:  str
    '''

    commas = []

    for i in range(len(brackets_line) - 1):
        first_sim = brackets_line[i]
        second_sim = brackets_line[i + 1]
        if ((first_sim not in [',', '('] or first_sim == ')') and second_sim == '('):
            commas.append(i + 1)
        if ((first_sim not in ['(']) and second_sim == '.'):
            commas.append(i + 1)

    commas = list(reversed(commas))

    for i in commas:
        brackets_line = brackets_line[0:i] + ',' + brackets_line[i:]

    brackets_line = '(' + brackets_line + ');'

    return brackets_line


def codewords_conversion(code_words: list, code_chars: list) -> str:
    '''
    Перевод кодовых слов в формат Ньюика (The Newick format).
    Длина списка code_words должна быть равна длине списка code_chars !!!

    :param code_words: Отсортированный (во возрастанию) список кодовых слов (str).
    :type code_words:  list

    :param code_chars: Список соответствующих кодовым словам символов (str).
    :type code_chars:  list

    :return: Строка скобочной последовательности в формате Ньюика.
    :rtype:  str
    '''

    # Запасная сортировка
    code_words = sorted(code_words)

    if(len(code_words) != len(code_chars)):
        print('Длины списков не совпадают!')
        return 'er'

    brackets_line = add_brackets(code_words, code_chars)
    result = add_commas(brackets_line)
    #print(result)
    return result