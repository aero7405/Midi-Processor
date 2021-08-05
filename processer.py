# that lol moment when you spell the file wrong and refuse to fix it 
import mido, random

# class to store a time and a message that is all
class Message:
	def __init__(self, base_message, absolute_time: float):
		self.base_message = base_message

		self.absolute_time = absolute_time

# sort messages by absolute time
def sort_messages(messages: list) -> list:
	sorted_messages = []

	# this has probably a terrible O(n) and I don't care
	for msg in messages:
		if len(sorted_messages) == 0:
			sorted_messages.append(msg)

		else:
			for i, other in enumerate(sorted_messages):
				if other.absolute_time < msg.absolute_time:
					sorted_messages.insert(i, msg)
					break
			else:
				# if current message is lowest so far
				sorted_messages.append(msg)

	sorted_messages.reverse() # don't question - just accept
	return sorted_messages

# foce value to be between r1 and r2
def _clamp(v, r1, r2=None) -> float:
	if r2 is None:
		return r1 if v < r1 else v
	else:
		return r2 if v < r1 else v if v < r2 else r2

# randomizes velocity and timing
def humanize_message(message, humanize_data: dict) -> None:
	if message.base_message.type in ["note_on", "note_off"]:

		message.absolute_time += random.randint(-humanize_data["timing_offset_range"], humanize_data["timing_offset_range"])
		if message.absolute_time < 0: message.absolute_time = 0

		if message.base_message.velocity != 0:
			new_velocity = message.base_message.velocity + random.randint(-humanize_data["velocity_offset_range"], humanize_data["velocity_offset_range"])
			message.base_message.velocity = _clamp(new_velocity, 1, 127)

# takes message and creates an expression from the velocity
def create_expression_from_message(message): # returns mido expression message or None
	if message.base_message.type in ["note_on", "note_off"]:
		return mido.Message(type="control_change", control=11, value=message.base_message.velocity, time=message.absolute_time) # control 11 if expression
	return None

# most processing opperations for midi given parameters from UI
def process_midi(input_file: str, track_index: int, humanize_data: dict, convert_to_expression: int, current_increment: int) -> None:

	input_midi = mido.MidiFile(input_file)

	# setting up output
	output_midi = mido.MidiFile()
	output_midi.add_track()

	# =========================================================
	# Applying parameters
	# =========================================================

	# sort tracks by time
	absolute_time = 0
	messages = []

	if len(input_midi.tracks) >= track_index:
		selected_track = input_midi.tracks[track_index]\

		for i, msg in enumerate(selected_track):

			absolute_time += msg.time

			#==================
			# processing data
			mes = Message(msg, absolute_time)
			humanize_message(mes, humanize_data) # alters message with adjustments

			expression = Message(create_expression_from_message(mes), absolute_time)
			if convert_to_expression and expression.base_message is not None:
				messages.append(expression)
			#==================
			messages.append(mes)

	messages = sort_messages(messages)

	# converting to reletive times
	last_time = 0
	for msg in messages:
		time_offset = msg.absolute_time - last_time
		last_time = msg.absolute_time
		msg.base_message.time = time_offset

		output_midi.tracks[0].append(msg.base_message)

	# outputing new file
	increment = "" if current_increment == 0 else "-" + str(current_increment)
	output_midi.save(input_file.split(".")[0] + "-processed" + increment + ".mid") # outputs 2 tracks for me in Waveform and I have no idea why but they can be merged so, :thumbsup: