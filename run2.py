import sys
from collections import deque
from typing import List, Dict


def solve(edges: Dict[str, List[str]]) -> List[str]:
    """
        Idea:
            BFS для поиска кратчайшего пути до шлюзов.
            Нашли шлюз -> добавляем пару.
    :param edges: Словарь связанности вершин
    :return: result: Список полученных пар для закрытия коридоров
    """
    result = []
    initial_node = 'a'
    initial_node_neighbours = sorted(edges[initial_node])
    paths_info = [('a', node) for node in initial_node_neighbours]
    q = deque(paths_info)
    visited = set()
    while q:
        from_node, current_node = q.popleft()
        # Вышли на шлюз
        if current_node.isupper():
            result.append(f'{current_node}-{from_node}')
            continue
        # Проверка, что мы не были в новой ноде
        if current_node not in visited:
            visited.add(current_node)
            node_neighbours = sorted(edges[current_node])
            for neighbour in node_neighbours:
                q.append((current_node, neighbour))  # Добавление соседей
    return result


def main():
    edges = {}
    for line in sys.stdin:
        line = line.strip()

        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                # Создание словаря связанности
                if node1 not in edges:
                    edges[node1] = []
                edges[node1].append(node2)
                if node2 not in edges:
                    edges[node2] = []
                edges[node2].append(node1)
    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
