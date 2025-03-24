from assistant.runners import SimpleRunner


if __name__ == '__main__':

    runner = SimpleRunner("./configs.yaml")
    runner.run()
