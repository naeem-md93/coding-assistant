

def read_text_file(path: str) -> str:
    with open(path, "r") as f:
        data = f.read()
    return data