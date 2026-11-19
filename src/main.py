import argparse
import os
import sys

from apkindex import find_package, get_dependencies, parse_index
from repository import download_index

# правила приема
def build_parser():
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
    return parser

# обработка ошибок
def validate(config):
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

#
def load_dependencies(config):
    if config["test_mode"]:
        raise RuntimeError("test mode is not supported yet")
    packages = parse_index(download_index(config["repo"]))
    package = find_package(packages, config["package"], config["version"])
    if package is None:
        raise RuntimeError(
            f"package {config['package']} {config['version']} not found")
    return get_dependencies(package)


def print_dependencies(config, dependencies):
    print(f"Direct dependencies of {config['package']} "
          f"{config['version']}:")
    if not dependencies:
        print("  (none)")
    for dependency in dependencies:
        print(f"  {dependency}")


def main():
    config = vars(build_parser().parse_args())
    try:
        validate(config)
        dependencies = load_dependencies(config)
    except (ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    print_dependencies(config, dependencies)


if __name__ == "__main__":
    main()