from google.genai import types, Client

from functions.call_function import call_function
from model_config import config


def execute(client: Client, messages: list[types.Content], user_prompt: str, verbose=False) -> bool:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=config(),
    )

    candidates = response.candidates
    if candidates:
        for candidate in candidates:
            messages.append(candidate.content)

    usage_metadata = response.usage_metadata
    if not usage_metadata:
        raise RuntimeError("No usage metadata found | request failed")
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {usage_metadata.prompt_token_count}")
        print(f"Response tokens: {usage_metadata.candidates_token_count}")

    function_calls = response.function_calls
    function_responses = []

    # Execute functions
    for function_call in function_calls if function_calls else []:
        result_call = call_function(function_call, verbose=verbose)
        if not result_call.parts:
            raise RuntimeError("No results found | request failed")
        function_response = result_call.parts[0].function_response
        if not function_response:
            raise RuntimeError("No results found | request failed")

        # if verbose:
        print(f"-> {function_response.response}")

        function_responses.append(result_call.parts[0])

    if not function_calls:
        print(f"Raneem AI: {response.text}")
        return False

    messages.append(types.Content(role="user", parts=function_responses))
    return True