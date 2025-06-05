from typing import Dict, Any, List, Union
import os
import dotenv
from together import Together

from .prompts import (
    PROJECT_DESCRIPTION_SYSTEM_PROMPT,
    PROJECT_DESCRIPTION_USER_PROMPT,
    USER_RESPOND_SYSTEM_PROMPT,
    USER_RESPOND_USER_PROMPT
)


dotenv.load_dotenv()


class TogetherAILLM:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.api_token = os.getenv("TOGETHER_AI_API_TOKEN")

    def retrieve_response(
        self,
        system_prompt: str,
        user_prompt: str,
        system_prompt_kwargs: Dict[str, Any] = None,
        user_prompt_kwargs: Dict[str, Any] = None,
        **kwargs
    ):
        client = Together(api_key=self.api_token)

        if system_prompt_kwargs is not None:
            system_prompt = system_prompt.format(**system_prompt_kwargs)

        if user_prompt_kwargs is not None:
            user_prompt = user_prompt.format(**user_prompt_kwargs)

        response = client.chat.completions.create(model=self.model_name, messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ], **kwargs)

        content = response.choices[0].message.content

        return content

    def get_project_description(self, indexer_data: List[Dict[str, Any]]) -> str:

        content = ""
        for i, d in enumerate(indexer_data):
            content += f"File {i + 1} Path: {d['path']}\n"
            content += f"File {i + 1} Last Modified: {d['last_modified']}\n"
            content += f"File {i + 1} Content: {d['content']}\n\n\n"

        response = self.retrieve_response(
            system_prompt=PROJECT_DESCRIPTION_SYSTEM_PROMPT,
            user_prompt=PROJECT_DESCRIPTION_USER_PROMPT,
            system_prompt_kwargs=None,
            user_prompt_kwargs={"content": content},
        )

        return response

    def respond_user(self, user_input: str, project_summary: str, relevant_data_tmp: List[Dict[str, Any]]) -> str:

        relevant_data = ""
        for i, d in enumerate(relevant_data_tmp):
            relevant_data += f"File {i + 1} Path: {d['path']}\n"
            relevant_data += f"File {i + 1} Last Modified: {d['last_modified']}\n"
            relevant_data += f"File {i + 1} Content: {d['content']}\n\n\n"

        response = self.retrieve_response(
            system_prompt=USER_RESPOND_SYSTEM_PROMPT,
            user_prompt=USER_RESPOND_USER_PROMPT,
            system_prompt_kwargs={"project_summary": project_summary},
            user_prompt_kwargs={"user_input": user_input, "relevant_data": relevant_data},
        )

        return response