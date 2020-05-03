from typing import List
from .filemanager import check_file_extension


def export_lines_to_text(lines: List[str], output_filename, omit_empty = True):
    with open(check_file_extension(output_filename, "txt"), "w") as f:
        for item in lines:
            if omit_empty:
                if str(item).strip() == "":
                    continue
            f.write(f"{item.strip()}\n")


def import_text_to_lines(file_name):
    lines = None

    with open(check_file_extension(file_name, "txt"), "r") as f:
        lines = f.readlines()

    if len(lines) == 0:
        return None

    return lines
