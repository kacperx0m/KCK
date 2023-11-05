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
        self.current_task_index = 0  # Track the index of the current task
        self.green = curses.color_pair(1)  # Define a green color pair
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

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

            if i == self.current_task_index:
                self.stdscr.addstr(self.y, self.x, self.tasks[i][0] + self.tasks[i][1], self.green)
            else:
                self.stdscr.addstr(self.y, self.x, self.tasks[i][0] + self.tasks[i][1])

            self.y += 1

    def saveTasks(self):
        file = open(self.defaultFile, "w")
        for task in self.tasks:
            file.write(task[0] + task[1] + "\n")

    def addTask(self, name):
        # self.newTasks.append('[ ] ' + name)
        self.tasks.append(['[ ] ', name])
        self.saveTasks()

    def delTask(self):
        if 0 <= self.current_task_index < len(self.tasks):
            del self.tasks[self.current_task_index]
            self.current_task_index = max(0, self.current_task_index - 1)
            self.saveTasks()

    def toggleCompletion(self):
        if 0 <= self.current_task_index < len(self.tasks):
            if "[ ]" in self.tasks[self.current_task_index][0]:
                self.tasks[self.current_task_index][0] = self.tasks[self.current_task_index][0].replace("[ ]", "[x]")
            else:
                self.tasks[self.current_task_index][0] = self.tasks[self.current_task_index][0].replace("[x]", "[ ]")
            self.saveTasks()

    def getX(self):
        return self.x

    def getY(self):
        return self.y

class TodoHelper():
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def showTodoHelper(self):
        self.stdscr.addstr(2, 54)

def todo(stdscr):
    key = 0
    stdscr.clear()
    stdscr.scrollok(1)
    tasks = Task(stdscr)
    tasks.loadTasks()
    tasks.scroll_pos = max(0, tasks.current_task_index - curses.LINES + 3)
    while key != 27:
        stdscr.clear()

        max_display_lines = curses.LINES - tasks.y  # Calculate the number of lines that can fit
        if tasks.current_task_index >= tasks.scroll_pos + max_display_lines:
            tasks.scroll_pos = tasks.current_task_index - max_display_lines

        tasks.showTasks()
        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            if tasks.current_task_index < len(tasks.tasks) - 1:
                tasks.current_task_index += 1
            if tasks.current_task_index >= tasks.scroll_pos + curses.LINES - 1:
                tasks.scroll_pos += 1

        elif key == curses.KEY_UP:
            if tasks.current_task_index > 0:
                tasks.current_task_index -= 1
            if tasks.current_task_index < tasks.scroll_pos:
                tasks.scroll_pos = tasks.current_task_index

        elif key == ord('+'):
            key = 0
            editable = ""
            y = tasks.getY()
            while editable != 27:
                stdscr.addstr(curses.LINES - 1, 2, editable)  # Display the text field
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

        elif key == ord(' '):
            tasks.toggleCompletion()

        elif key == 330:
            tasks.delTask()

curses.wrapper(todo)
