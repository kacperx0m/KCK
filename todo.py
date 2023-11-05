import curses


class Task():
    def __init__(self, stdscr):
        self.defaultFile = "tasks.txt"
        self.stdscr = stdscr
        self.tasks = []
        self.scroll_pos = 0  # Track the scroll position
        self.newTasks = []
        self.x = 2
        self.y = 2

    def loadTasks(self):
        file = open(self.defaultFile, "r")
        for line in file:
            line = line.strip('\n')
            line = line.split("] ")
            line[0] = line[0] + '] '
            self.tasks.append(line)

    def showTasks(self):
        self.y = 2
        max_display_lines = curses.LINES - self.y - 1  # Calculate the number of lines that can fit
        for i in range(self.scroll_pos, min(len(self.tasks), self.scroll_pos + max_display_lines)):
            self.x = 2
            self.stdscr.addstr(self.y, self.x, self.tasks[i][0] + self.tasks[i][1])
            self.y += 1

    def saveTasks(self):
        file = open(self.defaultFile, "a")
        for task in self.newTasks:
            file.write(task)

    def addTask(self, name):
        self.newTasks.append('[ ] '+name)
        self.saveTasks()

    def getX(self):
        return self.x

    def getY(self):
        return self.y

def todo(stdscr):
    key = 0
    stdscr.clear()
    stdscr.scrollok(1)
    tasks = Task(stdscr)
    tasks.loadTasks()
    while key != 27:
        stdscr.clear()
        tasks.showTasks()
        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            if tasks.scroll_pos < len(tasks.tasks) - curses.LINES:
                tasks.scroll_pos += 1
        elif key == curses.KEY_UP:
            if tasks.scroll_pos > 0:
                tasks.scroll_pos -= 1

        if key == ord('+'):
            key = 0
            editable = ""
            y = tasks.getY()
            while editable!= 27:
                stdscr.addstr(curses.LINES-1, 2, editable)  # Display the text field
                stdscr.refresh()

                key = stdscr.getch()

                if key == 10:  # Enter key
                    if editable == "":
                        break
                    tasks.addTask(editable)
                    break
                elif key == curses.KEY_BACKSPACE:  # Handle backspace
                    editable = editable[:-1]
                    stdscr.clear()
                elif key >= 32 and key <= 126:  # Accept printable characters
                    editable += chr(key)
                    stdscr.clear()
            tasks.showTasks()

        if key == 330:
            tasks.delTask(current)

curses.wrapper(todo)
