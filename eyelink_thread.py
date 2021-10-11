import threading
from pylsl import StreamInfo, StreamOutlet
import socket
import time
from pylink import getEYELINK, msecDelay, beginRealTimeMode
import pylsl

# written by Michael Bui


class EyeLinkLSL(threading.Thread):

    def __init__(self, sr=500, edf_file_name="TRIAL.edf"):
        threading.Thread.__init__(self)

        info = StreamInfo("EyeLink", "Gaze", 10, sr, 'double64', "eyelink-" + socket.gethostname())
        self.outlet = StreamOutlet(info)
        self.done = False
        self.sr = sr
        self.edf_file_name = edf_file_name

    def run(self):

        # beginRealTimeMode(100)

        getEYELINK().openDataFile(self.edf_file_name)
        getEYELINK().startRecording(1, 1, 1, 1)

        print("Now reading samples...")
        print("Press \'Esc\' to quit")

        while not self.done:
            # sample = getEYELINK().getNewestSample()

            if getEYELINK().getNextData() == 200:
                sample = getEYELINK().getNewestSample()
                now = pylsl.local_clock()
                ppd = sample.getPPD()
                values = [0, 0, 0, 0, 0, 0, ppd[0], ppd[1], sample.getTime(), now]
                if (sample.isLeftSample()) or (sample.isBinocular()):
                    values[0:2] = sample.getLeftEye().getGaze()
                    values[4] = sample.getLeftEye().getPupilSize()
                if (sample.isRightSample()) or (sample.isBinocular()):
                    values[2:4] = sample.getRightEye().getGaze()
                    values[5] = sample.getRightEye().getPupilSize()

                self.outlet.push_sample(pylsl.vectord(values), now)
            time.sleep(1.0 / (self.sr * 4))

        self.close()

    def terminate(self):
        self.done = True

    def close(self):
        getEYELINK().setOfflineMode()
        msecDelay(500)

        # Close the file and transfer it to Display PC
        getEYELINK().closeDataFile()
        getEYELINK().receiveDataFile(self.edf_file_name, self.edf_file_name)
        getEYELINK().close()
