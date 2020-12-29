from gqrx_scanner import*
import csv
import time

if __name__ == "__main__":

    Rec = Receiver()
    Rec.scan_start = True

    while(1):
        Rec._scan()
        #Rec.scan_start = False



