from assistant import ProjectManager


if __name__ == '__main__':

    runner = ProjectManager("./assistant/configs/default_configs.yaml")
    runner.run()
