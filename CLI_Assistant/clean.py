import shutil
import sys
from datetime import datetime
from pathlib import Path
import json
from .translate_char import normalize
from .show_result import show_result


with open(r"CLI_Assistant/extension_dict.json", "r") as file:
    extension_dict = json.load(file)


def is_file_exists(file, to_dir):
    """ if the file is exists with same name, this file will be renamed - 
    date-time will be added to file's name"""

    if file in to_dir.iterdir():
        add_name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
        new_name = file.resolve().stem + f"_{add_name}_" + file.suffix
        new_name_path = Path(to_dir, new_name)
        return new_name_path
    return file


def is_fold_exists(file, to_dir):
    """ Перевіряємо чи існує необхідна папка, якщо немає - створюємо;
    file - посилання на файл, який переміщаємо;    dr - посилання на папку, куди необхідно перемістити файл."""
    if to_dir.exists():
        folder_sort(file, to_dir)
    else:
        Path(to_dir).mkdir()
        folder_sort(file, to_dir)


def folder_sort(file, to_dir):
    """ змінює назву файла та переміщає в необхідну папку.
    file - посилання на файл,  який переміщаємо;    dr - посилання, на папку, куди необхідно перемістити файл."""
    latin_name = normalize(file.name)
    new_file = Path(to_dir, latin_name)
    file_path = is_file_exists(new_file, to_dir)
    file.replace(file_path)


def sort_file(folder_to_sort, p):
    """ Check extension of files, subfolders and sort it"""
    for i in p.iterdir():
        if i.name in ("documents", "audio", "video", "images", "archives", "other"): # the script ignores these folders.
            continue
        if i.is_file():
            flag = False  # if flag stay False - file's extension is not in extension_dict and we need move this file to "other"
            for f, suf in extension_dict.items():
                if i.suffix.lower() in suf:
                    to_dir = Path(folder_to_sort, f)
                    is_fold_exists(i, to_dir)
                    flag = True  # if file's extension was founded in extension_dict, flag == True
                else:
                    continue
            if not flag:
                # if flag == False: extension of file was not founded in extension_dict. We need move this file to "other"
                to_dir = Path(folder_to_sort, "other")
                is_fold_exists(i, to_dir)
        elif i.is_dir():
            if len(list(i.iterdir())) != 0:
                sort_file(folder_to_sort, i) # if the folder is not empty, recursively sort_file()
            else:
                shutil.rmtree(i)  # delete empty folders

    for j in p.iterdir():
        # unpacking archives
        if j.name == "archives" and len(list(j.iterdir())) != 0:
            for arch in j.iterdir():
                if arch.is_file() and arch.suffix in (".zip", ".gz", ".tar"):
                    try:
                        arch_dir_name = arch.resolve().stem  # створюємо назву папки, куди розпаковуємо архів (за назвою самого архіва)
                        path_to_unpack = Path(p, "archives", arch_dir_name) # створюємо шлях до папки розпаковки архіва
                        shutil.unpack_archive(arch, path_to_unpack)
                    except:
                        print(f"Attention: Error unpacking the archive '{arch.name}'!\n")
                    finally:
                        continue
                else:
                    continue
        elif j.is_dir() and not len(list(j.iterdir())):
            # delete empty folders:
            shutil.rmtree(j)


def main():
    path = sys.argv[1]  # run from the command line: `clean-folder /path/to folder/you want to clean/`
    # path = r"C:\Users\Rezerv\Desktop\trash"
    folder_to_sort = Path(path)
    p = Path(path)
    try:
        sort_file(folder_to_sort, p)
    except FileNotFoundError:
        print("\nThe folder was not found. Check the folder's path and run the command again!.\n")
        return
    return show_result(folder_to_sort)


if __name__ == "__main__":
    main()
