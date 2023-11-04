import calendar as cal
import datetime
import curses

class Calendar():
    #widok kalendarza
    months = {1: "styczen", 2: "luty", 3: "marzec", 4: "kwiecien", 5: "maj", 6: "czerwiec", 7: "lipiec", 8: "siepien", 9: "wrzesien", 10: "pazdziernik", 11: "listopad", 12: "grudzien"}
    days = {1: "poniedzialek", 2: "wtorek", 3: "sroda", 4: "czwartek", 5: "piatek", 6: "sobota", 7: "niedziela"}

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.current_day = datetime.date.today().day
        self.current_month = datetime.date.today().month
        self.current_year = datetime.date.today().year
        self.highlight_day = self.current_day
        self.stdscr.keypad(True)
        self.showCalendar1()

    def getYear(self):
        return datetime.date.today().year
    def getMonth(self):
        return self.months[datetime.date.today().month]

    def showDay(self):
        return datetime.date.today().day, self.days[datetime.date.today().weekday()]

    def showCalendar1(self):
        #widok tego miesiaca uzupelniony o dodatkowe dni
        print("                  ", self.getMonth(), self.getYear())
        print('=====================================================')

        kalendarz = cal.Calendar()
        week = 1
        currentMonth = []
        currentWeek = []
        for iterweekday in kalendarz.itermonthdates(2023, 11):
            currentWeek.append(iterweekday.day)
            if week == 7:
                week = 0
                currentMonth.append(currentWeek)
                currentWeek = []
            week += 1

        up = " ____  "
        down = " ----  "
        dayToday = datetime.date.today().day+29
        first=True
        today = "****** "
        print("  pon     wt      sr     czw      pt      so     nie")
        for week in currentMonth:
            for day in week:
                if day == dayToday:
                    print(today, end=" ")
                else:
                    print(up, end=" ")
            print()
            for day in week:
                if day == dayToday:
                    if day > 9:
                        print("#", day, "# ", end=" ")
                    else:
                        print("# ", day, "# ", end="")
                else:
                    if day > 9:
                        print("|", day, "| ", end=" ")
                    else:
                        print("| ", day, "|  ", end="")
            print()
            for day in week:
                if day == dayToday:
                    print(today, end=" ")
                else:
                    print(down, end=" ")
            print()

    def showCalendar2(self, chosenDay):
        #2 opcja wyswietlania kalendarza, tylko dni z tego miesiaca
        self.stdscr.clear()
        self.stdscr.refresh()

        print("                  ", self.getMonth(), self.getYear())
        print('=====================================================')

        kalendarz = cal.Calendar()
        week = 1
        currentMonth = []
        currentWeek = []
        for iterweekday in kalendarz.itermonthdays(2023, 11):
            if iterweekday==0:
                currentWeek.append(" ")
            else:
                currentWeek.append(str(iterweekday))
            if week == 7:
                week = 0
                currentMonth.append(currentWeek)
                currentWeek = []
            week += 1

        self.stdscr.clear()
        index=1
        monthLen=len(currentMonth)
        up = " ____  "
        blank = "       "
        down = " ----  "
        today = "****** "
        # dayToday = str(datetime.date.today().day)
        dayToday = str(chosenDay)
        print()
        print("  pon     wt      sr     czw      pt      so     nie")
        for week in currentMonth:
            # pierwszy i ostatni miesiac
            if index==1 or index==monthLen:
                # gora
                for day in week:
                    if day==" ":
                        print(blank, end=" ")
                    elif day== dayToday:
                        print(today, end=" ")
                    else:
                        print(up, end=" ")
                print()
                # srodek
                for day in week:
                    if day==" ":
                        print("       ", end=" ")
                    elif len(day)==1:
                        if day == dayToday:
                            print("# ", day, "# ", end=" ")
                        else:
                            print("| ", day, "| ", end=" ")
                    else:
                        if day== dayToday:
                            print("#", day, "# ", end=" ")
                        else:
                            print("|", day, "| ", end=" ")
                print()
                # dol
                for day in week:
                    if day == " ":
                        print(blank, end=" ")
                    elif day== dayToday:
                        print(today, end=" ")
                    else:
                        print(down, end=" ")
                print()

            # pozostale miesiace
            else:
                # gora
                for day in week:
                    if day== dayToday:
                        print(today, end=" ")
                    else:
                        print(up, end=" ")
                print()
                # srodek
                for day in week:
                    if day== dayToday:
                        if len(day) > 1:
                            print("#", day, "# ", end=" ")
                        else:
                            print("# ", day, "#  ", end="")
                    if len(day) > 1:
                        print("|", day, "| ", end=" ")
                    else:
                        print("| ", day, "|  ", end="")
                print()
                # dol
                for day in week:
                    if day== dayToday:
                        print(today, end=" ")
                    else:
                        print(down, end=" ")
                print()

            index+=1

            y, x = 2, 2  # Pozycja początkowa dla tekstu na ekranie
            for week in currentMonth:
                for day in week:
                    if day == " ":
                        self.stdscr.addstr(y, x, blank)
                    elif day == dayToday:
                        self.stdscr.addstr(y, x, today)
                    else:
                        self.stdscr.addstr(y, x, up)

                    # Zaktualizuj pozycję x
                    x += len(up)

                # Zaktualizuj pozycję y
                y += 1
                x = 2

            self.stdscr.refresh()

    def showCalendarCurse(self):
        # Clear the screen
        self.stdscr.clear()

        # Set the calendar title
        title = f"{self.getMonth()} {self.getYear()}"
        self.stdscr.addstr(1, (curses.COLS - len(title)) // 2, title, curses.A_BOLD)

        # Display the day headers
        day_headers = ["Pon", "Wt", "Sr", "Czw", "Pt", "So", "Nie"]
        for i, header in enumerate(day_headers):
            self.stdscr.addstr(3, i * 8 + 2, header, curses.A_BOLD)

        # Get the weekday of the 1st day of the month
        first_day = datetime.date(self.current_year, self.current_month, 1).weekday()

        # Calculate the number of days in the current month
        last_day = cal.monthrange(self.current_year, self.current_month)[1]

        # Display the calendar
        row, col = 4, (first_day * 8) + 2
        for day in range(1, last_day + 1):
            if day == self.highlight_day:
                self.stdscr.addstr(row, col, f"{day:2d}", curses.color_pair(1) | curses.A_BOLD)
            else:
                self.stdscr.addstr(row, col, f"{day:2d}")
            col += 8
            if col >= curses.COLS - 6:
                col = (first_day * 8) + 2
                row += 1

        # Refresh the screen to display changes
        self.stdscr.refresh()

class Events():
    # wydarzenia zapisywane do pliku
    # format - {data: wydarzenie}

    # moge dodac konstruktor polimorficzny? - ze rozna ilosc argumentow
    events = []
    defaultFile = "events.txt"

    def loadEvents(self, defaultFile):
        file = open(defaultFile, "r")
        for event in file:
            self.events.append(event)
        file.close()

    def showEvents(self):
        print(self.events)

    def saveEvent(self, name):
        file = open(name, "w")
        for event in self.events:
            file.write(str(event))
        file.close()

    def addEvent(self, date, description):
        self.events.append({date: description})
        self.saveEvent("events.txt")

    def removeEevnt(self, date):
        pass

class Notes():
    #luzne notatki, tez zapisywane do pliku
    pass

# class Menu():
#     #szybkie menu zaraz po odpaleniu programu, daje mozliwosc wyboru ktorejs funkcjonalnosci
#     print("Witaj w programie!")
#     print("Wybierz opcje: ")
#     print("1. Kalendarz")
#     print("2. Wydarzenia")
#     print("3. Notatnik")
#     print()
#     wybor = int(input("podaj numer: "))
#     match wybor:
#         case 1:
#             calendar = Calendar()
#             calendar.showCalendar1()
#         case 2:
#             events = Events()
#             events.addEvent("01.11.2023","urodziny dziadka")
#
# # menu = Menu()

def main(stdscr):
    calendar = Calendar(stdscr)
    stdscr.refresh()
    key = 0
    today = datetime.date.today().day
    while key != 27:  # ESC key to exit
        key = stdscr.getch()
        if key == curses.KEY_RIGHT:
            # Move the highlight to the next day
            stdscr.refresh()
            calendar.showCalendar2(today+1)  # Assuming max 31 days in a month
        elif key == curses.KEY_LEFT:
            # Move the highlight to the previous day
            stdscr.refresh()
            calendar.showCalendar2(today-1)
        stdscr.refresh()
        calendar.showCalendarCurse()

def main2(stdscr):
    today = datetime.date.today().day
    curses.curs_set(0)
    stdscr.clear()

    # Inicjalizacja Twojej klasy kalendarza
    your_calendar = Calendar(stdscr)
    your_calendar.stdscr = stdscr

    # Wywołanie funkcji showCalendar2
    your_calendar.showCalendar2(today)

    stdscr.getch()

curses.wrapper(main2)