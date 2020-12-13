"""
Created on 20.04.2019

:author: Ilya Krasnokutskiy
drawing tables

:functions:
    table_print
    table_part_print
    max_len_line
    table_check
"""


row_len = lambda r: len(r)          # Вычисляет количество строк в таблице
column_len = lambda r: len(r[0])    # Вычисляет количество столбцов в таблице


def table_check(list_m):
    """
    Проверка и заполнение недастоющих элементов таблицы
        замена всех элементов на строчный тип

    :param list_m: Входной двумерный массив
    :type  list_m: list

    :return: Возвращает заполненный список
    :rtype:  list
    """

    max_l = 0
    p = []

    t = []
    k = []

    for i in list_m:
        for j in i:
            t.append(str(j))
        k.append(t)
        t = []

    for l in k:
        if max_l < len(l):
            max_l = len(l)

    for n in k:
        while len(n) < max_l:
            n.append(" ")
        p.append(n)

    return p
 

def max_len_line(list_m, len_s = 0):  
    """
    Нахождение массива самых длинных строк в столбце / самой длинной строки

    :param list_m: Входной двумерный массив
    :type list_m:  list

    :param len_s: Переключатель результата (default 0)
    :type len_s:  int
    #len_s = 0: - возвращает список длин
    #len_s = 1: - возвращает максимальную длину
    

    :return: Возвращает массив самых длинных строк в столбце / самую длинную строку
    :rtype: list / int
    """

    max_l = 0
    max_all_l = 0
    len_list = []

    i = 0
    while i < column_len(list_m):
        j = 0    
        while j < row_len(list_m):
            if len(list_m[j][i]) > max_l:
                max_l = len(list_m[j][i])
                if max_l > max_all_l:
                    max_all_l = max_l
            j += 1
        i += 1
        len_list.append(max_l)
        max_l = 0

    if len_s == 0:
        return len_list
    if len_s == 1:
        return max_all_l
 

def table_part_print(list_m, select = 0, fixed_len = 0, part = 0, indent = 0, print_m = 1):      
    """
    Рисование частей таблицы / возвращение длины получившейся строки

    :param list_m: Входной двумерный массив
    :type list_m:  list

    :param select: Выделение первой строки (default 0)
    :type select:  int
    #len_s = 0: - не выделять первую строку
    #len_s = 1: - выделить первую строку

    :param fixed_len: Фиксированность ширины столбцов (default 0)
    :type fixed_len:  int
    #fixed_len = 0: - адаптивная ширина столбцов
    #fixed_len = 1: - фиксированная ширина столбцов

    :param part: Рисование частей таблицы (default 0)
    :type part:  int
    #part = 0: - рисование верхней части
    #part = 1: - рисование центрального блока   
    #part = 2: - рисование нижней части 

    :param indent: Размер дополнительных отступов (default 0)
    :type indent:  int

    :param print_m: рисование строки (default 1)
    :type print_m:  int
    #print_m = 0: - не рисовать строку
    #print_m = 1: - нарисовать строку

    :return: Возвращает длину получившейся строки
    :rtype:  int
    """

    st1 = ["┌","├","└"]
    st2 = ["┬","┼","┴"]
    st3 = ["┐","┤","┘"]

    st_spehial_1 = ["┏","┡", "┗"]
    st_spehial_2 = ["┳","╇", "┻"]
    st_spehial_3 = ["┓","┩", "┛"]

    l = ""
    str_main = []
    c = 0
    k = 0

    max_list = max_len_line(list_m, 0)
    max_all_l = max_len_line(list_m, 1)

    if select == 0:
        while c < ((column_len(list_m) * 2) - 1):
            if (c % 2) == 0:
                if fixed_len == 0:
                    str_main.append("─" * int(max_list[k]) + "─" * indent ) 
                if fixed_len == 1:
                    str_main.append("─" * max_all_l + "─" * indent )
                k += 1
            else:
                str_main.append(st2[part])
            c += 1

        str_main.insert(0, st1[part])
        str_main.insert(len(str_main), st3[part])

    if select == 1:
        while c < ((column_len(list_m) * 2) - 1):
            if (c % 2) == 0:
                if fixed_len == 0:
                    str_main.append("━" * int(max_list[k]) + "━" * indent ) 
                if fixed_len == 1:
                    str_main.append("━" * max_all_l + "━" * indent )
                k += 1
            else:
                str_main.append(st_spehial_2[part])
            c += 1

        str_main.insert(0, st_spehial_1[part])
        str_main.insert(len(str_main), st_spehial_3[part])

    if print_m == 1:
        print(l.join(str_main))

    return (len(l.join(str_main)))



def table_print(list_m, name = None, select = 0, fixed_len = 0, alignment = 1, indent = 0):        
    """
    Рисование таблицы 

    :param list_m: Входной двумерный массив
    :type list_m:  list

    :param name: Имя таблицы
    :type name:  str

    :param select: Выделение первой строки (default 0)
    :type select:  int
    #len_s = 0: - не выделять первую строку
    #len_s = 1: - выделить первую строку

    :param fixed_len: Фиксированность ширины столбцов (default 0)
    :type fixed_len:  int
    #fixed_len = 0: - адаптивная ширина столбцов
    #fixed_len = 1: - фиксированная ширина столбцов

    :param alignment: Выравнивание (default 1)
    :type alignment:  int
    #alignment = 0: - Выравнивание по левому краю
    #alignment = 1: - Выравнивание по центру
    #alignment = 2: - Выравнивание по правому краю

    :param indent: Размер дополнительных отступов (default 0)
    :type indent:  int
    """

    s = 0
    l_str = ""
    h = []

    list_m = table_check(list_m)

    len_name = table_part_print(list_m, 0, fixed_len, 0, indent, 0)

    if name != None:
        if len_name >= 9:                  
            h.append(name)
            len_name = ((len_name - len(name)) // 2)
            h.insert(0, " " * len_name)
            h.insert(len(h), " " * len_name)
            print(l_str.join(h))
        else:
            h.append(name)
            len_name = (len_name - 1) // 2
            h.insert(0, " " * len_name)
            h.insert(len(h), " " * len_name)
            print(l_str.join(h))

    if select == 0:
        table_part_print(list_m, 0, fixed_len, 0, indent)
        y = 1
    if select == 1:
        table_part_print(list_m, 1, fixed_len, 0, indent)
        y = 0

    if fixed_len == 0:
        max_list = max_len_line(list_m, 0)
    if fixed_len == 1:
        max_all_l = max_len_line(list_m, 1)

    st_spehial = ["┃","│"]

    for i in list_m:
        s += 1
        if s > 1:
            if select == 1:
                if s < 3:
                    y = 1
                    table_part_print(list_m, 1, fixed_len, 1, indent)
                else:
                    table_part_print(list_m, 0, fixed_len, 1, indent)
            else:
                table_part_print(list_m, 0, fixed_len, 1, indent)

        k = 0
        for j in i:
            if fixed_len == 0:
                if alignment == 0:
                    print(st_spehial[y] + j + " " * (max_list[k] + indent - len(j)), end = "")

                if alignment == 1:
                    print(st_spehial[y] + j.center(max_list[k] + indent), end = "")

                if alignment == 2:
                    print(st_spehial[y] + " " * (max_list[k] + indent - len(j)) + j, end = "")

            if fixed_len == 1:
                if alignment == 0:
                    print(st_spehial[y] + j + " " * (max_all_l + indent - len(j)), end = "")

                if alignment == 1:
                    print(st_spehial[y] + j.center(max_all_l + indent), end = "")

                if alignment == 2:
                    print(st_spehial[y] + " " * (max_all_l + indent - len(j)) + j, end = "")
            k += 1
        print(st_spehial[y])

    if select == 1:
        if row_len(list_m) == 1:
            table_part_print(list_m, 1, fixed_len, 2, indent)
        else:
            table_part_print(list_m, 0, fixed_len, 2, indent)
    else:
        table_part_print(list_m, 0, fixed_len, 2, indent)
