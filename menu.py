import calendar as cal
import datetime

class Calendar():
    #widok kalendarza
    months = {1: "styczen", 2: "luty", 3: "marzec", 4: "kwiecien", 5: "maj", 6: "czerwiec", 7: "lipiec", 8: "siepien", 9: "wrzesien", 10: "pazdziernik", 11: "listopad", 12: "grudzien"}
    days = {1: "poniedzialek", 2: "wtorek", 3: "sroda", 4: "czwartek", 5: "piatek", 6: "sobota", 7: "niedziela"}

    def getYear(self):
        return datetime.date.today().year
    def getMonth(self):
        return self.months[datetime.date.today().month+1]

    def showDay(self):
        return datetime.date.today().day, self.days[datetime.date.today().weekday()+1]

    def showCalendar1(self):
        #widok tego miesiaca uzupelniony o dodatkowe dni
        print("                  ", self.getMonth(), self.getYear())
        print('=====================================================')

        kalendarz = cal.Calendar()
        week = 1
        currentMonth = []
        currentWeek = []
        for iterweekday in kalendarz.itermonthdates(2023, 10):
            currentWeek.append(iterweekday.day)
            if week == 7:
                week = 0
                currentMonth.append(currentWeek)
                currentWeek = []
            week += 1

        up = " ____  "
        blank = "       "
        down = " ----  "
        dayToday = datetime.date.today().day
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

    def showCalendar2(self):
        #2 opcja wyswietlania kalendarza, tylko dni z tego miesiaca
        print("                  ", self.getMonth(), self.getYear())
        print('=====================================================')

        kalendarz = cal.Calendar()
        week = 1
        currentMonth = []
        currentWeek = []
        for iterweekday in kalendarz.itermonthdays(2023, 10):
            if iterweekday==0:
                currentWeek.append(" ")
            else:
                currentWeek.append(str(iterweekday))
            if week == 7:
                week = 0
                currentMonth.append(currentWeek)
                currentWeek = []
            week += 1

        index=1
        monthLen=len(currentMonth)
        up = " ____  "
        blank = "       "
        down = " ----  "
        today = " **** "
        print("  pon     wt      sr     czw      pt      so     nie")
        for week in currentMonth:
            if index==1 or index==monthLen:
                for day in week:
                    if day==" ":
                        print(blank, end=" ")
                    else:
                        print(up, end=" ")
                print()
                for day in week:
                    if day==" ":
                        print("       ", end=" ")
                    elif len(day)==1:
                        print("| ", day, "| ", end=" ")
                    else:
                        print("|", day, "| ", end=" ")
                print()
                for day in week:
                    if day == " ":
                        print(blank, end=" ")
                    else:
                        print(down, end=" ")
                print()

            else:
                for day in week:
                    print(up, end=" ")
                print()
                for day in week:
                    if len(day) > 1:
                        print("|", day, "| ", end=" ")
                    else:
                        print("| ", day, "|  ", end="")
                print()
                for day in week:
                    print(down, end=" ")
                print()

            index+=1


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

class Menu():
    #szybkie menu zaraz po odpaleniu programu, daje mozliwosc wyboru ktorejs funkcjonalnosci
    print("Witaj w programie!")
    print("Wybierz opcje: ")
    print("1. Kalendarz")
    print("2. Wydarzenia")
    print("3. Notatnik")
    print()
    wybor = int(input("podaj numer: "))
    match wybor:
        case 1:
            calendar = Calendar()
            calendar.showCalendar1()
        case 2:
            events = Events()
            events.addEvent("01.11.2023","urodziny dziadka")

menu = Menu()