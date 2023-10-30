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

        print("  pon     wt      sr     czw      pt      so     nie")
        for week in currentMonth:
            print(" ____    ____    ____    ____    ____    ____    ____")
            for day in week:
                if day > 9:
                    print("|", day, "| ", end=" ")
                else:
                    print("| ", day, "|  ", end="")
            print()
            print(" ----    ----    ----    ----    ----    ----    ----")

    def showCalendar2(self):
        #2 opcja wyswietlania kalendarza, tylko dni z tego miesiaca
        pass


class Events():
    # wydarzenia zapisywane do pliku
    events = []

    def loadEvents(self, name):
        file = open(name)
        for event in file:
            self.events.append(event)
        file.close()

    def showEvents(self):
        print(self.events)

    def addEvent(self):
        self.events.append()

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

menu = Menu()