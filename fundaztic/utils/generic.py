def save_file(file_path: str, write_content, write_method: str = "wb") -> None:
    with open(file_path, write_method) as f:
        f.write(write_content)
