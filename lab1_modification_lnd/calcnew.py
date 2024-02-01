#!/usr/bin/env python3

from operator import add, mul, sub, truediv

from compf import Compf


class CalcNew:
    def __init__(self):
        self.operators = {
            "+": add,
            "-": sub,
            "*": mul,
            "/": truediv,
        }

    def evaluate(self, expression):
        # Преобразуем выражение в обратную польскую нотацию с помощью Compf
        compiler = Compf()
        rpn_expression_usplit = compiler.compile(expression)
        print(f"Результат работы компилятора: {rpn_expression_usplit}")
        rpn_expression = rpn_expression_usplit.split()
        # Вычисляем выражение, представленное в ОПН
        return self.calculate_rpn(rpn_expression)

    def calculate_rpn(self, tokens):
        stack = []
        for token in tokens:
            if token.startswith("0b"):
                stack.append(int(token, 2))
            else:  # токен - оператор
                if len(stack) < 2:
                    raise ValueError("Некорректное выражение")
                right, left = stack.pop(), stack.pop()
                stack.append(self.operators[token](left, right))
        if len(stack) != 1:
            raise ValueError("Некорректное выражение")
        return stack[0]


if __name__ == "__main__":
    calc = CalcNew()
    while True:
        expression = input("Введите арифметическое выражение: ")
        try:
            result = calc.evaluate(expression)
            print(f"Результат: {result}\n")
        except Exception as e:
            print(f"Ошибка: {e}")
