import curses
import datetime
import calendar as cal
from datetime import datetime as datetim

months = {1: "styczen", 2: "luty", 3: "marzec", 4: "kwiecien", 5: "maj", 6: "czerwiec", 7: "lipiec", 8: "siepien", 9: "wrzesien", 10: "pazdziernik", 11: "listopad", 12: "grudzien"}
days = {1: "poniedzialek", 2: "wtorek", 3: "sroda", 4: "czwartek", 5: "piatek", 6: "sobota", 7: "niedziela"}
daysMonths = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
class Calendar():
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.current_day = datetime.date.today().day
        self.current_month = datetime.date.today().month
        self.current_year = datetime.date.today().year
        self.highlight_day = self.current_day
        self.x = 2
        self.x_max = 0
        self.y = 3
        self.stdscr.keypad(True)

    def showCalendar(self, chosenDay):
        self.stdscr.clear()

        week = 1
        currentMonth = []
        currentWeek = []
        calen = cal.Calendar()
        if chosenDay.month!=self.current_month:
            self.current_month = chosenDay.month
            if chosenDay.year!=self.current_year:
                self.current_year = chosenDay.year
        for iterweekday in calen.itermonthdates(self.current_year, self.current_month):
            if iterweekday == 0:
                currentWeek.append(" ")
            else:
                currentWeek.append(str(iterweekday))
            if week == 7:
                week = 0
                currentMonth.append(currentWeek)
                currentWeek = []
            week += 1

        down = " ----  "
        today = "****** "
        firstTime = True
        dayToday = str(chosenDay)
        self.stdscr.addstr(0, 20, months[self.current_month] + ' ' + str(self.current_year))
        self.stdscr.addstr(1, 2, '================================================')
        self.stdscr.addstr(3, 2, " pon     wt     sr    czw     pt     so    nie")
        self.x, self.y = 2, 4  # Pozycja początkowa dla tekstu na ekranie
        for week in currentMonth:
            now = False
            if dayToday in week:
                now = True
            for day in week:
                if day == dayToday:
                    self.stdscr.addstr(self.y, self.x, today)
                    self.x += len(today)
                else:
                    self.stdscr.addstr(self.y, self.x, down)
                    self.x += len(down)
            self.y+=1
            self.x=2

            for day in week:
                add = ""
                dateDay = datetim.strptime(day, '%Y-%m-%d').date()
                if dateDay.day <=9:
                    add = " "
                if day == dayToday:
                    self.stdscr.addstr(self.y, self.x, "# "+add+str(dateDay.day)+" #")
                    self.x += 7
                else:
                    self.stdscr.addstr(self.y, self.x, "| "+add+str(dateDay.day)+" |")
                    self.x += 7

            self.x_max=self.x
            self.y+=1
            self.x=2

            for day in week:
                if day == dayToday:
                    self.stdscr.addstr(self.y, self.x, today)
                    self.x += len(today)
                else:
                    self.stdscr.addstr(self.y, self.x, down)
                    self.x += len(down)
            self.y += 1
            self.x = 2

        self.stdscr.refresh()

    def getY(self):
        return self.y

    def getX(self):
        return self.x

    def getXMax(self):
        return self.x_max


class Events():
    # wydarzenia zapisywane do pliku
    # format - {data: wydarzenie}

    # moge dodac konstruktor polimorficzny? - ze rozna ilosc argumentow

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.defaultFile = "events.txt"
        self.events = {}
        self.loadEvents(self.defaultFile)

    def loadEvents(self, defaultFile):
        file = open(defaultFile, "r")
        for event in file:
            event = event.strip('\n')
            event = event.split(":")
            self.events[event[0]]=event[1]
        file.close()

    def showEvents(self, x, y, day):
        y+=2
        if str(day) in self.events.keys():
            self.stdscr.addstr(y, x, str(self.events[str(day)]))
            y += 1
        else:
            return


    def eventView(self, day):
        x, y = 2, 2
        if str(day) in self.events.keys():
            editable=str(self.events[str(day)])
        else:
            editable="pusto"
        while True:

            self.stdscr.addstr(y, x, "edytuj: " + editable)  # Display the text field
            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key == 10:  # Enter key
                self.events[str(day)]=editable
                # ignore empty event
                if self.events[str(day)]!="":
                    self.saveEvent(self.defaultFile)
                break  # Exit when Enter is pressed
            elif key == 27:  # ESC key
                return  # exit
            elif key == ord(':'): # ":" pressed
                self.stdscr.addstr(5, x, "znak : jest niedozwolony")
                # self.stdscr.refresh()
            elif key == curses.KEY_BACKSPACE:  # Handle backspace
                editable = editable[:-1]
                self.stdscr.clear()
            elif key >= 32 and key <= 126:  # Accept printable characters
                editable += chr(key)
                self.stdscr.clear()

    def saveEvent(self, name):
        file = open(name, "w")
        for event in self.events:
            event.strip('\n')
            file.write(str(event)+':'+str(self.events[event])+'\n')
        file.close()

    def addEvent(self, date, description):
        self.events.append({date: description})
        self.saveEvent("events.txt")

    def removeEevnt(self, date):
        pass

class Menu():
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.defaultFile = "start.txt"

    def showMenu(self):
        self.loadMenu()

    def loadMenu(self):
        f = open(self.defaultFile, "r")
        x = 10
        y = 1
        for line in f:
            self.stdscr.addstr(y, x, line)
            x = 10
            y += 1

class Helper():
    def __init__(self, stdscr, x):
        self.stdscr = stdscr
        self.x = x + 5
        self.y = 5

    def show(self):
        self.stdscr.addstr(self.y, self.x, "JAK KORZYSTAĆ:")

        self.stdscr.addstr(self.y+2, self.x, "[ESC] wychodzi")

        self.stdscr.addstr(self.y+4, self.x, "[ENTER] przechodzi do")
        self.stdscr.addstr(self.y+5, self.x, "wydarzeń dnia")

        self.stdscr.addstr(self.y+7, self.x, "[STRZAŁKA W LEWO, PRAWO]")
        self.stdscr.addstr(self.y+8, self.x, "przechodzi po dniach")

        self.stdscr.addstr(self.y+10, self.x, "[CTRL] ze strzałkami")
        self.stdscr.addstr(self.y+11, self.x, "przechodzi po miesiącach")

def main(stdscr):
    # stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)
    stdscr.clear()

    today = datetime.date.today().day
    dateToday = datetime.date.today()
    calendar = Calendar(stdscr)
    event = Events(stdscr)
    menu = Menu(stdscr)
    menu.showMenu()
    key = 0
    ctrl = 0
    while key != 27:
        key = stdscr.getch()
        if key == 49:
            calendar.showCalendar(dateToday)
            event.showEvents(calendar.getX(), calendar.getY(), dateToday)
            helper = Helper(stdscr, calendar.getXMax())
            helper.show()
            key = 0
            while key != 27:  # ESC wychodzi
                key = stdscr.getch()
                if key == 546: #lewo
                    dateToday -= datetime.timedelta(days=daysMonths[dateToday.month])
                    calendar.showCalendar(dateToday)
                    event.showEvents(calendar.getX(), calendar.getY(), dateToday)
                    helper.show()
                elif key == 561: #prawo
                    dateToday += datetime.timedelta(days=daysMonths[dateToday.month])
                    calendar.showCalendar(dateToday)
                    event.showEvents(calendar.getX(), calendar.getY(), dateToday)
                    helper.show()
                if key == curses.KEY_RIGHT:
                    # kolejny dzien
                    stdscr.refresh()
                    today += 1
                    dateToday += datetime.timedelta(days=1)
                    calendar.showCalendar(dateToday)
                    event.showEvents(calendar.getX(), calendar.getY(), dateToday)
                    helper.show()
                elif key == curses.KEY_LEFT:
                    # poprzedni dzien
                    stdscr.refresh()
                    today -= 1
                    dateToday -= datetime.timedelta(days=1)
                    calendar.showCalendar(dateToday)
                    event.showEvents(calendar.getX(), calendar.getY(), dateToday)
                    helper.show()
                # stdscr.refresh()
                elif key == 10:
                    # enter - wydarzenie
                    stdscr.clear()
                    event.eventView(dateToday)
                    stdscr.refresh()
                    calendar.showCalendar(dateToday)
                    event.showEvents(calendar.getX(), calendar.getY(), dateToday)
                    helper.show()
                ctrl = 0
            key = 0
            stdscr.clear()
            menu.showMenu()
        elif key == 50:
            stdscr.clear()
            stdscr.addstr(2, 2, "tryb graficzny nie jest jeszcze gotowy")
            while key != 27:
                key = stdscr.getch()
                continue
            key = 0
            stdscr.clear()
            menu.showMenu()
        elif key == 51:
            stdscr.clear()
            stdscr.addstr(2, 2, "tryb zadań nie jest jeszcze gotowy")
            while key != 27:
                key = stdscr.getch()
                continue
            key = 0
            stdscr.clear()
            menu.showMenu()
    # stdscr.refresh()



curses.wrapper(main)