def scan(self):
    """
    loop over the frequencies in the list, 
    and stop if the frequency is active (signal strength is high enough)
    """
    while(1):
        for freq in self.freqs.keys():
            self._set_freq(freq)
            self._set_mode(self.freqs[freq]['mode'])
            self._set_squelch(self.signalStrength)
            print (str(self._get_level()), str(freq))
            time.sleep(0.5)
            if float(self._get_level()) >= self.signalStrength and float(self._get_level()) != 0.0:
                time.sleep(0.1)
                timenow = str(time.localtime().tm_hour) + ':' + str(time.localtime().tm_min) + \
                ':' + str(time.localtime().tm_sec)
                while float(self._get_level()) >= self.signalStrength + 1.5 and float(self._get_level()) != 0.0:
                    print (timenow, freq, self.freqs[freq]['tag'],self._get_level()),
                    time.sleep(self.waitTime)
