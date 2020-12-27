import telnetlib
import csv
import time

class Receiver:

    def __init__(self, hostname='127.0.0.1', port=7356, directory='/', waitTime=3, signalStrength=-31):
        self.host = hostname
        self.port = port
        self.directory = directory
        self.waitTime = waitTime
        self.signalStrength = signalStrength

    def _set_freq(self, freq):
        return self._update("F %s" % freq)

    def _set_mode(self, mode):
        return self._update("M %s" % mode)

    def _set_squelch(self, sql):
        return self._update("L SQL %s" % sql)

    def _get_level(self):
        return self._update("l")

    def _get_mode(self):
        return self._update('m')

    def _update(self, msg):
        """
        update the frequency/mode GQRX is listening to
        """
        try:
            tn = telnetlib.Telnet(self.host, self.port)
        except Exception as e: 
            print("Error connecting to " + self.host + ":" + str(self.port) + "\n\t" + str(e))
            exit()
        tn.write(('%s\n' % msg).encode('ascii'))
        response = tn.read_some().decode('ascii').strip()
        tn.write('c\n'.encode('ascii'))
        return response
