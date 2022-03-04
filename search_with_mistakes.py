import numpy as np
import pandas as pd
import math
import re
import sys

# вычисление расстояния Левенштейна между 2 словами
def ratio_coef(input_str: str, correct_str: str):
    M = len(input_str)
    N = len(correct_str)
    matrix = np.zeros((M + 1, N + 1), dtype = int) # матрица длиной введенного
    for i in range(0, M + 1):
        matrix[i, 0] = i
    for i in range(0, N + 1):
        matrix[0, i] = i

    for i in range(1, M + 1):
        for j in range(1, N + 1):
            if input_str[i - 1] == correct_str[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[i, j] = min(matrix[i - 1, j - 1] + cost,
                                matrix[i - 1, j] + 1,
                                matrix[i, j - 1] + 1)
    return matrix[M, N]

# получение индекса схожести к введенному слову
def get_index(correct_str, length_input):
    length_correct = len(correct_str)
    max_length = max(length_correct, length_input)
    min_coef = 2.75
    if abs(length_correct - length_input) > math.ceil(max_length / min_coef):
        return 0
    else:
        dist = ratio_coef(input_str, correct_str)
#    print(correct_str, dist, 1.0 - dist/max (length_input, length_correct))
    return 1.0 - dist/max_length



# НАЧАЛО ВЫПОЛНЕНИЯ ПРОГРАММЫ
df_decision = pd.read_csv('номера_судебных_решений.txt', encoding='cp1251', sep = '\n', header = None)
df_laws = pd.read_csv('номера_законов.txt', encoding='cp1251', sep = '\n', header = None)

print('Введите запрос: ')
input_str = input()
input_str = input_str.lower()
length_input = len(input_str)
if re.fullmatch(r'^[\W]+$', input_str):
    print("Неверный ввод!")
    sys.exit()

input_str_without_symb = re.sub(r'[\W]+', r'', input_str) # преобразование строки, состоящей из букв и цифр (исключая другие символы)
len_input_str_without_symb = len(input_str_without_symb)

pattern = ""
for i in range(0, len_input_str_without_symb):
    pattern += "[\W0]*" + "[" + input_str_without_symb[i] + input_str_without_symb[i].swapcase() + "]"
pattern += ".*"
reg_exp = r'({})'.format(pattern)
#print(reg_exp)

# поиск среди номеров судебных решений
df_decision = df_decision[0].str.extract(reg_exp).dropna()
current_list = df_decision[0].tolist()
print('\nСреди номеров судебных решений:')
for score, out_str in list(sorted(((get_index(str.lower(), length_input), str) for str in current_list), reverse = True))[:5]:
    if score != 0:
        print(f"{out_str:20}{100*score: 3.2f}")


# поиск среди номеров номеров законов
df_laws = df_laws[0].str.extract(reg_exp).dropna()
current_list = df_laws[0].tolist()
print('\nСреди номеров законов:')
for score, out_str in list(sorted(((get_index(str.lower(), length_input), str) for str in current_list), reverse = True))[:5]:
    if score != 0:
        print(f"{out_str:20}{100*score: 3.2f}")
