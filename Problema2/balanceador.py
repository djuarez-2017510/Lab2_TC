#!/usr/bin/env python3
import sys

def balance_check(expr):
    stack = []
    logs = []
    # Mapeo para verificar correspondencia de símbolos de cierre
    pairs = {')': '(', ']': '[', '}': '{'}

    for idx, ch in enumerate(expr):
        if ch in '([{':
            stack.append(ch)
            logs.append(f"Lectura '{ch}' en pos {idx}: push → pila = {stack}")
        elif ch in ')]}':
            if stack and stack[-1] == pairs[ch]:
                stack.pop()
                logs.append(f"Lectura '{ch}' en pos {idx}: pop  → pila = {stack}")
            else:
                esperado = pairs[ch]
                encontrado = stack[-1] if stack else None
                logs.append(
                    f"Lectura '{ch}' en pos {idx}: pop fallido "
                    f"(esperaba '{esperado}', encontró '{encontrado}') → pila = {stack}"
                )
                return False, logs

    if stack:
        logs.append(f"Pila no vacía al final: {stack}")
        return False, logs
    else:
        logs.append("Pila vacía al finalizar → expresión balanceada")
        return True, logs

def main():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <archivo_expresiones>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except IOError as e:
        print(f"No se pudo abrir el archivo: {e}")
        sys.exit(1)

    for i, line in enumerate(lines, start=1):
        expr = line.strip()
        if not expr:
            continue

        print(f"--- Línea {i}: {expr}")
        balanced, logs = balance_check(expr)

        print("Pasos de la pila:")
        for log in logs:
            print("  " + log)

        if balanced:
            print("Resultado: Bien balanceada\n")
        else:
            print("Resultado: No balanceada\n")

if __name__ == '__main__':
    main()
