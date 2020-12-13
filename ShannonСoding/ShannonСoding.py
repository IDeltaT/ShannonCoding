#----------------------------------------------
# Program by Krasnokutskiy.I.
# VKB-33
#
# Version   ---Date---    ----- Info -----
#   1.0     05.12.2020    Initial version
#
# ShannonCoding 
# Алгоритм Шеннона
# (Построение дерева кодовых слов, расчет
#  энтропии и средней длины кодовых слов)
#----------------------------------------------


import string
from ete3 import Tree, TreeStyle
from math import log2, ceil, fsum
from printable import table_print
from floatbin import float_to_binary
from codewordsconv import codewords_conversion


def input_probabilities():
    '''
    Запрос вероятностей или же выход из программы.

    :return: Возвращает список вероятностей или код ошибки.
    :rtype:  list
    '''

    print("Введите вероятности через пробел (минимум: 2, максимум: 52)")
    print("Для выхода из программы введите 'ex':")

    response = input().split()
    if (response == ["ex"]):
        exit()

    # Проверка на количество вводимых вероятностей (минимум: 2, максимум: 52)
    elif (len(response) <= 1):
        print("Введите минимум два значения!")
        return ["er"]
    elif (len(response) > 52):
        print("Максимальное количество вводимых вероятностей: 52 !\n")
        return ["er"]
    else:
        try:
            # Преобразование str -> float
            probabilities = list(map(float, response))  

        except:
            print("Неверный формат ввода! \n")
            return ["er"]

    # Обрезание нулей
    probabilities = [i for i in probabilities if i != 0]

    # Проверка на 1
    if 1 in probabilities:
        print('В вероятностях присутствует 1!')
        return ["er"]    

    # Проверка на отрицательные числа
    for i in probabilities:
        if(i <= 0):
            print("Вероятность не может быть отрицательной, либо равной нулю! \n")
            return ["er"]
         
    # Проверка условия нормировки (сумма вероятностей должна быть равна 1)
    prob_sum = fsum(probabilities)
    print('Сумма вероятностей:', prob_sum)
    if (prob_sum == 1):
        print('Условие нормировки выполнено\n')
        return probabilities
    else:
        print('Условие нормировки не выполнено!!!\n')
        return ["er"]


def sorting_dictionary_value(char_dict):
    '''
    Сортировка словаря по вероятности (по убыванию).

    :param char_dict: Словарь, где в роли ключей выступают символы, 
        в роли значений - вероятности.
    :type char_dict:  dict

    :return: Кортеж, содержащий список отсортированных вероятностей и список 
        соответствующих им символов.
    :rtype:  (list, list)
    '''

    sort_char = []
    sort_prob = []

    sort_char_dict = list(char_dict.items())
    sort_char_dict.sort(key = lambda i: i[1], reverse = True)
    for i in sort_char_dict:
        sort_char.append(i[0])
        sort_prob.append(i[1])

    return (sort_char, sort_prob)


def probability_summation(sort_prob):
    '''
    Пошаговое суммирование отсортированных вероятностей с сохранением шагов в список.

    :param sort_prob: Список, содержащий отсортированные вероятности.
    :type sort_prob:  list

    :return: Список накопления суммы вероятностей.
    :rtype:  list
    '''

    prob_sum = [0.0]

    k = 0
    for i in sort_prob[:-1]:
        prob_sum.append(prob_sum[k] + i)
        k += 1

    return prob_sum


def calculating_word_length(sort_prob):
    '''
    Подсчет итоговых длин кодовых слов.

    :param sort_prob: Список, содержащий отсортированные вероятности.
    :type sort_prob:  list

    :return: Кортеж, содержащий список длин кодовых слов и список логарифмов
        по основанию 2 от отсортированных вероятностей.
    :rtype:  (list, list)
    '''

    words_len = []
    log_probs = []
    
    for i in sort_prob:
        log_prob = -log2(i)
        log_probs.append(round(log_prob, 4))
        words_len.append(ceil(log_prob))

    return(words_len, log_probs)


def calculation_code_words(prob_sum, words_len):
    '''
    Расчет итоговых кодовых слов.

    :param prob_sum: Список, содержащий накопления суммы вероятностей.
    :type prob_sum:  list

    :param words_len: Список, содержащий длины кодовых слов.
    :type words_len:  list

    :return: Список итоговых кодовых слов.
    :rtype:  list
    '''
  
    code_words = []
    k = 0
    for i in prob_sum:
        l = words_len[k]
        binary_code = float_to_binary(i).split('.')[-1].ljust(l, '0')
        code_words.append(binary_code[:words_len[k]])
        k += 1

    return code_words


def entropy_calculation(number_char, sort_prob, log_probs):
    '''
    Расчет энтропии источника.

    :param number_char: Количество вероятностей.
    :type number_char:  int

    :param sort_prob: Список, содержащий отсортированные вероятности.
    :type sort_prob:  list

    :param log_probs: Список, содержащий логарифмы
        по основанию 2 от отсортированных вероятностей.
    :type log_probs:  list

    :return: Энтропия источника.
    :rtype:  float
    '''

    H = 0
    for i in range(number_char):
        H += sort_prob[i] * log_probs[i]
    return H


def average_len_codewords(number_char, sort_prob, words_len):
    '''
    Расчет средней длины кодовых слов.

    :param number_char: Количество вероятностей.
    :type number_char:  int

    :param sort_prob: Список, содержащий отсортированные вероятности.
    :type sort_prob:  list

    :param words_len: Список, содержащий длины кодовых слов.
    :type words_len:  list

    :return: Средняя длина кодовых слов.
    :rtype:  float
    '''
 
    K = 0
    for i in range(number_char):
        K += sort_prob[i] * words_len[i]
    return K


def tree_show(Newick_string, output_format = 1, rotation = -90):
    '''
    Построение и вывод дерева.

    :param Newick_string: скобочная последовательность (The Newick format).
    :type Newick_string:  str

    :param output_format: Формат вывода. (default 1)
    :type output_format:  int
    #output_format = 0: - сохранение в PNG формате.
    #output_format = 1: - Вывод на экран (интерактивный режим).

    :param rotation: Поворот дерева в градусах. (default -90)
    :type rotation:  int
    '''

    t = Tree(Newick_string)

    ts = TreeStyle()
    ts.min_leaf_separation = 60    
    ts.rotation = -90

    if (output_format == 1):
        t.show(tree_style = ts )
    elif (output_format == 0):
        t.render('tree1.PNG', tree_style = ts, w = 400)
    else:
        print('Неверный аргумент tree_show: output_format!')


def main():
    '''
    Главная функция.
    '''

    # Примеры для проверки
    # 0.123 0.114 0.654 0.782 0.3333 0.1 0.0001 0.487 0.001
    # 0.21 0.01 0.45 0.1 0.1 0.13

    # Ввод вероятностей
    probabilities = input_probabilities()
    while (probabilities == ["er"]):
        probabilities = input_probabilities()
    
    # Подсчет количества символов
    number_char = len(probabilities)
    print("Количество символов: n =", number_char)

    # Связь символа и вероятности
    # string.ascii_letters
    # abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ - 52
    char_dict = {}
    
    for i in range(number_char):
        char_dict[string.ascii_letters[i]] = probabilities[i]

    # Вывод получившейся таблицы (символ - вероятность)
    print()
    table_print([list(char_dict.keys()),probabilities], indent = 2, name = "Введенные данные")

    print()

    # Сортировка словаря по значению
    sort_char, sort_prob = sorting_dictionary_value(char_dict)

    # Вывод получившейся таблицы (символ - вероятность(отсортирована))
    table_print([sort_char, sort_prob], indent = 2, name = "Сортировка по вероятности")

    # Суммирование вероятностей (с сохранением промежуточных сумм)
    prob_sum = probability_summation(sort_prob)

    print()

    # Вычисление длины будущих кодовых слов
    words_len, log_probs = calculating_word_length(sort_prob)

    # Вычисление кодовых слов 
    code_words = calculation_code_words(prob_sum, words_len)

    # Заполнение итоговой таблицы
    final_table = [['Буква', 'Вероятность', 'Длина кодового слова (K)', 'Кодовое слово']]

    for i in range(number_char):
        final_table.append([sort_char[i], sort_prob[i], words_len[i], code_words[i]])

    # Вывод итоговой таблицы
    table_print(final_table, indent = 2, name = "Итоговая таблица", select = 1)

    print()

    # Расчет энтропии источника
    H = entropy_calculation(number_char, sort_prob, log_probs)
    print('Энтропия источника:', round(H, 4))

    # Расчет средней длины кодовых слов
    K = average_len_codewords(number_char, sort_prob, words_len)
    print('Средняя длина кодовых слов:', round(K, 4))

    print()

    # Построение дерева
    Newick_string = codewords_conversion(code_words, sort_char)
    tree_show(Newick_string, 1)


if __name__ == "__main__":
    '''
    Выполнение программы.
    '''
    main()