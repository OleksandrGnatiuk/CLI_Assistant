from collections import UserDict
from datetime import datetime
import pickle
from pathlib import Path
import re


class WrongLengthPhoneError(Exception):
    """ Exception for wrong length of the phone number """


class LetterInPhoneError(Exception):
    """ Exception when a letter is in the phone number """


class Field:
    """ Class for creating fields """

    def __init__(self, value: str):
        self._value = value.strip()

    def __str__(self):
        return self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value.strip().lower().title()


class Name(Field):
    """ Class for creating fields 'name' """

    @Field.value.setter
    def value(self, value: str):
        self._value = value.strip().lower().title()


class Phone(Field):
    """ Class for creating fields 'phone' """

    @staticmethod
    def sanitize_phone_number(phone: str):

        new_phone = str(phone).strip().removeprefix("+").replace(
            "(", "").replace(")", "").replace("-", "").replace(" ", "")
        try:
            new_phone = [str(int(i)) for i in new_phone]
        except ValueError:
            raise LetterInPhoneError("There is letter in the phone number!")

        else:
            new_phone = "".join(new_phone)
            if len(new_phone) == 12:
                return f"+{new_phone}"
            elif len(new_phone) == 10:
                return f"+38{new_phone}"
            else:
                raise WrongLengthPhoneError(
                    "Length of the phone's number is wrong")

    def __init__(self, value: str):
        self._value = Phone.sanitize_phone_number(value)

    @Field.value.setter
    def value(self, value: str):
        self._value = Phone.sanitize_phone_number(value)


class Birthday:
    """ Class for creating fields 'birthday' """

    @staticmethod
    def validate_date(year, month, day):
        try:
            birthday = datetime(year=year, month=month, day=day)
        except ValueError:
            print("Date is not correct\nPlease write date in format: yyyy-m-d")
        else:
            return str(birthday.date())

    def __init__(self, year, month, day):
        self.__birthday = self.validate_date(year, month, day)

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, year, month, day):
        self.__birthday = self.validate_date(year, month, day)


class Email(Field):

    def __str__(self):
        return self._value

    @staticmethod
    def validate_email(email: str) -> str:
        pattern = r"[A-Za-z]+[_.A-Za-z0-9]?[A-Za-z]+@[a-z_]+\.[a-z_]+"
        result = re.findall(pattern, email)
        return result[0]

    @Field.value.setter
    def value(self, value: str):
        if self.validate_email(value):
            self._value = value


class Record:
    """ Class for creating contacts """

    def __init__(self, name: Name, phone: list[Phone] = None, birthday=None, email: Email = None):
        self.name = name
        self.email = email

        if birthday is not None:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = None

        self.phones = []
        if phone:
            self.phones.extend(phone)

    def days_to_bd(self):
        cur_date = datetime.now().date()
        cur_year = cur_date.year

        if self.birthday is not None:
            birthday = datetime.strptime(self.birthday, '%Y-%m-%d')
            this_year_birthday = datetime(cur_year, birthday.month,
                                          birthday.day).date()
            delta = this_year_birthday - cur_date
            if delta.days >= 0:
                return f"{self.name}'s birthday will be in {delta.days} days"
            else:
                next_year_birthday = datetime(cur_year + 1, birthday.month,
                                              birthday.day).date()
                delta = next_year_birthday - cur_date
                return f"{self.name}'s birthday will be in {delta.days} days"
        else:
            return f"{self.name}'s birthday is unknown"

    def add_birthday(self, year, month, day):
        self.birthday = Birthday.validate_date(int(year), int(month), int(day))

    def add_phone(self, phone: str):
        phone = Phone(phone)
        if phone:
            lst = [phone.value for phone in self.phones]
            if phone.value not in lst:
                self.phones.append(phone)
                return "Phone was added"
        else:
            raise ValueError("Phone number is not correct")

    def change_phone(self, old_phone: str, new_phone: str):
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)

        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return "phone was changed"

    def change_email(self, new_email: str):
        self.email = Email(new_email)

    def delete_email(self):
        self.email = None

    def delete_phone(self, old_phone: str):
        old_phone = Phone(old_phone)
        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)

    def add_email(self, email: str):
        email = Email(email)
        if email:
            self.email = email

    def get_contact(self):
        if self.phones:
            phones = ", ".join([str(ph) for ph in self.phones])
        else:
            phones = None
        return {
            "name": str(self.name.value),
            "phone": phones,
            "birthday": self.birthday,
            "email": str(self.email),
        }


class AddressBook(UserDict):
    """ Class for creating address books """

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def remove_record(self, name: str):
        name = name.lower().title()
        if name in self.data:
            self.data.pop(name)

    def all_records(self):
        return {key: value.get_contact() for key, value in self.data.items()}

    def iterator(self):
        for record in self.data.values():
            yield record.get_contact()


p = Path("address_book.bin")
address_book = AddressBook()
if p.exists():
    with open("address_book.bin", "rb") as file:
        address_book.data = pickle.load(file)
