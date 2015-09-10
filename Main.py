#!/usr/bin/python3
import flask, argparse, os
import Tracks

class FlaskApp(flask.Flask):
	def __init__(self, trackPaths, name=__name__):
		flask.Flask.__init__(self, name)
		self.registerRoutes()
		self.tracks={}
		for path in trackPaths:
			for track in Tracks.allTracks(path):
				self.tracks[track.name]=track
		self.player=Tracks.Player()

	def registerRoutes(self):
		self.add_url_rule("/tracks/", view_func=self.allTracks)
		self.add_url_rule("/tracks/<trackName>", view_func=self.playTrack)
		self.add_url_rule("/tracks/stopPlaying", view_func=self.stopPlaying)

	def allTracks(self):
		return flask.render_template("allTracks.html", title="All tracks", tracks=sorted(self.tracks.keys()))

	def playTrack(self, trackName):
		track=self.tracks[trackName]
		self.player.playTrack(track.path)
		return flask.render_template("playTrack.html", title="Play track {}".format(track.name),
			track=track)

	def stopPlaying(self):
		self.player.stopPlaying()
		return flask.redirect("/tracks/")

if __name__ == "__main__":
	parser=argparse.ArgumentParser()
	parser.add_argument("--path", default=os.getcwd(), dest="trackPath", type=str,
		help="Set the path where the music files are located (for multiple, sep by ',')")
	parser.add_argument("--host", default="127.0.0.1", dest="host", type=str,
		help="Specify the host the server should bind to.")
	parser.add_argument("--port", default=8000, dest="port", type=int,
		help="Specify the port the server should bind to.")
	args=parser.parse_args()
	app=FlaskApp(args.trackPath.split(","))
	app.run(host=args.host, port=args.port, debug=False)
