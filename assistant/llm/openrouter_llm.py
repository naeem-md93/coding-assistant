import json
from typing import Dict, Any, List, Union
import os
import dotenv
import requests
import numpy as np


from .prompts import (
    CONTENT_DESCRIPTION_SYSTEM_PROMPT,
    CONTENT_DESCRIPTION_USER_PROMPT,
    PROJECT_DESCRIPTION_SYSTEM_PROMPT,
    PROJECT_DESCRIPTION_USER_PROMPT,
    USER_RESPOND_SYSTEM_PROMPT,
    USER_RESPOND_USER_PROMPT
)


dotenv.load_dotenv()


class OpenRouterLLM:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def retrieve_response(
        self,
        system_prompt: str,
        user_prompt: str,
        system_prompt_kwargs: Dict[str, Any] = None,
        user_prompt_kwargs: Dict[str, Any] = None,
        **kwargs
    ) -> str:

        if system_prompt_kwargs is not None:
            system_prompt = system_prompt.format(**system_prompt_kwargs)

        if user_prompt_kwargs is not None:
            user_prompt = user_prompt.format(**user_prompt_kwargs)

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_TOKEN')}",
        }

        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        }

        response = requests.post(url=self.api_url, headers=headers, data=json.dumps(data))
        response = response.json()["choices"][0]["message"]["content"]

        if "</think>" in response:
            start_index = response.find("</think>") + len("</think>")
            response = response[start_index:]

        return response

    def get_content_description(self, file_path: str, content: str) -> str:

        response = self.retrieve_response(
            system_prompt=CONTENT_DESCRIPTION_SYSTEM_PROMPT,
            user_prompt=CONTENT_DESCRIPTION_USER_PROMPT,
            system_prompt_kwargs=None,
            user_prompt_kwargs={"file_path": file_path, "content": content},
            **{
                "temperature": 0.95
            }
        )

        return response

    def get_project_description(self, project_file_descriptions: Dict[str, Dict[str, Union[str, np.ndarray]]]) -> str:

        content = ""
        for i, (_, d) in enumerate(project_file_descriptions.items()):
            content += f"File {i + 1} Path: {d['file_path']}\n"
            content += f"File {i + 1} Description: {d['description']}\n\n"
        response = self.retrieve_response(
            system_prompt=PROJECT_DESCRIPTION_SYSTEM_PROMPT,
            user_prompt=PROJECT_DESCRIPTION_USER_PROMPT,
            system_prompt_kwargs={"content": content},
            user_prompt_kwargs=None,
            **{
                "temperature": 0.95
            }
        )

        return response

    def respond_user(self, user_input: str, project_summary: str, relevant_data_tmp: List[Dict[str, Any]]) -> str:

        relevant_data = ""
        for i, d in enumerate(relevant_data_tmp):
            relevant_data += f"File {i + 1} Path: {d['file_path']}\n"
            relevant_data += f"File {i + 1} Description: {d['description']}\n"
            relevant_data += f"File {i + 1} Content: {d['content']}\n\n"


        response = self.retrieve_response(
            system_prompt=USER_RESPOND_SYSTEM_PROMPT,
            user_prompt=USER_RESPOND_USER_PROMPT,
            system_prompt_kwargs={"project_summary": project_summary},
            user_prompt_kwargs={"user_input": user_input, "relevant_data": relevant_data},
            **{
                "temperature": 0.95
            }
        )

        return response