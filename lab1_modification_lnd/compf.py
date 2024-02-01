#!/usr/bin/env python3

import re

from stack import Stack


class Compf:
    """
    Стековый компилятор формул поддерживает формулы,
    содержащие римские числа (например, II как 2, IX как 9),
    и компилирует их в программы для стекового калькулятора
    с числами в двоичной системе счисления.
    Все операции трактуются как правоассоциативные.
    """

    def __init__(self):
        self.s = Stack()
        self.data = []

    def compile(self, str):
        self.data.clear()
        # Добавляем скобки для упрощения обработки
        self.process_formula("(" + str + ")")
        return " ".join(self.data)

    def process_formula(self, formula):
        # Разбиваем входную строку на токены
        tokens = re.findall(r"\d+|[IVXLCDM]+|\+|\-|\*|\/|\(|\)", formula)
        for token in tokens:
            self.process_symbol(token)

    def process_symbol(self, token):
        if re.match(r"^[IVXLCDM]+$", token):
            binary = self.roman_to_binary(token)
            self.data.append(binary)
        elif token in "+-*/":
            self.process_suspended_operators(token)
            self.s.push(token)
        elif token == "(":
            self.s.push(token)
        elif token == ")":
            self.process_suspended_operators(token)
            self.s.pop()

    def process_suspended_operators(self, token):
        if len(self.s.array) == 0:
            return
        while self.is_precedes(self.s.top(), token):
            self.process_oper(self.s.pop())

    def process_oper(self, token):
        self.data.append(token)

    def roman_to_binary(self, roman):
        value = self.roman_to_decimal(roman)
        return f"0b{bin(value)[2:]}"

    def roman_to_decimal(self, roman):
        roman_numerals = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }
        value = 0
        prev_value = 0
        for char in reversed(roman):
            decimal = roman_numerals[char]
            if decimal < prev_value:
                value -= decimal
            else:
                value += decimal
            prev_value = decimal
        return value

    @staticmethod
    def priority(token):
        return 1 if token in "+-" else 2

    @staticmethod
    def is_precedes(a, b):
        if a == "(":
            return False
        elif b == ")":
            return True
        else:
            return Compf.priority(a) >= Compf.priority(b)


if __name__ == "__main__":
    compf = Compf()
    while True:
        formula = input("Арифметическая формула: ")
        print(f"Результат компиляции: {compf.compile(formula)}")
        print()
