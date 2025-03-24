

def get_file_content(path: str) -> str:

    with open(path, 'r') as stream:
        content = stream.read()

    return content
