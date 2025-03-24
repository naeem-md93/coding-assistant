import hashlib


def hash_file_content(content: str) -> str:

        content = content.encode("utf-8")
        content = hashlib.md5(content).hexdigest()
        
        return content