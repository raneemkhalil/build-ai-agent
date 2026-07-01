from enum import Enum

from google.genai import types

class Schemas(Enum):
    SCHEMA_GET_FILES_INFO = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                ),
            },
        ),
    )
    SCHEMA_GET_FILE_CONTENT = types.FunctionDeclaration(
        name="get_file_content",
        description="Returns file content",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="File path to read, relative to the working directory (default is the working directory itself)",
                )
            }
        )
    )
    SCHEMA_RUN_PYTHON_FILE = types.FunctionDeclaration(
        name="run_python_file",
        description="Calling the script file to run",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Script file to call, relative to the working directory (default is the working directory itself)",
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    description="Argument to pass to the script file",
                    items=types.Schema(
                        type=types.Type.STRING,
                    )
                )
            }
        )
    )
    SCHEMA_WRITE_FILE = types.FunctionDeclaration(
        name="write_file",
        description="Write some content to a file",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="File path to write, relative to the working directory (default is the working directory itself)",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="Content to write",
                )
            }
        )
    )
