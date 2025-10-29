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
    :param edges: Словарь смежности вершин
    :param start: стартовая точка
    :return: кортеж из 3х элементов:
     (Шлюз, Откуда в этот шлюз попали, первый шаг)
    """
    if start not in edges or not edges[start]:
        return None

    q = deque()
    visited = {start}
    # сразу добавляем соседей стартовой вершины
    for node in sorted(edges[start]):
        q.append((start, node, 1, node))
        visited.add(node)

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
        for neighbour in sorted(edges.get(current_node, [])):
            if neighbour not in visited:
                visited.add(neighbour)
                q.append((current_node, neighbour, depth + 1, first_step))

    if not founded:
        return None

    # сортируем по шлюзу и по узлу (лексикографически)
    founded.sort(key=lambda x: (x[0], x[1]))
    return founded[0]


def solve(edges: Dict[str, List[str]]) -> List[str]:
    """
        Idea:
            Симуляция движения вируса и удаления шлюзов.
            Как только убрали все опасные шлюзы - return
    :param edges: Словарь смежности вершин
    :return: Последовательность закрывания шлюзов - ответ на задачу
    """
    result = []
    current_pos = 'a'
    while True:
        founded = bfs(edges, current_pos)
        if not founded:
            break
        gateway, from_node, first_step = founded
        result.append(f'{gateway}-{from_node}')
        break_halls(edges, gateway, from_node)
        current_pos = first_step
    return result


def break_halls(edges: Dict[str, List[str]], gateway: str, node: str) -> None:
    """
        Idea:
            Очистка коридоров после закрытия шлюза
    :param edges: Словарь смежности вершин
    :param gateway: Шлюз
    :param node: Нода узла
    :return: None
    """
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
