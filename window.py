"""
Tkinter was a mistake...



but I can code it fast and that is what matters
"""


import tkinter as tk
from tkinter import filedialog, messagebox
import pathlib

import tooltip

class App(tk.Tk):
	def __init__(self, _callback):
		super().__init__()

		# initializing variables
		self.midi_path = None
		self.callback = _callback # callback given must take args

		# tkinter window parameters hardcoded
		self.title("Midi Processer")
		#self.geometry("300x300")
		#self.resizable(False, False)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)

		for i in range(1, 7): # number of grid rows
			self.grid_rowconfigure(i, minsize=30)

		#==============================
		# defining widgets
		#==============================
		self.apply_button = tk.Button(text="Apply", command=self._apply_callback)
		self.apply_button.grid(row=7, column=0, columnspan=2, sticky="ew")
		self.apply_button_tooltip = tooltip.CreateToolTip(self.apply_button, "Apply parameters to selected input file.")

		self.midi_path_button = tk.Button(text="Find Midi Input Path", command=self._path_callback)
		self.midi_path_button.grid(row=1, column=0, sticky="ew")
		self.midi_path_label = tk.Label(text="None")
		self.midi_path_label.grid(row=1, column=1)
		self.midi_path_button_tooltip = tooltip.CreateToolTip(self.midi_path_button, "Select the path of the input midi.")

		self.timing_offset_range_label = tk.Label(text="Timing Offset Range")
		self.timing_offset_range_label.grid(row=2, column=0)
		self.timing_offset_range_slider = tk.Scale(to=50, orient="horizontal")
		self.timing_offset_range_slider.grid(row=2, column=1)
		self.timing_offset_range_slider_tooltip = tooltip.CreateToolTip(self.timing_offset_range_slider, "Randomly add delay or predelay to a note to make it sound more human.")

		self.velocity_offset_range_label = tk.Label(text="Velocity Offset Range")
		self.velocity_offset_range_label.grid(row=3, column=0)
		self.velocity_offset_range_slider = tk.Scale(to=50, orient="horizontal")
		self.velocity_offset_range_slider.grid(row=3, column=1)
		self.velocity_offset_range_slider_tooltip = tooltip.CreateToolTip(self.velocity_offset_range_slider, "Randomly adjust velocity of a note to make it sound more human.")

		self.expression_label = tk.Label(text="Convert Velocity to Expression")
		self.expression_label.grid(row=4, column=0)
		self.convert_to_expression = tk.IntVar()
		self.expression_button = tk.Checkbutton(variable=self.convert_to_expression)
		self.expression_button.grid(row=4, column=1, sticky="ew")
		self.expression_button_tooltip = tooltip.CreateToolTip(self.expression_button, "Convert velocities to expression for easy use with some vsts.")

		self.increment_label = tk.Label(text="Increment Filenames")
		self.increment_label.grid(row=5, column=0)
		self.increment_filename = tk.IntVar()
		self.current_increment = 0
		self.increment_button = tk.Checkbutton(variable=self.increment_filename)
		self.increment_button.grid(row=5, column=1, sticky="ew")
		self.increment_button_tooltip = tooltip.CreateToolTip(self.increment_button, "Increment filenames to avoid writing to existing files.")

		self.track_label = tk.Label(text="Track Index")
		self.track_label.grid(row=6, column=0)
		self.track_entry = tk.Spinbox(from_=0, to=256, validate="key", validatecommand=(self.register(self.validate_spinbox), "%S"))
		self.track_entry.grid(row=6, column=1, sticky="ew")
		self.track_entry.tooltip = tooltip.CreateToolTip(self.track_entry, ("An integer index of the track in the midi. Take note that Musescore exports every stave as a new track not every instrument!"))

	#===============================
	# callbacks
	#===============================

	def validate_spinbox(self, S: str) -> bool:
		return S.isdigit() or S == ""

	def _apply_callback(self) -> None:
		# callback for the apply button
		# applies the parameters described
		# parameters are (input_file: str, track_index: int, humanize_data: dict, convert_to_expression: int, current_increment: int)
		if self.midi_path is not None:
			if self.increment_filename.get(): self.current_increment += 1

			self.callback(
				self.midi_path,
				int(self.track_entry.get()),
				{
					"timing_offset_range": self.timing_offset_range_slider.get(),
					"velocity_offset_range": self.velocity_offset_range_slider.get()
				},
				self.convert_to_expression.get(),
				0 if not (self.increment_filename.get()) else self.current_increment # value of 0 means do not increment
				)
			tk.messagebox.showinfo("Task Completed", "The file was successfully processed!")
		else:
			tk.messagebox.showwarning("Warning", "No input path is selected!")

	def _path_callback(self) -> None:
		# opens dialogue to find path of input midi
		fname = filedialog.askopenfilename()
		self.midi_path = fname
		fname = fname.split("/")
		fname = fname[len(fname)-1] # dumb way of doing it but who am I do complain, it works

		if len(fname) > 15:
			fname = fname[0:15] + "..." # limits the size of the filename display so it fits

		self.midi_path_label.config(text=fname)
		self.midi_path_label.grid()


#==============================
# testing
#==============================

def test_callback(*args) -> None:
	print(args)

if __name__ == "__main__":
	app = App(test_callback)
	app.mainloop()