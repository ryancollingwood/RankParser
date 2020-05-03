import os
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


if ENV_VARIABLE_NAME not in os.environ:
    print(f"Graphviz environment variable not set - will be downloaded to: {INSTALL_TO_DIRECTORY}")
    download_graphviz(WIN_GRAPHVIZ_URL, DESTINATION_FILE)
    extract_zip(DESTINATION_FILE, INSTALL_TO_DIRECTORY)

    print("Setting Environment Variable")
    os.environ[ENV_VARIABLE_NAME] = DOT_PATH
