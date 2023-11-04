import curses

def main(stdscr):
    stdscr.clear()
    stdscr.refresh()

    while True:
        key = stdscr.getch()

        if key == 27:  # Escape key to exit the loop
            break

        if key == 17:  # Ctrl key
            next_key = stdscr.getch()  # Get the next key
            if next_key == curses.KEY_RIGHT:
                # Handle Ctrl+Right Arrow key
                stdscr.addstr("Ctrl+Right Arrow Pressed\n")
            elif next_key == curses.KEY_LEFT:
                # Handle Ctrl+Left Arrow key
                stdscr.addstr("Ctrl+Left Arrow Pressed\n")
            elif next_key == curses.KEY_UP:
                # Handle Ctrl+Up Arrow key
                stdscr.addstr("Ctrl+Up Arrow Pressed\n")
            elif next_key == curses.KEY_DOWN:
                # Handle Ctrl+Down Arrow key
                stdscr.addstr("Ctrl+Down Arrow Pressed\n")
        else:
            # Handle other keys
            stdscr.addstr("Key pressed: " + str(key) + "\n")

        stdscr.refresh()

curses.wrapper(main)