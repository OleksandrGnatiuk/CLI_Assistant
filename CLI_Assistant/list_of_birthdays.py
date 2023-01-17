from datetime import datetime, timedelta
from collections import defaultdict

weekdays = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}


def get_birthdays_per_week(users, period=7):
    """ функція виводить список іменинників за вказаний період"""
    current_date = datetime.now()
    current_date = current_date.date()
    end = current_date + timedelta(days=period)

    # створюємо словник, де ключ - дата (об'єкт datetime), а значення: список іменинників
    dct = defaultdict(list)

    for user in users:
        for name, birthday in user.items():
            # замінюємо рік народження іменинників на поточний рік, щоб можна було порівнювати дати
            str_b = birthday.strftime('%y %m %d').split()
            str_b[0] = str(current_date.year)
            str_b = " ".join(str_b)
            birthday = datetime.strptime(str_b, '%Y %m %d')
            birthday = birthday.date()

            # перевіряємо чи припадає д.н. людини на заданий період:
            if current_date <= birthday < end:
                w_day = birthday.weekday()
                if w_day not in (5, 6):
                    # Якщо д.н. припадає на будній день - включаємо в список на той день
                    dct[birthday].append(name)
                elif w_day == 5:
                    # Якщо д.н. припадає на суботу - включаємо в список через два дні - на понеділок
                    dct[birthday + timedelta(days=2)].append(name)
                elif w_day == 6:
                    # Якщо д.н. припадає на неділю - включаємо в список через день - на понеділок
                    dct[birthday + timedelta(days=1)].append(name)
            else:
                continue

    # Оскільки словник має не відсортовані ключі (дати), створюємо допоміжний список, в якому будуть відсортовані ключі
    lst = sorted(dct)

    for d in lst:
        # для виводу результату згідно умови задачі, перетворимо список іменинників на строку:
        lst = ", ".join(dct[d])
        print(f"{weekdays[d.weekday()]}: {lst}")
    if len(dct) == 0:
        print("В данний період днів народження немає!")



#
# if __name__ == "__main__":
#     users = [
#         {"Tanya": datetime(1985, 1, 19)},
#         {"Galyna": datetime(1955, 1, 19)},
#         {"Vasil": datetime(1955, 1, 20)},
#         {"Sasha": datetime(1976, 1, 18)},
#         {"Sofiya": datetime(2013, 1, 23)},
#         {"Roman": datetime(2016, 1, 20)},
#         {"Mukola": datetime(1979, 1, 22)},
#         {"Andriy": datetime(2003, 1, 21)},
#         {"Ulya": datetime(1996, 1, 29)}
#     ]
#
#     get_birthdays_per_week(users, 4)
