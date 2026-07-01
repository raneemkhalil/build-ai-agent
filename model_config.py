from functions.call_function import functions_to_use
from google.genai import types

from settings import SYSTEM_PROMPT


def config():
    # to provide to the LLM.
    available_functions = types.Tool(
        function_declarations=functions_to_use,
    )

    return types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0, tools=[available_functions])


