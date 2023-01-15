import pickle
from datetime import datetime
from pathlib import Path


class RecordNote:

    def __init__(self, note: str):
        self.note = note
        self.tags = set()
        self.date = datetime.now().date()

    def __str__(self):
        result = f'\ndate {self.date}\n{self.note}\n\ntags {self.tags}'
        return result

    def edit_text(self, text):
        self.note = text

    def add_tags(self, tags: list[str]):
        for tag in tags:
            self.tags.add(tag.lower())

    def __del__(self):
        return f"The Note was delete"


class Notebook:
    """Class for creating notes"""

    notes = {}
    counter = 0

    @classmethod
    def read_from_file(cls):
        try:
            with open("notes.bin", "rb") as file:
                result = pickle.load(file)
            return result
        except FileNotFoundError:
            cls.notes = {}

    @classmethod
    def save_to_file(cls):
        with open("notes.bin", "wb") as file:
            pickle.dump(cls.notes, file)

    def add_new_note(self, note: RecordNote):
        id = self.counter + 1
        self.notes[id] = note
        Notebook.counter += 1

    def show_all_notes(self):
        if len(self.notes) > 0:
            result = ""
            for id, rec in self.notes.items():
                tags = ", ".join(rec.tags)
                date = rec.date
                result += f"\nid: {id}          date: {date} \n\n{rec.note}\n\ntags: {tags} \n\n*********\n"
            return result
        else:
            return f"\nNotebook is empty \n"

    def show_note(self, id):
        tags = ", ".join(self.notes[id].tags)
        return f"\nid: {id}        date: {self.notes[id].date} \n\n{self.notes[id].note}\n\ntags: {tags} \n\n********\n "

    def id_is_exist(func):
        """Decorator checks if id exists"""
        def wrapper(*args):
            id = args[1]
            if id in Notebook.notes:
                result = func(*args)
                Notebook.save_to_file()
                return result
            else:
                print(f"\nThe note with id={id} is not exists\n")

        return wrapper

    @id_is_exist
    def to_edit_text(self, id, text):
        self.notes[id].edit_text(text)

    @id_is_exist
    def to_add_tags(self, id, tags: list[str]):
        self.notes[id].add_tags(tags)

    @id_is_exist
    def to_remove_note(self, id):
        del self.notes[id]

    def search(self, text_to_search):
        for id, value in self.notes.items():
            if text_to_search.lower() in value.note.lower(
            ) or text_to_search.lower() in value.tags:
                tags = ", ".join(value.tags)
                result = f"\nid: {id}        date: {value.date} \n\n{value.note}\n\ntags: {tags} \n\n********\n "
                print(result)


file = Path("notes.bin")
nb = Notebook()

if file.exists():
    with open("notes.bin", "rb") as f:
        nb.notes = pickle.load(f)

if __name__ == "__main__":
    # text = "Json – is a good way for serializing files in Python"
    # f = RecordNote(text)
    # nb.add_new_note(f)
    # nb.to_add_tags(1, ["Json", "серіалізація"])
    # nb.to_edit_text(1, "Але є ще безліч інших способів серіалізації")
    # f2 = RecordNote("Pickle is another way for serializating objects")
    # nb.add_new_note(f2)
    # nb.to_add_tags(2, ['pickle'])
    # nb.to_remove_note(1)
    # print(nb.show_note(1))
    print(nb.show_all_notes())
    # nb.search("pickle")
