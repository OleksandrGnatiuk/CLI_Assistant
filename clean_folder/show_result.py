import collections


def show_result(p):

    total_dict = collections.defaultdict(list)  # collect file's suffix
    files_dict = collections.defaultdict(list)  # collect file's name

    for item in p.iterdir():
        if item.is_dir():
            for file in item.iterdir():
                if file.is_file():
                    total_dict[item.name].append(file.suffix)
                    files_dict[item.name].append(file.name)
    for k, v in files_dict.items():
        print()
        print(f" Folder '{k}' contains files: ")
        print(f" ---- {v}")

    print()
    print("               *** File sorting completed successfully! ***   ")
    print("---------------------------------------------------------------------------")
    print("| {:^14} |{:^9}| {:^40} ".format("Folder", "files,pcs", "file's extensions"))
    print("---------------------------------------------------------------------------")

    for key, value in total_dict.items():
        k, a, b = key, len(value), ", ".join(set(value))
        print("| {:<14} |{:^9}| {:<40} ".format(k, a, b))

    print("----------------------------------------------------------------------------")



