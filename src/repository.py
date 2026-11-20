import io
import tarfile
import urllib.error
import urllib.request

ARCH = "x86_64"
INDEX_ARCHIVE = "APKINDEX.tar.gz"
INDEX_FILE = "APKINDEX"
TIMEOUT_SECONDS = 30

'''создание полноценной ссылки'''
def build_index_url(repo_url):
    return f"{repo_url.rstrip('/')}/{ARCH}/{INDEX_ARCHIVE}"

'''распаковка архива'''
def extract_index_text(data):
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
            return archive.extractfile(INDEX_FILE).read().decode("utf-8")
    except (tarfile.TarError, KeyError, OSError) as error:
        raise RuntimeError(f"bad index archive: {error}") from error

'''установка'''
def download_index(repo_url):
    url = build_index_url(repo_url)
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as reply:
            data = reply.read()
    except (urllib.error.URLError, TimeoutError) as error:
        raise RuntimeError(f"cannot download {url}: {error}") from error
    return extract_index_text(data)