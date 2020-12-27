from gqrx_scanner import*
import csv
import time

def load_config(freq_csv='freq.csv'):
    """
    read the csv file with the frequencies & modes
    in it into a dict{} where keys are the freq and
    the value is a dict with the mode and a tag
    """
    freqs = {}
    with open(freq_csv, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        for row in reader:
            if int(row[3]) == 1:
                freq = row[0]
                freqs[freq] = {"mode":row[1],"tag": row[2]}
    return freqs

def tune_rec(freq, mode, tag, sql):

    print ("Настройка приемника")
    print (freq, mode, tag, sql)
    
    Rec._set_freq(freq)
    Rec._set_mode(mode)
    Rec._set_squelch(sql)

def get_RSSI():

    res = 0
    for i in range(3):
        RSSI = Rec._get_level()
        res+=float(RSSI)
        time.sleep(0.45)
    res = res / 3
    return int(res)

if __name__ == "__main__":

    freq_set  = load_config()

    Rec = Receiver()

    for key, values in freq_set.items():
        freq = key
        mode = freq_set[key]["mode"]
        tag = freq_set[key]["tag"]
        sql = -30

        tune_rec(freq, mode, tag, sql)

        time.sleep(0.2)

        res =  get_RSSI()
        print (res)

        #print ("Анализ данных уровня")



