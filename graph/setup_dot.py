import os
import subprocess
from urllib import request
from zipfile import ZipFile

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


def extract_zip(file_name, destination_folder):
    print(f"Extracting {file_name} to {destination_folder}")
    with ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)

    os.remove(file_name)
    print("Extraction complete")


def where_dot():
    result = None
    try:
        result = subprocess.check_output("where dot.exe", shell=True)
    except subprocess.CalledProcessError:
        pass

    if result is None:
        try:
            result = subprocess.check_output("whereis dot.exe", shell=True)
        except subprocess.CalledProcessError:
            pass

    if result is None:
        return None

    result = result.decode("utf-8").split("\r\n")[0]
    result = os.path.split(result)[0]

    return result


def setup_dot():
    install_path = where_dot()

    if install_path is None:
        print(f"Graphviz not found on path - will be downloaded to: {INSTALL_TO_DIRECTORY}")
        download_graphviz(WIN_GRAPHVIZ_URL, DESTINATION_FILE)
        extract_zip(DESTINATION_FILE, INSTALL_TO_DIRECTORY)
        print("Setting Environment Variable")
        os.environ["PATH"] += os.pathsep + DOT_PATH
    else:
        if install_path not in os.environ["PATH"]:
            print("Setting Environment Variable")
            os.environ["PATH"] += os.pathsep + install_path


if __name__ == "__main__":
    setup_dot()
