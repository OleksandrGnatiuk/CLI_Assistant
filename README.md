
## CLI Assistant

The assistant was written in the __OOP paradigm__, the following libraries were used: __re, datetime, pathlib, collections, shutil, json, pickle__.
The address book saves to __pickle__ file.
___

### CLI assistant helps to manage the address book

if you want:

- [x] To __get short tips__ on how to use you can call `help` command at any time during your work with assistant

<p>

- [x] to __add new contact__ and one or more phones (for example 2 phones), write command: `add contact <name> <phone> <phone>`
- [x] to __remove contact__, write command: `remove contact <name>`

<p>

- [x] to __add phone to contact__, write command: `add phone <name> <one phone>`
- [x] to __change phone of contact__, write command: `change phone <name> <old phone> <new phone>`
- [x] to __remove phone of contact__, write command: `remove phone <name> <old phone>`

<p>

- [x] to __add e-mail to contact__, write command: `add email <name> <e-mail>`
- [x] to __change e-mail of contact__, write command: `change email <name> <new e-mail>`
- [x] to __remove e-mail of contact__, write command: `remove email <name>`

<p>

- [x] to __add birthday of contact__, write command: `add birthday <name> <yyyy-m-d>`
- [x] to __see how many days to contact's birthday__, write command: `days to birthday <name>`

<p>

- [x] to __search contact__ with <text to search>, write command: `search <text to search>`
- [x] to __see full record of contact__, write: `phone <name>`
- [x] to __see all contacts__, write command: `show all`
- [x] to __say goodbye__, write one of these commands: `good bye` or `close` or `exit`
- [x] to __say hello__, write command: `hello`

<p>

- [x] to __sort files in folder__ , write command: `clean-folder <path to folder>`

___

### Clean-folder script

<p> This script can sort all files in the folder. The script sorts all files according to file's extensions.</p>

- [x] if this folder is not exists, you'll see a message in console.
- [x] The script sorts files according to file's extensions and replaces files to the destination folders.
- [x] Default destination folders are `documents`, `images`, `video`, `audio` and `archives`.
- [x] if you want to set your own rules of sorting files you have to change **extension_dict.json** file:

  ```python
{
    "documents": [".doc", ".docx", ".xls", ".xlsx", ".txt", ".pdf"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "archives": [".zip", ".gz", ".tar"],
}
  ```

- [x] All files with relevant extensions will be moved to these folders;
- [x] Other files will be replaced to folder `other`;
- [x] if these folders were not exist its will be created;
- [x] The script recursively checks all subfolders and replaces all files to destination folders;
- [x] Empty folders will be deleted;
- [x] Files with Cyrillic name will be **renamed to Latin name**;
- [x] if subfolders involve the files with the same name, these files will be renamed - **date-time will be added to file's name**;
- [x] All archives will be unpacked to subfolder with the name as archive's name in folder `archive`;
- [x] if archive is broken, script will continue its work without unpacking this archive. In console you'll see message about this broken archive;
- [x] When script finishes to clean folder, you'll see the report.

If any questions, please contact to oleksandr.gnatiuk@gmail.com
