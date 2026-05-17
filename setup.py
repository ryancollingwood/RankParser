import os
import shutil
from urllib import request

ENV_VARIABLE_NAME = "GRAPHVIZ_DOT"
WIN_GRAPHVIZ_URL = "https://graphviz.gitlab.io/_pages/Download/windows/graphviz-2.38.zip"
DESTINATION_FILE = WIN_GRAPHVIZ_URL.split("/")[-1]
INSTALL_TO_DIRECTORY = "".join(DESTINATION_FILE.split(".")[0:-1])
DOT_PATH = f"{INSTALL_TO_DIRECTORY}/release/bin"


def download_graphviz(url, destination_file):
    print(f"Downloading Graphviz from: {url}")
    filedata = request.urlopen(WIN_GRAPHVIZ_URL)
    data_to_write = filedata.read()

    with open(destination_file, 'wb') as f:
        f.write(data_to_write)

    print("Download complete")


def where_dot():
    """Locate the Graphviz dot executable."""
    dot_path = shutil.which("dot")
    if dot_path:
        return os.path.dirname(dot_path)
    return None


if __name__ == "__main__":
    install_path = where_dot()

    if install_path is None:
        print(f"Graphviz not found on path - will be downloaded to: {INSTALL_TO_DIRECTORY}")
        download_graphviz(WIN_GRAPHVIZ_URL, DESTINATION_FILE)

        print(f"Extracting {DESTINATION_FILE} to {INSTALL_TO_DIRECTORY}")
        shutil.unpack_archive(DESTINATION_FILE, INSTALL_TO_DIRECTORY)
        os.remove(DESTINATION_FILE)
        print("Extraction complete")

        print("Setting Environment Variable")
        os.environ["PATH"] += os.pathsep + DOT_PATH
    else:
        if install_path not in os.environ.get("PATH", ""):
            print("Setting Environment Variable")
            os.environ["PATH"] += os.pathsep + install_path
