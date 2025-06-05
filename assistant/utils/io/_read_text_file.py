

def read_text_file(file_path: str) -> str:
    with open(file_path, 'r') as stream:
        content = stream.read()
    return content