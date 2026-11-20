from collections import deque

VERSION_OPERATORS = ("=", "<", ">", "~")
PAIR_SEPARATOR = ":"


def strip_version(dep_name):
    """Отрезает ограничение версии (например >=1.0) от имени зависимости."""
    for operator in VERSION_OPERATORS:
        if operator in dep_name:
            dep_name, _, _ = dep_name.partition(operator)
    return dep_name


def parse_test_repo(path):
    """Читает тестовый файл графа ('A: B C') в словарь зависимостей."""
    graph_data = {}
    with open(path, encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or PAIR_SEPARATOR not in line:
                continue
            pkg, _, deps_str = line.partition(PAIR_SEPARATOR)
            graph_data[pkg.strip()] = deps_str.split()
    return graph_data


def build_index_map(packages):
    """Строит словарь зависимостей по именам пакетов и их токенам (p:)."""
    dep_map = {}
    for pkg in packages:
        name = pkg.get("P")
        deps = pkg.get("D", "").split()
        if name and name not in dep_map:
            dep_map[name] = deps
        for token in pkg.get("p", "").split():
            clean_token = strip_version(token)
            if clean_token not in dep_map:
                dep_map[clean_token] = deps
    return dep_map


def is_filtered(name, filter_sub):
    """Проверяет, нужно ли пропустить пакет по подстроке фильтра."""
    return bool(filter_sub) and filter_sub in name


def build_dependency_graph(start_pkg, dep_map, filter_sub=""):
    """Строит граф зависимостей обходом BFS без рекурсии."""
    if is_filtered(start_pkg, filter_sub):
        return {}
    graph = {start_pkg: []}
    visited = {start_pkg}
    queue = deque([start_pkg])
    while queue:
        current = queue.popleft()
        raw_deps = dep_map.get(current, [])
        clean_deps = [strip_version(item) for item in raw_deps]
        visible = [d for d in clean_deps if not is_filtered(d, filter_sub)]
        graph[current] = visible
        for dep in visible:
            if dep not in visited:
                visited.add(dep)
                graph.setdefault(dep, [])
                queue.append(dep)
    return graph
