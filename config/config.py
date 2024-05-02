import json
import os

def load_config():
    # Correct the path to where the config.json is actually located
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Gets the directory of the current script
    config_path = os.path.join(dir_path, 'config.json') 
    with open(config_path, "r") as file:
        config = json.load(file)
    return config
