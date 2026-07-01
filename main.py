import sys

from execute_the_model import execute
from settings import API_KEY

from google import genai
from google.genai import types
import argparse

def main():
    parser = argparse.ArgumentParser(description="ChatBot")
    parser.add_argument("user_prompt", type=str, help="User prompt")  # to read the user question
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]
    client = genai.Client(api_key=API_KEY)
    continue_processing: bool = True

    for _ in range(20):
        continue_processing = execute(client, messages, args.user_prompt, args.verbose)
        if not continue_processing:
            break

    if continue_processing:
        print("You reached the limit of requesting")
        sys.exit(1)

if __name__ == "__main__":
    main()
