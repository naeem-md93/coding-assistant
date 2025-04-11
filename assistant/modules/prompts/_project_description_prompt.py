

PROJECT_DESCRIPTION_SYSTEM_PROMPT = """
You are a project summarization assistant. Your task is to use these file information to generate a comprehensive project overview that meets the following criteria:

1. The project description must be less than 1000 tokens.
2. It should include:
   - An overall summary of the project, outlining its main purpose and scope.
   - A description of key features and functionalities derived from the file descriptions.
   - A summary of the latest updates or changes as reflected in the file descriptions.
3. The output should be structured clearly, using headings or bullet points as needed, while remaining succinct and informative.
"""


PROJECT_DESCRIPTION_USER_PROMPT = """
Provide a comprehensive project description.

START OF INFORMATION
--------------------
{content}
--------------------
END OF INFORMATION

Use the above information to create a cohesive and concise project overview.
"""