#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Precedencia y asociatividad para operadores de regex
PRECEDENCE = {
    '^': (4, 'right'),    # Exponenciación
    '*': (3, 'left'),     # Cero o más
    '·': (2, 'left'),     # Concatenación interna (oculta en resultado)
    '|': (1, 'left'),     # Alternación (OR)
}


def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        c = expr[i]
        if c == '\\':
            if i + 1 >= len(expr): raise ValueError("Escape '\\' sin carácter a continuación")
            tokens.append('\\' + expr[i+1]); i += 2
        elif c == '[':
            j = i + 1
            while j < len(expr) and expr[j] != ']':
                if expr[j] == '\\': j += 2
                else: j += 1
            if j >= len(expr) or expr[j] != ']': raise ValueError("Clase '[' sin cerrar con ']' en la expresión")
            tokens.append(expr[i:j+1]); i = j + 1
        else:
            tokens.append(c); i += 1
    return tokens


def expand_quantifiers(tokens):
    result = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in ('+', '?'):
            if not result: raise ValueError(f"Operador '{t}' sin operando previo")
            prev = result.pop()
            if t == '+': result.extend([prev, prev, '*'])
            else:        result.extend(['(', prev, '|', 'ε', ')'])
            i += 1
        else:
            result.append(t); i += 1
    return result


def validate(tokens):
    prev = None
    for t in tokens:
        if t == '*':
            if prev is None or prev in ('|', '('): raise ValueError("Operador '*' mal posicionado")
        if t == '|':
            if prev is None or prev == '|': raise ValueError("Operador '|' mal posicionado o repetido")
        prev = t
    if prev in ('|', '('): raise ValueError(f"Expresión termina con operador inválido '{prev}'")


def add_concatenation(tokens):
    output = []
    def is_operand(x): return x not in ('|', '(', ')')
    prev = None
    for t in tokens:
        if prev is not None and (is_operand(prev) or prev == ')') and (is_operand(t) or t == '('):
            output.append('·')
        output.append(t); prev = t
    return output


def shunting_yard(tokens):
    output = []
    stack = []
    for t in tokens:
        if t == '(':
            stack.append(t)
        elif t == ')':
            while stack and stack[-1] != '(': output.append(stack.pop())
            stack.pop()
        elif t in PRECEDENCE:
            p1, assoc1 = PRECEDENCE[t]
            while stack and stack[-1] in PRECEDENCE:
                p2, _ = PRECEDENCE[stack[-1]]
                if p2 > p1 or (p2 == p1 and assoc1 == 'left'): output.append(stack.pop())
                else: break
            stack.append(t)
        else:
            output.append(t)
    while stack: output.append(stack.pop())
    return output


def main():
    filename = 'expreS.txt'
    try:
        lines = open(filename, encoding='utf-8').read().splitlines()
    except IOError as e:
        print(f"Error leyendo '{filename}': {e}"); return

    for idx, line in enumerate(lines, start=1):
        expr = line.strip()
        if not expr: continue
        try:
            tokens = tokenize(expr)
            tokens = expand_quantifiers(tokens)
            validate(tokens)
            concat_tokens = add_concatenation(tokens)
            postfix = shunting_yard(concat_tokens)
            postfix_clean = ''.join(t for t in postfix if t != '·')
            print(f"=== Línea {idx}: {expr} ===")
            print(f"(a) Postfija: {postfix_clean}\n")
        except ValueError as err:
            print(f"Error en línea {idx} ('{expr}'): {err}\n")

if __name__ == '__main__': main()
