import re
from typing import List

# Приоритеты операторов
precedence = {
    '|': 1,
    '.': 2,
    '*': 3,
    '+': 3,
    '?': 3
}

def tokenize(regex: str) -> List[str]:
    """
    Разбивает регулярное выражение на токены.
    """
    tokens = []
    i = 0
    while i < len(regex):
        c = regex[i]
        if c == '\\':  # экранированный символ
            tokens.append(regex[i:i+2])
            i += 2
        elif c in {'(', ')', '|', '.', '*', '+', '?'}:
            tokens.append(c)
            i += 1
        elif c == '[':  # множество символов
            j = i + 1
            chars = []
            while j < len(regex) and regex[j] != ']':
                chars.append(regex[j])
                j += 1
            if j == len(regex):
                raise ValueError("Unmatched [ in expression")
            group = '|'.join(chars)
            tokens.append('(')
            tokens += list(group)
            tokens.append(')')
            i = j + 1
        elif c == '{':  # повторение: {n} или {n,m}
            j = i
            while j < len(regex) and regex[j] != '}':
                j += 1
            tokens.append(regex[i:j+1])
            i = j + 1
        else:
            tokens.append(c)
            i += 1
    return tokens


def insert_concat(tokens: List[str]) -> List[str]:
    """
    Вставляет символ конкатенации '.' там, где она подразумевается.
    Например: ab → a.b
    """
    result = []
    for i in range(len(tokens)):
        token = tokens[i]
        result.append(token)
        if i + 1 < len(tokens):
            t1, t2 = token, tokens[i + 1]
            if (
                t1 not in {'(', '|'} and
                t2 not in {')', '|', '*', '+', '?'}
            ):
                result.append('.')
    return result


def to_postfix(tokens: List[str]) -> List[str]:
    """
    Преобразует список токенов в постфиксную форму (обратную польскую нотацию).
    """
    output = []
    stack = []
    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # убираем '('
        elif token in precedence:
            while (stack and stack[-1] in precedence and
                   precedence[stack[-1]] >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)
        else:
            output.append(token)
    while stack:
        output.append(stack.pop())
    return output
