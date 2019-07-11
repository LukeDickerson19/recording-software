import curses
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0,10,"Hit 'q' to quit")
stdscr.refresh()

key = ''
player = 'o'
x, y = 2, 20
# https://stackoverflow.com/questions/10693256/how-to-accept-keypress-in-command-line-python
while key != ord('q'):
	# stdscr.erase()
	key = stdscr.getch()
	# stdscr.addch(20,25,key)
	if key == curses.KEY_UP: 
		y -= 1
	elif key == curses.KEY_DOWN: 
		y += 1
	elif key == curses.KEY_LEFT:
		x -= 1
	elif key == curses.KEY_RIGHT:
		x += 1
	stdscr.addstr(y, x, player)
	stdscr.refresh()

curses.endwin()