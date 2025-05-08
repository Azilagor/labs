import re
from typing import List

# Приоритеты операторов
priority = {
    '|': 1,
    '.': 2,
    '*': 3,
    '+': 3,
    '?': 3
}

def tokenize(regex: str) -> List[str]:
    tokens = []
    i = 0
    while i < len(regex):
        c = regex[i]
        if c == '&':
            if i + 1 >= len(regex):
                raise ValueError("Dangling & escape at end of regex")
            tokens.append(regex[i+1])
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
        elif c == '{':  # повторение {n} или {n,m}
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
    output = []
    stack = []
    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  
        elif token in priority:
            while (stack and stack[-1] in priority and
                   priority[stack[-1]] >= priority[token]):
                output.append(stack.pop())
            stack.append(token)
        else:
            output.append(token)
    while stack:
        output.append(stack.pop())
    return output
