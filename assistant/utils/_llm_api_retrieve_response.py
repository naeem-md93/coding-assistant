from typing import Dict, Any
import os
import json
import requests


def llm_api_retrieve_response(
    api_url: str,
    api_token:str,
    model_name: str,
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
        "Authorization": f"Bearer {api_token}",
    }

    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    }
    data.update(kwargs)

    response = requests.post(url=api_url, headers=headers, data=json.dumps(data))
    print(vars(response))
    response = response.json()["choices"][0]["message"]["content"]

    if "</think>" in response:
        start_index = response.find("</think>") + len("</think>")
        response = response[start_index:]

    return response