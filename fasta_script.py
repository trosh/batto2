#!/usr/bin/env python3

import subprocess
from sys import argv

fn_to_realname = {
        "NC_000964.extract.faa" : "Bacillus_subtilis",
        "NC_009725.extract.faa" : "Bacillus_amyloliquefaciens_FZB42",
        "NC_009848.extract.faa" : "Bacillus_pumilus_SAFR_032",
        "NC_014171.extract.faa" : "Bacillus_thuringiensis_BMB171",
        "NC_012472.extract.faa" : "Bacillus_cereus_03BB102",
        "NC_003997.extract.faa" : "Bacillus_anthracis_Ames",
        "NC_015634.extract.faa" : "Bacillus_coagulans_2_6",
        "NC_006322.extract.faa" : "Bacillus_licheniformis_ATCC_14580",
        "NC_000913.extract.faa" : "Escherichia_coli_K_12_substr__MG1655",
        "NC_011770.extract.faa" : "Pseudomonas_aeruginosa_LESB58",
        "NC_009428.extract.faa" : "Rhodobacter_sphaeroides_ATCC_17025",
        "NC_016114.extract.faa" : "Streptomyces_flavogriseus_ATCC_33331",
        "NC_012803.extract.faa" : "Micrococcus_luteus_NCTC_2665_uid59033",
        "NC_002662.extract.faa" : "Lactococcus_lactis_Il1403"}

cds = argv[1:]
fn_to_indices = {}
indices_to_realname = {}
cnt = 0
for fn in cds:
    fn_to_indices[str(fn)] = cnt
    try:
        indices_to_realname[str(cnt)] = fn_to_realname[fn]
    except KeyError:
        print("Pas bon filename ça")
        exit(1)
    cnt += 1

from itertools import combinations
matrix = {}
for i in combinations(cds, 2):
    proc = subprocess.Popen(
            ['fasta36', '-w', '80', '-b=1', '-mBB', '-s', 'BP62',
             '-a', i[0], i[1]],
            stdout=subprocess.PIPE)
    fasta_output = proc.communicate()[0].decode(encoding="utf-8").split('\n')
    identities = []
    for line in fasta_output:
        if 'Identities' in line:
            identities.append(int(line.strip().split(' ')[3][1:-3]))
    ind0 = fn_to_indices[i[0]]
    ind1 = fn_to_indices[i[1]]
    if ind0 in matrix:
        matrix[ind0][ind1] = max(identities)
    else:
        matrix[ind0] = {ind1 : max(identities)}
    if ind1 in matrix:
        matrix[ind1][ind0] = max(identities)
    else:
        matrix[ind1] = {ind0 : max(identities)}

import json
with open("distances.json", "w") as distfile:
    json.dump({"D":matrix, "names":indices_to_realname}, distfile)

