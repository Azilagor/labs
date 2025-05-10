import re, time, random
from ply_parser import method_ply
from fsm import FSMWrapper


MAX_LENGTH = 63
server_stats = {}

def record_server(server):
    if server in server_stats:
        server_stats[server] += 1
    else:
        server_stats[server] = 1

def method_regex(line):
    pattern = re.compile(r"^nfs://([a-zA-Z]+)(/[a-zA-Z]+/)([a-zA-Z]+/)*([a-zA-Z]+(/)?)?$")
    match = pattern.fullmatch(line.strip())
    if not match:
        return False, None
    path = line.strip()[6:]
    if len(path) > MAX_LENGTH:
        return False, None
    return True, match.group(1)

def method_smc(line):
    fsm = FSMWrapper()
    try:
        path = line.strip()
        if not path.startswith("nfs://"):
            return False, None

        for ch in path:
            fsm.input(ch)
        fsm.input('\0')  # сигнал конца строки
    except Exception:
        return False, None

    return fsm.accepted and fsm.server is not None, fsm.server



def process_line(line, method):
    if method == 1:
        return method_regex(line)
    elif method == 2:
        return method_smc(line)
    elif method == 3:
        return method_ply(line)
    return False, None


def generate(n):
    sample_words = ["server", "backup", "images", "photos", "gamma", "lib", "alpha", "data", "project"]
    lines = []

    for _ in range(n):
        server = random.choice(sample_words).capitalize()
        catalog = random.choice(sample_words)
        path = f"nfs://{server}/{catalog}/"

        parts = []
        num_segments = random.randint(0, 4)
        for _ in range(num_segments):
            segment = random.choice(sample_words)
            if random.choice([True, False]):
                segment += "/"
            parts.append(segment)

        full_path = path + "".join(parts)
        lines.append(full_path)

    return lines



def benchmark(n=100):
    lines = generate(n)


    with open("generated.txt", "w") as f:
        f.writelines(line + "\n" for line in lines)

    print(f" Сгенерировано {n} строк и сохранено в generated.txt")

    methods = {
        "Регулярки": method_regex,
        "SMC": method_smc,
        "PLY": method_ply,
    }

    for name, method in methods.items():
        valid = 0
        start = time.perf_counter()
        for line in lines:
            ok, _ = method(line)
            if ok:
                valid += 1
        elapsed = time.perf_counter() - start

        print(f"\n Метод: {name}")
        print(f" Время: {elapsed:.6f} сек")

def run():
    method = int(input("Выберите метод (1-regex, 2-SMC, 3-PLY): "))
    filename = "input.txt"
    with open(filename, "r") as f:
        lines = f.readlines()

    start_time = time.perf_counter()
    for line in lines:
        ok, server = process_line(line.strip(), method)
        if ok:
            print(f"OK: {line.strip()}")
            record_server(server)
        else:
            print(f"INVALID: {line.strip()}")
    end_time = time.perf_counter()

    print("\n Статистика по серверам:")
    for name, count in server_stats.items():
        print(f"{name}: {count} раз")

    print(f"\n Время выполнения: {end_time - start_time:.6f} секунд")

def main():
    print("Выберите режим:")
    print("1) Проверка input.txt")
    print("2) Генерация и тестирование всех методов")
    mode = int(input("Введите режим (1/2): "))

    if mode == 1:
        run()
    elif mode == 2:
        n = int(input("Сколько строк сгенерировать? "))
        benchmark(n)

if __name__ == "__main__":
    main()