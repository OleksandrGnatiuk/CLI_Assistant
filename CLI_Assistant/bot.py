import pickle
import re
from Classes import address_book, Record, Name
from exceptions import input_error
from pathlib import Path
from clean_folder.clean import sort_file, show_result


def save_to_pickle():
    """ Save address book in pickle file"""

    with open("address_book.bin", "wb") as file:
        pickle.dump(address_book.data, file)


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


def show_all(s):
    """ Функція виводить всі записи в телефонній книзі при команді 'show all' """

    if len(address_book) == 0:
        return "Phone book is empty"
    result = ''
    for record in address_book.values():
        result += f"{record.get_contact()}\n"
    return result


def clean_f(path):
    folder_to_sort = Path(path)
    p = Path(path)
    try:
        sort_file(folder_to_sort, p)
    except FileNotFoundError:
        print("\nThe folder was not found. Check the folder's path and run the command again!.\n")
        return
    return show_result(folder_to_sort)


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

    9) to add birthday of contact, write command: add birthday <name> <yyyy-m-d>
    10) to see how many days to contact's birthday, write command: days to birthday <name>

    11) to search contact, where is 'text', write command: search <text>
    12) to see full record of contact, write: phone <name>
    13) to see all contacts, write command: show all
    14) to say goodbye, write one of these commands: good bye / close / exit
    15) to say hello, write command: hello
    16) to see help, write command: help
    
    17) to sort file in folder, write command: clean-folder <path to folder>
    """
    return rules


# Словник, де ключі - ключові слова в командах, а значення - функції, які при цих командах викликаються
commands = {
    "remove contact": remove_contact,
    "add phone": add_phone,
    "change phone": change_ph,
    "change email": change_em,
    "remove phone": remove_phone,
    "remove email": remove_em,
    "add birthday": add_contact_birthday,
    "add email": add_em,
    "days to birthday": days_to_birthday,
    "add contact": add_contact,
    "search": search,
    "phone": contact,
    "show all": show_all,
    "hello": say_hello,
    "good bye": say_goodbye,
    "close": say_goodbye,
    "exit": say_goodbye,
    "clean-folder": clean_f,
    "help": helps
}


@input_error
def main():
    while True:
        command = input("Enter command: ")

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
