def check_file_extension(output_file, extension = "txt"):
    if not output_file.lower()[-4:] == f".{extension}":
        return f"{output_file}.{extension}"
    return output_file
