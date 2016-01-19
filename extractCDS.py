#!/usr/bin/env python3

from sys import argv

if len(argv) < 3:
    print("usage: extractCDS query reference_in [...]")
    exit(1)

with open(argv[1]) as queryfaa:
    query = queryfaa.readline().strip()[1:].split(' ')[0].lower()

with open(argv[2]) as refinfaa:
    found = False
    refout_filename = ""
    for line in refinfaa:
        if line[0] == '>':
            cdsname = line.split('|')[2]
            if query in cdsname.lower():
                found = True
                refout_filename = cdsname.split(' ')[0] + ".faa"
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

