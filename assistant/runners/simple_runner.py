import logging
from typing import List
from tqdm import tqdm

from .. import utils
from ..embedders import SimpleEmbedder
from ..indexers import JsonIndexer, TextIndexer
from ..llm import OpenRouterLLM


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class SimpleRunner:
    def __init__(self, configs_path: str) -> None:
        try:

            logging.info(f"Loading configurations from {configs_path}")
            configs = utils.read_yaml_configs(configs_path)
            logging.debug(f"Configs loaded: {configs}")

            checkpoint_path = configs.pop("checkpoints_path")

            self.project_indexer = JsonIndexer(checkpoint_path, "coding_assistant_project_index.json")
            self.summary_indexer = TextIndexer(checkpoint_path, "coding_assistant_project_summary.txt")
            self.history = TextIndexer(checkpoint_path, "history.md")
            self.embedder = SimpleEmbedder(configs.pop("embedding_model_name"))
            self.llm = OpenRouterLLM(configs.pop("llm_model_name"))

            self.project_path = configs.pop("project_path")
            self.file_extensions = configs.pop("file_extensions")
            self.update_summary = False
            logging.info("Initialization complete")

        except Exception as e:
            logging.error(f"Failed to initialize SimpleRunner: {e}")
            raise

    def remove_old_project_indexes(self, project_files: List[str]) -> None:
        try:
            logging.info("Removing old project indexes")
            for fp in self.project_indexer.get_content().keys():
                if fp not in project_files:
                    logging.debug(f"Removing index for {fp}")
                    self.project_indexer.remove_data(fp)
            logging.info("Old project indexes removed")
        except Exception as e:
            logging.error(f"Failed to remove old project indexes: {e}")

    def check_file_index(self, fp) -> None:

        try:
            logging.info(f"Checking index for file {fp}")

            content = utils.get_file_content(fp)
            if len(content) == 0:
                logging.debug(f"File {fp} is empty, skipping")
                return

            if len(content) > 4096:
                logging.warning(f"Content too long ({len(content)} > 4096) for file {fp}")

            content_hash = utils.hash_file_content(content)

            data = self.project_indexer.get_data(fp)

            if len(data) != 0:
                if content_hash == data["hash"]:
                    logging.debug(f"File {fp} content has not changed, skipping")
                    return

            content_embedding = self.embedder.embed(content)
            description = self.llm.get_content_description(fp, content)
            description_embedding = self.embedder.embed(description)
            logging.debug(f"Generated description for {fp}: {description}")

            data = {
                'file_path': fp,
                "hash": content_hash,
                "content": content,
                "description": description,
                'content_embedding': content_embedding,
                'description_embedding': description_embedding,
            }

            self.project_indexer.update_content(fp, data)
            self.project_indexer.write_content()
            self.update_summary = True
            logging.info(f"Index for {fp} updated")
        except Exception as e:
            logging.error(f"Failed to check file index for {fp}: {e}")

    def update_project_index(self) -> None:
        try:
            logging.info("Updating project index")
            project_files = utils.get_file_paths(self.project_path, self.file_extensions)

            self.remove_old_project_indexes(project_files)

            self.update_summary = False
            for fp in tqdm(project_files):
                self.check_file_index(fp)

            if self.update_summary:
                description = self.llm.get_project_description(self.project_indexer.get_content())
                self.summary_indexer.update_content(description)
                self.summary_indexer.write_content()
                logging.info("Project summary updated")
        except Exception as e:
            logging.error(f"Failed to update project index: {e}")

    def run(self) -> None:
        try:
            logging.info("Starting interaction loop")
            # Main loop to interact with the user
            while True:
                self.update_project_index()

                user_input = input("Enter your request (or 'q' to quit): ")
                if user_input == "q":
                    break

                # Generate embedding for the user input
                query_embedding = self.embedder.embed(user_input)

                relevant_data = self.project_indexer.search_content(query_embedding, top_k=5)
                logging.debug(f"Relevant data found: {relevant_data}")

                # Generate suggestions
                suggestions = self.llm.respond_user(
                    user_input,
                    self.summary_indexer.get_content(),
                    relevant_data
                )
                logging.info(f"Suggestions generated: {suggestions}")

                sep = "\n***\n"
                txt = f"# Q: {user_input}{sep}# A:\n{suggestions}"
                self.history.append_content(txt, sep)
                self.history.write_content()
                print(suggestions)
        except Exception as e:
            logging.error(f"Interaction loop failed: {e}")
        finally:
            logging.info("Interaction loop ended")