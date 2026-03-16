import pytest
from input_output.text import export_lines_to_text, import_text_to_lines

def test_export_lines_to_text_default(tmp_path):
    output_file = tmp_path / "test_default.txt"
    lines = ["  line1  ", "", "  line2  ", "\n"]
    export_lines_to_text(lines, str(output_file))

    assert output_file.exists()
    content = output_file.read_text()
    assert content == "line1\nline2\n"

def test_export_lines_to_text_no_omit(tmp_path):
    output_file = tmp_path / "test_no_omit.txt"
    lines = ["line1", "", "line2"]
    export_lines_to_text(lines, str(output_file), omit_empty=False)

    assert output_file.exists()
    content = output_file.read_text()
    assert content == "line1\n\nline2\n"

def test_export_lines_to_text_extension(tmp_path):
    output_file_base = tmp_path / "test_ext"
    output_file_expected = tmp_path / "test_ext.txt"
    lines = ["line1"]
    export_lines_to_text(lines, str(output_file_base))

    assert output_file_expected.exists()
    assert output_file_expected.read_text() == "line1\n"

def test_import_text_to_lines_success(tmp_path):
    input_file = tmp_path / "test_import.txt"
    input_file.write_text("line1\nline2\n")

    lines = import_text_to_lines(str(input_file))
    assert lines == ["line1\n", "line2\n"]

def test_import_text_to_lines_empty(tmp_path):
    input_file = tmp_path / "test_empty.txt"
    input_file.write_text("")

    lines = import_text_to_lines(str(input_file))
    assert lines is None

def test_import_text_to_lines_extension(tmp_path):
    input_file_real = tmp_path / "test_import_ext.txt"
    input_file_real.write_text("line1\n")

    # Passing path without .txt, it should still work
    lines = import_text_to_lines(str(tmp_path / "test_import_ext"))
    assert lines == ["line1\n"]
