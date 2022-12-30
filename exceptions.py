from Classes import LetterInPhoneError, WrongLengthPhoneError

def input_error(func):
    """ Декоратор, що повідомляє про виключення """

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return "This record is not exist"
        except ValueError:
            return "This record is not correct!"
        except IndexError:
            return "This command is wrong"
        except LetterInPhoneError:
            return "There is letter in phone number!"
        except WrongLengthPhoneError:
            return "Length of phone's number is wrong!"
    return wrapper 
