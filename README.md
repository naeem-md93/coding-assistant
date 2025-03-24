# AI Programming Assistant

## Project Overview

### Purpose and Scope
This project automates the analysis and summarization of codebases and project directories. It leverages pre-trained transformer models to generate embeddings and descriptions of file contents, and uses language models to provide comprehensive summaries and responses to user queries based on the indexed data. The main functionalities include indexing and managing project files, generating descriptions, and interacting with the user to provide contextually relevant information.

### Key Features and Functionalities

- **Utils Module (`./assistant/utils/`):**
    - **File Operations:**
        - `get_file_paths`: Finds and lists file paths based on specified extensions.
        - `read_text_file`: Reads the content of text files.
        - `write_json_file`: Writes data to JSON files, ensuring directory paths exist.
        - `hash_file_content`: Computes MD5 hashes of file contents.
        - `read_yaml_configs`: Loads configurations from YAML files, converting them to `ConfigBox`.
        - `get_file_content`: Retrieves content from any specified file.
        - `read_json_file`: Reads and parses JSON files.
        - `write_text_file`: Writes content to text files, overwriting existing content if necessary.

- **Runners Module (`./assistant/runners/`):**
    - **Project Interaction:**
        - `SimpleRunner`: Manages the lifecycle of file indexing, removing old indexes, checking and updating file indexes, and running the interaction loop to update the index and respond to user queries.

- **Indexers Module (`./assistant/indexers/`):**
    - **File Indexing:**
        - `TextIndexer`: Reads, updates, writes, appends, and clears text files.
        - `JsonIndexer`: Manages JSON files by reading, updating, writing, clearing, and searching for specific data entries based on query embeddings.

- **Embedders Module (`./assistant/embedders/`):**
    - **Embedding Generation:**
        - `SimpleEmbedder`: Generates embeddings for texts and batches of texts using specified transformer models.

- **LLM Module (`./assistant/llm/`):**
    - **Language Model Interaction:**
        - `LMStudioLLM`: Interacts with LM Studio language models to retrieve responses, generate content descriptions, generate project descriptions, and respond to user queries.
        - `OpenRouterLLM`: Interacts with the OpenRouter API to achieve similar functionalities.
        - `HuggingFaceLLM`: Interacts with Hugging Face models for generating responses and descriptions.

- **Prompts Module (`./assistant/llm/prompts/`):**
    - **System and User Prompts:**
        - `CONTENT_DESCRIPTION_SYSTEM_PROMPT` and `CONTENT_DESCRIPTION_USER_PROMPT`: Define the prompts for generating descriptions of file contents.
        - `PROJECT_DESCRIPTION_SYSTEM_PROMPT` and `PROJECT_DESCRIPTION_USER_PROMPT`: Define the prompts for generating comprehensive project descriptions.
        - `USER_RESPOND_SYSTEM_PROMPT` and `USER_RESPOND_USER_PROMPT`: Define the prompts for guiding AI responses to user queries.

### Configuration
- **Default Configurations (`./assistant/configs/default_configs.yaml`):**
    - Holds essential settings such as paths to checkpoints and data, model names for embeddings and language tasks, and file extensions to manage.

### Latest Updates or Changes
- The `utils` module has been enhanced with comprehensive file handling functions, including reading, writing, and hashing for both text and JSON files.
- The `SimpleRunner` class in the `runners` module now supports more robust file index management, with methods like `remove_old_project_indexes`, `check_file_index`, and `update_project_index`.
- The `JsonIndexer` class includes additional functionalities for processing data after reading and before writing, ensuring that embeddings are stored and retrieved efficiently.
- Prompts for content and project descriptions have been standardized and centralized in the `prompts` module, making the system more modular and easier to maintain.
- The interaction methods in the `llm` module (`LMStudioLLM`, `OpenRouterLLM`, `HuggingFaceLLM`) have been refined to ensure consistent and efficient processing of user queries and responses.

## How to Use This Project

### Prerequisites
- Python 3.12 or newer
- Necessary libraries (e.g., `hashlib`, `yaml`, `torch`, etc.) can be installed via `pip install -r requirements.txt`.

### Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/naeem-md93/programming-assistant.git
   cd programming-assistant
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create an env file:**
   ```bash
    cp .env.example .env
   ```

4. **Create an OpenRouter API Key:**
   <br>
    - Create a free account at [https://openrouter.ai/](openrouter.ai) and place the API TOKEN in the `.env` file
    
5. **Configure:**
   - Create a copy of the configuration file located at `assistant/configs/default_configs.yaml` and modify it as needed:
    ```bash
    cp assistant/configs/default_configs.yaml config.yaml
    nano config.yaml
    ```
    
6. **Run and Index Your Project:**
   - see `how_it_works.py` file for instructions on how to use it.
   
### Example
The assistant first needs to index your project files.

```python
from assistant.runners import SimpleRunner

# Pass your config file
runner = SimpleRunner("path-to-your-config-file")
runner.run()
```
after a complete indexing, it will prompt you to get your request
