import argparse
import os
import sys

from apkindex import find_package, parse_index
from graph import build_dependency_graph, build_index_map, get_load_order, parse_test_repo
from repository import download_index


def build_parser():
    """Описание параметров командной строки."""
    parser = argparse.ArgumentParser(
        description="Dependency graph visualizer for Alpine packages")
    parser.add_argument("--package", required=True,
                        help="name of the package to analyze")
    parser.add_argument("--repo", required=True,
                        help="repository URL or path to a test file")
    parser.add_argument("--test-mode", action="store_true",
                        help="treat --repo as a path to a test graph file")
    parser.add_argument("--version", required=True,
                        help="package version")
    parser.add_argument("--output", default="graph.svg",
                        help="name of the generated image file")
    parser.add_argument("--ascii-tree", action="store_true",
                        help="print dependencies as an ASCII tree")
    parser.add_argument("--filter", default="", dest="filter_substring",
                        help="skip packages whose name contains this")
    parser.add_argument("--load-order", action="store_true",
                        help="print package installation order")

    return parser


def validate(config):
    """Проверка корректности переданных параметров."""
    if not config["package"].strip():
        raise ValueError("package name must not be empty")
    if not config["version"].strip():
        raise ValueError("version must not be empty")
    if not config["output"].endswith(".svg"):
        raise ValueError("output file must have the .svg extension")
    if config["test_mode"]:
        if not os.path.isfile(config["repo"]):
            raise ValueError(f"test file not found: {config['repo']}")
    elif not config["repo"].startswith(("http://", "https://")):
        raise ValueError("repo must be an http(s) URL (or use --test-mode)")


def resolve_graph(config):
    """Загружает данные и строит граф зависимостей."""
    if config["test_mode"]:
        dep_map = parse_test_repo(config["repo"])
        if config["package"] not in dep_map:
            raise RuntimeError(f"package {config['package']} not found")
        return build_dependency_graph(
            config["package"], dep_map, config["filter_substring"])
    packages = parse_index(download_index(config["repo"]))
    target = find_package(packages, config["package"], config["version"])
    if target is None:
        raise RuntimeError(
            f"package {config['package']} {config['version']} not found")
    dep_map = build_index_map(packages)
    dep_map[config["package"]] = target.get("D", "").split()
    return build_dependency_graph(
        config["package"], dep_map, config["filter_substring"])


def print_graph(graph):
    """Выводит граф зависимостей построчно."""
    if not graph:
        print("(empty graph)")
        return
    for pkg, deps in graph.items():
        joined = ", ".join(deps) if deps else "(none)"
        print(f"{pkg} -> {joined}")


def print_load_order(order):
    """Выводит порядок загрузки зависимостей."""
    if not order:
        print("(empty load order)")
        return
    for step, pkg in enumerate(order, start=1):
        print(f"{step}. {pkg}")


def main():
    """Точка входа: чтение аргументов, проверка и вывод результата."""
    config = vars(build_parser().parse_args())
    try:
        validate(config)
        graph = resolve_graph(config)
    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    if config["load_order"]:
        print_load_order(get_load_order(config["package"], graph))
    else:
        print_graph(graph)


if __name__ == "__main__":
    main()
