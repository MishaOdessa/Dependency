

RELEASE_PREFIX = "-r"

#разделение по блокам
def parse_index(text):
    packages = []
    for block in text.split("\n\n"):
        package = {}
        for line in block.splitlines():
            key, _, value = line.partition(":")
            package[key] = value
        if package:
            packages.append(package)
    return packages

# разделение по строкам
def find_package(packages, name, version):
    for package in packages:
        if package.get("P") != name:
            continue
        index_version = package.get("V", "")
        prefix = version + RELEASE_PREFIX
        if index_version == version or index_version.startswith(prefix):
            return package
    return None

# разделение строки в словарь
def get_dependencies(package):
    return package.get("D", "").split()