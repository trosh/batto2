#!/usr/bin/env python3

from sys import argv

if len(argv) < 3:
    print("usage: extractCDS query reference_in [...] [> reference_out]")
    exit(1)

with open(argv[1]) as queryfaa:
    query = queryfaa.readline().strip()[1:].split(' ')[0].lower()

with open(argv[2]) as refinfaa:
    for line in refinfaa:
        if line[0] == '>':
            cdsname = line.split('|')[2]
            if query in cdsname.lower():
                print(line, end='') # print cds header
                break
    for line in refinfaa: # keep on printing lines until next cds
        if line[0] == '>':
            break
        print(line, end='')

