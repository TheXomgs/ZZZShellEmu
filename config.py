from configparser import ConfigParser

def get_config(path):
    config = ConfigParser()
    config.read(path)
    return config