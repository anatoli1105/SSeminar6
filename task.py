#2 - Реализовать RLE алгоритм. реализовать модуль сжатия и восстановления данных. Входные и выходные данные хранятся в отдельных файлах 
# (в одном файлике отрывок из какой-то книги, а втором файлике — сжатая версия этого текста). 

text=[]
path='text.txt'
data=open (path,'r')
for i in data:
    text.append(i)
data.close()
print (text)
i=0
b=1
rle_coding=[]
N=text[0]
rle_coding2=[]
while i<len(N)-1:
    if N[i]==N[i+1]:
        b+=1
    else:
        rle_coding.append(b)
        rle_coding.append(N[i])
        b=1
    i+=1
rle_coding.append(b)
rle_coding.append(N[-1])
rle_coding_2=[]
string_name = [str(i) for i in rle_coding]
rle_coding_2=",".join(string_name)
print(rle_coding_2)
print(rle_coding)
data=open('text4.txt','w')
data.writelines(rle_coding_2)
data.close()
j=0
decoder=[]
while j< len(rle_coding):
    for i in range(rle_coding[j]):
        decoder.append(rle_coding[j+1])
    j+=2
decoder=''.join(decoder)
print(decoder)
#======================================================
#3 -  ROT13 - это простой шифр подстановки букв, который заменяет букву буквой, 
#которая идет через 13 букв после нее в алфавите. ROT13 является примером шифра Цезаря.
#Создайте функцию, которая принимает строку и возвращает строку, зашифрованную с помощью Rot13 . 
#Если в строку включены числа или специальные символы, они должны быть возвращены как есть. 
#Также создайте функцию, которая расшифровывает эту строку обратно (некий начальный аналог шифрования сообщений). 
#Не использовать функцию encode.
#| A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U | V | W | X | Y | Z |
#--------------------------------------------------------------------------------------------------------  
#| N | O | P | Q | R | S | T | U | V | W | X | Y | Z | A | B | C | D | E | F | G | H | I | J | K | L | M |


text = "abcrtfghjykffffftrewuy"
alphabet = "abcdefghijklmnopqrstuvwxyz"
ro13_text = "".join([alphabet[(alphabet.find(a)+13)%26] for a in text])
print(ro13_text)

#==============================================================================

# Написать программу вычисления арифметического выражения заданного строкой. Используются операции +,-,/,*. приоритет операций стандартный.

import re

def GN(func, *args):
    def exec(text: str):
        return func(text, *args)
    return exec

def token(text: str, token_text: str):
    if text.startswith(token_text):
        return token_text, text[len(token_text):]
    return None, text

def rexpr(text: str, regex: str):
    text = text.lstrip()
    res = re.match(regex, text)
    if res:
        return res.group(0), text[res.end():]
    else:
        return None, text

def serial(text, *funcs):
    res, rest = [], text
    for func in funcs:
        resd, restd = func(rest)
        if resd is None:
            return None, text
        res.append(resd)
        rest = restd
    if len(res) == 0:
        return None, text
    return res, rest

def alternative(text, *funcs):
    for func in funcs:
        res, rest = func(text)
        if res is not None:
            return res, rest
    return None, text

def optional(text, func):
    res, rest = func(text)
    return [res], rest

def num(expr):
    res, rest = rexpr(expr, r"^[+-]?\d(\.\d+)?")
    if res is not None:
        return float(res), rest
    return res, rest

def value(expr):
    sign = GN(rexpr, r"[+-]")
    maybe_sign = GN(optional,  sign)
    val = GN(alternative, num, grouping)
    res, rest = serial(expr, maybe_sign, val)

    if res is None:
        return None, expr

    numb = res[1]
    if res[0][0] == "-":
        return -numb, rest
    return numb, rest

def grouping(expr):
    opened_bracket = GN(token, "(") 
    closed_bracket = GN(token, ")")  

    res, rest = serial(expr, opened_bracket, term, closed_bracket)

    if res is None:
        return None, expr
    return res[1], rest

def mul(expr):
    full_expr = GN(serial, value, GN(rexpr, r"[*/]"), mul)
    res, rest = alternative(expr, full_expr, value)

    if res is None:
        return None, expr

    if isinstance(res, float):
        return res, rest

    numb1 = res[0]
    op = res[1]
    numb2 = res[2]

    if op == "*":
        return numb1 * numb2, rest
    if op == "/":
        return numb1 / numb2, rest

    return None, expr

def sum(expr):
    full_expr = GN(serial, mul, GN(rexpr, r"[+-]"), sum)
    res, rest = alternative(expr, full_expr, mul)

    if res is None:
        return None, expr

    if isinstance(res, float):
        return res, rest

    numb1 = res[0]
    op = res[1]
    numb2 = res[2]

    if op == "+":
        return numb1 + numb2, rest
    if op == "-":
        return numb1 - numb2, rest

    return None, expr

def term(expr):
    return sum(expr)


print(term("(2 + 2) * 2/1"))

