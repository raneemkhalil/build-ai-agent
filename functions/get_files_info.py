import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    msg = ""
    try:
        working_directory_path = os.path.abspath(working_directory)
        directory_path = os.path.normpath(os.path.join(working_directory_path, directory)) # to delete any '..' in the path

        if not os.path.isdir(directory_path):
            return f'Error: "{directory}" is not a directory'

        valid_directory = os.path.commonpath([working_directory_path, directory_path]) == working_directory_path # commonpath method return the shared path between to paths or more

        # Without this restriction, the LLM might run amok anywhere on the machine,
        # reading sensitive files or overwriting important data.
        # This is a very important step that we'll bake into every function the LLM can call.
        if not valid_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        files_or_dirs = os.scandir(directory_path)
    except Exception as e:
        return f'Error: {e}'

    for entry in files_or_dirs:
        msg = msg + f'- {entry.name}: file_size={os.path.getsize(entry.path)} bytes, is_dir={entry.is_dir()}'
    return msg