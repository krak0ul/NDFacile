import os
import re
from PIL import Image, ImageFile


def load_image(file_path: str) -> ImageFile:
    """
    Loads an image from filepath
    Returns a PIL ImageFile object
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"file '{file_path}' was not found")

    else:
        return Image.open(file_path)


def collect_files(files_dir: str) -> list[str]:
    """
    Collects all files paths from a directory and its subdirectories.
    Returns a list of all collected file paths.
    """
    file_paths = []
    
    for dirpath, dirnames, filenames in os.walk(files_dir):
        for filename in filenames:
            # if filename.lower().endswith('.jsonl'):
            full_path = os.path.join(dirpath, filename)
            file_paths.append(full_path)
    
    return file_paths

def rename_img(img: ImageFile, img_date: str, img_price: float):
    try:
        # TODO: add an iterator or random id if 2 files are NaN_Nan
        formatted_date = re.sub("/", "-", img_date)
        formatted_price = re.sub("\\.", "-", str(img_price))
        img.save(f"./img/parsed/{formatted_date}_{formatted_price}.jpeg")            
    except:
        raise FileExistsError(f"File \"./img/parsed/{img_date}_{img_price}.jpeg \" already exists.")