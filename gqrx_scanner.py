import telnetlib
import csv
import time

class Receiver:

    def __init__(self, hostname='127.0.0.1', port=7356, directory='/', waitTime=3,\
                     signalStrength=-30, csvfile = 'freq.csv', sql = -31):
        self.host = hostname
        self.port = port
        self.directory = directory
        self.waitTime = waitTime
        self.signalStrength = signalStrength
        self.csvfile = csvfile
        self.freqs = {}
        self.scan_start = False
        self.sql = sql

        freqs = {}
        with open(self.csvfile, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for row in reader:
                if int(row[3]) == 1:
                    freq = row[0]
                    self.freqs[freq] = {"mode":row[1],"tag": row[2]}

    def _set_freq(self, freq):
        return self._update("F %s" % freq)

    def _set_mode(self, mode):
        return self._update("M %s" % mode)

    def _set_squelch(self, sql):
        return self._update("L SQL %s" % self.sql)

    def _get_level(self):
        return self._update("l STRENGTH")

    def _get_mode(self):
        return self._update('m')

    def _scan(self):

        if self.scan_start == True:
            for key, values in self.freqs.items():
                freq = key
                mode = self.freqs[key]["mode"]
                tag = self.freqs[key]["tag"]

                self._set_freq(freq)
                self._set_mode(mode)
                self._set_squelch(self.sql)
                time.sleep(0.2)
                res = self._calc_RSSI()

                if res >= self.signalStrength:
                    print ("********************************************")
                    time.sleep(0.1)
                    while res >= self.signalStrength:
                        print ("частота " + str(freq) + " уровень" + str(res))
                        time.sleep(3.0)
                        res = self._calc_RSSI()
                else:
                    print ("********************************************")
                    print ("частота " + str(freq) + " уровень" + str(res))

    def _calc_RSSI(self):
        res = 0
        for i in range(3):
            RSSI = self._get_level()
            res+=float(RSSI)
            time.sleep(0.45)
        res = res / 3
        return int(res)

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
