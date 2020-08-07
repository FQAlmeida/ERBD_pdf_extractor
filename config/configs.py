from yaml import (load, FullLoader)
from pathlib import Path
from typing import (List)
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "files.yaml"

def _get_configs():
    with Path(CONFIG_PATH).open("r") as config_file:
        configs = load(config_file, Loader=FullLoader)
    return configs   

configs = _get_configs()

def _get_years() -> List[int]:
    return configs['files']["years"]

def _get_file_path_template() -> str:
    return configs['files']["file_names_template"]

def _get_root_folder() -> str:
    return configs['files']["root_folder"]

def get_document_paths() -> List[Path]:
    template_name = _get_file_path_template()
    years = _get_years()
    root_folder = _get_root_folder()
    filepaths = list()
    for year in years:
        filename = template_name.replace(r"{{year}}", str(year)) + ".pdf"
        filepath = Path(".") / root_folder / str(year) / filename
        filepaths.append(filepath)
    return filepaths