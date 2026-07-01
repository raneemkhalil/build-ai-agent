import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory_path = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_directory_path, file_path)) # to delete any '..' in the path
        valid_directory = os.path.commonpath([working_directory_path, abs_file_path]) == working_directory_path # commonpath method return the shared path between to paths or more

        # Without this restriction, the LLM might run amok anywhere on the machine,
        # reading sensitive files or overwriting important data.
        # This is a very important step that we'll bake into every function the LLM can call.
        if not valid_directory:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

        parent_dirs = "/".join(abs_file_path.split("/")[0:-1])
        if not os.path.exists(parent_dirs):
            os.makedirs(parent_dirs, exist_ok=True)

        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        with open(abs_file_path, "w") as file:
            file.write(content)
    except Exception as error:
        return f'Error: {error}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
