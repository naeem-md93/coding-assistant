from typing import Dict, Any, List, Union
import os
import dotenv

from .. import utils


from .prompts import (
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
        self.api_token = os.getenv("OPENROUTER_API_TOKEN")

    def get_project_description(self, indexer_data: List[Dict[str, Any]]) -> str:

        content = ""
        for i, d in enumerate(indexer_data):
            content += f"File {i + 1} Path: {d['path']}\n"
            content += f"File {i + 1} Last Modified: {d['last_modified']}\n"
            content += f"File {i + 1} Content: {d['content']}\n\n\n"

        response = utils.llm_api_retrieve_response(
            api_url=self.api_url,
            api_token=self.api_token,
            model_name=self.model_name,
            system_prompt=PROJECT_DESCRIPTION_SYSTEM_PROMPT,
            user_prompt=PROJECT_DESCRIPTION_USER_PROMPT,
            system_prompt_kwargs=None,
            user_prompt_kwargs={"content": content},
            **{
                "temperature": 0.2
            }
        )

        return response

    def respond_user(self, user_input: str, project_summary: str, relevant_data_tmp: List[Dict[str, Any]]) -> str:

        relevant_data = ""
        for i, d in enumerate(relevant_data_tmp):
            relevant_data += f"File {i + 1} Path: {d['path']}\n"
            relevant_data += f"File {i + 1} Last Modified: {d['last_modified']}\n"
            relevant_data += f"File {i + 1} Content: {d['content']}\n\n\n"


        response = utils.llm_api_retrieve_response(
            api_url=self.api_url,
            api_token=self.api_token,
            model_name=self.model_name,
            system_prompt=USER_RESPOND_SYSTEM_PROMPT,
            user_prompt=USER_RESPOND_USER_PROMPT,
            system_prompt_kwargs={"project_summary": project_summary},
            user_prompt_kwargs={"user_input": user_input, "relevant_data": relevant_data},
            **{
                "temperature": 0.2
            }
        )

        return response