
# curses creates a screen in the comand line where you can write stuff
# its also useful for getting ser input without pausing execution of the
# rest of the program (this might not be useful considering pyo might be
# able to continue even w/ input() pausing normal execution)

# ... also its pretty annoying ...

# source:
# https://stackoverflow.com/questions/10693256/how-to-accept-keypress-in-command-line-python


import curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0,10,"Hit 'q' to quit")
stdscr.refresh()

key = ''
while key != ord('q'):
    key = stdscr.getch()
    stdscr.addch(20, 25, key)
    stdscr.refresh()
    if key == curses.KEY_UP:
        stdscr.addstr(2, 20, "Up")
    elif key == curses.KEY_DOWN:
        stdscr.addstr(3, 20, "Down")

curses.endwin()
