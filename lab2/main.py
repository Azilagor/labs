from regex_engine import Regex
from nfa_dfa import DFA, dfa_to_regex, simplify_regex
import re

def print_menu():
    print("\n=== Регулярное выражение: Меню ===")
    print("1. Ввести выражение и скомпилировать")
    print("2. Проверить строку на соответствие")
    print("3. Пересечение с другим выражением")
    print("4. Разность с другим выражением")
    print("5. Показать восстановленную регулярку")
    print("6. Проверить совпадение оригинала и восстановления")
    print("7. Выход")


def main():
    regex = None

    while True:
        print_menu()
        choice = input("Выберите действие (1-7): ").strip()

        if choice == "1":
            pattern = input("Введите регулярное выражение: ")
            try:
                regex = Regex(pattern).compile()
                print("\n DFA построен:")
                #regex.dfa.print_dfa_console()

                restored = simplify_regex(dfa_to_regex(regex))
                print("\n Восстановленная регулярка по автомату:", restored)
            except Exception as e:
                print(" Ошибка компиляции:", e)

        elif choice == "2":
            if not regex:
                print(" Сначала скомпилируйте выражение.")
                continue
            test_str = input("Введите строку для проверки: ")
            result = regex.match(test_str)
            print(" Совпадает!" if result else " Не совпадает.")

        elif choice == "3":
            if not regex:
                print(" Сначала скомпилируйте выражение.")
                continue
            pattern2 = input("Введите второе выражение: ")
            try:
                other = Regex(pattern2).compile()
                regex = regex.intersect(other)
                print(" Пересечение выполнено. Используется новое выражение.")
            except Exception as e:
                print(" Ошибка пересечения:", e)

        elif choice == "4":
            if not regex:
                print(" Сначала скомпилируйте выражение.")
                continue
            pattern2 = input("Введите второе выражение: ")
            try:
                other = Regex(pattern2).compile()
                regex = regex.difference(other)
                print(" Разность выполнена. Используется новое выражение.")
            except Exception as e:
                print(" Ошибка разности:", e)

        elif choice == "5":
            if not regex:
                print(" Сначала скомпилируйте выражение.")
                continue
            print("\n Восстановленная регулярка:", simplify_regex(dfa_to_regex(regex.dfa)))

        elif choice == "6":
            if not regex or regex.pattern is None:
                print(" Нельзя сравнить — нет оригинала.")
                continue
            restored = simplify_regex(dfa_to_regex(regex.dfa))
            pattern = regex.pattern
            print(f"\nОригинал:      {pattern}")
            print(f"Восстановлено: {restored}")

            samples = input("Введите строки через пробел для сравнения: ").split()
            py_orig = re.compile(f"^{pattern}$")
            py_restored = re.compile(f"^{restored}$")
            for s in samples:
                o = bool(py_orig.fullmatch(s))
                r = bool(py_restored.fullmatch(s))
                status = " Совпадают" if o == r else " Разные"
                print(f"{s:<15} | оригинал: {o} | восстановлено: {r} | {status}")

        elif choice == "7":
            print(" Выход...")
            break

        else:
            print(" Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
