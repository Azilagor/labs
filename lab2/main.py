from regex_engine import Regex
from nfa_dfa import DFA

def print_menu():
    print("\n=== Регулярное выражение: Меню ===")
    print("1. Ввести выражение и скомпилировать")
    print("2. Проверить строку на соответствие")
    print("3. Пересечение с другим выражением")
    print("4. Разность с другим выражением")
    print("5. Выйти")

def main():
    regex = None

    while True:
        print_menu()
        choice = input("Выберите действие (1-5): ")

        if choice == "1":
            pattern = input("Введите регулярное выражение: ")
            try:
                regex = Regex(pattern).compile()
                regex.dfa.print_dfa_console()
                
                print(" Выражение успешно скомпилировано.")
                restored = regex.dfa.to_regex()
                
                print("\n Восстановленная регулярка по автомату:", restored)
            except Exception as e:
                print("Ошибка компиляции:", e)

        elif choice == "2":
            if not regex:
                print(" Сначала скомпилируйте выражение.")
                continue
            test_str = input("Введите строку для проверки: ")
            result = regex.match(test_str)
            print(" Совпадает!" if result else " Не совпадает.")

        elif choice == "3":
            if not regex:
                print("Сначала скомпилируйте выражение.")
                continue
            pattern2 = input("Введите второе выражение: ")
            try:
                other = Regex(pattern2).compile()
                regex = regex.intersect(other)
                print(" Пересечение выполнено. Теперь используется новое выражение.")
            except Exception as e:
                print("Ошибка пересечения:", e)

        elif choice == "4":
            if not regex:
                print(" Сначала скомпилируйте выражение.")
                continue
            pattern2 = input("Введите второе выражение: ")
            try:
                other = Regex(pattern2).compile()
                regex = regex.difference(other)
                print(" Разность выполнена. Теперь используется новое выражение.")
            except Exception as e:
                print("Ошибка разности:", e)

        elif choice == "5":
            print("Выход...")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
