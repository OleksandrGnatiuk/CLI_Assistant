import pickle
import re
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from .classes import *
from .exceptions import input_error
from .clean import sort_file, show_result
from .notes import *


def save_to_pickle():
    """ Save address book in pickle file"""

    with open("address_book.bin", "wb") as fh:
        pickle.dump(address_book.data, fh)


@input_error
def search(value: str):
    """ Search contact where there is 'text' in the fields: name and phone """

    for record in address_book:
        contact1 = address_book[record]
        for text in contact1.get_contact().values():
            if text is not None:
                if re.findall(value, text):
                    print(address_book[record].get_contact())
                    break


def say_hello(s=None):
    return "How can I help you?"


def say_goodbye(s=None):
    return "Good bye!"


@input_error
def add_contact(value):
    """ Add new contact to address book """

    name, *phones = value.lower().title().strip().split()
    name = Name(name.lower().title())

    if name.value not in address_book:
        record = Record(name)
        address_book.add_record(record)
        if phones:
            for phone in phones:
                record.add_phone(phone)
        save_to_pickle()
        return f"Contact {name.value.title()} was created"
    else:
        return f"Contact {name.value.title()} already exists"


@input_error
def add_em(value):
    name, email = value.split()
    name = name.title()
    if name.title() in address_book:
        address_book[name.title()].add_email(email)
        save_to_pickle()
        return f"The e-mail for {name.title()} was recorded"
    else:
        return f"Contact {name.title()} does not exist"


@input_error
def add_address(value):
    name, address = value.split(" ", 1)
    name = name.title()
    if name.title() in address_book:
        address_book[name.title()].add_adrs(address)
        save_to_pickle()
        return f"The address for {name.title()} was recorded"
    else:
        return f"Contact {name.title()} does not exist"


@input_error
def change_address(value):
    name, address = value.split(" ", 1)
    name = name.title()
    if name.strip().lower().title() in address_book:
        address_book[name.title()].change_adrs(address)
        save_to_pickle()
        return f"The address for {name.title()} was changed"
    else:
        return f"Contact {name.title()} does not exists"


@input_error
def remove_address(value):
    name = value.lower().title().strip()
    if name.title() in address_book:
        address_book[name.title()].delete_adrs()
        save_to_pickle()
        return f"Address for {name.title()} was delete"
    else:
        return f"Contact {name.title()} does not exist"


@input_error
def change_em(value: str):
    name, new_em = value.split()

    if name.strip().lower().title() in address_book:
        address_book[name.strip().lower().title()].change_email(new_em)
        save_to_pickle()
        return f"The e-mail for {name.title()} was changed"
    else:
        return f"Contact {name.title()} does not exists"


@input_error
def remove_em(value):
    name = value.lower().title().strip()

    if name.title() in address_book:
        address_book[name.title()].delete_email()
        save_to_pickle()
        return f"E-mail for {name.title()} was delete"
    else:
        return f"Contact {name.title()} does not exist"


@input_error
def remove_bd(value):
    name = value.lower().title().strip()

    if name.title() in address_book:
        address_book[name.title()].delete_birthday()
        save_to_pickle()
        return f"Birthday for {name.title()} was delete"
    else:
        return f"Contact {name.title()} does not exist"



@input_error
def add_phone(value):
    name, phone = value.lower().strip().title().split()

    if name.title() in address_book:
        address_book[name.title()].add_phone(phone)
        save_to_pickle()
        return f"The phone number for {name.title()} was recorded"
    else:
        return f"Contact {name.title()} does not exist"


@input_error
def remove_phone(value):
    name, phone = value.lower().title().strip().split()

    if name.title() in address_book:
        address_book[name.title()].delete_phone(phone)
        save_to_pickle()
        return f"Phone for {name.title()} was delete"
    else:
        return f"Contact {name.title()} does not exist"


@input_error
def add_contact_birthday(value):
    name, birthday = value.lower().strip().split()
    birthday = tuple(birthday.split("-"))

    if name.title() in address_book:
        address_book[name.title()].add_birthday(*birthday)
        save_to_pickle()
        return f"The Birthday for {name.title()} was recorded"
    else:
        return f"Contact {name.title()} does not exists"


@input_error
def days_to_birthday(name):
    if name.title() in address_book:
        if not address_book[name.title()].birthday is None:
            days = address_book[name.title()].days_to_bd()
            return days
        else:
            return f"{name.title()}'s birthday is unknown"
    else:
        return f"Contact {name.title()} does not exists"


@input_error
def change_ph(value: str):
    name, old_phone, new_phone = value.split()

    if name.strip().lower().title() in address_book:
        address_book[name.strip().lower().title()].change_phone(
            old_phone, new_phone)
        save_to_pickle()
    else:
        return f"Contact {name.title()} does not exists"


@input_error
def remove_contact(name: str):
    record = address_book[name.strip().lower().title()]
    address_book.remove_record(record.name.value)
    save_to_pickle()
    return f"Contact {name.title()} was removed"


@input_error
def contact(name):
    """ Функція відображає номер телефону абонента, ім'я якого було в команді 'phone ...'"""
    if name.title() in address_book:
        record = address_book[name.title()]
        return record.get_contact()
    else:
        return f"Contact {name.title()} does not exist"


@input_error
def show_all(s):
    """ Функція виводить всі записи в телефонній книзі при команді 'show all' """

    if len(address_book) == 0:
        return "Phone book is empty"
    result = ''
    for record in address_book.values():
        result += f"{record.get_contact()}\n"
    return result


@input_error
def clean_f(path):
    folder_to_sort = Path(path)
    p = Path(path)
    try:
        sort_file(folder_to_sort, p)
    except FileNotFoundError:
        print(
            "\nThe folder was not found. Check the folder's path and run the command again!.\n"
        )
        return
    return show_result(folder_to_sort)


@input_error
def new_note(text):
    note_ = RecordNote(text)
    nb.add_new_note(note_)
    return f"The note was created"


@input_error
def ed_note(value):
    id_, text = value.split(" ", 1)
    nb.to_edit_text(id_, text)
    return f"The note was changed"


@input_error
def tags(value):
    id_, *tags_ = value.split()
    nb.to_add_tags(id_, list(tags_))
    return f"Tags for note id:{id_} was added"


@input_error
def sh_notes(value):
    return nb.show_all_notes()


@input_error
def del_notes(id_):
    return nb.to_remove_note(id_)


@input_error
def search_n(text_to_search):
    return nb.search_note(text_to_search)


@input_error
def search_t(tag_to_search):
    return nb.search_tag(tag_to_search)


@input_error
def note(id_):
    return nb.show_note(id_)


def get_birthdays(value=None):
    if value is None:
        period = 7
    else:
        period = int(value.strip())
    return address_book.list_of_birthday(period)


@input_error
def helps(s=None):
    rules = """List of commands:
    1) to add new contact and one or more phones, write command: add contact <name> <phone> <phone> <phone>
    2) to remove contact, write command: remove contact <name>

    3) to add phone, write command: add phone <name> <one phone>
    4) to change phone, write command: change phone <name> <old phone> <new phone>
    5) to remove phone, write command: remove phone <name> <old phone>

    6) to add e-mail, write command: add email <name> <e-mail>
    7) to change e-mail, write command: change email <name> <new e-mail>
    8) to remove e-mail, write command: remove email <name>

    9) to add address, write command: add address <name> <address>
    10) to change address, write command: change address <name> <new address>
    11) to remove address, write command: remove address <name>

    12) to add birthday of contact, write command: add birthday <name> <yyyy-m-d>
    13) to remove birthday, write command: remove birthday <name>
    14) to see how many days to contact's birthday, write command: days to birthday <name>
    15) to see list of birthdays in period, write command: birthdays <period - number of days>

    16) to search contact, where is 'text', write command: search <text>
    17) to see full record of contact, write: phone <name>
    18) to see all contacts, write command: show all
    19) to say goodbye, write one of these commands: good bye / close / exit
    20) to say hello, write command: hello
    21) to see help, write command: help

    22) to sort file in folder, write command: clean-folder <path to folder>

    23) to add note use command: add note <text>
    24) to edit note use command: edit notes <id> <edited text>
    25) to add tags use command: add tags <id> <tag1 tag2 tag3...>
    26) to show all notes use command: show notes
    27) to show any note use command: note <id>
    28) to delete note use command: delete note <id>
    29) to search notes use command: search notes <text_to_search>
    30) to search tags use command: search tags <tag_to_search>
    """
    return rules


# Словник, де ключі - ключові слова в командах, а значення - функції, які при цих командах викликаються
commands = {
    "birthdays": get_birthdays,
    "remove contact": remove_contact,
    "add phone": add_phone,
    "change phone": change_ph,
    "change email": change_em,
    "change address": change_address,
    "remove phone": remove_phone,
    "remove email": remove_em,
    "remove birthday": remove_bd,
    "remove address": remove_address,
    "add birthday": add_contact_birthday,
    "add email": add_em,
    "add address": add_address,
    "days to birthday": days_to_birthday,
    "add contact": add_contact,
    "phone": contact,
    "show all": show_all,
    "hello": say_hello,
    "good bye": say_goodbye,
    "close": say_goodbye,
    "exit": say_goodbye,
    "clean-folder": clean_f,
    "help": helps,
    "add note": new_note,
    "edit note": ed_note,
    "add tags": tags,
    "show notes": sh_notes,
    "delete note": del_notes,
    "search notes": search_n,
    "search tags": search_t,
    "note": note,
    "search": search,
}

cli_completer = WordCompleter([command for command in commands])

@input_error
def main():
    while True:
        command = prompt('Enter command: ', completer=cli_completer)
        if command.lower() in (".", "close", "exit", "good bye"):
            say_goodbye()
            break

        for key in commands:
            if command.lower().strip().startswith(key):
                print(commands[key](command[len(key):].strip()))
                break


if __name__ == "__main__":
    main()
    save_to_pickle()
