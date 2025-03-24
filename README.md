# AI Programming Assistant

## Project Overview

### Purpose and Scope
This project is designed to manage, analyze, and provide summaries of a codebase or project directory. It leverages file handling utilities, embedding, indexing, and language models to offer insights and descriptions of the files and the project as a whole. The system is flexible, supporting various configuration options to tailor the analysis to specific needs.

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

### Latest Updates or Changes
- **Enhanced Configuration Handling:** The `read_yaml_configs` function now returns a `ConfigBox` for easier access and manipulation of configuration settings.
- **Integrated Indexers:** `JsonIndexer` and `TextIndexer` classes provide robust methods for content management, including appending and clearing data.
- **Embedding Capabilities:** The `SimpleEmbedder` supports batch embedding, allowing for efficient processing of multiple texts at once.
- **Improved Language Model Interactions:** The `LMStudioLLM` and `OpenRouterLLM` classes offer more flexible and versatile interactions with language models, adapting to different use cases and user inputs.

## Project Structure

- **Package Initialization:** The `__init__.py` files in various packages (`utils`, `runners`, `indexers`, `embedders`, `llm`) initialize and define the public APIs of these modules, ensuring only necessary functions and classes are exposed.
- **Main Script (`how_it_works.py`):** This script serves as the entry point, initializing a `SimpleRunner` with configurations from `configs.yaml` and running the process.

## Configuration Files

- **Default Configurations (`default_configs.yaml`):** Set essential paths, model names, and file handling rules.
- **Custom Configurations (`configs.yaml`):** Allow customization of configurations for specific projects and use cases.


## Usage

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
    
### Running the Project

1. Ensure all dependencies are installed.
2. Run the main script:
   ```bash
   python how_it_works.py
   ```

### Example Configuration

```yaml
checkpoints_path: "./assistant_data"
embedding_model_name: "sentence-transformers/all-MiniLM-L6-v2"
llm_model_name: "Qwen/Qwen2.5-Coder-32B-Instruct"
project_path: "./"
file_extensions:
  - '.py'
  - '.yaml'
  - '.json'
exclude_dirs:
  - "assistant_data/"
  - ".venv/"
```

## Contributing

Contributions are welcome!