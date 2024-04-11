from setuptools import find_packages,setup
from typing import List
NAME = 'sensor'
VERSION = '0.0.0.1'
AUTHOR_EMAIL_ID = 'talk2pankajx@gmail.com'
HYPEN_E_DOT = "-e ."
REQUIREMENTS_FILE_NAME = 'requirements.txt'

def get_requirements(file_path:str = REQUIREMENTS_FILE_NAME)->List[str]:
    requirements =[]
    with open(file_path) as file_obj:
       requirements = file_obj.readlines()
       requirements = [req.replace("\n","") for req in requirements]
    if HYPEN_E_DOT in requirements:
        requirements.remove( HYPEN_E_DOT)
    return requirements

setup(name = NAME,
version= VERSION,
author = AUTHOR_EMAIL_ID,
packages = find_packages(),

)