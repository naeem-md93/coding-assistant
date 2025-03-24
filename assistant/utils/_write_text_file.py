

def write_text_file(save_path: str, text: str) -> None:
    with open(save_path, "w") as outfile:
        outfile.write(text)