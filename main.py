import processer
import window

def callback(*args):
	processer.process_midi(args[0], args[1], args[2], args[3], args[4])

if __name__ == "__main__":
	window.App(callback).mainloop()