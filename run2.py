import sys
from collections import deque
from typing import List, Dict, Tuple, Optional


def bfs(edges: Dict[str, list], start: str) \
        -> Optional[Tuple[str, ...]]:
    """
        Idea:
            Пробегаемся бфсом в поиске шлюза.
            Если нашли шлюз, не возвращаем, а складываем в массив ответов.
            Затем среди них выберем лексикографически меньший. Его и вернем.
    :param edges: Словарь смежности ребер.
    :param start: стартовая точка
    :return: кортеж из 3х элементов:
     (Шлюз, Откуда в этот шлюз попали, первый шаг)
    """
    if start not in edges or not edges[start]:
        return None

    q = deque([(start, node, 1, node) for node in sorted(edges[start])])
    visited = {start}
    founded = []
    min_depth = None
    founded_gateways = set()
    while q:
        from_node, current_node, depth, first_step = q.popleft()

        # Если уже нашли шлюз на меньшей глубине — дальше нет смысла
        if min_depth is not None and depth > min_depth:
            break

        if current_node.isupper():
            # Проверки нового шлюза на закрытие
            if min_depth is None:
                min_depth = depth
            if depth == min_depth and current_node not in founded_gateways:
                founded.append((current_node, from_node, first_step))
                founded_gateways.add(current_node)
            continue

        if current_node not in visited:
            visited.add(current_node)
            for neighbour in sorted(edges.get(current_node, [])):
                q.append((current_node, neighbour, depth + 1, first_step))

    if not founded:
        return None

    founded.sort(key=lambda x: x[0])
    return founded[0]


def solve(edges: Dict[str, List[str]]) -> List[str]:
    """
        Idea:
            Симуляция движения вируса и удаления шлюзов.
            Как только убрали все опасные шлюзы - return
    :param edges: Словарь смежности ребер
    :return: Последовательность закрывания шлюзов - ответ на задачу
    """
    result = []
    current_pos = 'a'
    while True:
        founded = bfs(edges, current_pos)
        if not founded:
            return result
        gateway, from_node, first_step = founded
        result.append(f'{gateway}-{from_node}')
        break_halls(edges, gateway, from_node)
        new_virus_pos = bfs(edges, current_pos)
        if not new_virus_pos or new_virus_pos[2] not in edges:
            return result
        current_pos = new_virus_pos[2]


def break_halls(edges: Dict[str, List[str]], gateway: str, node: str) -> None:
    if node in edges.get(gateway, []):
        edges[gateway].remove(node)
    if gateway in edges.get(node, []):
        edges[node].remove(gateway)


def main():
    edges = {}
    for line in sys.stdin:
        line = line.strip()
        if line:
            node1, sep, node2 = line.partition('-')
            if sep:
                edges.setdefault(node1, []).append(node2)
                edges.setdefault(node2, []).append(node1)

    result = solve(edges)
    for edge in result:
        print(edge)


if __name__ == "__main__":
    main()
