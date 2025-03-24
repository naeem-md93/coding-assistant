from assistant.runners import SimpleRunner


if __name__ == '__main__':

    runner = SimpleRunner("./assistant/configs/default_configs.yaml")
    runner.run()
