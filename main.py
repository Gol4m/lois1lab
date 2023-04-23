# Лабораторная работа № 1 по дисциплине ЛОИС
# Выполнена студентом группы 021702 БГУИР Голяницким Владиславом Александровичем

# Файл main.py предназначен для проверки, является ли введённная строка формулой СДНФ.
# Использование результатов иных лиц:
# Функции is_valid, count_bracket, find_unary, find_binary были использованы для проверки является ли строка
# формулой в сокращённом языке логики высказываний, автор - Василёнок Анна, гр. 021702

# Задание: "проверить, является ли формула СДНФ".


disjunction = "\\/"
conjunction = "/\\"

ATOM = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
        'Y', 'Z']

OPERATIONS = ['\\/', '/\\', '!', '~', '->']
OPERATIONS_WHITOUT_COUNJUCTION = ['\\/', '!', '~', '->']


def is_valid(formula):
    iteration = count_bracket(formula)
    result = True
    while formula not in ATOM:
        if iteration == 0:
            return False
        else:
            formula = find_unary(formula)
            formula = find_binary(formula)
            iteration -= 1
            result = True
    return result


def count_bracket(formula):
    return formula.count('(')


def find_unary(formula):
    for symbol in ATOM:
        formula = formula.replace(f'(!{symbol})', 'N')
    return formula


def find_binary(formula):
    for operation in OPERATIONS:
        for symbol_1 in ATOM:
            for symbol_2 in ATOM:
                formula = formula.replace(f'({symbol_1}{operation}{symbol_2})', 'N')
    return formula

#
# def check_conjunction(conj):  # если вокруг дизъюнкций есть операции корме конъюкции то возвращаем False
#     answer = True
#     conj = conj.replace("!", "")  # удаляем все ! для дальнейшей проверки
#     for operation in OPERATIONS_WHITOUT_COUNJUCTION:
#         for symbol_1 in ATOM:
#             for symbol_2 in ATOM:
#                 if f'{symbol_1}{operation}{symbol_2}' in conj:
#                     answer = False
#     return answer
#
#
# def check_negation(conj):
#     conj = conj.replace(conjunction, "")  # Удаляем все коньюкции
#     return conj
#
#
# def is_sdnff(formula):
#     answer = True
#     disj_pos_list = []
#     if disjunction in formula:
#         disj_pos_first = formula.index(disjunction)
#         disj_pos_list.append(disj_pos_first)
#         for index, pos in enumerate(disj_pos_list):
#             if formula.find(disjunction, pos + 1) == -1:
#                 break
#             disj_pos_list.append(formula.index(disjunction, pos + 1))
#
#
#         # проверка отрицаний
#         negation_check_list = []
#         negation_check_list.append(check_negation(formula[0:disj_pos_list[0]]))
#
#         i = 0
#         while i <= len(disj_pos_list) - 1:
#             if i == len(disj_pos_list) - 1:
#                 negation_check_list.append(check_negation(formula[disj_pos_list[i] + 2: len(formula)]))
#                 break
#             negation_check_list.append(check_negation(formula[disj_pos_list[i] + 2:disj_pos_list[i + 1]]))
#             i += 1
#
#         # print(negation_check_list)
#         for i in range(len(negation_check_list) - 1):
#             for j in range(i + 1, len(negation_check_list)):
#                 if negation_check_list[i] == negation_check_list[j]:
#                     # print("есть одинаковые")
#                     answer = False
#
#         # проверка что между дизъункциями стоят конъюкции
#         conjunction_br_checks = []
#
#         # print(formula[0:disj_pos_list[0]])
#         conjunction_br_checks.append(check_conjunction(formula[0:disj_pos_list[0]]))
#         i = 0
#         while i <= len(disj_pos_list) - 1:
#             if i == len(disj_pos_list) - 1:
#                 conjunction_br_checks.append(check_conjunction(formula[disj_pos_list[i] + 2: len(formula)]))
#                 break
#             conjunction_br_checks.append(check_conjunction(formula[disj_pos_list[i] + 2:disj_pos_list[i + 1]]))
#             i += 1
#
#         # Если есть хоть одна ошибка из всех скобок то возвращаем False
#         if False in conjunction_br_checks:
#             answer = False
#     else:
#         answer = False
#
#     return answer

def change_negation(formula):
    atom_dict = dict()
    ind = 0
    for symbol1 in ATOM:
        if f'(!{symbol1})' in formula:
            while f'(!{symbol1})' in formula:
                formula = formula.replace(f'(!{symbol1})', f'{ind}', 1)
                atom_dict.update({f'{ind}': f'!{symbol1}'})
                ind += 1
    return formula, atom_dict

def change_conjution(formula, atom_dict):
    atom_dict_keys = list(atom_dict.keys())
    ind = len(atom_dict_keys)
    print(ind)

    for symbol1 in ATOM:
        for symbol2 in ATOM:
            if symbol2 in formula:
                if f'({symbol1}/\\{symbol2})' in formula:
                    while f'({symbol1}/\\{symbol2})' in formula:
                        formula = formula.replace(f'({symbol1}/\\{symbol2})', str(ind), 1)
                        atom_dict.update({f'{ind}': f'{symbol1}{symbol2}'})
                        ind += 1
    atom_dict_keys = list(atom_dict.keys())
    print(formula)
    for key in atom_dict_keys:
        for key2 in atom_dict_keys:
            for symbol in ATOM:
                if f'({symbol}/\\{key})' in formula:
                    while f'({symbol}/\\{key})' in formula:
                        formula = formula.replace(f'({symbol}/\\{key})', key)
                        atom_dict.update({f'{key}': f'{symbol}{atom_dict[key]}'})
                if f'({key}/\\{symbol})' in formula:
                    while f'({key}/\\{symbol})' in formula:
                        formula = formula.replace(f'({key}/\\{symbol})', key)
                        atom_dict.update({f'{key}': f'{atom_dict[key]}{symbol}'})
                if f'({key}/\\{key2})' in formula:
                    formula = formula.replace(f'({key}/\\{key2})', key)
                    if int(key) != len(atom_dict_keys)-1:
                        atom_dict.update({f'{key}': f'{atom_dict[key]}{atom_dict[key2]}'})
                        atom_dict.pop(key2)
    print(formula, atom_dict)
    return formula, atom_dict


def change_disjunction(formula, atom_dict):
    print(len(atom_dict))
    print(list(atom_dict.keys()))
    i = 0
    while i != len(atom_dict) - 1:
        for key1 in list(atom_dict.keys()):
            for key2 in list(atom_dict.keys()):
                if f'({key1}\\/{key2})' in formula:
                    print(formula)
                    formula = formula.replace(f'({key1}\\/{key2})', key1)
                    print(formula)

        i += 1
    return formula

def is_sdnf2(formula):
    print("Проверяем формулу:", formula)

    answer = False
    atom_dict = {}
    # Сворачиваем отрицания в ключи
    formula, atom_dict = change_negation(formula)

    print(formula, atom_dict)
    atom_dict_keys = atom_dict.keys()

    # Сворачиваем конъюкции в ключи
    formula, atom_dict = change_conjution(formula, atom_dict)
    print(formula, atom_dict)
    if formula in list(atom_dict.keys()):
        answer = False

    # Сворачиваем дизъюнкции в ключи
    formula = change_disjunction(formula, atom_dict)
    if formula in list(atom_dict.keys()):
        answer = True

    atoms_to_check = []
    for key in atom_dict:
        atoms_to_check.append(atom_dict[key])

    # Проверяем на одинаковые символы
    for i in range(len(atoms_to_check) - 1):
        for j in range(i + 1, len(atoms_to_check)):
            if atoms_to_check[i] == atoms_to_check[j]:
                #print("есть одинаковые")
                answer = False


    return answer

# (A/\B)  !!!!!!
# (A\/(!A))  !!!!!

# ((A/\(B\/(!A)))/\B) не проблема)
if __name__ == "__main__":
    #(((((!A)/\B)/\C)\/(((!A)/\B)/\(!C)))\/((A/\B)/\C)) СДНФ
    #(((((!A)/\B)\/(A/\(!B)))\/(A/\B))\/((!A)/\(!B)))
    #'((((A/\B)\/(A/\(!B)))\/((!A)/\B))\/((!A)/\(!B)))'
    #(((((!A)->B)/\C)\/(((!A)/\B)~(!C)))\/((A/\B)/\C))  Формула написана правильно, но это не СДНФ

    sdnf = input("Введите формулу: ")
    # sdnf_part_2 = sdnf.replace('(', '')
    # sdnf_part_2 = sdnf_part_2.replace(')', '')
    if is_valid(sdnf) and is_sdnf2(sdnf):
        print("Это СДНФ")
    elif is_valid(sdnf):
        print("Формула написана правильно, но это не СДНФ")
    else:
        print("Ошибка в формуле")



