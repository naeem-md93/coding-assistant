from datetime import datetime


def get_now():
    return datetime.today().strftime('%Y_%m_%d_%H_%M_%S')