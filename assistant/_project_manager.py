from typing import List, Dict
from tqdm import tqdm

from . import utils
from .modules import (
    TransformersEmbedder,
    JsonIndexer,
    TextIndexer,
    OpenRouterLLM,
    FileManager
)


class ProjectManager:
    def __init__(self, config_file_path: str) -> None:

        configs = utils.read_yaml_config_file(config_file_path)

        checkpoint_path = configs.pop("checkpoints_path")
        self.project_path = configs.pop("project_path")
        self.file_extensions = configs.pop("file_extensions")
        self.ignore_dirs = configs.pop("ignore_dirs")

        self.file_change_tracker = JsonIndexer(checkpoint_path, "file_change_tracker.json")
        self.project_indexer = JsonIndexer(checkpoint_path, "project_index.json")
        self.summary_indexer = TextIndexer(checkpoint_path, "project_summary.txt")
        self.history = TextIndexer(checkpoint_path, "conversation_history.md")

        self.embedder = TransformersEmbedder(configs.pop("embedding_model_name"))
        self.llm = OpenRouterLLM(configs.pop("llm_model_name"))

    def get_file_objs_for_indexing(self, project_file_paths: List[str]) -> List[FileManager]:

        file_objs = []

        for file_path in project_file_paths:

            if len(utils.read_text_file(file_path)) == 0:
                continue

            file_obj = FileManager(file_path)

            if self.project_indexer.is_key_exists(file_path):
                if file_obj.hash != self.project_indexer.get_data(file_path)["hash"]:
                    file_objs.append(file_obj)
            else:
                file_objs.append(file_obj)

        return file_objs

    def remove_old_project_indexes(self, indexing_file_objs: List[FileManager]) -> None:
        indexing_hashes = [obj.path for obj in indexing_file_objs]

        for key in list(self.project_indexer.get_content().keys()):
            if key not in indexing_hashes:
                self.project_indexer.remove_data(key)

    def index_a_file(self, file_obj: FileManager) -> None:
        self.project_indexer.add_data(file_obj.path, {
            "path": file_obj.path,
            "hash": file_obj.hash,
            "type": file_obj.extensions,
            "content": file_obj.content,
            "last_modified": utils.get_now(),
            "embedding": self.embedder.batch_embed([file_obj.content]).tolist()[0]
        })
        self.project_indexer.write_content()

    def run(self) -> None:

        while True:
            project_file_paths = utils.get_project_file_paths(self.project_path, self.file_extensions, self.ignore_dirs)

            indexing_file_objs = self.get_file_objs_for_indexing(project_file_paths)

            self.remove_old_project_indexes(indexing_file_objs)

            for file_obj in tqdm(indexing_file_objs):
                self.index_a_file(file_obj)

            if len(indexing_file_objs) > 0:
                description = self.llm.get_project_description(list(self.project_indexer.get_content().values()))
                self.summary_indexer.update_content(description)
                self.summary_indexer.write_content()

            user_input = input("Enter your request (or 'q' to quit): ")
            if user_input == "q":
                break

            query_embedding = self.embedder.batch_embed([user_input])
            relevant_data = utils.search_database(query_embedding, self.project_indexer.get_content(), topk=5)
            suggestions = self.llm.respond_user(user_input, self.summary_indexer.get_content(), relevant_data)

            sep = "\n***\n"
            txt = f"# Q: {user_input}{sep}# A:\n{suggestions}"
            self.history.append_content(txt, sep)
            self.history.write_content()
            print(suggestions)