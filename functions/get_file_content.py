import os

from settings import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    content = ""
    try:
        working_directory_path = os.path.abspath(working_directory)
        file_path = os.path.normpath(os.path.join(working_directory_path, file_path)) # to delete any '..' in the path

        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        valid_directory = os.path.commonpath([working_directory_path, file_path]) == working_directory_path # commonpath method return the shared path between to paths or more

        # Without this restriction, the LLM might run amok anywhere on the machine,
        # reading sensitive files or overwriting important data.
        # This is a very important step that we'll bake into every function the LLM can call.
        if not valid_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except Exception as error:
        return f'Error: {error}'

    with open(file_path, "r") as file:
        content = file.read(MAX_CHARS)
        # After reading the first MAX_CHARS...
        if file.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    return content