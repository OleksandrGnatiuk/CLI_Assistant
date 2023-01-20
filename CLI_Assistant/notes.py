import pickle
from datetime import datetime
from pathlib import Path


class RecordNote:

    def __init__(self, note: str):
        self.note = note
        self.tags = set()
        self.date = datetime.now().date()

    def edit_text(self, text_):
        self.note = text_

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
            with open("notes.bin", "rb") as fh:
                result = pickle.load(fh)
            return result
        except FileNotFoundError:
            cls.notes = {}

    @classmethod
    def save_to_file(cls):
        with open("notes.bin", "wb") as fh:
            pickle.dump(cls.notes, fh)

    def add_new_note(self, note: RecordNote):
        id_ = self.counter + 1
        self.notes[id_] = note
        Notebook.counter += 1
        self.save_to_file()

    def show_all_notes(self):
        if len(self.notes) > 0:
            result = ""
            for id_, rec in self.notes.items():
                tags = ", ".join(rec.tags)
                date = rec.date
                result += f"\nid: {id_}      date: {date} \n{rec.note}\ntags: {tags} \n=========\n"
            return result
        else:
            return f"Notebook is empty"

    def is_id_exist(func):
        """Decorator checks if id exists"""

        def wrapper(*args):
            id_ = args[1]
            if int(id_) in args[0].notes:
                result = func(*args)
                Notebook.save_to_file()
                return result
            else:
                print(f"\nThe note with id={id_} is not exists\n")

        return wrapper

    @is_id_exist
    def to_edit_text(self, id_, text_):
        self.notes[int(id_)].edit_text(text_)

    @is_id_exist
    def to_add_tags(self, id_, tags: list[str]):
        self.notes[int(id_)].add_tags(tags)

    @is_id_exist
    def to_remove_note(self, id_):
        del self.notes[int(id_)]
        print(f"The note id:{id_} was delete!")

    @is_id_exist
    def show_note(self, id_):
        tags = ", ".join(self.notes[int(id_)].tags)
        return f"\nid: {id_}     date: {self.notes[int(id_)].date} \n{self.notes[int(id_)].note}\ntags: {tags} \n========\n "

    def search_note(self, text_to_search: str):
        for id_, value in self.notes.items():
            if text_to_search.lower().strip() in value.note.lower():
                tags = ", ".join(value.tags)
                result = f"id: {id_}    date: {value.date} \n{value.note}\ntags: {tags} \n========\n "
                print(result)

    def search_tag(self, tag_to_search: str):
        for id_, value in self.notes.items():
            if tag_to_search.lower().strip() in value.tags:
                tags = ", ".join(value.tags)
                result = f"id: {id_}    date: {value.date} \n{value.note}\ntags: {tags} \n========\n "
                print(result)


file = Path("notes.bin")
nb = Notebook()

if file.exists():
    with open("notes.bin", "rb") as f:
        dct = pickle.load(f)
        nb.notes.update(dct)
        ids = [int(i) for i in nb.notes]
        if len(ids) > 0:
            nb.counter = max(ids)
        else:
            nb.counter = 0
