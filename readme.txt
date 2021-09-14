This is an updated version of the eyelink app for python 3.7.

Requirements:
pylsl (tested with 1.14)

This program streams the x/y positions of both eyes, timestamps, pupil and pixelPerDegree

This program also saves the data (default as `TRIAL.EDF`), be sure to modify the command call to give it a unique name every run

The tool tries to establish a connection to the EyeLink, if none is found. If you use e.g. pygaze, this should work out of the box.

Only one program can have a connection to the eyelink at the same time. Thus, in order to control calibration etc. and stream, one needs to start the program in an extra thread
You can use the following code to do so:

XXX

