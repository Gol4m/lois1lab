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

    for symbol1 in ATOM:
        for symbol2 in ATOM:
            if symbol2 in formula:
                if f'({symbol1}/\\{symbol2})' in formula:
                    while f'({symbol1}/\\{symbol2})' in formula:
                        formula = formula.replace(f'({symbol1}/\\{symbol2})', str(ind), 1)
                        atom_dict.update({f'{ind}': f'{symbol1}{symbol2}'})
                        ind += 1
    atom_dict_keys = list(atom_dict.keys())

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

    return formula, atom_dict


def change_disjunction(formula, atom_dict):
    i = 0
    while i != len(atom_dict) - 1:
        for key1 in list(atom_dict.keys()):
            for key2 in list(atom_dict.keys()):
                if f'({key1}\\/{key2})' in formula:
                    formula = formula.replace(f'({key1}\\/{key2})', key1)
        i += 1
    return formula


def small_sdnf(formula):
    for symbol in ATOM:
        if f'((!{symbol})\\/{symbol})' == formula:
            return True
        if f'({symbol}\\/(!{symbol}))' == formula:
            return True
    return False


def is_sdnf2(formula):
    print("Проверяем формулу:", formula)

    if "\\/" not in formula:
        return False

    if small_sdnf(formula):
        return True

    answer = False

    # Сворачиваем отрицания в ключи
    formula, atom_dict = change_negation(formula)


    # Сворачиваем конъюкции в ключи
    formula, atom_dict = change_conjution(formula, atom_dict)
    #print(formula, atom_dict)
    if formula in list(atom_dict.keys()):
        answer = False

    # Сворачиваем дизъюнкции в ключи
    formula = change_disjunction(formula, atom_dict)
    #print(formula, atom_dict)
    if formula in list(atom_dict.keys()):
        answer = True

    # Проверяем на одинаковые символы
    atoms_to_check = []
    for key in atom_dict:
        atoms_to_check.append(atom_dict[key])

    for i in range(len(atoms_to_check) - 1):
        for j in range(i + 1, len(atoms_to_check)):
            if atoms_to_check[i] == atoms_to_check[j]:
                #print("есть одинаковые")
                answer = False

    # Проверяем на последовательность букв
    letter_sequence = []
    for letter in atoms_to_check:
        letter2 = letter.replace("!", "")
        letter_sequence.append(letter2)

    for i in range(len(letter_sequence) - 1):
        for j in range(i + 1, len(letter_sequence)):
            if letter_sequence[i] != letter_sequence[j]:
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
    if is_valid(sdnf) and is_sdnf2(sdnf):
        print("Это СДНФ")
    elif is_valid(sdnf):
        print("Формула написана правильно, но это не СДНФ")
    else:
        print("Ошибка в формуле")



