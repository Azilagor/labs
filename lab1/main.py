import re
import time
from flex import method_flex
from ply_parser import method_ply
from smc import method_smc


MAX_LENGTH = 63
server_stats = {}

def record_server(server):
    if server in server_stats:
        server_stats[server] += 1
    else:
        server_stats[server] = 1

def method_regex(line):
    pattern = re.compile(r"^nfs://([a-zA-Z]+)(/[a-zA-Z]+)*$")
    match = pattern.fullmatch(line.strip())
    if not match:
        return False, None
    path = line.strip()[6:]
    if len(path) > MAX_LENGTH:
        return False, None
    return True, match.group(1)


def process_line(line, method):
    if method == 1:
        return method_regex(line)
    elif method == 2:
        return method_smc(line)
    elif method == 3:
        return method_flex()
    elif method == 4:
        return method_ply(line)
    return False, None

def main():
    print("Выберите метод проверки:")
    print("1) Регулярные выражения")
    print("2) SMC вариант 1 (ручная проверка)")
    print("3) SMC вариант 2 (символьный автомат)")
    print("4) Ply (лексер + парсер)")
    method = int(input("Введите номер метода (1/2/3)/4: "))

    print("\nВыберите источник ввода:")
    print("1) Ввод из файла")
    source = int(input("Введите номер источника (1): "))

    lines = []
    if source == 1:
        filename = "input.txt"
        with open(filename, "r") as f:
            lines = f.readlines()

    print("\nРезультаты проверки:\n")
    start_time = time.perf_counter()

    for line in lines:
        ok, server = process_line(line.strip(), method)
        if ok:
            print(f"OK: {line.strip()}")
            record_server(server)
        else:
            print(f"INVALID: {line.strip()}")

    end_time = time.perf_counter()
    elapsed = end_time - start_time

    print("\n📊 Статистика по серверам:")
    for name, count in server_stats.items():
        print(f"{name}: {count} раз")

    print(f"\n⏱️ Время выполнения: {elapsed:.6f} секунд")

if __name__ == "__main__":
    main()