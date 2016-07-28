#!/bin/python
import csv
import uuid
import os

BLIND_STRING = "blind"

class Blind:

    def __init__(self):
        """ Initialize """

    def get_filenames(self):
        """ get the filenames to obfuscate """
        l = os.listdir(".")
        return [i for i in l if not (i.endswith(".py") or i.endswith(".csv") or i.startswith(BLIND_STRING) or os.path.isdir(i) or i.startswith("."))]

    def get_blind_name(self, prevblind, ext):
        found = False
        blind = ""
        while not found:
            blind = BLIND_STRING + "_" + str(uuid.uuid4().hex) + ext
            if blind not in prevblind:
                found = True
        return blind

    def blind_filenames(self):
        fnames = self.get_filenames()
        blind_names = []
        for fname in fnames:
            _, ext = os.path.splitext(fname)
            blind_names.append(self.get_blind_name(blind_names, ext))
        data = self.swap_axes([fnames, blind_names])
        self.write_csv("key.csv", data)
        self.rename_files(data)

    def swap_axes(self, data):
        swap = []
#        colnum = -1
        for col in data:
#            colnum += 1
            rownum = -1
            for item in col:
                rownum += 1
                if rownum > (len(swap) - 1):
                    swap.append([])
                swap[rownum].append(item)
        return swap

    def write_csv(self, filename, data):
        outfile = open (filename, "w", encoding='latin1')
        writer = csv.writer (outfile, delimiter = ',')
        for line in data:
            writer.writerow (line)
        
    def rename_files(self, data):
        for row in data:
            pre = row[0]
            post = row[1]
            os.rename(pre, post)

    def blind_done(self):
        l = os.listdir(".")
        bdone = False
        for f in l:
            if f.startswith(BLIND_STRING):
                bdone = True
        return bdone

    def reverse_blind_filenames(self):
        #print("reverse blind not implemented")
        reverse_data = []
        with open ("key.csv", "r", encoding='latin1') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            for line in reader:
                reverse_data.append([line[1], line[0]])
        self.rename_files(reverse_data)

    def run(self):
        if self.blind_done():
            self.reverse_blind_filenames();
        else:
            self.blind_filenames();

b = Blind()
b.run()
