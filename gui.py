import calendar
import datetime
import tkinter as tk
from calendar import Calendar, day_name
#from organizer import Calendar

class GUI():

    window = tk.Tk()
    window.title("Callendar")
    mainFrame = tk.Frame()

    # moge dac 3 lub 4 framy
    # jeden do daty, jeden do przyciskow, jeden do kalendarza, jeden do pokazywania liczby wydarzen
    # pack sie nada, argument size=tk.LEFT do ustawiania kolejnosc jednego za drugim framem

    #place zeby recznie ustawiac lokalizacje elementow
    #grid idealne do kalendarza
    dateSelected = datetime.date.today()
    iterDate = datetime.date.today() # opcjonalne
    curr = 0 # [column ,row]
    original = 0
    start, end = 0, 0
    position = [0, 0]

    def handleRight(self):
        daysInMonth = calendar.monthrange(self.dateSelected.year, self.dateSelected.month)[1]
        self.dateSelected += datetime.timedelta(days=daysInMonth)
        self.curr = 1
        self.show()

    def handleLeft(self):
        daysInMonth = calendar.monthrange(self.dateSelected.year, self.dateSelected.month)[1]
        self.dateSelected -= datetime.timedelta(days=daysInMonth)
        self.curr = -1
        self.show()

    def keyLeft(self, frameCalendar):
        print(self.curr, self.start ,self.end)
        frameCalendar.grid_slaves(row=self.curr[1], column=self.curr[0])[0].configure(bg=self.original, borderwidth=1)
        if (self.curr[0]>=1):
            self.curr[0] -= 1
        else:
            self.curr[1] -= 1
            self.curr[0] = 6
        if (self.curr[1] == 1 and self.curr[0] == self.start[0]-1):
            # self.curr = self.end.copy()
            self.handleLeft()
            return
        cell = frameCalendar.grid_slaves(row=self.curr[1], column=self.curr[0])[0]
        cell.configure(bg="red", borderwidth=2)
        # label_widget = cell.winfo_children()[0]
        # label_widget.configure(bg="pale green")

    def keyRight(self, frameCalendar):
        print(self.curr, self.start ,self.end)
        frameCalendar.grid_slaves(row=self.curr[1], column=self.curr[0])[0].configure(bg=self.original, borderwidth=1)
        if (self.curr[0] <= 5):
            self.curr[0] += 1
        else:
            self.curr[1] += 1
            self.curr[0] = 0
        if (self.curr[1] == self.end[1] and self.curr[0] > self.end[0]):
            # self.curr = self.start.copy()
            self.handleRight()
            return
        cell = frameCalendar.grid_slaves(row=self.curr[1], column=self.curr[0])[0]
        cell.configure(bg="red", borderwidth=2)

    def show(self):
        print(self.curr, self.start, self.end)
        self.start = 0
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        topFrame = tk.Frame(master=self.mainFrame, bg="yellow")
        buttonRight = tk.Button(master=topFrame, text=" > ", width=1, height=2, bg="blue", relief=tk.GROOVE,
                                command=self.handleRight)
        buttonLeft = tk.Button(master=topFrame, text=" < ", width=1, height=2, bg="blue", relief=tk.RIDGE,
                               command=self.handleLeft)
        name = tk.Label(master=topFrame, text=self.dateSelected.strftime("%B-%Y"))

        buttonLeft.grid(row=0, column=0)
        name.grid(row=0, column=1)
        buttonRight.grid(row=0, column=2)
        topFrame.pack()


        c = Calendar()

        day_names = list(day_name)
        frameCalendar = tk.Frame(master=self.mainFrame)
        for d, dName in enumerate(day_names):
            dayNames = tk.Frame(
                master=frameCalendar,
                relief="solid",
                borderwidth=1
            )
            self.original = dayNames.cget("bg")
            dayNames.grid(row=0, column=d, pady=2)
            dayLabel = tk.Label(master=dayNames, text=dName)
            dayLabel.pack()

        # i - columns , j - rows
        i, j = 0, 1

        self.iterDate = datetime.date(self.dateSelected.year, self.dateSelected.month, 1)

        for d in [x for x in c.itermonthdates(self.iterDate.year, self.iterDate.month) if x.month == self.iterDate.month]:
            calendarFrame = tk.Frame(
                master=frameCalendar,
                relief=tk.RAISED,
                borderwidth=1
            )
            i = d.weekday()
            if not self.start:
                self.start = [i, j]
            if i % 7 == 0:
                j += 1
            calendarFrame.grid(row=j, column=i % 7, pady=2)
            label = tk.Label(master=calendarFrame, text=d.strftime("%d"))
            if d == datetime.date.today() and self.curr == 0:
                label.configure(bg="green2")
                self.curr = [i, j]
            label.pack()
            self.end = [i, j]
            self.position = self.end.copy()

        if self.curr == -1:
            self.curr = self.end.copy()
        if self.curr == 1:
            self.curr = self.start.copy()


        frameCalendar.grid_columnconfigure([0,1,2,3,4,5,6], weight=1, uniform="fred")
        frameCalendar.pack(padx=5, pady=5)

        cell = frameCalendar.grid_slaves(row=self.curr[1], column=self.curr[0])[0]
        cell.configure(bg="red", borderwidth=2)

        print(self.curr, self.start, self.end)

        # entry = tk.Entry(width=5)
        # entry.insert(0, "pusto")
        # entry.pack()

        # self.window.bind("KP_LEFT", self.keyLeft(frameCalendar))
        # self.window.bind("KP_RIGHT", self.keyRight(frameCalendar))

        self.window.bind("<Left>", lambda event, frame=frameCalendar: self.keyLeft(frame))
        self.window.bind("<Right>", lambda event, frame=frameCalendar: self.keyRight(frame))
        self.mainFrame.pack()
        self.window.mainloop()


gui = GUI()
gui.show()