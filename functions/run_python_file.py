import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    response = ""
    try:
        working_directory_path = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(working_directory_path, file_path)) # to delete any '..' in the path
        valid_directory = os.path.commonpath([working_directory_path, absolute_file_path]) == working_directory_path # commonpath method return the shared path between to paths or more

        # Without this restriction, the LLM might run amok anywhere on the machine,
        # reading sensitive files or overwriting important data.
        # This is a very important step that we'll bake into every function the LLM can call.
        if not valid_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

    except Exception as error:
        return f'Error: {error}'

    command = ["python", absolute_file_path]

    if args:
        command.extend(args)

    try:
        processing = subprocess.run(command, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        return 'Timeout: expired'
    except Exception as error:
        return f"Error: executing Python file: {error}"

    # If we don’t set text = True, the output will be in bytes, so you’d need to decode manually:
    # result.stdout.decode("utf-8")
    try:
        stdout = processing.stdout
        stderr = processing.stderr

        if processing.returncode:
            response = response + f"Process exited with code {processing.returncode}"
        if not stdout and not stderr:
            response = response + "\nNo output produced"
        else:
            response = response + f"\n{'STDOUT:' + stdout if stdout else ''}\n{'STDERR:' + stderr if stderr else ''}"
    except Exception as error:
        return f"Error: executing Python file: {error}"

    return response
