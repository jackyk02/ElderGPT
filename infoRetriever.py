import json
import os
from typing import List

def list_files()-> List[str]:
    """
    This function helps to list files in the data folder, each detiling instances of medication consumption by the user
    :return: list of filenames, each detailing instances of medication consumption by the user
    """
    files = []
    for item in os.listdir("./data"):
        full_path = os.path.join("./data", item)
        if os.path.isfile(full_path):
            files.append(item)
    return files

def read_file(fileName:str)-> List[str]:
    """
    This function helps to read a file in the data folder, each detiling instances of medication consumption by the user
    :param fileName: name of the file
    :return: list of dates the user consumed the medication"""
    with open('./data/'+fileName) as json_file:
        data = json.load(json_file)
        return list(set(data))