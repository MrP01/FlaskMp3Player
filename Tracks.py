import os, subprocess

class Track(object):
	def __init__(self, name, path):
		self.name=name
		self.path=path

def allTracks(path):
	tracks=[]
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith(".mp3"):
				tracks.append(Track(os.path.basename(file), os.path.join(root, file)))
	return tracks

class Player(object):
	def __init__(self):
		self.currentProcess=None

	def playTrack(self, trackPath):
		self.stopPlaying()
		#This is a comment
		self.currentProcess=subprocess.Popen(["mpg321", trackPath], stdout=subprocess.PIPE,
			stderr=subprocess.PIPE, stdin=subprocess.PIPE)

	def stopPlaying(self):
		if self.currentProcess is None:
			return
		self.currentProcess.terminate()
