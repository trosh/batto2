#!/usr/bin/env python3

from sys import argv
import os

if len(argv) < 3:
    print("usage: extractCDS query reference_in [...]")
    exit(1)

with open(argv[1]) as queryfaa:
    query = queryfaa.readline().strip()[1:].split(' ')[0].lower()

with open(argv[2]) as refinfaa:
    for line in refinfaa:
        if line[0] == '>':
            cdsname = line.split('|')[2]
            if query in cdsname.lower():
                refout_filename = cdsname.split(' ')[0] + ".faa"
                if os.path.isfile(refout_filename):
                    question = "overwrite "+refout_filename+" ? [Yn]"
                    answer = input(question).lower()
                    if len(answer) > 0 and answer[0] != "y":
                        print("disregarding "+refout_filename+", continuing")
                        continue
                    print("overwriting "+refout_filename)
                else:
                    print("writing to "+refout_filename)
                with open(refout_filename, "w") as refoutfaa:
                    refoutfaa.write(line) # print cds header
                    # keep on printing lines until next cds
                    while True:
                        line = refinfaa.readline()
                        if line[0] == '>':
                            break
                        refoutfaa.write(line)
                break

