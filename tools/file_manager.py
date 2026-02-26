import os

def read_file(file_path: str) -> str:
    """
    Reads the contents of a file. Provide the absolute or relative path to the file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def write_file(file_path: str, content: str) -> str:
    """
    Writes or overwrites content to a file. Provide the path and the full content to write.
    """
    try:
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}."
    except Exception as e:
        return f"Error writing to file {file_path}: {str(e)}"

def list_directory(directory_path: str = ".") -> str:
    """
    Lists the contents of a directory. Specify the path, defaults to current directory.
    """
    try:
        items = os.listdir(directory_path)
        return "\n".join(items)
    except Exception as e:
        return f"Error listing directory {directory_path}: {str(e)}"
