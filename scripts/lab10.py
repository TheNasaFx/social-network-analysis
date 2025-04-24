import dynetx as dn
import dynetx.algorithms as al
import networkx as nx

# Динамик граф үүсгэх
g = dn.DynGraph()

# Ирмэгүүдийг цаг хугацааны тэмдэглэгээтэй нэмэх (логик дараалалтай)
g.add_interaction("A", "B", t=1)  # t=1: A -> B
g.add_interaction("B", "C", t=2)  # t=2: B -> C
g.add_interaction("C", "E", t=3)  # t=3: C -> E
g.add_interaction("A", "D", t=2)  # t=2: A -> D
g.add_interaction("D", "E", t=4)  # t=4: D -> E
g.add_interaction("A", "E", t=5)  # t=5: A -> E (шууд зам)

# Графийн бүтцийг шалгах
print("Бүх ирмэгүүд:", g.edges())

# Тодорхой нэг снапшот (t=1) дээрх статик граф
snapshot_t1 = g.time_slice(1)
print("Снапшот t=1 дээрх оройнууд:", snapshot_t1.nodes())
print("Снапшот t=1 дээрх ирмэгүүд:", snapshot_t1.edges())

# Глобал хэмжээнд замуудыг олох (A-с E хүртэл, t=1-ээс t=5 хүртэл)
start_node = "A"
end_node = "E"
start_time = 1
end_time = 5

paths = al.time_respecting_paths(g, start_node, end_node, start=start_time, end=end_time)
print(f"\n{start_node}-с {end_node} хүртэлх цаг хугацааг харгалзсан замууд:")
for i, path in enumerate(paths):
    print(f"Зам {i+1}: {path}")

# Замуудыг шинжлэх функц (форматаас хамааралгүй, бат бөх хувилбар)
def analyze_paths(paths):
    if not paths:
        print("\nЗamuудын шинжилгээ: Зам олдсонгүй")
        return

    # Цагийн тэмдэглэгээг авах туслах функцууд
    def get_time_diff(path):
        if isinstance(path, list) and all(isinstance(p, tuple) and len(p) == 3 for p in path):
            return path[-1][2] - path[0][2]
        return float('inf')  # Формат буруу бол хамгийн их утга

    def get_end_time(path):
        if isinstance(path, list) and all(isinstance(p, tuple) and len(p) == 3 for p in path):
            return path[-1][2]
        return float('inf')

    # Замын төрлүүдийг олох
    shortest_path = min(paths, key=len)
    fastest_path = min(paths, key=get_time_diff)
    foremost_path = min(paths, key=get_end_time)

    print("\nЗamuудын шинжилгээ:")
    print(f"Shortest (хамгийн богино): {shortest_path}")
    print(f"Fastest (хамгийн хурдан): {fastest_path}")
    print(f"Foremost (хамгийн эрт ирэх): {foremost_path}")

    shortest_paths = [p for p in paths if len(p) == len(shortest_path)]
    fastest_shortest = min(shortest_paths, key=get_time_diff)
    fastest_paths = [p for p in paths if get_time_diff(p) == get_time_diff(fastest_path)]
    shortest_fastest = min(fastest_paths, key=len)
    
    print(f"Fastest Shortest: {fastest_shortest}")
    print(f"Shortest Fastest: {shortest_fastest}")

# Шинжилгээг гүйцэтгэх
analyze_paths(paths)

