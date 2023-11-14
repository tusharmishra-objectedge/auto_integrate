import openai
from auto_integrate_cli.settings.default import (
    OPENAI_API_KEY,
    OPENAI_API_ORG_ID,
)

from .base import BaseMapper

openai.organization = OPENAI_API_ORG_ID
openai.api_key = OPENAI_API_KEY


class OpenAIAPIMapper(BaseMapper):
    def __init__(self, api1, api2):
        super().__init__(api1, api2)

    def map(self, engine="text-davinci-003"):
        instruction = f"""Map fields from api1 to api2 while maintaining
        context like with description and constraints if provided. Also,
        considering data types integration feasibility. api1: {self.api1} and
        api2: {self.api2}. Answer in JSON format:
        field_name_from_api1: field_name_from_api2, ...
        """
        if engine == "text-davinci-003":
            return self.completion_map(engine=engine, prompt=instruction)
        if engine == "gpt-3.5-turbo-16k":
            return self.chat_completion_map(
                engine=engine, instruction=instruction
            )
        raise ValueError(f"Unknown engine: {engine}")

    def completion_map(self, engine="text-davinci-003", prompt=None):
        if not prompt:
            print("Prompt is empty.")
            return {}
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                max_tokens=3000,
                # temperature=0.5,
            )
        except openai.error.RateLimitError:
            print("Rate limit exceeded.")
            return {}
        # print(f"\nResponse: {response}\n")
        return self.parse_response(response.choices[0].text.strip())

    def chat_completion_map(
        self, engine="gpt-3.5-turbo-16k", instruction=None
    ):
        messages = [
            {
                "role": "system",
                "content": "Assistant's response is always in JSON.",
            },
            {"role": "user", "content": f"{instruction}"},
        ]
        try:
            response = openai.ChatCompletion.create(
                model=engine,
                messages=messages,
                max_tokens=3000,
                # temperature=0.5,
            )
            print(f"\nResponse: {response}\n")
        except openai.error.RateLimitError:
            print("Rate limit exceeded.")
            return {}
        return self.parse_response(response.choices[0].message.content.strip())

    def parse_response(self, generated_mapping):
        # generated_mapping = response.choices[0].text.strip()

        print(f"\nGenerated mapping: \n{generated_mapping}\n")

        field_mapping = {}

        for line in generated_mapping.split("\n"):
            parts = line.split(":")
            if len(parts) == 2:
                field_mapping[parts[0].strip()] = parts[1].strip()

        print(f"\nField mapping: {field_mapping}\n")

        return field_mapping
