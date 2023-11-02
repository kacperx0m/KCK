import curses
import datetime
import calendar as cal

class Calendar():
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.current_day = datetime.date.today().day
        self.current_month = datetime.date.today().month
        self.current_year = datetime.date.today().year
        self.highlight_day = self.current_day
        self.x = 2
        self.y = 2
        self.stdscr.keypad(True)

    def showCalendar(self, chosenDay):
        self.stdscr.clear()
        week = 1
        currentMonth = []
        currentWeek = []
        calen = cal.Calendar()
        for iterweekday in calen.itermonthdates(self.current_year, self.current_month):
            if iterweekday == 0:
                currentWeek.append(" ")
            else:
                currentWeek.append(str(iterweekday.day))
            if week == 7:
                week = 0
                currentMonth.append(currentWeek)
                currentWeek = []
            week += 1

        down = " ----  "
        today = "****** "
        dayToday = str(chosenDay)
        self.x, self.y = 2, 2  # Pozycja początkowa dla tekstu na ekranie
        for week in currentMonth:
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
                if day == dayToday:
                    self.stdscr.addstr(self.y, self.x, "# "+day+" #")
                    self.x += 7
                else:
                    self.stdscr.addstr(self.y, self.x, "| "+day+" |")
                    self.x += 7

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


    def showEvent(self, day):
        print(self.events[day])

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


def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    today = datetime.date.today().day
    dateToday = datetime.date.today()
    calendar = Calendar(stdscr)
    event = Events(stdscr)
    calendar.showCalendar(today)
    event.showEvents(calendar.getX(), calendar.getY(), dateToday)
    # stdscr.refresh()
    key = 0

    while key != 27:  # ESC wychodzi
        key = stdscr.getch()
        if key == curses.KEY_RIGHT:
            # kolejny dzien
            stdscr.refresh()
            today+=1
            dateToday += datetime.timedelta(days=1)
            calendar.showCalendar(today)
            event.showEvents(calendar.getX(), calendar.getY(), dateToday)
        elif key == curses.KEY_LEFT:
            # poprzedni dzien
            stdscr.refresh()
            today-=1
            dateToday -= datetime.timedelta(days=1)
            calendar.showCalendar(today)
            event.showEvents(calendar.getX(), calendar.getY(), dateToday)
        # stdscr.refresh()
        elif key == curses.KEY_ENTER:
            # wydarzenie
            stdscr.refresh()
            event.showEvents(calendar.getX(), calendar.getY(), dateToday)

curses.wrapper(main)