#!/usr/bin/env python3

from sys import argv
import os

if len(argv) < 3:
    print("usage: extractCDS query input_reference_filenames")
    exit(1)

query = argv[1].strip().lower()

refins = argv[2:]

for refin_filename in refins:
    with open(refin_filename) as refinfaa:
        for line in refinfaa:
            if line[0] == '>':
                words = line.split('|')
                if query in words[2].lower():
                    refout_filename = '.'.join(refin_filename.split('/')[-1].split('.')[:-1]) + ".extract.faa"
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

